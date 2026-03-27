import geopandas as gpd

huella_path = 'capas/amg_huella_de_city_1990a2015.gpkg' # Oops fixed path below
huella_path = 'capas/amg_huella_de_ciudad_1990a2015.gpkg'
vial_path = 'capas/amg_sistema_vial_primario_regional.gpkg'

print(f"Inspeccionando Huella: {huella_path}")
huella = gpd.read_file(huella_path)
print(f"Columnas: {huella.columns.tolist()}")
print(f"Head:\n{huella.head()}")
print(f"CRS: {huella.crs}")

print(f"\nInspeccionando Vialidades: {vial_path}")
vial = gpd.read_file(vial_path)
print(f"Columnas: {vial.columns.tolist()}")
print(f"Head:\n{vial.head()}")
print(f"CRS: {vial.crs}")
