---
marp: false
theme: default
paginate: true
html: true
header: " "
footer: "Análisis de Emergencias AMG 2019–2023"
---
<style>
  section {
    font-family: 'Arial', sans-serif;
    font-size: 24px;
    padding: 40px;
  }
  h1 { font-size: 1.6em; color: #1a73e8; line-height: 1.2; border-bottom: none; }
  h2 { font-size: 1.1em; color: #555; border-bottom: none; margin-top: 5px; }
  h3 { font-size: 0.9em; color: #777; font-weight: normal; }
  
  .participants {
    font-size: 0.7em;
    margin-top: 25px;
    line-height: 1.5;
  }
  .participants a { color: #1a73e8; text-decoration: none; }

  .tag {
    display: inline-block;
    background: #e8f0fe;
    color: #1a73e8;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.7em;
    margin: 2px;
  }
  
  /* Ajuste de columnas para evitar desbordamiento */
  .content-wrapper {
    display: grid;
    grid-template-columns: 1.6fr 1.2fr;
    gap: 20px;
    align-items: start;
    margin-top: 10px;
  }
  
  .image-col {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  
  .image-col img {
    max-height: 420px;
    max-width: 100%;
    object-fit: contain;
    border: 1px solid #eee;
  }

  .text-col {
    font-size: 0.8em;
    line-height: 1.35;
  }
  
  .text-col h3 {
    margin: 0 0 8px 0;
    font-size: 1.1em;
  }

  /* Estilo para listado de mapas interactivos */
  .map-list {
    margin-top: 20px;
    list-style: none;
    padding: 0;
  }
  .map-list a {
    display: block;
    padding: 8px 0;
    color: #1a73e8;
    text-decoration: none;
    font-weight: bold;
    border-bottom: 1px solid #eee;
  }
  
  /* Formato de Tablas Compacto */
  table {
    width: 100%;
    font-size: 0.85em;
    border-collapse: collapse;
    margin: 8px 0;
    border: 1px solid #e0e0e0;
    table-layout: auto;
  }
  th {
    background-color: #f1f3f4;
    color: #1a73e8;
    padding: 6px;
    text-align: left;
    border-bottom: 2px solid #1a73e8;
  }
  td {
    padding: 4px 6px;
    border-bottom: 1px solid #eee;
  }
  tr:nth-child(even) {
    background-color: #fafafa;
  }
  
  img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }
  
  .logos-container {
    position: absolute;
    bottom: 30px;
    right: 40px;
    display: flex;
    gap: 20px;
    align-items: center;
  }
  .logos-container img {
    height: 60px;
    width: auto;
    border-radius: 0;
  }

  .cluster-grid {
    display: flex;
    gap: 15px;
    justify-content: center;
    align-items: flex-start;
  }
  .cluster-item {
    flex: 1;
    text-align: center;
  }
  .cluster-item img {
    width: 100%;
    border: 1px solid #444;
  }
  .cluster-item p {
    font-size: 0.7em;
    margin-top: 5px;
    color: #666;
    font-weight: bold;
  }
</style>

# Integración de políticas de mitigación de riesgo en la actualización de instrumentos de planeación municipal
## Histórico de Emergencias: Análisis de Tendencias y Concentración Espacial
### Área Metropolitana de Guadalajara · 2019–2023

<div class="participants">

**Ana Díaz-Aldret** | [orcid.org/0000-0001-5759-7563](http://orcid.org/0000-0001-5759-7563)  
**Mayra Gamboa-González** | [orcid.org/0000-0003-1260-0241](https://orcid.org/0000-0003-1260-0241)  
**Alejandro Padilla-Lepe** | [orcid.org/0000-0002-8164-7601](https://orcid.org/0000-0002-8164-7601)

</div>

<div class="logos-container">
  <img src="logotipos/logo_udg.png" alt="Logo Universidad de Guadalajara">
  <img src="logotipos/logo_unam.png" alt="Logo UNAM">
</div>

---

# Introducción

<div class="content-wrapper">
<div style="flex: 1.2;">

- El **Área Metropolitana de Guadalajara (AMG)** concentra más de **5.2 millones** de habitantes distribuidos en 10 municipios.
- La gestión de emergencias es competencia de las **unidades de Protección Civil** y bomberos municipales.
- Contar con un **análisis histórico estandarizado** permite identificar patrones, planificar recursos y tomar decisiones basadas en evidencia.

</div>
<div style="flex: 1; background: #f8f9fa; padding: 1.5rem; border-left: 5px solid #1a73e8;">

**Fuente de datos**
Registros históricos del Sistema de Emergencias del AMG (2019–2023), con más de **158,000 reportes** georeferenciados.

</div>
</div>

---

# Objetivos

<div class="content-wrapper">
<div class="image-col">

## Objetivos de análisis
1. Identificar la **tendencia anual** de emergencias en el AMG.
2. Comparar la **carga por municipio** a lo largo del tiempo.
3. Detectar los **tipos de incidentes más frecuentes**.
4. Visualizar la **concentración espacial** por año.


</div>
<div class="text-col">

| Dimensión | Variable |
|---|---|
| Temporal | Año (2019–2023) |
| Territorial | Municipio |
| Tipológica | Incidente |
| Geoespacial | Coordenadas X Y |

</div>
</div>

---

# Metodología

<div class="content-wrapper">
<div class="image-col">

### Procesamiento
- Se descargaron los reportes de emergencias del sitio web de Zoom Metropolitano.
- Se generó el archivo CSV.
- Estandarización de fechas y extracción de año.
- Estandarización de incidentes con 20+ categorías agrupadas por palabras clave.
- Ejecución de clustering espacial (**DBSCAN**) para identificación de núcleos críticos.
- Análisis de **niveles de priorización** estatal y municipal para sitios recurrentes.
- Evaluación de **vulnerabilidad física ante incendios** y marginación urbana.

</div>
<div class="text-col" style="background: #f8f9fa; padding: 15px; border-radius: 8px;">

**Principales categorías estandarizadas**
<span class="tag">Incendio Pastizal</span> <span class="tag">Gas LP / Fuga</span>
<span class="tag">Enjambre Abejas</span> <span class="tag">Accidente Vial</span>
<span class="tag">Atención Prehospitalaria</span> <span class="tag">Rescate</span>
<span class="tag">Inundación</span> <span class="tag">Corto Circuito</span>
<span class="tag">Pirotecnia</span> <span class="tag">Fauna/Animales</span>

</div>
</div>

---

# Tendencias

<div class="content-wrapper">
<div class="image-col">

![Tendencia anual](analisis_emergencias/tendencia_anual_total.png)

</div>
<div class="text-col">

- El volumen de emergencias aumentó notablemente entre 2019 y 2022.
- 2019 cuenta con datos parciales (a partir de septiembre).
- El periodo 2020–2023 muestra la demanda operativa completa.

</div>
</div>

---

# Tendencia por Municipio

<div class="content-wrapper">
<div class="image-col">

![Tendencia por municipio](analisis_emergencias/tendencia_por_municipio.png)

</div>
<div class="text-col">

- **Guadalajara** y **Zapopan** concentran la mayor carga operativa histórica.
- Municipios como **Tlajomulco** y **El Salto** muestran crecimiento sostenido.
- El crecimiento refleja la expansión urbana en la periferia del AMG.

</div>
</div>

---

# Tendencia por Tipo de Incidente

<div class="content-wrapper">
<div class="image-col">

![Tendencia por incidente](analisis_emergencias/tendencia_por_incidente.png)

</div>
<div class="text-col">

- **Derrame de hidrocarguros**: Derrame de hidrocarburos.
- **Incendios de pastizal**: Alta estacionalidad (marzo–mayo).
- **Enjambres**: Segundo incidente en frecuencia absoluta.
- **Fugas de Gas LP**: Emergencia crítica con presencia constante durante todo el año.

</div>
</div>

---

# Concentración Espacial: Mapas de Calor

Los mapas interactivos identifican zonas de alta densidad de reportes por año.

<div class="map-list">
  <a href="analisis_emergencias/mapa_calor_2019.html">Mapa 2019</a>
  <a href="analisis_emergencias/mapa_calor_2020.html">Mapa 2020</a>
  <a href="analisis_emergencias/mapa_calor_2021.html">Mapa 2021</a>
  <a href="analisis_emergencias/mapa_calor_2022.html">Mapa 2022</a>
  <a href="analisis_emergencias/mapa_calor_2023.html">Mapa 2023</a>
</div>

*Nota: Abrir los archivos HTML para navegación y análisis de clusters.*

---

# Análisis de Clustering Espacial (DBSCAN)

<div class="content-wrapper">
<div class="image-col">

![Resumen clustering](analisis_emergencias/clustering_resumen.png)

</div>
<div class="text-col">

### Metodología
- Se utilizó el algoritmo **DBSCAN** para detectar concentraciones de alta densidad.
- **Parámetros**: EPS de ~400m y un mínimo de 30 reportes por zona.
- **Objetivo**: Diferenciar entre incidentes aislados (ruido) y núcleos operativos recurrentes.

</div>
</div>

---

# Evolución de Clusters: 2019–2021

<div class="cluster-grid">
  <div class="cluster-item">
    <img src="analisis_emergencias/clustering_2019.png">
    <p>2019</p>
  </div>
  <div class="cluster-item">
    <img src="analisis_emergencias/clustering_2020.png">
    <p>2020</p>
  </div>
  <div class="cluster-item">
    <img src="analisis_emergencias/clustering_2021.png">
    <p>2021</p>
  </div>
</div>

---

# Evolución de Clusters: 2022–2023

<div class="cluster-grid">
  <div class="cluster-item">
    <img src="analisis_emergencias/clustering_2022.png">
    <p>2022</p>
  </div>
  <div class="cluster-item">
    <img src="analisis_emergencias/clustering_2023.png">
    <p>2023</p>
  </div>
</div>

---

# Expansión Urbana y Estructura Vial Primaria

<div class="content-wrapper">
<div class="image-col">

![Crecimiento Urbano](analisis_territorial/mapa_expansion_vialidades.png)

</div>
<div class="text-col">

### Dinámica Territorial
- La superficie urbana se ha duplicado desde **1990**, alcanzando los **1,107 km²** en 2015.
- El **Sistema Vial Primario (VP)** articula el crecimiento hacia el sur y noreste del AMG.

| Periodo | Área (km²) |
| :--- | :---: |
| 1990 | 538.31 |
| 2000 | 690.90 |
| 2010 | 824.10 |
| **2015** | **1,106.99** |

</div>
</div>

---

# Grado de Marginación Urbana (2020)

<div class="content-wrapper">
<div class="image-col">

![Marginación](analisis_territorial/mapa_marginacion_urbana.png)

</div>
<div class="text-col">

### Vulnerabilidad por Colonia
- Se analizaron **1,991 colonias** en el AMG.
- **340 colonias** presentan grados de marginación **Altos o Muy altos**, localizándose mayoritariamente en las periferias.
- Existe una superposición entre la baja calidad de servicios y las zonas vulnerables a inundaciones.

| Grado | Colonias |
| :--- | :---: |
| Muy alto | 41 |
| Alto | 299 |
| Medio | 518 |
| Bajo | 570 |
| Muy bajo | 563 |

</div>
</div>

---

# Vulnerabilidad Física ante Incendios

<div class="content-wrapper">
<div class="image-col">

![Vulnerabilidad Incendios](analisis_riesgo/mapa_vulnerabilidad_incendios.png)

</div>
<div class="text-col">

### Riesgos por Exposición
- Se evaluaron **3,020 km²** del territorio metropolitano.
- El **39%** de la superficie analizada presenta vulnerabilidad **Alta o Muy alta**.
- La identificación de estas zonas permite orientar políticas de protección civil y ordenamiento territorial.

| Nivel | Superficie (km²) |
| :--- | :---: |
| Muy alta | 438.10 |
| Alta | 744.81 |
| Media | 333.15 |
| Baja | 731.31 |
| Muy baja | 772.95 |

</div>
</div>

---

# Cruce 1: Huella Urbana vs. Incendios

<div class="content-wrapper">
<div class="image-col">

![Cruce Huella](analisis_cruces/mapa_cruce_huella_incendio.png)

</div>
<div class="text-col">

### Análisis de Exposición
- Se analizó la intersección de la huella urbana 2015 con las zonas de riesgo de incendio.
- **26.8 km²** de la ciudad se encuentran bajo riesgo directo.
- Representa el **2.4%** de la mancha urbana total, principalmente en zonas de interfase.

| Variable | Valor |
| :--- | :---: |
| Área Urbana 2015 | 1,107 km² |
| Área en Riesgo | 26.77 km² |
| % Expuesta | 2.4% |

</div>
</div>

---

# Cruce 2: Marginación vs. Incendios

<div class="content-wrapper">
<div class="image-col">

![Cruce Marginación](analisis_cruces/mapa_cruce_marginacion_incendio.png)

</div>
<div class="text-col">

### Triple Vulnerabilidad
- Se cruzaron colonias con **Marginación Alta/Muy Alta** y riesgo de incendio.
- **57 colonias críticas** se localizan en zonas de alta vulnerabilidad física.
- Estas áreas requieren atención prioritaria por su limitada capacidad de respuesta.

| Categoría | Cantidad |
| :--- | :---: |
| Colonias Críticas | 340 |
| En Riesgo Incendio | 57 |
| % Colonias | 16.8% |

</div>
</div>

---

# Cruce 3: Inundación vs. Incendio

<div class="content-wrapper">
<div class="image-col">

![Cruce Sitios](analisis_cruces/mapa_cruce_sitios_incendio.png)

</div>
<div class="text-col">

### Diferenciación de Riesgos
- Se contrastaron los **sitios recurrentes de inundación** con la vulnerabilidad a incendios.
- **Resultado**: 0 coincidencias detectadas entre los 1,037 sitios.
- Esto confirma una **separación geoespacial** clara entre los riesgos hídricos (fondo de valle) y de incendio (laderas/bosque).

</div>
</div>

---

# Priorización de Sitios Recurrentes (2022-2023)

<div class="content-wrapper">
<div class="image-col">

![Sitios por municipio](analisis_priorizacion/sitios_por_municipio.png)

</div>
<div class="text-col">

### Análisis de Priorización
- Se analizaron **1,037 registros** de sitios recurrentes documentados.
- **Zapopan** y **Guadalajara** concentran la mayor densidad de sitios que requieren intervención técnica.
- El análisis integra variables de recurrencia y nivel de riesgo reportado.

</div>
</div>

---

# Niveles de Priorización en el AMG

<div class="content-wrapper">
<div class="image-col">

![Distribución Prioridades](analisis_priorizacion/distribucion_prioridades.png)

</div>
<div class="text-col" style="background: #f8f9fa; padding: 15px; border-radius: 8px;">

**Hallazgos Clave**
- Los niveles **Media** y **Alta** predominan en las zonas de expansión urbana.
- Existe una alta correlación entre los clusters de emergencias históricas y los sitios priorizados.

<div class="map-list" style="margin-top: 20px;">
  <a href="analisis_priorizacion/mapa_priorizacion_interactivo.html">Ver Mapa Interactivo de Priorización</a>
</div>

</div>
</div>

---

# Conclusiones

- **Tendencia creciente**: El volumen de emergencias ha aumentado consistentemente entre 2020 y 2022.
- **Concentración urbana**: Guadalajara y Zapopan acumulan más del 50% de los reportes.
- **Incendios estacionales**: La recurrencia en el periodo de estiaje permite anticipar la asignación de recursos.
- **Fauna urbana**: Los enjambres representan un reto operativo de alta frecuencia.
- **Zonas críticas (Clusters)**: El análisis DBSCAN identifica núcleos persistentes de alta densidad, fundamentando la priorización espacial en los programas de mitigación.
- **Expansión y Exposición**: El crecimiento de la huella urbana (duplicada desde 1990) y la extensión del sistema vial primario incrementan la exposición en zonas de reciente consolidación.
- **Vulnerabilidad Social**: Los altos grados de marginación en la periferia agudizan el impacto de las emergencias recurrentes (57 colonias críticas en riesgo de incendio).
- **Diferenciación de Riesgos**: El análisis de cruces confirma una clara separación geográfica entre riesgos de inundación e incendio, permitiendo el diseño de estrategias territoriales diferenciadas.
- **Estandarización**: Permite análisis comparativos robustos para la planeación académica y gubernamental.


<!--
---

# Próximos Pasos

<div class="content-wrapper">
<div style="flex: 1;">

### Datos
- Búsqueda e integración de datos 2024.
- Incorporar datos socioeconómicos de INEGI.
- Validación de duplicados.

</div>
<div style="flex: 1;">

### Análisis
- Modelado predictivo de impacto.
- Análisis de tiempos de respuesta por zona.
- Integración de indicadores de vulnerabilidad social (INEGI).

</div>
</div>
-->
---

# Referencias

- **IMEPLAN** – Zoom metropolitano.
- **Protección Civil Jalisco** – Registros históricos de atención (2019–2023).
- **INEGI** – Marco Geoestadístico Municipal, AMG.
- **CONAVI** – Indicadores de vivienda.
<!--
- **Folium / Leaflet.js** – Visualización de mapas interactivos.
- **Seaborn / Matplotlib** – Visualización estadística en Python.
- **Marp** – Framework de presentaciones Markdown.
-->
---

# Gracias

### Integración de políticas de mitigación de riesgo
Análisis de Emergencias AMG 2019–2023