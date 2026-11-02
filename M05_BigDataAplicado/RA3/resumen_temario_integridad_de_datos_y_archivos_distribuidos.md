# Resumen del temario: integridad de datos y mantenimiento de sistemas de archivos distribuidos
## Fuente exclusiva: IABD_M05_T03.pdf

---

## 1. Calidad de datos

### 1.1 Introducción
Los datos son el activo más valioso en el entorno Big Data. Datos de baja calidad generan decisiones erróneas y pérdidas económicas. La calidad implica que los datos sean **precisos, consistentes, completos y actuales**.

### 1.2 Técnicas de calidad de datos

#### 1.2.1 Validación de datos
Proceso que comprueba que los datos cumplen **reglas o restricciones** definidas (formatos, rangos, tipos).
- Validación de **tipos de datos**: comprobar que un campo numérico no contiene texto
- Validación de **rangos**: edad entre 0 y 120, precio > 0
- Validación de **formatos**: emails con `@`, fechas en formato `YYYY-MM-DD`
- Validación de **integridad referencial**: que una FK exista en la tabla referenciada

#### 1.2.2 Limpieza de datos
- Eliminación de **duplicados** (`drop_duplicates` en Pandas)
- Tratamiento de **valores nulos** (`dropna`, `fillna`)
- Eliminación de **valores fuera de rango** (ej: edad < 0 o > 120)
- Corrección de **errores** de formato y tipografía

#### 1.2.3 Normalización y estandarización
- **Normalización (Min-Max Scaling):** ajusta los valores al rango [0, 1]
  - `valor_normalizado = (valor - min) / (max - min)`
- **Estandarización (Z-score):** media = 0, desviación estándar = 1
  - Útil cuando los datos siguen distribución normal y en algoritmos de regresión lineal

#### 1.2.4 Monitoreo continuo
Control en tiempo real de la calidad de datos que avisa cuando se detectan valores anómalos. Herramienta: **Deequ** de Apache Spark, que implementa métricas predefinidas de calidad.

#### 1.2.5 Enriquecimiento de datos
Añadir información de fuentes externas para ampliar el valor de los datos originales. Ejemplo: combinar una BBDD de clientes con datos demográficos externos vía merge por ID.

#### 1.2.6 Data Profiling
Análisis de datos para entender sus características: distribuciones, frecuencias, correlaciones, outliers. Herramienta: **pandas-profiling** (ahora `ydata-profiling`) — genera informes HTML detallados automáticamente.

#### 1.2.7 Verificación de consistencia
Comprobar que no existen entidades con identificadores duplicados pero valores distintos (ej: mismo ID con dos nombres diferentes).

### 1.3 Herramientas alternativas
| Herramienta | Tipo | Característica |
|-------------|------|---------------|
| **Talend Data Preparation** | ETL con interfaz gráfica | Intuitivo, versiones gratuita y de pago |
| **Apache Spark (PySpark)** | Procesamiento distribuido | Open source, funciones de calidad integradas, Deequ |
| **OpenRefine** | Interfaz gráfica | Open source, datos estructurados y no estructurados |

---

## 2. Verificación de integridad de datos

En sistemas distribuidos la integridad es crítica: los datos viajan entre nodos y pueden corromperse por errores de red, hardware o ataques. Una corrupción puede causar decisiones empresariales erróneas (sector financiero, médico).

### 2.1 Suma de verificación (Checksum)
Un checksum es un **valor numérico** calculado a partir de un bloque de datos con un algoritmo específico. Se almacena y transmite junto con los datos. Al recibirlos, se recalcula el hash y se compara:
- **Coinciden** → datos íntegros
- **No coinciden** → datos alterados o corruptos

### 2.2 Algoritmos de checksum

| Algoritmo | Salida | Velocidad | Uso principal |
|-----------|--------|-----------|--------------|
| **CRC** (Cyclic Redundancy Check) | Residuo de división XOR | Muy rápido | Protocolos de red (Ethernet), detección de errores en transmisión |
| **MD5** (Message Digest Algorithm 5) | 128 bits (hexadecimal) | Rápido | Verificación de archivos descargados |
| **SHA** (Secure Hash Algorithm) | 256 bits | Más lento | Seguridad de información; difícil de revertir o colisionar |

