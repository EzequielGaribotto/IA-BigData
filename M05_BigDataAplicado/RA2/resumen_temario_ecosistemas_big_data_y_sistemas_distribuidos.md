# Resumen del temario: ecosistemas Big Data y gestión de sistemas distribuidos
## Fuente exclusiva: IABD_M05_T02.pdf

---

## 1. Computación distribuida vs computación paralela

### 1.1 Computación distribuida
- Múltiples **nodos** cooperan a través de una red para resolver tareas conjuntamente
- Los nodos **no necesitan compartir espacio físico** — pueden estar en ubicaciones distintas
- Características clave: **cooperación entre nodos**, **comunicación** (con protocolos optimizados para minimizar latencia), **transparencia** (interfaz unificada que oculta la complejidad)
- Ejemplos: Cassandra, MongoDB en modo distribuido

### 1.2 Computación paralela
- Múltiples tareas se ejecutan **dentro de un mismo sistema o nodo**, aprovechando varios procesadores o núcleos
- Objetivo: aumentar velocidad de procesamiento con recursos internos
- Tipos de descomposición: **de datos** (varios procesadores operan en bloques de los mismos datos) o **funcional** (cada procesador ejecuta una función distinta)
- Ejemplo: supercomputadores científicos con miles de procesadores en una sola máquina

| Aspecto | Distribuida | Paralela |
|---------|-------------|----------|
| Ubicación | Múltiples máquinas/nodos en red | Una misma máquina (varios núcleos) |
| Escalabilidad típica | Horizontal | Procesadores adicionales (vertical) |
| Comunicación | A través de red (mayor latencia) | Memoria compartida (menor latencia) |
| Ejemplo | Hadoop, Cassandra | Supercomputadores, GPU computing |

---

## 2. Escalabilidad y paralelismo

### En sistemas distribuidos
- **Horizontal** (añadir nodos): más habitual — mejora disponibilidad y redundancia
- **Vertical** (mejorar un nodo): más simple pero con límites físicos
- La **tolerancia a fallos** complementa la escalabilidad horizontal: la redundancia asegura continuidad si un nodo falla

### En sistemas paralelos
- **Escalabilidad de procesadores** (paralela): añadir núcleos/procesadores a la misma máquina
- **Horizontal en clústeres de alto rendimiento**: menos común, pero posible

---

## 3. Tolerancia a fallos

En sistemas distribuidos es **inevitable** que fallen nodos (hardware, red, software). El sistema debe continuar funcionando correctamente.

### 3.1 Mecanismos principales

| Mecanismo | Cómo funciona |
|-----------|--------------|
| **Replicación de datos** | Múltiples copias en diferentes nodos; si uno falla, las réplicas responden. Síncrona o asíncrona |
| **Checkpointing** | Guarda el estado del sistema en intervalos regulares; permite reiniciar desde el último checkpoint en vez de desde cero |
| **Sharding** | Divide la BBDD en fragmentos (*shards*) distribuidos en nodos; si uno falla, los demás siguen operando |
| **Quorum** | Número mínimo de réplicas que deben confirmar una operación para que se ejecute; garantiza consistencia parcial |
| **Detección de fallos** | Monitoreo continuo de nodos; **heartbeats** (señales periódicas de vida); redistribución automática al detectar un fallo |

### 3.2 Algoritmos de consenso

Aseguran que **todos los nodos acuerden un valor o decisión**, incluso cuando algunos fallen.

**Paxos:**
- 3 roles: *proposer* (propone un valor), *acceptor* (acepta o rechaza la propuesta), *learner* (aprende el valor acordado)
- Muy robusto y tolerante a fallos, pero complejo de implementar

**Raft:**
- Diseñado para ser más fácil de entender e implementar que Paxos
- Divide el consenso en: elección de líder, replicación de logs, seguridad
- Más comprensible por su diseño modular

---

## 4. Sharding y particionamiento

El **sharding** divide una BBDD grande en fragmentos (*shards*) que se distribuyen en distintos nodos:
- Cada nodo gestiona solo su shard → mejor rendimiento en consultas locales
- Reduce la carga en cada nodo individual
- Permite escalar horizontalmente la capacidad de almacenamiento y procesamiento

**Estrategias de particionamiento:**
- Por **rango** (valores numéricos o alfabéticos)
- Por **hash** (distribución uniforme, evita hot spots)
- Por **directorio** (tabla de mapeo explícita)

---

## 5. Herramientas del ecosistema Hadoop

### 5.1 MapReduce (repaso desde T01)
Procesamiento masivo en fases Map → Shuffle&Sort → Reduce → HDFS.

### 5.2 Apache Pig
- Lenguaje de alto nivel (**Pig Latin**) para procesar datos en Hadoop
- Se compila a trabajos MapReduce internamente
- Ideal para transformaciones de datos ETL sin escribir MapReduce manualmente

### 5.3 Apache Hive
- Motor de consultas tipo **SQL sobre datos en Hadoop** (HiveQL)
- Permite a analistas usar SQL estándar sobre datos no relacionales
- No adecuado para baja latencia (genera jobs MapReduce)

### 5.4 Apache Oozie
- Planificador de flujos de trabajo (**workflow scheduler**) para Hadoop
- Permite encadenar y automatizar jobs de MapReduce, Pig, Hive, Sqoop, etc.
- Define flujos en XML (DAG de tareas)

### 5.5 Apache Sqoop
- Herramienta para **transferir datos entre Hadoop/HDFS y bases de datos relacionales** (MySQL, PostgreSQL, Oracle)
- Importa/exporta tablas completas o incrementalmente
- Usa JDBC para conectarse a BBDD relacionales

---

## 6. Conceptos clave (glosario)

| Término | Definición |
|---------|-----------|
| **Computación distribuida** | Procesamiento repartido en múltiples nodos conectados en red |
| **Computación paralela** | Procesamiento simultáneo en varios procesadores/núcleos de una misma máquina |
| **Sharding** | División de una BBDD en fragmentos distribuidos en diferentes nodos |
| **Replicación** | Copias de los datos en múltiples nodos para tolerancia a fallos |
| **Checkpointing** | Guardado periódico del estado del sistema para recuperación ante fallos |
| **Quorum** | Número mínimo de réplicas que deben aprobar una operación |
| **Heartbeat** | Señal periódica que un nodo envía para indicar que sigue activo |
| **Paxos** | Algoritmo de consenso robusto pero complejo; 3 roles: proposer, acceptor, learner |
| **Raft** | Algoritmo de consenso más sencillo que Paxos; basado en líder electo |
| **Apache Pig** | Lenguaje Pig Latin para ETL sobre Hadoop (compila a MapReduce) |
| **Apache Hive** | SQL sobre Hadoop (HiveQL); para analistas que prefieren SQL |
| **Apache Oozie** | Planificador de flujos de trabajo en Hadoop |
| **Apache Sqoop** | Importación/exportación de datos entre HDFS y BBDD relacionales |

---

## 7. Test autoevaluativo (respuestas)

| Pregunta | Respuesta |
|----------|----------|
| 1. Sistema que divide datos en fragmentos distribuidos en nodos | **Sharding** |
| 2. Algoritmo de consenso robusto con 3 roles | **Paxos** |
| 3. Herramienta para ejecutar SQL sobre Hadoop | **Apache Hive** |
| 4. Mecanismo que guarda el estado para recuperación ante fallos | **Checkpointing** |
| 5. Tipo de escalabilidad que añade más nodos a la red | **Escalabilidad horizontal** |
