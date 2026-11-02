# Resumen con ejercicios: sistemas de almacenamiento de datos y herramientas del centro de datos

> Basado en: IABD_M05_T01.pdf  
> Ejercicios obligatorios: IABD_M05_ACT_OBL_01.docx (Ejercicios 5 y 6)  
> Ejercicios optativos: IABD_M05_ACT_OPT_01.docx (Ejercicios 1–4) + Actividades_RA1.pdf (Ejercicios 1 y 2)

---

## 1. Tipos de Sistemas de Almacenamiento de Datos

### Conceptos previos clave

| Concepto | Definición |
|----------|-----------|
| **Escalabilidad vertical** (scaling up) | Mejorar un único servidor: más RAM, más CPU, más disco |
| **Escalabilidad horizontal** (scaling out) | Añadir más servidores/nodos que trabajan en paralelo |

---

### 1.1 Bases de Datos Relacionales (SQL)

Organizan la información en **tablas con filas y columnas** con esquema bien definido.

| Aspecto | Detalle |
|---------|---------|
| **Lenguaje** | SQL (Structured Query Language) |
| **Escalabilidad** | Vertical (más RAM/CPU en un servidor) |
| **Integridad** | Transacciones ACID, claves primarias/foráneas |
| **Datos** | Estructurados |
| **Ventajas** | Consistencia, consultas complejas, integridad garantizada |
| **Desventajas** | Poco flexible con datos no estructurados, limitada para Big Data masivo |
| **Ejemplos** | MySQL, PostgreSQL, Oracle |
| **Uso típico** | Aplicaciones de ventas, transacciones financieras, sistemas con datos estructurados |

> **ACID:** Atomicidad, Consistencia, Aislamiento, Durabilidad — garantiza que las transacciones son seguras y completas.

---

### 1.2 Bases de Datos NoSQL

Diseñadas para **datos no estructurados y semiestructurados**. Escalabilidad horizontal nativa.

#### Cuatro tipos principales

| Tipo | Cómo almacena | Ejemplos | Caso de uso |
|------|--------------|----------|-------------|
| **Clave-Valor** | Pares clave→valor | Redis, DynamoDB | Perfiles de usuario, gestión de sesiones, búsquedas rápidas |
| **Documentos** | Documentos JSON/BSON/XML | MongoDB, CouchDB | Aplicaciones web, catálogos de productos, contenido |
| **Columnas** | Familias de columnas (no filas) | Cassandra, HBase | Logs, análisis de grandes volúmenes distribuidos |
| **Grafos** | Nodos, aristas y propiedades | Neo4j, Amazon Neptune | Redes sociales, motores de recomendación |

**SQL vs NoSQL — diferencia clave:**

| | SQL | NoSQL |
|-|-----|-------|
| Transacciones fuertes (ACID) | ✓ Mayor soporte | Menor soporte |
| Escalabilidad | Vertical | Horizontal |
| Datos | Estructurados | No/semi estructurados |
| Esquema | Rígido | Flexible |

---

### 1.3 Almacenamiento en la Nube

Servicio que permite almacenar datos en **centros de datos remotos** accesibles por Internet.

| Tipo | Cómo funciona | Ejemplos | Uso |
|------|--------------|----------|-----|
| **Objetos** | Datos como objetos con metadatos e ID único; almacenados en buckets | Amazon S3, Google Cloud Storage, Azure Blob | Imágenes, vídeos, datos no estructurados |
| **Archivos** | Estructura jerárquica (carpetas/subcarpetas), acceso múltiple simultáneo | Amazon EFS, Google Filestore, Azure Files | Varios usuarios/servidores acceden al mismo archivo |
| **Bloques** | Datos divididos en bloques independientes de tamaño fijo | Amazon EBS, Google Persistent Disks, Azure Disk | Bases de datos, sistemas operativos, alta velocidad |

---

### 1.4 Modelos de Servicio en la Nube (IaaS / PaaS / SaaS)

| Modelo | Qué ofrece | El cliente gestiona | Ejemplo |
|--------|-----------|---------------------|---------|
| **IaaS** (Infrastructure as a Service) | Infraestructura virtualizada (servidores, redes, almacenamiento) | Software, configuraciones, aplicaciones | AWS EC2, Azure VMs |
| **PaaS** (Platform as a Service) | IaaS + herramientas de desarrollo, BBDD, servicios analíticos, SO | Solo las aplicaciones | Google App Engine, Heroku |
| **SaaS** (Software as a Service) | Aplicaciones completas en la nube | Nada (solo uso) | Gmail, Salesforce, Office 365 |

