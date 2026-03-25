"""
generar_presentacion.py
Genera la presentación en formato Marp (.md) y la exporta a HTML y PDF.
Usa el estilo del ejemplo CSMobilityToolbox.
"""

import os
import subprocess

output_dir = "/Users/lepe/proyectos/riesgos"
output_md = os.path.join(output_dir, "presentacion_riesgos.md")
output_html = os.path.join(output_dir, "presentacion_riesgos.html")
output_pdf = os.path.join(output_dir, "presentacion_riesgos.pdf")

# ─── Contenido de la presentación ────────────────────────────────────────────

marp_template = """\
---
marp: true
theme: default
paginate: true
html: true
header: "&nbsp;"
footer: "&nbsp;"
---

<!-- _class: title -->
<style>
  section {
    font-family: 'Arial', sans-serif;
    font-size: 1rem;
  }
  h1 { font-size: 1.8em; }
  h2 { font-size: 1.2em; color: #555; }
  .tag {
    display: inline-block;
    background: #e8f0fe;
    color: #1a73e8;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.75em;
    margin: 2px;
  }
  table { font-size: 0.85em; width: 100%; }
  th { background: #1a73e8; color: white; }
</style>

# Histórico de Emergencias
## Análisis de Tendencias y Concentración Espacial
### Área Metropolitana de Guadalajara · 2019–2023

---

# Introducción

<div style="display: flex; gap: 2rem; align-items: flex-start;">

<div style="flex: 1.2; font-size: 1.1em;">

- El **Área Metropolitana de Guadalajara (AMG)** concentra más de **5.2 millones** de habitantes distribuidos en 10 municipios.
- La gestión de emergencias es competencia de las **unidades de Protección Civil** y bomberos municipales.
- Contar con un **análisis histórico estandarizado** permite identificar patrones, planificar recursos y tomar decisiones basadas en evidencia.

</div>

<div style="flex: 1; font-size: 1em;">

> ℹ️ **Fuente de datos**
>
> Registros históricos del Sistema de Emergencias del AMG (2019–2023), con más de **158,000 reportes** georeferenciados.

</div>

</div>

---

# Objetivos

<div style="display: flex; gap: 2rem; align-items: flex-start;">
<div style="flex: 1;">

## 🎯 Objetivos de análisis

1. Identificar la **tendencia anual** de emergencias en el AMG.
2. Comparar la **carga por municipio** a lo largo del tiempo.
3. Detectar los **tipos de incidentes más frecuentes** y su evolución.
4. Visualizar la **concentración espacial** por año mediante mapas de calor.
5. Estandarizar la **taxonomía de incidentes** para mejorar la consistencia del reporte.

</div>

<div style="flex: 1; padding-top: 1rem;">

| Dimensión | Variable analizada |
|---|---|
| Temporal | Año (2019–2023) |
| Territorial | Municipio (AMG) |
| Tipológica | Tipo de incidente |
| Espacial | Coordenadas XY |

</div>
</div>

---

# Metodología

<div style="display: flex; gap: 2rem;">
<div style="flex: 1; font-size: 1.1em;">

### Datos
- Archivo CSV con codificación **UTF-8**
- Columnas clave: `fecha`, `Municipio`, `Incidente`, `x`, `y`

### Procesamiento
- Parsing de fechas y extracción de año
- **Estandarización de incidentes**: función de normalización con 20+ categorías agrupadas por palabras clave, normalización de acentos con `unicodedata`

### Visualización
- Gráficas con `matplotlib` / `seaborn`
- Mapas de calor interactivos con `folium`

</div>
<div style="flex: 1; font-size: 0.9em; background: #f8f9fa; padding: 1rem; border-radius: 8px;">

**Categorías de incidentes estandarizadas**

<span class="tag">Incendio Pastizal</span>
<span class="tag">Incendio Lote Baldío</span>
<span class="tag">Incendio Casa Habitación</span>
<span class="tag">Incendio Comercio</span>
<span class="tag">Incendio Fábrica</span>
<span class="tag">Incendio Vehículo</span>
<span class="tag">Gas LP / Fuga</span>
<span class="tag">Enjambre Abejas/Avispas</span>
<span class="tag">Accidente Vial</span>
<span class="tag">Atención Prehospitalaria</span>
<span class="tag">Rescate de Personas</span>
<span class="tag">Caída de Árbol</span>
<span class="tag">Inundación</span>
<span class="tag">Hundimiento</span>
<span class="tag">Fauna/Animales</span>
<span class="tag">Pirotecnia</span>
<span class="tag">Corto Circuito</span>
<span class="tag">Gases/Químicos</span>
<span class="tag">Vigilancia</span>
<span class="tag">Apoyo Ciudadano</span>

</div>
</div>

---

# Tendencia Global Anual

<div style="display: flex; gap: 2rem; align-items: center;">
<div style="flex: 2;">

![Tendencia anual](analisis_emergencias/tendencia_anual_total.png)

</div>
<div style="flex: 1; font-size: 1.1em;">

- El número de emergencias aumentó de manera notable entre 2019 y 2022.
- 2019 cuenta con datos parciales (a partir de septiembre).
- El periodo 2020–2023 muestra la demanda operativa completa.

</div>
</div>

---

# Tendencia por Municipio

<div style="display: flex; gap: 2rem; align-items: center;">
<div style="flex: 2;">

![Tendencia por municipio](analisis_emergencias/tendencia_por_municipio.png)

</div>
<div style="flex: 1; font-size: 1.05em;">

- **Guadalajara** y **Zapopan** concentran la mayor carga operativa.
- Municipios como **Tlajomulco** y **El Salto** muestran crecimiento sostenido.
- El crecimiento refleja la expansión urbana en la periferia del AMG.

</div>
</div>

---

# Tendencia por Tipo de Incidente

<div style="display: flex; gap: 2rem; align-items: center;">
<div style="flex: 2;">

![Tendencia por incidente](analisis_emergencias/tendencia_por_incidente.png)

</div>
<div style="flex: 1; font-size: 1.05em;">

- Los **incendios de pastizal** presentan clara **estacionalidad** (temporada de estiaje).
- Los **enjambres de abejas/avispas** son el segundo tipo más frecuente.
- El **Gas LP** es una emergencia recurrente y constante a lo largo de todos los años.

</div>
</div>

---

# Concentración Espacial: Mapas de Calor

Los mapas interactivos permiten identificar **zonas de alta densidad** de reportes para cada año.

<div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">

<div style="flex: 1; min-width: 160px; background: #f1f3f4; border-radius: 8px; padding: 1rem; text-align: center;">
🗺️ <a href="analisis_emergencias/mapa_calor_2019.html"><strong>2019</strong></a>
</div>
<div style="flex: 1; min-width: 160px; background: #f1f3f4; border-radius: 8px; padding: 1rem; text-align: center;">
🗺️ <a href="analisis_emergencias/mapa_calor_2020.html"><strong>2020</strong></a>
</div>
<div style="flex: 1; min-width: 160px; background: #f1f3f4; border-radius: 8px; padding: 1rem; text-align: center;">
🗺️ <a href="analisis_emergencias/mapa_calor_2021.html"><strong>2021</strong></a>
</div>
<div style="flex: 1; min-width: 160px; background: #f1f3f4; border-radius: 8px; padding: 1rem; text-align: center;">
🗺️ <a href="analisis_emergencias/mapa_calor_2022.html"><strong>2022</strong></a>
</div>
<div style="flex: 1; min-width: 160px; background: #f1f3f4; border-radius: 8px; padding: 1rem; text-align: center;">
🗺️ <a href="analisis_emergencias/mapa_calor_2023.html"><strong>2023</strong></a>
</div>

</div>

> 💡 Abrir los archivos `.html` directamente en el navegador para exploración interactiva.

---

# Conclusiones

<div style="font-size: 1.1em;">

1. 📈 **Tendencia creciente**: El volumen de emergencias ha aumentado consistentemente entre 2020 y 2022.
2. 🏙️ **Concentración urbana**: Guadalajara y Zapopan acumulan más del 50% de los reportes, aunque la periferia (Tlajomulco, El Salto) crece proporcionalmente más.
3. 🔥 **Incendios estacionales**: Los incendios de pastizal son altamente estacionales (estiaje marzo–mayo), lo que permite anticipar recursos.
4. 🐝 **Fauna urbana**: Los enjambres de abejas/avispas representan un reto operativo de alta frecuencia.
5. 📊 **Taxonomía**: La estandarización de la columna `Incidente` permite análisis comparativos que antes no eran posibles.

</div>

---

# Próximos Pasos

<div style="display: flex; gap: 2rem;">
<div style="flex: 1;">

### Datos
- Integración de datos 2024 al histórico
- Incorporar datos socioeconómicos (AGEB, INEGI)
- Validación de registros duplicados o sin coordenadas

</div>
<div style="flex: 1;">

### Análisis
- Modelado predictivo por temporada
- Análisis de tiempos de respuesta
- Clustering espacial de zonas de riesgo

</div>
<div style="flex: 1;">

### Productos
- Dashboard interactivo en tiempo real
- Reporte periódico automatizado
- Integración con sistemas de despacho

</div>
</div>

---

# Referencias

<div style="font-size: 1em; line-height: 1.8;">

- **Protección Civil Jalisco** – Registros históricos de atención de emergencias (2019–2023).
- **INEGI** – Marco Geoestadístico Municipal, Área Metropolitana de Guadalajara.
- **IIEG Jalisco** – Indicadores demográficos del AMG.
- **Folium / Leaflet.js** – Visualización de mapas interactivos. https://python-visualization.github.io/folium/
- **Seaborn / Matplotlib** – Visualización estadística en Python. https://seaborn.pydata.org
- **Marp** – Framework de presentaciones en Markdown. https://marp.app

</div>

---

<!-- _class: title -->

# Gracias

### Área Metropolitana de Guadalajara · Análisis de Emergencias 2019–2023

"""

