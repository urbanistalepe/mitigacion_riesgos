import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import os
import warnings
warnings.filterwarnings('ignore')

try:
    from pyproj import Transformer
    HAS_PYPROJ = True
except ImportError:
    HAS_PYPROJ = False

# Configuración de estilo
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 8)

# Directorio de salida
output_dir = "analisis_priorizacion"
os.makedirs(output_dir, exist_ok=True)

def analyze():
    print(f"{'='*50}")
    print("ANÁLISIS DE PRIORIZACIÓN DE SITIOS RECURRENTES - AMG")
    print(f"{'='*50}")
    
    csv_path = 'amg_nivel_priorizacion.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: No se encuentra el archivo {csv_path}")
        return

    print(f"Cargando {csv_path}...")
    try:
        # Intentamos con cp1252 por caracteres latinos comunes en archivos de gobierno
        df = pd.read_csv(csv_path, encoding='cp1252')
    except Exception:
        df = pd.read_csv(csv_path, encoding='utf-8')

    print(f"Registros cargados: {len(df)}")
    
    # --- 1. Limpieza de Municipio (Columna NOMBRE según instrucción) ---
    def limpiar_municipio(nombre):
        if pd.isna(nombre): return "S/D"
        nombre = str(nombre).upper()
        if "GUADALAJARA" in nombre: return "GUADALAJARA"
        if "ZAPOPAN" in nombre: return "ZAPOPAN"
        if "TLAJOMULCO" in nombre: return "TLAJOMULCO"
        if "TONALÁ" in nombre: return "TONALÁ"
        if "EL SALTO" in nombre: return "EL SALTO"
        if "TLAQUEPAQUE" in nombre: return "TLAQUEPAQUE"
        if "IXTLAHUACÁN" in nombre: return "IXTLAHUACÁN"
        if "JUANACATLÁN" in nombre: return "JUANACATLÁN"
        if "ZAPOTLANEJO" in nombre: return "ZAPOTLANEJO"
        return "OTRO / S/D"

    df['municipio_std'] = df['NOMBRE'].apply(limpiar_municipio)
    
    # --- 2. Análisis de Priorización (Columna Nivel_de_p) ---
    def limpiar_prioridad(p):
        if pd.isna(p): return "S/D"
        p = str(p).strip().capitalize()
        # Mapeo de variaciones
        if "Baja" in p: return "Baja"
        if "Media" in p: return "Media"
        if "Alta" in p: return "Alta"
        if "Muy alta" in p: return "Muy alta"
        if "Muy baja" in p: return "Muy baja"
        return "S/D"

    df['prioridad_std'] = df['Nivel_de_p'].apply(limpiar_prioridad)

    # --- 3. Generación de Gráficas ---
    
    # Gráfica 1: Histogramas por Municipio
    print("Generando gráfica por municipio...")
    plt.figure()
    mun_filtered = df[df['municipio_std'] != "OTRO / S/D"]
    if not mun_filtered.empty:
        order_mun = mun_filtered['municipio_std'].value_counts().index
        sns.countplot(data=mun_filtered, y='municipio_std', order=order_mun, palette="viridis")
        plt.title('Sitios Recurrentes de Inundación por Municipio', fontsize=16)
        plt.xlabel('Cantidad de Sitios')
        plt.ylabel('Municipio')
        plt.savefig(os.path.join(output_dir, 'sitios_por_municipio.png'), bbox_inches='tight', dpi=200)
    plt.close()

    # Gráfica 2: Prioridad Global
    print("Generando gráfica de prioridades...")
    plt.figure()
    prio_counts = df[df['prioridad_std'] != "S/D"]['prioridad_std'].value_counts()
    if not prio_counts.empty:
        order_prio = ['Muy alta', 'Alta', 'Media', 'Baja', 'Muy baja']
        existing_order = [o for o in order_prio if o in prio_counts.index]
        sns.barplot(x=prio_counts.index, y=prio_counts.values, order=existing_order, palette="magma")
        plt.title('Distribución de Niveles de Priorización (AMG)', fontsize=16)
        plt.ylabel('Número de Sitios')
        plt.savefig(os.path.join(output_dir, 'distribucion_prioridades.png'), bbox_inches='tight', dpi=200)
    plt.close()

    # --- 4. Análisis Espacial ---
    if HAS_PYPROJ:
        print("Transformando coordenadas (EPSG:32613 -> EPSG:4326)...")
        transformer = Transformer.from_crs("epsg:32613", "epsg:4326", always_xy=True)
        
        # Eliminar nulos en coordenadas
        df_geo = df.dropna(subset=['x', 'y'])
        
        # Transformar
        df_geo['lon'], df_geo['lat'] = transformer.transform(df_geo['x'].values, df_geo['y'].values)
        
        print("Creando mapa interactivo...")
        # Centrar en Guadalajara
        m = folium.Map(location=[20.67, -103.35], zoom_start=11, tiles='CartoDB Positron')
        
        marker_cluster = MarkerCluster(name="Sitios Recurrentes").add_to(m)
        
        color_map = {
            'Muy alta': 'darkred',
            'Alta': 'red',
            'Media': 'orange',
            'Baja': 'green',
            'Muy baja': 'darkgreen',
            'S/D': 'gray'
        }
        
        for _, row in df_geo.iterrows():
            color = color_map.get(row['prioridad_std'], 'gray')
            # Limpiar popups de caracteres extraños para folium
            popup_text = f"<b>ID:</b> {row['id']}<br><b>Prioridad:</b> {row['prioridad_std']}<br><b>Mecanismo:</b> {row['Mecanismo_']}"
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(marker_cluster)
            
        m.save(os.path.join(output_dir, 'mapa_priorizacion_interactivo.html'))
        print(f"Mapa interactivo guardado en {output_dir}/mapa_priorizacion_interactivo.html")
    else:
        print("\n[!] ADVERTENCIA: 'pyproj' no está instalado. No se pudo generar el mapa.")
        print("    Para habilitar mapas, ejecute: pip install pyproj")

    # --- 5. Resumen Estadístico ---
    print("\nResumen de Prioridad por Municipio:")
    summary = pd.crosstab(df['municipio_std'], df['prioridad_std'])
    print(summary)
    summary.to_csv(os.path.join(output_dir, 'resumen_municipio_prioridad.csv'))

    print(f"\nProceso completado. Archivos generados en: {output_dir}")

if __name__ == "__main__":
    analyze()
