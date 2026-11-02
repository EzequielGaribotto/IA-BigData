# Resumen del temario: sistemas de almacenamiento de datos y herramientas del centro de datos
## Fuente exclusiva: IABD_M05_T01.pdf

---

## 1. Tipos de sistemas de almacenamiento

### Conceptos previos

| Concepto | Definición |
|----------|-----------|
| **Escalabilidad vertical** (scaling up) | Mejorar un servidor único: más RAM, CPU, disco |
| **Escalabilidad horizontal** (scaling out) | Añadir más servidores/nodos que trabajan juntos distribuyendo el trabajo |

---

### 1.1 Bases de datos relacionales (SQL)

- Organizan la información en **tablas con filas y columnas** con esquema bien definido
- Lenguaje: **SQL** (Structured Query Language)
- Integridad garantizada mediante claves primarias, foráneas y restricciones
- **Escalabilidad vertical** — limitadas para volúmenes extremadamente grandes
- Buena integración con sistemas Big Data como Hadoop para extracción de datos
- **Ideal para:** transacciones complejas y datos con estructura clara y bien definida
- **Transacciones ACID:** Atomicidad, Consistencia, Aislamiento, Durabilidad — garantizan mayor soporte y consistencia frente a NoSQL

---

### 1.2 Bases de datos NoSQL

- Diseñadas para datos **no estructurados y semiestructurados** (vídeos, imágenes, texto, audio)
- **Escalabilidad horizontal** — añaden servidores según crece la carga
- No usan SQL; se adaptan a diferentes tipos de datos y aplicaciones

#### Cuatro tipos de NoSQL

| Tipo | Almacenamiento | Ejemplos | Uso típico |
|------|---------------|---------|------------|
| **Clave-Valor** | Pares clave→valor, acceso por clave única | Redis, Amazon DynamoDB | Perfiles de usuario, gestión de sesiones, búsquedas rápidas |
| **Documentos** | Documentos JSON/BSON/XML, pueden ser anidados | MongoDB, CouchDB | Apps web, plataformas de contenido, catálogos de productos |
| **Columnas** | Familias de columnas (no filas) | Apache Cassandra, HBase | Big Data distribuido, almacenamiento de logs |
| **Grafos** | Nodos, aristas y propiedades | Neo4j, Amazon Neptune | Análisis de redes sociales, motores de recomendación |

> **SQL vs NoSQL:** para transacciones fuertes (ACID), SQL garantiza mayor soporte y consistencia.

---

### 1.3 Almacenamiento en la nube

Servicio que permite almacenar datos en centros de datos remotos gestionados por un proveedor. Accesibles desde cualquier dispositivo con Internet.

| Tipo | Cómo almacena | Ejemplos | Uso |
|------|--------------|---------|-----|
| **Objetos** | Datos como "objetos" con metadatos + identificador único; en buckets | Amazon S3, Google Cloud Storage, Azure Blob | Imágenes, vídeos, datos no estructurados; escalabilidad ilimitada |
| **Archivos** | Estructura jerárquica (carpetas/subcarpetas); protocolos NFS/SMB | Amazon EFS, Google Filestore, Azure Files | Varios usuarios/servidores acceden a los mismos archivos simultáneamente |
| **Bloques** | Datos divididos en bloques de tamaño fijo gestionados independientemente | Amazon EBS, Google Persistent Disks, Azure Disk | Bases de datos, sistemas operativos; baja latencia, alto rendimiento |

---

### 1.4 Modelos de servicio en la nube

| Modelo | Qué proporciona | El cliente gestiona |
|--------|----------------|---------------------|
| **IaaS** (Infrastructure as a Service) | Infraestructura virtualizada: servidores, máquinas virtuales, redes, almacenamiento | Software, configuraciones, aplicaciones |
| **PaaS** (Platform as a Service) | IaaS + herramientas de desarrollo, BBDD, servicios analíticos, SO | Solo las aplicaciones |
| **SaaS** (Software as a Service) | Aplicaciones completas en cloud; copias de seguridad continuas | Solo el uso |

---

