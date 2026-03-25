import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import os
import unicodedata

# Configuración de estilo
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams['figure.figsize'] = (12, 8)

# Directorio de salida
output_dir = "/Users/lepe/proyectos/riesgos/analisis_emergencias"
os.makedirs(output_dir, exist_ok=True)

def quitar_acentos(texto):
    """Elimina acentos y normaliza caracteres especiales."""
    try:
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    except Exception:
        return texto

def normalizar_incidente(texto):
    """Estandariza la columna Incidente en categorías únicas y limpias."""
    if pd.isna(texto):
        return "OTRO"
    texto = quitar_acentos(str(texto)).upper().strip()

    # --- INCENDIOS ---
    if any(k in texto for k in ["PASTIZAL", "MALEZA", "HIERBA"]):
        return "INCENDIO DE PASTIZAL/MALEZA"
    if any(k in texto for k in ["BALDIO", "LOTE BALDO"]):
        return "INCENDIO DE LOTE BALDIO"
    if any(k in texto for k in ["CASA", "HABITACI", "DOMESTICO", "DOMICILIO"]):
        return "INCENDIO CASA HABITACION"
    if any(k in texto for k in ["COMERCIO", "LOCAL COMER", "RESTAURAN", "NEGOCIO"]):
        return "INCENDIO DE COMERCIO"
    if any(k in texto for k in ["FABRICA", "INDUSTRIA", "BODEGA", "PLANTA"]):
        return "INCENDIO DE FABRICA/INDUSTRIA"
    if any(k in texto for k in ["VEHICULO", "AUTOMOVIL", "CAMION", "CAMIONETA", "TRAILER", "MOTO"]):
        return "INCENDIO DE VEHICULO"
    if any(k in texto for k in ["NEUMATICO", "LLANTA"]):
        return "INCENDIO DE NEUMATICOS"
    if any(k in texto for k in ["BASURA", "RESIDUOS"]):
        return "INCENDIO DE BASURA"
    if "INCENDIO" in texto:
        return "INCENDIO OTROS"

    # --- GAS Y PRODUCTOS PELIGROSOS ---
    if any(k in texto for k in ["GAS LP", "GAS L.P", "FUGA DE GAS", "GAS NATURAL"]):
        return "GAS LP / FUGA DE GAS"
    if any(k in texto for k in ["HIDROCARBURO", "DERRAME", "COMBUSTIBLE", "DIESEL"]):
        return "DERRAME DE HIDROCARBURO"
    if any(k in texto for k in ["GAS TOXICO", "GASES TOXICOS", "OLOR A QUIMICO", "QUIMICO", "OLOR A GAS", "MATERIAL PELIGROSO"]):
        return "GASES/QUIMICOS PELIGROSOS"

    # --- FAUNA ---
    if any(k in texto for k in ["ENJAMBRE", "ABEJA", "AVISPA", "SOMITE"]):
        return "ENJAMBRE DE ABEJAS/AVISPAS"
    if any(k in texto for k in ["ANIMAL SUELTO", "EQUINO", "BOVINO", "FAUNA SILVESTRE", "RESCATE ANIMAL",
                                  "CAPTURA", "LIBERACION DE ANIMAL"]):
        return "FAUNA / ANIMALES SUELTOS"

    # --- ACCIDENTES VIALES ---
    if any(k in texto for k in ["ACCIDENTE MULTIPLE", "ACCIDENTE CON LESIONADO", "ACCIDENTE DE MOTO",
                                  "ACCIDENTE VIAL", "CHOQUE", "VOLCADURA", "ATROPELLADO",
                                  "SALIDA DE CAMINO", "ACCIDENTE ACUATICO"]):
        return "ACCIDENTE VIAL"

    # --- PERSONAS: APOYO PREHOSPITALARIO Y RESCATE ---
    if any(k in texto for k in ["PREHOSPITALARIA", "PREHOSP", "ENFERMO", "LESIONADO"]):
        return "ATENCION PREHOSPITALARIA"
    if any(k in texto for k in ["PERSONA ATRAPADA", "RESCATE", "DERRUMBE", "PERSONA EN ALTURA"]):
        return "RESCATE DE PERSONAS"
    if any(k in texto for k in ["SUICIDIO", "AMENAZA"]):
        return "AMENAZA / TENTATIVA DE SUICIDIO"

    # --- INFRAESTRUCTURA Y FENOMENOS NATURALES ---
    if any(k in texto for k in ["ARBOL", "RAMA", "ARBOL CAIDO"]):
        return "CAIDA DE ARBOL/RAMA"
    if any(k in texto for k in ["INUNDACION", "ENCHARCAMIENTO", "VIA PUBLICA"]):
        return "INUNDACION / ENCHARCAMIENTO"
    if any(k in texto for k in ["SOCAVAMIENTO", "HUNDIMIENTO", "AGRIETAMIENTO"]):
        return "SOCAVAMIENTO / HUNDIMIENTO"
    if any(k in texto for k in ["CORTO CIRCUITO", "CORTO", "ELECTRICO", "CABLE"]):
        return "CORTO CIRCUITO / ELECTRICIDAD"

    # --- EVENTOS Y ORDEN PUBLICO ---
    if any(k in texto for k in ["COHETE", "FUEGO ARTIFICIAL", "PIROTECNIA", "DETONACION"]):
        return "PIROTECNIA / FUEGOS ARTIFICIALES"
    if any(k in texto for k in ["CONCENTRACION MASIVA", "EVENTO", "MANIFESTACION"]):
        return "CONCENTRACION MASIVA / EVENTO"

    # --- SERVICIOS Y APOYO CIUDADANO ---
    if any(k in texto for k in ["RECORRIDO", "VIGILANCIA", "PREVENCION"]):
        return "RECORRIDO DE VIGILANCIA"
    if any(k in texto for k in ["APOYO", "SERVICIO PUBLICO", "SOLICITUD", "OTROS APOYO"]):
        return "APOYO Y SERVICIOS CIUDADANOS"

    # --- MEDIO AMBIENTE ---
    if any(k in texto for k in ["MEDIO AMBIENTE", "OTROS MEDIO"]):
        return "MEDIO AMBIENTE / OTROS"

    return "OTRO"

