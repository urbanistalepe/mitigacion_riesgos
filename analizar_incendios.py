import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import os
from matplotlib.lines import Line2D

# Configuración
plt.rcParams['font.sans-serif'] = 'Arial'
output_dir = "analisis_riesgo"
os.makedirs(output_dir, exist_ok=True)

# Colores consistentes con la presentación
colors_risk = {
    'Muy alta': '#b0292b',
    'Alta': '#f53d40',
    'Media': '#ff9c4b',
    'Baja': '#addd8e',
    'Muy baja': '#238443'
}

def analyze():
    print("Iniciando análisis de vulnerabilidad a incendios...")
    path = 'capas/vwamg_vulnerabilidad_fisica_ante_incendios.gpkg'
    if not os.path.exists(path):
        print(f"Error: No se encuentra {path}")
        return

    fires = gpd.read_file(path)
    
    # 1. Cálculo de Áreas
    print("Calculando superficies por nivel de vulnerabilidad...")
    fires['area_km2'] = fires.geometry.area / 1_000_000
    areas = fires.groupby('Vulnerabil')['area_km2'].sum()

    # Tabla markdown
    with open(os.path.join(output_dir, 'tabla_vulnerabilidad_incendios.md'), 'w') as f:
        f.write("| Nivel de Vulnerabilidad | Superficie (km²) |\n")
        f.write("| :--- | :---: |\n")
        order = ['Muy alta', 'Alta', 'Media', 'Baja', 'Muy baja']
        for v in order:
            if v in areas.index:
                f.write(f"| {v} | {areas[v]:,.2f} |\n")

    # 2. Generación del Mapa
    print("Generando mapa de vulnerabilidad...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    order_rev = order[::-1] # Dibujamos de menor a mayor riesgo para destacar los puntos rojos
    for v in order_rev:
        if v in fires['Vulnerabil'].unique():
            subset = fires[fires['Vulnerabil'] == v]
            subset.plot(ax=ax, color=colors_risk.get(v), label=v, alpha=0.85, zorder=2)
            
    try:
        cx.add_basemap(ax, crs=fires.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.6, zorder=1)
    except Exception as e:
        print(f"Error basemap: {e}")
        
    ax.set_title('Vulnerabilidad Física ante Incendios en el AMG', fontsize=15, pad=15)
    ax.set_axis_off()
    
    # Leyenda
    legend_elements = [Line2D([0], [0], color=colors_risk[v], lw=6, label=v) for v in order if v in areas.index]
    ax.legend(handles=legend_elements, loc='lower right', title='Vulnerabilidad', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'mapa_vulnerabilidad_incendios.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"Análisis finalizado exitosamente. Archivos en: {output_dir}")

if __name__ == "__main__":
    analyze()