### 1.5 Diseño y gestión de sistemas de almacenamiento

**Factores clave:**

**Seguridad** — 4 componentes esenciales:
1. **Control de acceso:** roles y niveles de usuario para evitar accesos no autorizados
2. **Cifrado de datos:** datos almacenados y en tránsito cifrados
3. **Auditorías:** detección de accesos anómalos, monitoreo en tiempo real
4. **Copias de seguridad:** respaldo ante fallos + planes de recuperación ante desastres

**Escalabilidad** — elegir entre vertical u horizontal según previsión de crecimiento

**Costos** — estrategias de optimización:
- **Tiered storage:** datos frecuentes en discos rápidos, menos frecuentes en discos económicos
- **Compresión de datos:** reducen el espacio ocupado
- **Deduplicación:** eliminar copias redundantes

**Metodología de diseño en 8 pasos:**
1. Definir requisitos (volumen, tipos de datos, frecuencia de acceso, regulaciones)
2. Elegir tipo de almacenamiento
3. Estrategia de escalabilidad
4. Seguridad y control de acceso
5. Optimización del rendimiento (indexación, caché, balanceo de carga)
6. Gestión del flujo de datos (batch vs tiempo real)
7. Recuperación de desastres
8. Mantenimiento y monitoreo

---

## 2. Procesamiento de datos almacenados

### 2.1 Indexación

Estructura que almacena referencias a los datos de forma organizada para **acelerar búsquedas** (como el índice de un libro).

| Tipo | Descripción |
|------|-------------|
| **SQL — índice simple** | En columna específica; evita revisar fila por fila |
| **Índice compuesto** | Usa varias columnas como criterio |
| **NoSQL (MongoDB)** | Índice automático en `_id`; permite adicionales |

**Desventajas:** mayor uso de espacio en disco; ralentiza escrituras (hay que actualizar el índice).

---

### 2.2 Optimización de consultas

| Técnica | En qué consiste |
|---------|----------------|
| **Uso de índices** | Reduce filas a revisar significativamente |
| **Partición de tablas** | Divide la tabla en partes más pequeñas gestionadas independientemente |
| **Desnormalización** | Combinar tablas para evitar joins costosos (a costa de redundancia) |
| **Consultas paralelas** | Divide y vencerás: varias consultas pequeñas en paralelo |

---

### 2.3 Procesamiento distribuido

Para volúmenes muy grandes se usan frameworks que distribuyen el procesamiento entre nodos.

#### MapReduce (Hadoop)

Paradigma de procesamiento masivo en clusters. Tres fases:

```
Datos de entrada → división en splits (bloques de 128-256 MB)
        ↓
FASE MAP: cada nodo aplica función Map → pares clave-valor (en paralelo)
        ↓
FASE SHUFFLE & SORT: reorganiza y ordena datos intermedios por clave
        ↓
FASE REDUCE: agrupa por clave → función Reduce (sumas, estadísticas) → salida en HDFS
```

#### Apache Spark

Evolución de MapReduce. Procesa datos directamente en **memoria RAM** (evita I/O de disco entre pasos → mucho más rápido en iteraciones).

| Componente | Descripción |
|-----------|-------------|
| **RDD** (Resilient Distributed Dataset) | Unidad fundamental: colección distribuida e inmutable, permite cálculos en paralelo |
| **DataFrames / Datasets** | Abstracciones modernas para datos estructurados/semiestructurados |
| **Spark Streaming** | Procesamiento en tiempo real |

---

## 3. Ingestión y transformación de datos

### 3.1 Tipos de ingestión

| Tipo | Cuándo se procesa | Ideal para |
|------|------------------|-----------|
| **Por lotes (Batch)** | A intervalos regulares (hora, día, semana) | Análisis históricos, grandes volúmenes sin urgencia |
| **Tiempo real** | Continuamente, a medida que llegan | Decisiones inmediatas, infraestructura más compleja |
| **Arquitectura Lambda** | Combina ambos: capa de lotes + capa de velocidad + capa de servicio | Sistemas que necesitan los dos modos |

### 3.2 Transformación de datos