# Cargar datos
print("Cargando datos (UTF-8)...")
try:
    df = pd.read_csv('/Users/lepe/proyectos/riesgos/historico_emergencias_amg.csv', encoding='utf-8')
except Exception as e:
    print(f"Error al cargar con utf-8, intentando con cp1252: {e}")
    df = pd.read_csv('/Users/lepe/proyectos/riesgos/historico_emergencias_amg.csv', encoding='cp1252')

print(f"Datos cargados: {df.shape[0]} registros.")

# Preprocesamiento
print("Procesando y estandarizando datos...")
df['fecha_pd'] = pd.to_datetime(df['fecha'], errors='coerce')
df['year'] = df['fecha_pd'].dt.year

# Estandarizar Incidente
df['Incidente_std'] = df['Incidente'].apply(normalizar_incidente)

# Eliminar registros con fechas inválidas o sin coordenadas
df = df.dropna(subset=['year', 'x', 'y'])
df['year'] = df['year'].astype(int)

# 1. Gráfica de tendencia por año (Total)
plt.figure()
sns.countplot(data=df, x='year', color='skyblue')
plt.title('Número de Emergencias por Año (Total)', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Emergencias', fontsize=12)
plt.savefig(os.path.join(output_dir, 'tendencia_anual_total.png'), dpi=300)
plt.close()

# 2. Gráfica de tendencia por municipio (Usando la columna 'Municipio' estandarizada por el usuario)
municipios_count = df['Municipio'].value_counts()
top_municipios = municipios_count.head(10).index.tolist()
df_top_mun = df[df['Municipio'].isin(top_municipios)]

plt.figure()
sns.countplot(data=df_top_mun, x='year', hue='Municipio')
plt.title('Tendencia de Emergencias por Municipio', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Emergencias', fontsize=12)
plt.legend(title='Municipio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'tendencia_por_municipio.png'), dpi=300)
plt.close()

# 3. Gráfica de tendencia por tipo de incidente estandarizado (Top 8)
incidentes_std_count = df['Incidente_std'].value_counts()
top_incidentes = incidentes_std_count.head(8).index.tolist()
df_top_inc = df[df['Incidente_std'].isin(top_incidentes)]

plt.figure()
data_incidents = df_top_inc.groupby(['year', 'Incidente_std']).size().reset_index(name='count')
sns.lineplot(data=data_incidents, x='year', y='count', hue='Incidente_std', marker='o')
plt.title('Tendencia por Tipo de Incidente (Estandarizado)', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Emergencias', fontsize=12)
plt.legend(title='Incidente', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'tendencia_por_incidente.png'), dpi=300)
plt.close()

# 4. Mapas de Calor por año
print("Generando mapas de calor...")
for year in sorted(df['year'].unique()):
    print(f"Generando mapa para el año {year}...")
    df_year = df[df['year'] == year]
    
    center_lat = df_year['y'].mean()
    center_lon = df_year['x'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB dark_matter')
    heat_data = df_year[['y', 'x']].dropna().values.tolist()
    HeatMap(heat_data, radius=12, blur=10).add_to(m)
    m.save(os.path.join(output_dir, f'mapa_calor_{year}.html'))

# ─── 5. Clustering Espacial (DBSCAN) ─────────────────────────────────────────
print("Ejecutando clustering espacial (DBSCAN)...")

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.patches as mpatches

CLUSTER_PALETTE = [
    "#e41a1c", "#377eb8", "#4daf4a", "#ff7f00",
    "#a65628", "#984ea3", "#f781bf", "#00bfbf",
    "#7fbc41", "#d6604d", "#4393c3", "#878787"
]

cluster_summary = []

for year in sorted(df['year'].unique()):
    print(f"  Clustering {year}...")
    df_year = df[df['year'] == year].dropna(subset=['x', 'y']).copy()

    coords = df_year[['y', 'x']].values
    coords_scaled = StandardScaler().fit_transform(coords)

    # eps ~400m en coordenadas escaladas; min_samples ajustado a densidad
    db = DBSCAN(eps=0.08, min_samples=30).fit(coords_scaled)
    df_year['cluster'] = db.labels_

    n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    n_noise = (db.labels_ == -1).sum()
    cluster_summary.append({'year': year, 'n_clusters': n_clusters, 'n_noise': n_noise})
    print(f"    -> {n_clusters} clusters, {n_noise} puntos de ruido")

    # Mapa estático por año
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')

    noise = df_year[df_year['cluster'] == -1]
    ax.scatter(noise['x'], noise['y'], s=2, c='#555566', alpha=0.3, label='Sin cluster')

    unique_clusters = sorted([c for c in df_year['cluster'].unique() if c >= 0])
    handles = []
    for i, cid in enumerate(unique_clusters):
        color = CLUSTER_PALETTE[i % len(CLUSTER_PALETTE)]
        subset = df_year[df_year['cluster'] == cid]
        ax.scatter(subset['x'], subset['y'], s=6, c=color, alpha=0.65, zorder=3)
        cx, cy = subset['x'].mean(), subset['y'].mean()
        ax.text(cx, cy, str(cid + 1), color='white', fontsize=8, fontweight='bold',
                ha='center', va='center', zorder=5,
                bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.85, ec='none'))
        handles.append(mpatches.Patch(color=color, label=f'Cluster {cid + 1} (n={len(subset):,})'))

    handles.append(mpatches.Patch(color='#555566', label=f'Sin cluster (n={len(noise):,})'))
    ax.legend(handles=handles, loc='lower right', fontsize=7,
              facecolor='#111122', labelcolor='white', framealpha=0.85)
    ax.set_title(f'Clustering Espacial de Emergencias — {year}', color='white', fontsize=14, pad=12)
    ax.set_xlabel('Longitud', color='#aaaaaa', fontsize=9)
    ax.set_ylabel('Latitud', color='#aaaaaa', fontsize=9)
    ax.tick_params(colors='#aaaaaa')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333344')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'clustering_{year}.png'), dpi=200, facecolor=fig.get_facecolor())
    plt.close()

# Gráfica resumen: número de clusters por año
df_summary = pd.DataFrame(cluster_summary)
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df_summary['year'].astype(str), df_summary['n_clusters'],
              color='#377eb8', edgecolor='white', linewidth=0.7)
for bar, val in zip(bars, df_summary['n_clusters']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
            str(val), ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('Zonas de Concentracion de Emergencias (DBSCAN) por Ano', fontsize=13)
ax.set_xlabel('Ano', fontsize=11)
ax.set_ylabel('Numero de Clusters', fontsize=11)
ax.set_ylim(0, df_summary['n_clusters'].max() + 2)
ax.grid(axis='y', alpha=0.4)
sns.despine()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'clustering_resumen.png'), dpi=200)
plt.close()

print(f"Analisis completado. Los resultados estan en: {output_dir}")