---

## 2. Procesamiento de Datos Almacenados

### 2.1 Indexación

Estructura que almacena referencias a los datos de forma organizada para **acelerar las búsquedas** (como el índice de un libro).

| Tipo | Descripción |
|------|-------------|
| **Índice simple** (SQL) | En una columna específica; evita revisar fila por fila |
| **Índice compuesto** | Usa varias columnas como criterio de búsqueda |
| **Índice NoSQL** | MongoDB crea índice en `_id` por defecto; permite índices adicionales |

**Desventajas:** mayor uso de disco y ralentiza escrituras (hay que actualizar el índice también).

---

### 2.2 Optimización de Consultas

| Técnica | En qué consiste |
|---------|----------------|
| **Uso de índices** | Reduce significativamente el número de filas a revisar |
| **Partición de tablas** | Divide la tabla original en partes más pequeñas gestionadas independientemente |
| **Desnormalización** | Combina tablas para evitar joins costosos (a costa de redundancia) |
| **Consultas paralelas** | Divide y vencerás: varias consultas pequeñas en paralelo |

---

### 2.3 Procesamiento Distribuido

Para volúmenes muy grandes: **Apache Hadoop** y **Apache Spark** distribuyen el procesamiento entre nodos.

#### MapReduce (Hadoop)

Paradigma de procesamiento masivo en clusters. Tres fases:

```
Datos de entrada
       ↓
  FASE MAP: divide en splits → cada nodo aplica función Map → pares clave-valor
       ↓
  SHUFFLE & SORT: reorganiza y ordena por clave
       ↓
  FASE REDUCE: agrupa por clave → función Reduce (sumas, estadísticas) → salida en HDFS
```

#### Apache Spark

Evolución de MapReduce que procesa los datos en **memoria RAM** (evita escrituras en disco entre pasos).

| Componente | Descripción |
|-----------|-------------|
| **RDD** (Resilient Distributed Dataset) | Unidad fundamental de datos: colección distribuida e inmutable que permite cálculos en paralelo |
| **DataFrames / Datasets** | Abstracciones modernas para datos estructurados y semiestructurados |
| **Spark Streaming** | Procesamiento en tiempo real |

**Ventaja clave de Spark vs Hadoop MapReduce:** mucho más rápido en tareas con múltiples iteraciones porque evita I/O de disco en cada paso.

---

## 3. Ingestión y Transformación de Datos

### 3.1 Tipos de Ingestión

| Tipo | Cuándo se procesa | Ideal para | Ejemplo |
|------|-------------------|-----------|---------|
| **Por lotes (Batch)** | A intervalos regulares (hora, día, semana) | Análisis históricos, grandes volúmenes sin urgencia | Informes diarios de ventas |
| **Tiempo real (Streaming)** | A medida que llegan los datos | Decisiones inmediatas, alertas | Detección de fraude, monitorización |
| **Arquitectura Lambda** | Combina ambos: capa de lotes + capa de velocidad + capa de servicio | Sistemas que necesitan ambos modos | Plataformas de análisis híbridas |

### 3.2 Transformación de Datos (ETL)

| Técnica | Qué hace |
|---------|---------|
| **Limpieza** | Eliminar duplicados, nulos, errores |
| **Filtrado** | Seleccionar subconjuntos según criterio |
| **Conversión de formatos** | Cambiar formato de los datos para su análisis |
| **Normalización** | Ajustar a rango común (ej: 0–1) |
| **Desnormalización** | Combinar tablas eliminando relaciones entre ellas |
| **Agregación** | Calcular promedios, sumas, máximos sobre los datos |

---

## 4. Presentación de Resultados

### 4.1 Herramientas de visualización

| Herramienta | Descripción | Ejemplos |
|------------|-------------|---------|
| **Dashboards interactivos** | Paneles de control con gráficos actualizados en tiempo real; filtros dinámicos | Tableau, Power BI, Google Data Studio |
| **Informes interactivos** | Permiten análisis ad-hoc, drill-down (detalle por capas), exportación PDF/Excel | Power BI, Tableau |
| **Elementos visuales avanzados** | Mapas geoespaciales, diagramas Sankey, gráficos de burbujas | — |