| Técnica | Descripción |
|---------|-------------|
| **Limpieza** | Eliminar duplicados, nulos, errores |
| **Filtrado** | Seleccionar subconjuntos según criterio |
| **Conversión de formatos** | Cambiar formato para su análisis |
| **Normalización** | Ajustar a rango común (ej: 0–1) |
| **Desnormalización** | Combinar tablas eliminando relaciones |
| **Agregación** | Calcular promedios, sumas, máximos |

> El PDF indica que este apartado se verá más a fondo en el Módulo 4 (Sistemas de Big Data).

---

## 4. Presentación de resultados

### 4.1 Dashboards interactivos

Paneles de control con vista gráfica de datos actualizada en tiempo real. Permiten filtrar y personalizar vistas. Tipos de gráficos: barras, líneas, áreas, mapas de calor.

**Ejemplos:** Tableau, Power BI, Google Data Studio

### 4.2 Informes interactivos

Informes con funcionalidades de exploración activa:
- **Análisis ad-hoc:** ajustar parámetros para vistas personalizadas
- **Drill-down / drill-through:** profundizar de visión general a detalle
- **Exportación:** PDF, Excel, etc.

### 4.3 Elementos visuales avanzados

- **Mapas geoespaciales:** datos con componente geográfica
- **Diagramas Sankey:** flujo de información entre etapas de un proceso
- **Gráficos de dispersión/burbujas:** relaciones entre múltiples variables

### 4.4 Storytelling con datos

Contar historias a través de los datos para que los resultados tengan mayor impacto:
- **Narrativas visuales:** texto + imágenes + gráficos integrados
- **Contextualización:** explicar por qué los resultados son relevantes para los objetivos de la empresa

---

## 5. Conceptos clave (glosario del PDF)

| Término | Definición |
|---------|-----------|
| **Big Data** | Conjuntos de datos demasiado grandes o complejos para herramientas tradicionales |
| **SQL / RDBMS** | BBDD con tablas relacionadas, ACID, escalabilidad vertical |
| **NoSQL** | BBDD flexible para datos no estructurados, escalabilidad horizontal |
| **IaaS/PaaS/SaaS** | Modelos de servicio cloud: infraestructura / plataforma / software |
| **MapReduce** | Map (pares clave-valor en paralelo) → Shuffle → Reduce (agrega por clave) |
| **Apache Spark** | MapReduce en memoria RAM — más rápido en iteraciones |
| **RDD** | Unidad fundamental de Spark: distribuida, inmutable, paralela |
| **Indexación** | Estructura para acelerar búsquedas a costa de espacio y velocidad de escritura |
| **Batch** | Procesamiento por lotes a intervalos regulares |
| **Tiempo real** | Procesamiento continuo a medida que llegan los datos |
| **ETL** | Extract → Transform → Load: pipeline estándar de ingestión |
| **Dashboard** | Panel de control con visualizaciones dinámicas (Tableau, Power BI) |
| **Storytelling** | Contar historias con datos para comunicar insights con mayor impacto |

---

## 6. Test autoevaluativo (respuestas)

| Pregunta | Respuesta |
|----------|----------|
| 1. Sistema que organiza datos en tablas con relaciones | **b) Bases de datos relacionales** |
| 2. Factor clave en diseño de almacenamiento | **b) Seguridad de los datos** |
| 3. Método para optimizar búsqueda | **a) Indexación** |
| 4. Técnica que procesa datos en intervalos regulares | **a) Procesamiento por lotes** |
| 5. Herramienta para dashboards interactivos | **a) Tableau** |

---

## 7. Actividades del PDF ("Ponlo en práctica")

**Actividad 1:** Tabla comparativa SQL / NoSQL / Cloud con: tipo de datos, ventajas, desventajas, escalabilidad, casos de uso. Reflexión sobre cuál elegir para grandes volúmenes en tiempo real.

**Actividad 2:** Elegir entre SQL y NoSQL para: (1) aplicación de ventas con datos estructurados y consultas SQL → SQL; (2) análisis de redes sociales con datos no estructurados y tiempo real → NoSQL.
