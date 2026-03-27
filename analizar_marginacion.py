import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import os
from matplotlib.lines import Line2D

# Configuración de estilo
plt.rcParams['font.sans-serif'] = 'Arial'

# Directorios
output_dir = "analisis_territorial"
os.makedirs(output_dir, exist_ok=True)

# Paleta de colores para marginación
colors_margin = {
    'Muy alto': '#b0292b',
    'Alto': '#f53d40',
    'Medio': '#ff9c4b',
    'Bajo': '#addd8e',
    'Muy bajo': '#238443'
}

def analyze_marginalization():
    print("Iniciando análisis de marginación urbana...")
    path = 'capas/indice_marginacion_urbana_colonia.gpkg'
    if not os.path.exists(path):
        print(f"Error: No se encuentra {path}")
        return

    margin = gpd.read_file(path)
    print(f"Capa cargada: {len(margin)} colonias.")

    # 1. Estadísticas
    counts = margin['GM_2020'].value_counts()
    with open(os.path.join(output_dir, 'tabla_marginacion.md'), 'w') as f:
        f.write("| Grado de Marginación | Número de Colonias |\n")
        f.write("| :--- | :---: |\n")
        for gm in ['Muy alto', 'Alto', 'Medio', 'Bajo', 'Muy bajo']:
            f.write(f"| {gm} | {counts.get(gm, 0):,} |\n")

    # 2. Generación del Mapa
    print("Generando mapa de marginación...")
    # Ajustamos proporciones para evitar que sea demasiado alto en la lámina
    fig, ax = plt.subplots(figsize=(12, 10))

    order = ['Muy alto', 'Alto', 'Medio', 'Bajo', 'Muy bajo']
    for gm in order:
        subset = margin[margin['GM_2020'] == gm]
        subset.plot(ax=ax, color=colors_margin.get(gm), label=gm, alpha=0.8, zorder=2)

    try:
        cx.add_basemap(ax, crs=margin.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.6, zorder=1)
    except Exception as e:
        print(f"Nota: No se pudo añadir mapa base: {e}")

    ax.set_title('Grado de Marginación Urbana por Colonia - AMG (2020)', fontsize=15, pad=15)
    ax.set_axis_off()

    # Leyenda
    legend_elements = [Line2D([0], [0], color=colors_margin[gm], lw=6, label=gm) for gm in order]
    ax.legend(handles=legend_elements, loc='lower right', title='Nivel de Marginación', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'mapa_marginacion_urbana.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"Análisis de marginación completado. Archivos en: {output_dir}")

if __name__ == "__main__":
    analyze_marginalization()