# ─── Escribir el .md ─────────────────────────────────────────────────────────

print(f"Escribiendo presentación: {output_md}")
with open(output_md, "w", encoding="utf-8") as f:
    f.write(marp_template)

print("✅ presentacion_riesgos.md generado.")

# ─── Exportar a HTML ─────────────────────────────────────────────────────────

print("\nExportando a HTML...")
result_html = subprocess.run(
    ["npx", "-y", "@marp-team/marp-cli", output_md, "--html", "-o", output_html, "--allow-local-files"],
    cwd=output_dir,
    capture_output=True,
    text=True
)
if result_html.returncode == 0:
    print(f"✅ HTML exportado: {output_html}")
else:
    print(f"⚠️  Error en HTML:\n{result_html.stderr}")

# ─── Exportar a PDF ──────────────────────────────────────────────────────────

print("\nExportando a PDF (puede tardar unos segundos al descargar Chromium)...")
result_pdf = subprocess.run(
    ["npx", "-y", "@marp-team/marp-cli", output_md, "--pdf", "-o", output_pdf, "--allow-local-files"],
    cwd=output_dir,
    capture_output=True,
    text=True
)
if result_pdf.returncode == 0:
    print(f"✅ PDF exportado: {output_pdf}")
else:
    print(f"⚠️  Error en PDF:\n{result_pdf.stderr}")

print("\n🎉 Proceso completado.")
