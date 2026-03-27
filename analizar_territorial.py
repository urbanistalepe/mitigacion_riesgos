import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import os
import pandas as pd
from matplotlib.lines import Line2D

# Configuración de estilo
plt.rcParams['font.sans-serif'] = 'Arial'

# Directorios
output_dir = "analisis_territorial"
os.makedirs(output_dir, exist_ok=True)

# Colores para periodos (Gama de verdes para huella urbana)
colors = {
    '1990': '#d9f0a3',
    '2000': '#addd8e',
    '2010': '#78c679',
    '2015': '#238443'
}

# Rutas
huella_path = 'capas/amg_huella_de_ciudad_1990a2015.gpkg'
vial_path = 'capas/amg_sistema_vial_primario_regional.gpkg'

def generate_analysis():
    print("Cargando capas geográficas...")
    huella = gpd.read_file(huella_path)
    vial = gpd.read_file(vial_path)

    # 1. Análisis de Superficies
    print("Calculando superficies...")
    # Asegurar que esté en un sistema métrico para cálculo de áreas (EPSG:32613 ya lo es)
    huella['area_km2'] = huella.geometry.area / 1_000_000
    areas_by_period = huella.groupby('FECHA')['area_km2'].sum().sort_index()

    # Preparar tabla markdown
    table_content = "| Periodo (Año) | Área de Huella Urbana (km²) |\n"
    table_content += "| :--- | :---: |\n"
    for year, area in areas_by_period.items():
        table_content += f"| {year} | {area:,.2f} |\n"
    
    total_area = areas_by_period['2015']
    table_content += f"| **Acumulado 2015** | **{total_area:,.2f}** |\n"

    with open(os.path.join(output_dir, 'tabla_superficies.md'), 'w') as f:
        f.write(table_content)

    # 2. Generación del Mapa
    print("Generando mapa de crecimiento y vialidades...")
    fig, ax = plt.subplots(figsize=(14, 14))

    # Graficar huella acumulativa
    # Nota: Los datos de 2015 suelen incluir los de años anteriores si es acumulativo, 
    # pero aquí graficaremos por periodos si son polígonos separados por año.
    # Según el nombre del archivo, son periodos.
    for year in sorted(huella['FECHA'].unique(), reverse=True):
        subset = huella[huella['FECHA'] == year]
        subset.plot(ax=ax, color=colors.get(year, '#cccccc'), label=f'Expansión {year}', alpha=0.85, zorder=2)

    # Filtrar y graficar vialidades VP (Actual y Proyecto)
    # Según la inspección, SubClas 'V-P-...' son las primarias.
    vial_vp = vial[vial['SubClas'].str.startswith('V-P', na=False)]
    vial_vp.plot(ax=ax, color='#e41a1c', linewidth=1.2, label='Vialidades Principales (VP)', zorder=4)

    # Añadir mapa base
    try:
        cx.add_basemap(ax, crs=huella.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.7, zorder=1)
    except Exception as e:
        print(f"Nota: No se pudo añadir el mapa base (error de conexión o librería): {e}")

    ax.set_title('Dinámica de Crecimiento Urbano y Estructura Vial Primaria (1990-2015)', fontsize=16, pad=20)
    ax.set_axis_off()

    # Leyenda personalizada
    legend_elements = [
        Line2D([0], [0], color=colors['2015'], lw=6, label='Huella 2015'),
        Line2D([0], [0], color=colors['2010'], lw=6, label='Huella 2010'),
        Line2D([0], [0], color=colors['2000'], lw=6, label='Huella 2000'),
        Line2D([0], [0], color=colors['1990'], lw=6, label='Huella 1990'),
        Line2D([0], [0], color='#e41a1c', lw=2, label='Vialidades Principales (Actual/Proyecto)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, fontsize=10)

    plt.tight_layout()
    map_filename = os.path.join(output_dir, 'mapa_expansion_vialidades.png')
    plt.savefig(map_filename, dpi=200, bbox_inches='tight')
    plt.close()

    print(f"Análisis territorial completado. Archivos en: {output_dir}")

if __name__ == "__main__":
    generate_analysis()