### 4.2 Storytelling con Datos

Contar historias a través de los datos para que los resultados tengan mayor impacto:
- **Narrativas visuales:** texto + imágenes + gráficos integrados
- **Contextualización:** explicar por qué los resultados son relevantes para los objetivos de la empresa
- Objetivo: comunicar los **insights más importantes**, no solo mostrar datos

---

## 5. Test Autoevaluativo — Respuestas

| Pregunta | Respuesta correcta |
|----------|-------------------|
| 1. Sistema que organiza datos en tablas con relaciones | **b) Bases de datos relacionales** |
| 2. Factor clave al diseñar un sistema de almacenamiento | **b) Seguridad de los datos** |
| 3. Método para optimizar búsqueda de datos | **a) Indexación** |
| 4. Técnica que procesa grandes volúmenes en intervalos regulares | **a) Procesamiento por lotes** |
| 5. Herramienta para dashboards interactivos | **a) Tableau** |

---

## 6. Ejercicios Obligatorios (ACT_OBL_01)

### Ejercicio 5 — Diagrama de base de datos para biblioteca (dbdiagram.io)

**Tablas y restricciones:**

```
Table Autores {
  AutorID     int         [pk]
  Nombre      varchar(100) [not null]
  Apellido    varchar(100) [not null]
}

Table Libros {
  LibroID          int          [pk]
  Titulo           varchar(200) [not null]
  AutorID          int          [ref: > Autores.AutorID]
  ISBN             varchar(13)  [unique, not null]
  AnioPublicacion  int          [note: '> 0']
}

Table Prestamos {
  PrestamoID      int   [pk]
  LibroID         int   [ref: > Libros.LibroID]
  FechaPrestamo   date  [not null]
  FechaDevolucion date
  UsuarioID       int   [not null]
}
```

**Reglas clave:**
- Cada libro tiene ISBN único
- Autores deben tener nombre Y apellido (ambos not null)
- `FechaDevolucion` puede ser NULL (libro aún no devuelto)
- `AnioPublicacion` debe ser > 0

