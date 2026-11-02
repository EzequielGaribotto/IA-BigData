# Resumen del temario: monitorización, optimización y solución de sistemas
## Fuente exclusiva: IABD_M05_T04.pdf

---

## 1. Herramientas de monitorización

La **monitorización** consiste en recopilar, analizar y visualizar datos del estado y comportamiento del sistema en todo momento. Permite detectar errores con antelación, mejorar el rendimiento y evitar cuellos de botella.

**Cuello de botella:** punto de restricción que limita el rendimiento general del sistema — el "embudo" donde no pueden pasar todos los datos.

### 1.1 Monitorización del sistema de archivos HDFS (NameNode)

El **NameNode** gestiona los **metadatos de HDFS** (bloques disponibles, directorios, archivos).

**Interfaz web NameNode** muestra:
- Espacio de almacenamiento total y capacidad disponible
- Número de DataNodes activos en el clúster
- Bloques de datos almacenados y su distribución
- Estado de las replicaciones (previene pérdida de tolerancia a fallos)

**Comandos de línea de comandos:**
- `hdfs dfsadmin -report`: estado de DataNodes, capacidad, bloques
- `hdfs dfsadmin -fetchDatanodeInfo`: información detallada de nodos de datos

**Herramienta externa:** Apache Ambari — integra monitoreo completo del clúster Hadoop.

### 1.2 Monitorización JobTracker

El **JobTracker** coordina la ejecución de trabajos MapReduce: asigna tareas y gestiona su estado. Es el "supervisor" del trabajo en el clúster.

**Interfaz web JobTracker** muestra:
- Estado actual de tareas en ejecución
- Recursos utilizados (CPU, memoria)
- Tiempo de ejecución de cada tarea
- Flujo de trabajo con dependencias entre tareas

**Comandos:**
- `hadoop job -list`: lista todos los jobs en ejecución
- `hadoop job -status <jobID>`: progreso y estado de un job específico

**Herramienta externa:** Apache Ambari también monitoriza el JobTracker.

### 1.3 Monitorización del clúster con Ganglia

**Ganglia** proporciona información en tiempo real sobre el estado de cada nodo del clúster.

Funcionalidades:
- **Monitoreo de recursos**: CPU, memoria, ancho de banda por nodo
- **Detección de anomalías**: análisis de los datos recopilados para detectar nodos sobrecargados
- **Visualización gráfica**: interfaz web con métricas por nodo

### 1.4 Otras herramientas de monitorización

| Herramienta | Función | Características |
|-------------|---------|----------------|
| **Prometheus** | Recolección de métricas en tiempo real | Genera reportes, consultas, alertas; ideal para Docker y entornos dinámicos |
| **Grafana** | Visualización de datos | Dashboards interactivos; se integra con Prometheus y otras fuentes de datos |
| **Nagios** | Monitorización de infraestructura | Alertas y notificaciones sobre servidores, aplicaciones y redes |
| **Zabbix** | Monitorización de servidores y redes | Similar a Nagios; informes de rendimiento personalizados |

---

## 2. Análisis de históricos

El análisis de datos históricos permite entender el comportamiento del sistema a lo largo del tiempo y detectar:
- **Cuellos de botella** recurrentes
- **Tendencias** emergentes (problemas que se pueden detener antes de que escalen)
- **Efectividad de optimizaciones**: comparar antes y después de un cambio de configuración

### 2.1 Fases del análisis histórico

1. **Recogida de datos**: métricas de CPU, memoria, almacenamiento, red; desde servidores, aplicaciones, BBDD
2. **Procesamiento de datos**: agregación de fuentes, normalización, cálculo de estadísticas (media, mediana, desviación estándar)
3. **Visualización**: dashboards (visión general) y reports periódicos (resumen del estado)

### 2.2 Optimización de la configuración

**HDFS:**
- Tamaño de bloques → optimiza eficiencia de lectura/escritura
- Número de replicaciones → equilibrio entre tolerancia a fallos y espacio
- Configuración de DataNodes → memoria y capacidad de almacenamiento

**JobTracker:**
- Número de slots de ejecución → más tareas en paralelo
- Recursos por tarea → asignación de CPU y memoria por job

**Tareas MapReduce:**
- Nivel de paralelismo → ajustar número de mappers/reducers
- Optimización del código → menos recursos, mejor tiempo de ejecución

---

## 3. Generación de alertas

Las alertas avisan de forma inmediata cuando algo falla, evitando sobrecarga de información y asegurando atención a problemas críticos.

### Tipos de alertas
- **Por umbrales**: saltar cuando una métrica supera un límite (ej: CPU > 90%)
- **Por eventos**: caída de un servicio o nodo
- **Por anomalías**: desviaciones detectadas en el análisis de datos

### Canales de notificación
- **Notificaciones**: SMS, mensajería (Slack, email)
- **Escalación**: alertas críticas no resueltas escalan a niveles superiores

---

## 4. Prevención de errores — checklist periódico

- **Análisis de logs**: log del clúster y de las tareas para detectar problemas
- **Herramientas de depuración**: Job History Server — visualiza el progreso de tareas y analiza fallos
- **Comprobación de configuración**: revisar que los ajustes del clúster sean correctos
- **Estado de los nodos**: verificar periódicamente que ningún nodo esté sobrecargado

---

## 5. Conceptos clave (glosario)

| Término | Definición |
|---------|-----------|
| **Monitorización** | Recopilación, análisis y visualización continua del estado del sistema |
| **Cuello de botella** | Punto de restricción que limita el rendimiento general del sistema |
| **NameNode** | Componente de Hadoop que gestiona los metadatos de HDFS |
| **JobTracker** | Componente de Hadoop que coordina la ejecución de tareas MapReduce |
| **Ganglia** | Herramienta de monitorización distribuida: CPU, memoria, ancho de banda por nodo |
| **Prometheus** | Sistema de recolección de métricas en tiempo real con alertas |
| **Grafana** | Herramienta de visualización que crea dashboards sobre múltiples fuentes |
| **Nagios** | Sistema de monitorización de infraestructura con alertas y notificaciones |
| **Ambari** | Plataforma de gestión y monitorización de clústeres Hadoop |
| **Job History Server** | Herramienta para analizar el progreso y fallos de trabajos MapReduce pasados |
| **Alerta por umbral** | Notificación que se activa cuando una métrica supera un valor definido |
| **Escalación de alertas** | Proceso de escalar alertas no resueltas a un nivel superior de responsabilidad |

---

## 6. Test autoevaluativo (respuestas)

| Pregunta | Respuesta |
|----------|----------|
| 1. Herramienta que NO se usa para monitorizar Hadoop | **Apache Kafka** (es una plataforma de streaming, no de monitorización) |
| 2. Qué proporciona `hdfs dfsadmin -report` | **Estado de los DataNodes y su capacidad de almacenamiento** |
| 3. Qué es un cuello de botella | **Una restricción que limita el rendimiento general del sistema** |
| 4. Para qué sirve `hadoop job -status <jobID>` | **Ver el progreso de un job en particular** |
| 5. Qué se puede obtener del análisis de históricos | **Patrones de comportamiento y posibles cuellos de botella** |