**CRC:** divide el bloque de datos por un polinomio generador usando XOR; el residuo es el checksum.
**MD5:** mezclas, rotaciones y sumas sobre los datos → número hexadecimal de 128 bits.
**SHA-256:** procesa en bloques de 512 bits con operaciones bitwise → 256 bits; muy seguro.

### 2.3 Sumas de verificación en HDFS
HDFS implementa checksums de forma nativa:
1. Al **escribir** un bloque, HDFS genera un checksum y lo almacena junto al bloque en cada réplica
2. Al **leer**, HDFS recalcula el checksum y lo compara con el almacenado
3. Si **no coincide**, recupera el bloque desde otra réplica y notifica al administrador
4. Las verificaciones pueden hacerse de forma **asíncrona** para no degradar el rendimiento
5. Los algoritmos de consenso (Paxos/Raft) garantizan acuerdo sobre los checksums entre nodos

---

## 3. Migración de datos entre clústeres

Un clúster = conjunto de nodos/servidores que trabajan como sistema único. Mover datos entre clústeres es necesario por escalabilidad, rendimiento o migración de infraestructura.

### 3.1 Estrategias de transferencia

| Técnica | Descripción |
|---------|-------------|
| **Compresión** | Reducir tamaño antes de transferir → menor ancho de banda y más velocidad |
| **Transferencia incremental** | Migrar solo los datos que han cambiado desde la última migración |
| **Protocolos optimizados** | GridFTP, Rsync — minimizan tiempo de inactividad y errores |

### 3.2 Sincronización entre clústeres

| Tipo | Cuándo |
|------|--------|
| **Tiempo real** | Ambos clústeres siempre idénticos; herramientas: Apache Kafka, DataSync |
| **Por intervalos** | Sincronización periódica; menor carga en el sistema |
| **Manual** | El administrador inicia el proceso; máximo control humano |

### 3.3 Minimización de pérdidas
- **Copias de seguridad y restauración**: backups para recuperación en caso de fallo
- **Verificación de integridad durante la migración**: checksums en cada fase

### 3.4 Tipos de migración
- **Migración en caliente**: el sistema sigue funcionando mientras se migran los datos
- **Migración en frío**: el sistema está fuera de línea durante la migración

---

## 4. Gestión de metadatos

Los **metadatos** son datos sobre datos: describen la estructura, ubicación, estado y contexto de los datos principales.

### Tipos de metadatos

| Tipo | Qué describe |
|------|-------------|
| **Descriptivos** | Contenido (título, autor, descripción) |
| **Estructurales** | Organización de los datos |
| **Administrativos** | Origen, acceso, derechos de uso |

### Importancia en sistemas distribuidos
- Permiten a HDFS **identificar la ubicación de cada bloque** en el clúster
- Facilitan la **búsqueda y recuperación** de datos
- Permiten **control de versiones** cuando los datos cambian continuamente
- Durante la migración, los metadatos deben transferirse y actualizarse para reflejar la nueva ubicación

### Desafíos de los metadatos
- **Escalabilidad**: a más datos, más metadatos
- **Consistencia**: los datos cambian de nodo → los metadatos deben actualizarse; se usan replicación y algoritmos de consenso
- **Disponibilidad**: los metadatos deben estar siempre disponibles → almacenados en sistemas altamente redundantes

---

## 5. Conceptos clave (glosario)

| Término | Definición |
|---------|-----------|
| **Integridad de datos** | Los datos son precisos, consistentes y no han sido alterados |
| **Checksum / Suma de verificación** | Valor numérico calculado de un bloque de datos para verificar que no ha sido alterado |
| **CRC** | Algoritmo de checksum rápido; residuo de división XOR; usado en protocolos de red |
| **MD5** | Hash de 128 bits; verificación de archivos |
| **SHA-256** | Hash de 256 bits; alta seguridad |
| **Data Profiling** | Análisis automático de distribuciones, frecuencias y patrones de un dataset |
| **Normalización** | Ajustar valores al rango [0, 1] (Min-Max Scaling) |
| **Estandarización** | Ajustar datos a media=0 y std=1 (Z-score) |
| **Metadatos** | Datos que describen otros datos (ubicación, estructura, acceso) |
| **Migración en caliente** | Migración de datos con el sistema en funcionamiento |
| **Migración en frío** | Migración de datos con el sistema fuera de línea |
| **Deequ** | Librería de Apache Spark para monitoreo continuo de calidad de datos |
| **Enriquecimiento** | Añadir información de fuentes externas a los datos originales |