> Implementar en [dbdiagram.io](https://dbdiagram.io) usando la sintaxis DBML anterior.

---

### Ejercicio 6 — Documentos JSON y consultas MongoDB (Mongo Playground)

#### Creación de 5 documentos JSON

Restricciones a cumplir:
- Al menos 1 cliente < 30 años
- Al menos 2 clientes < 30 años O de Madrid
- Solo 3 clientes con compras > 100€
- Al menos 1 cliente ha comprado un "Portátil"
- 1 cliente de ciudad distinta a Madrid, Barcelona o Sevilla

**Ejemplo de estructura de documento:**

```json
{
  "cliente_id": 1,
  "nombre": "Ana García",
  "edad": 25,
  "ciudad": "Madrid",
  "compras": [
    { "producto": "Portátil", "precio": 899.99, "fecha": "2024-03-15" },
    { "producto": "Ratón",    "precio": 29.99,  "fecha": "2024-03-20" }
  ]
}
```

#### Consultas MongoDB

**Consulta 1 — Clientes con alguna compra > 100€:**
```javascript
db.clientes.find({ "compras.precio": { $gt: 100 } })
```
*Usa el operador `$gt` (greater than) sobre el array de compras. MongoDB busca en cada elemento del array si algún precio supera 100€.*

---

**Consulta 2 — Nombre y ciudad de compradores de "Portátil":**
```javascript
db.clientes.find(
  { "compras.producto": "Portátil" },
  { nombre: 1, ciudad: 1, _id: 0 }
)
```
*Filtra por producto en el array y proyecta solo los campos `nombre` y `ciudad` (el `0` en `_id` lo excluye).*

---

**Consulta 3 — Clientes de Madrid con edad > 30:**
```javascript
db.clientes.find({
  ciudad: "Madrid",
  edad: { $gt: 30 }
})
```
*Combina dos condiciones con AND implícito. Filtra por ciudad exacta y edad mayor de 30.*

---

**Consulta 4 — Compras del cliente más joven:**
```javascript
db.clientes.find(
  {},
  { compras: 1, _id: 0 }
).sort({ edad: 1 }).limit(1)
```
*Ordena por edad ascendente (`1`) y toma el primer documento. Proyecta solo el array de compras.*

---

**Consulta 5 — Clientes con al menos 2 compras:**
```javascript
db.clientes.find({
  $expr: { $gte: [{ $size: "$compras" }, 2] }
})
```
*Usa `$size` para contar elementos del array `compras` y `$gte` para filtrar los que tienen 2 o más.*

---

## 7. Ejercicios Optativos (ACT_OPT_01)

### Ejercicio 1 — Cuatro tipos de NoSQL con ejemplos prácticos

| Tipo | Ejemplo de uso práctico |
|------|------------------------|
| **Clave-Valor** (Redis) | Almacenar sesiones de usuario en e-commerce: la clave es el `sessionID` y el valor los datos del carrito. Acceso en microsegundos. |
| **Documentos** (MongoDB) | Catálogo de productos en Amazon: cada producto es un documento JSON con campos variables (algunos tienen talla, otros peso, etc.). |
| **Columnas** (Cassandra) | Registro de logs de servidores: millones de escrituras por segundo distribuidas en nodos, consultas por rango de tiempo. |
| **Grafos** (Neo4j) | Motor de recomendación de Netflix: los nodos son usuarios y películas; las aristas representan "ha visto", "ha valorado", "es similar a". |

---

### Ejercicio 2 — Sistema de almacenamiento para red social emergente

**Tipo de base de datos:**
- **NoSQL de documentos (MongoDB)** para perfiles, publicaciones y comentarios (datos semi-estructurados, esquema variable)
- **NoSQL de grafos (Neo4j)** para relaciones entre usuarios (seguidos, seguidores, recomendaciones)
- **Clave-Valor (Redis)** para caché de sesiones y feeds en tiempo real

**Estrategia de escalabilidad:**
- **Escalabilidad horizontal**: añadir nodos cuando crezca la carga (NoSQL está diseñado para esto)
- **Sharding**: distribuir datos entre nodos por ID de usuario
- **Replicación**: copias en múltiples nodos para alta disponibilidad

**Medidas de seguridad:**
- Control de acceso con roles (solo el propio usuario modifica su perfil)
- Cifrado en tránsito (HTTPS/TLS) y en reposo
- Auditorías y monitorización de accesos anómalos
- Copias de seguridad automáticas y plan de recuperación ante desastres

---

### Ejercicio 3 — Almacenamiento en nube para e-commerce (imágenes + transacciones)

**Imágenes de productos → Almacenamiento de Objetos (Amazon S3)**
- Las imágenes son datos no estructurados de tamaño variable
- S3 ofrece escalabilidad prácticamente ilimitada con pago por uso
- Permite configurar metadatos (producto, categoría, fecha) para facilitar búsquedas
- Alta disponibilidad y durabilidad (99.999999999%)

**Transacciones financieras → Base de datos Relacional (RDS / Aurora)**
- Las transacciones requieren garantías ACID (no se puede perder un pago a medias)
- Datos estructurados: cliente, importe, fecha, estado
- Consultas SQL complejas para informes financieros
- También en nube: Amazon RDS, Google Cloud SQL

---

### Ejercicio 4 — Nube vs Almacenamiento Local para pequeña empresa

| Factor | Nube | Local |
|--------|------|-------|
| **Coste inicial** | Bajo (pago por uso) | Alto (hardware, instalación) |
| **Coste a largo plazo** | Puede crecer con el uso | Fijo una vez amortizado |
| **Escalabilidad** | Inmediata, ilimitada | Limitada, requiere nueva inversión |
| **Seguridad** | Gestionada por el proveedor (certificaciones) | Responsabilidad propia |
| **Accesibilidad** | Desde cualquier lugar con Internet | Solo en red local (VPN para remoto) |
| **Mantenimiento** | Gestionado por el proveedor | Equipo IT propio necesario |
| **Dependencia** | Del proveedor y la conexión a Internet | Independiente |

**Conclusión:** para una pequeña empresa sin equipo IT dedicado, la nube es generalmente más ventajosa por el menor coste inicial, la escalabilidad inmediata y la externalización del mantenimiento. El principal riesgo es la dependencia del proveedor y la conexión a Internet.

---

## 8. Actividades RA1 — Pandas, Polars, PySpark y MongoDB

### Ejercicio 1 — Comparación Pandas / Polars / PySpark con MovieLens 20M

**Dataset:** MovieLens 20M (`userId`, `movieId`, `rating`, `timestamp`, `title`, `genres`)

**Tareas a implementar (en cada herramienta):**
1. Cargar `movielens_superdataset.csv`
2. Filtrar películas de género "Action" con `rating ≥ 4`
3. Calcular media y desviación estándar de ratings por usuario
4. Ordenar películas por rating promedio descendente
5. Convertir `timestamp` a fecha legible
6. Medir tiempos de ejecución de cada operación

**Entornos:**
- **Pandas** → Google Colab
- **Polars** (normal + LazyFrame) → Google Colab
- **PySpark** → Databricks Community Edition

#### Diferencias clave entre herramientas

| | Pandas | Polars | PySpark |
|-|--------|--------|---------|
| **Ejecución** | Inmediata, en memoria | Inmediata o lazy (LazyFrame) | Distribuida en cluster |
| **Escalabilidad** | Un solo nodo, limitado a RAM | Un nodo, muy eficiente | Multi-nodo, Big Data real |
| **Velocidad (dataset pequeño)** | Buena | Muy buena (Rust) | Overhead de inicio alto |
| **Velocidad (dataset grande)** | Peor | Mejor que Pandas | Mejor para TB de datos |
| **LazyFrame (Polars)** | No | Sí — optimiza el plan antes de ejecutar | Similar a Spark DAG |
| **Uso en industria** | Análisis exploratorio, ML | Sustituto moderno de Pandas | Data Engineering, ETL masivo |

**Polars LazyFrame:**
- Modo normal: ejecuta cada operación inmediatamente
- LazyFrame: construye un plan de ejecución y lo optimiza antes de ejecutar → más eficiente, especialmente con múltiples operaciones encadenadas

**Preguntas de reflexión:**
1. **Diferencias de rendimiento:** Pandas es más lento con datasets grandes por limitaciones de memoria de un solo nodo; Polars es significativamente más rápido gracias a su implementación en Rust y paralelismo nativo; PySpark tiene overhead de inicio pero es el más escalable.
2. **Mejora con LazyFrame:** el optimizador puede reordenar operaciones, eliminar cálculos innecesarios y aplicar predicates pushdown (filtrar antes de cargar todo).
3. **Escalabilidad:** Pandas no escala bien; Polars mejora pero sigue siendo un solo nodo; PySpark es la solución para datasets que no caben en memoria.
4. **Uso en industria:** Pandas en ciencia de datos y prototipado; Polars como sustituto moderno de Pandas; PySpark en pipelines de datos a escala de producción.

---

### Ejercicio 2 — JSON y MongoDB (Mongo Playground)

*(Ver Ejercicio 6 de ACT_OBL_01 — misma estructura y consultas)*

El ejercicio de Actividades_RA1.pdf tiene exactamente las mismas restricciones y consultas que el Ejercicio 6 obligatorio. Referirse a la sección 6 de este documento para la solución completa.

---

## 9. Conceptos Clave para el Examen

| Concepto | Definición en una línea |
|----------|------------------------|
| **Big Data** | Conjuntos de datos demasiado grandes o complejos para herramientas tradicionales |
| **SQL** | BBDD relacional, esquema rígido, ACID, escalabilidad vertical |
| **NoSQL** | BBDD flexible, datos no estructurados, escalabilidad horizontal |
| **IaaS/PaaS/SaaS** | Infraestructura / Plataforma / Software como servicio en la nube |
| **MapReduce** | Map (pares clave-valor en paralelo) → Shuffle → Reduce (agrega por clave) |
| **Apache Spark** | MapReduce en memoria RAM — mucho más rápido en iteraciones |
| **RDD** | Unidad de datos de Spark: distribuida, inmutable, paralela |
| **Batch vs Streaming** | Por lotes (intervalos) vs tiempo real (continuo) |
| **Indexación** | Estructura para acelerar búsquedas a costa de más disco y más lenta escritura |
| **ETL** | Extract → Transform → Load: pipeline estándar de ingestión de datos |
| **Dashboard** | Panel de control con visualizaciones en tiempo real (Tableau, Power BI) |
| **Storytelling** | Contar historias con datos para comunicar insights de forma efectiva |
