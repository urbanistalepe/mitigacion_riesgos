import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
import os
from matplotlib.lines import Line2D

# Configuración
plt.rcParams['font.sans-serif'] = 'Arial'
output_dir = "analisis_cruces"
os.makedirs(output_dir, exist_ok=True)

def analyze_crosses():
    print("Cargando capas para análisis de cruces...")
    huella = gpd.read_file('capas/amg_huella_de_ciudad_1990a2015.gpkg')
    margin = gpd.read_file('capas/indice_marginacion_urbana_colonia.gpkg')
    fires = gpd.read_file('capas/vwamg_vulnerabilidad_fisica_ante_incendios.gpkg')
    sites_df = pd.read_csv('amg_nivel_priorizacion.csv', encoding='latin-1')
    sites = gpd.GeoDataFrame(sites_df, geometry=gpd.points_from_xy(sites_df.x, sites_df.y), crs="EPSG:32613")

    # Definir niveles críticos
    fire_critical = fires[fires['Vulnerabil'].isin(['Alta', 'Muy alta'])]
    margin_critical = margin[margin['GM_2020'].isin(['Alto', 'Muy alto'])]

    # --- CRUCE 1: HUELLA URBANA 2015 VS INCENDIOS ---
    print("Analizando Cruce 1: Huella 2015 vs Incendios...")
    huella_2015 = huella[huella['FECHA'] == '2015']
    inter_huella = gpd.overlay(huella_2015, fire_critical, how='intersection')
    
    area_inter = inter_huella.geometry.area.sum() / 1_000_000
    area_total_2015 = huella_2015.geometry.area.sum() / 1_000_000
    pct_huella = (area_inter / area_total_2015) * 100

    # Mapa 1
    fig, ax = plt.subplots(figsize=(10, 8))
    huella_2015.plot(ax=ax, color='#eeeeee', label='Huella Urbana Total', zorder=1)
    fire_critical.plot(ax=ax, color='#ff9c4b', alpha=0.3, label='Vulnerabilidad Alta/Muy Alta', zorder=2)
    inter_huella.plot(ax=ax, color='#e41a1c', label='Zonas Urbanas en Riesgo', zorder=3)
    cx.add_basemap(ax, crs=huella.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.5)
    ax.set_title('Exposición de la Huella Urbana a Riesgo de Incendio (2015)', fontsize=14)
    ax.set_axis_off()
    plt.savefig(os.path.join(output_dir, 'mapa_cruce_huella_incendio.png'), dpi=200, bbox_inches='tight')
    plt.close()

    # --- CRUCE 2: MARGINACIÓN VS INCENDIOS ---
    print("Analizando Cruce 2: Marginación vs Incendios...")
    inter_margin = gpd.overlay(margin_critical, fire_critical, how='intersection')
    cols_in_risk = inter_margin['CVE_COL'].nunique()
    total_cols_high = margin_critical['CVE_COL'].nunique()
    pct_margin = (cols_in_risk / total_cols_high) * 100

    # Mapa 2
    fig, ax = plt.subplots(figsize=(10, 8))
    margin_critical.plot(ax=ax, color='#addd8e', alpha=0.4, label='Marginación Alta/Muy Alta', zorder=1)
    inter_margin.plot(ax=ax, color='#b0292b', label='Colonias en Doble Riesgo', zorder=2)
    cx.add_basemap(ax, crs=huella.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.5)
    ax.set_title('Superposición de Marginación y Vulnerabilidad a Incendios', fontsize=14)
    ax.set_axis_off()
    plt.savefig(os.path.join(output_dir, 'mapa_cruce_marginacion_incendio.png'), dpi=200, bbox_inches='tight')
    plt.close()

    # --- CRUCE 3: SITIOS RECURRENTES VS INCENDIOS ---
    print("Analizando Cruce 3: Sitios Recurrentes vs Incendios...")
    sites_in_fire = gpd.sjoin(sites, fire_critical, how='inner', predicate='intersects')
    count_sites = len(sites_in_fire)
    total_sites = len(sites)
    pct_sites = (count_sites / total_sites) * 100

    # Mapa 3
    fig, ax = plt.subplots(figsize=(10, 8))
    fire_critical.plot(ax=ax, color='#ff9c4b', alpha=0.2, zorder=1)
    sites.plot(ax=ax, color='gray', markersize=3, alpha=0.5, label='Sitios Totales', zorder=2)
    sites_in_fire.plot(ax=ax, color='#e41a1c', markersize=8, label='Sitios en Zonas de Incendio', zorder=3)
    cx.add_basemap(ax, crs=huella.crs.to_string(), source=cx.providers.CartoDB.Positron, alpha=0.5)
    ax.set_title('Sitios Recurrentes (Inundación) en Zonas de Incendio', fontsize=14)
    ax.set_axis_off()
    plt.savefig(os.path.join(output_dir, 'mapa_cruce_sitios_incendio.png'), dpi=200, bbox_inches='tight')
    plt.close()

    # --- GENERAR TABLAS EN MARKDOWN ---
    with open(os.path.join(output_dir, 'resumen_cruces.md'), 'w') as f:
        f.write("# Resumen de Análisis de Cruces Espaciales\n\n")
        
        f.write("### 1. Huella Urbana vs Incendios\n")
        f.write(f"- Área urbana 2015 en riesgo: **{area_inter:,.2f} km²**\n")
        f.write(f"- Porcentaje de la mancha urbana expuesta: **{pct_huella:.1f}%**\n\n")
        
        f.write("### 2. Marginación vs Incendios\n")
        f.write(f"- Colonias críticas (Marginación Alta/Muy Alta): **{total_cols_high}**\n")
        f.write(f"- Colonias críticas en zonas de incendio: **{cols_in_risk}** (**{pct_margin:.1f}%**)\n\n")
        
        f.write("### 3. Sitios Recurrentes vs Incendios\n")
        f.write(f"- Total de sitios recurrentes analizados: **{total_sites}**\n")
        f.write(f"- Sitios localizados en zonas de vulnerabilidad física a incendios: **{count_sites}** (**{pct_sites:.1f}%**)\n")

    print(f"Análisis de cruces completado. Archivos en: {output_dir}")

if __name__ == "__main__":
    analyze_crosses()
