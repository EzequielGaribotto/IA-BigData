# Resumen del temario: validación de técnicas de Big Data y modelos de inteligencia de negocios (BI)
## Fuente exclusiva: IABD_M05_T05.pdf

---

## 1. Inteligencia de Negocios (BI)

**BI (Business Intelligence)** es el conjunto de procesos, herramientas y tecnologías que permiten a las organizaciones recopilar, procesar y analizar datos para extraer información de valor y apoyar la **toma de decisiones estratégicas**.

Los modelos BI presentan los resultados mediante informes, dashboards y análisis avanzados para dar una visión clara de la realidad de la empresa.

### 1.1 Importancia de BI

- **Visión en tiempo real**: datos actualizados permiten detectar problemas y oportunidades de forma inmediata
- **Eficiencia operativa**: análisis histórico revela procesos lentos, cuellos de botella o gastos innecesarios
- **Decisiones basadas en hechos**: convierte datos en información verificable que respalda cada decisión

**Beneficios directos:**
- Mejora la eficiencia operativa
- Optimiza la gestión de recursos
- Aumenta la rentabilidad
- Facilita la detección de fraudes
- Identifica nuevas oportunidades de mercado
- Personaliza la experiencia del cliente

---

## 2. Tipos de modelos BI

| Modelo | Pregunta que responde | Descripción | Ejemplo real |
|--------|----------------------|-------------|-------------|
| **Descriptivo** | ¿Qué pasó? | Analiza datos históricos para identificar patrones y tendencias | Informes de ventas, análisis de costos |
| **Predictivo** | ¿Qué pasará? | Predice el futuro con minería de datos y ML sobre datos históricos y actuales | Amazon: recomendaciones de productos |
| **Prescriptivo** | ¿Qué hacer? | Recomienda acciones concretas para maximizar el resultado | Proponer cambios en cadena de suministro para reducir costos |
| **Operacional** | ¿Qué pasa ahora? | Monitoriza operaciones diarias en tiempo real para decisiones inmediatas | Walmart: gestión de cadena de suministro en tiempo real |

> **Modelo diagnóstico** (mencionado en el PDF pero no en la lista principal): explica **por qué** algo sucedió, identificando patrones y anomalías en datos históricos.

---

## 3. Proceso KDD (Knowledge Discovery in Databases)

El **KDD** reúne todas las fases de un proyecto Big Data desde el dato hasta la información de valor. Proporciona un marco estructurado para extraer patrones y tendencias.

### 3.1 Etapas del proceso KDD

```
1. SELECCIÓN → 2. LIMPIEZA → 3. TRANSFORMACIÓN → 4. MINERÍA → 5. INTERPRETACIÓN
```

#### 3.1.1 Selección de datos
Identificar y seleccionar los datos relevantes para el problema planteado.
- **Fuentes internas**: datos de la propia empresa (BBDD de clientes, inventarios, transacciones, ERP, CRM)
- **Fuentes externas**: datos de competencia, tendencias de mercado, redes sociales (estructurados y no estructurados)
- Hay que garantizar suficiente volumen y que los datos reflejen la realidad de forma veraz

#### 3.1.2 Limpieza de datos
La fase que más tiempo consume pero más impacto tiene en la calidad del resultado:
- Eliminación de duplicados
- Tratamiento de valores nulos
- Tratamiento de valores faltantes
- Corrección de errores (formatos, rangos inválidos)
- Filtrado de datos irrelevantes

#### 3.1.3 Transformación de datos
Adaptar los datos al formato adecuado para el análisis:
- **Normalización**: valores entre 0 y 1
- **Variables categóricas a numéricas**: codificación (one-hot encoding, label encoding)
- **Creación de nuevas variables**: columnas derivadas que aportan información adicional
- **Agregación**: unir datos para obtener resúmenes (ventas diarias → mensuales)
- **Descomposición**: separar una columna en varias (dirección → ciudad, calle, código postal)

#### 3.1.4 Minería de datos
Aplicar algoritmos y técnicas para extraer patrones ocultos. Técnicas principales:
- **Clustering** (agrupamiento no supervisado)
- **Regresión** (predicción de valores continuos)
- **Árboles de decisión** (clasificación interpretable)
- **Random forest** (ensemble de árboles)
- **Redes neuronales** (Deep Learning)

#### 3.1.5 Interpretación y evaluación
Analizar si los patrones descubiertos son útiles y aplicables:
- **Evaluación de precisión**: comparar patrones con la realidad
- **Relevancia empresarial**: ¿el patrón responde a la pregunta inicial? Descartar los que no aportan valor
- **Implementación en estrategias**: integrar los patrones útiles en el plan de acción de la empresa

---

## 4. Implantación de modelos BI

### 4.1 Áreas clave de integración

| Área | Qué se analiza |
|------|---------------|
| **Datos financieros** | Ingresos, costos, presupuestos, riesgos, áreas de ahorro |
| **Datos de clientes** | Gustos, comportamientos, segmentación → personalización y fidelización |
| **Datos de marketing** | Efectividad de campañas publicitarias |
| **Datos de redes sociales** | Opiniones, tendencias, sentimiento de marca (no estructurados) |

### 4.2 Fuentes de datos

**Internas:**
- **ERP** (Enterprise Resource Planning): gestiona finanzas, inventarios, operaciones — BBDD relacionales
- **CRM** (Customer Relationship Management): interacciones con clientes, ventas, campañas

**Externas:**
- APIs de redes sociales (Twitter/X, Instagram, Facebook)
- Informes de mercado y análisis de competencia
- Proveedores de datos especializados

---

## 5. Validación de modelos BI

La validación garantiza que los modelos producen resultados **precisos y robustos** antes de usarlos en la toma de decisiones.

### 5.1 Pruebas A/B
Comparar dos versiones del modelo (A y B) con datos distintos para determinar cuál ofrece mejor resultado:
1. Definir hipótesis claras
2. Crear dos versiones del modelo
3. Ejecutar ambas con sus respectivos datos
4. Comparar resultados con métricas de evaluación
5. Implementar la versión ganadora

**Ventaja:** comparación directa; detecta mejoras sin implementar constantemente; reduce riesgo.

### 5.2 Análisis de sensibilidad
Estudia cómo los cambios en las **variables de entrada** afectan el resultado:
1. Identificar variables clave
2. Definir rangos de variación
3. Ejecutar simulaciones
4. Evaluar el impacto
5. Ajustar el modelo

**Ventaja:** identifica las variables más influyentes; optimiza el modelo encontrando valores óptimos.

### 5.3 Validación cruzada
Divide los datos en partes: unas para entrenar y otras para validar. Se usa principalmente para los **modelos de IA/ML** dentro del proyecto BI (no para dashboards o informes).

---

## 6. KPIs (Key Performance Indicators)
Una vez definidos los objetivos estratégicos, se deben definir **KPIs** — indicadores claros de desempeño que miden el progreso hacia esos objetivos.

---

## 7. Conceptos clave (glosario)

| Término | Definición |
|---------|-----------|
| **BI (Business Intelligence)** | Procesos y tecnologías para convertir datos en información para la toma de decisiones |
| **Modelo descriptivo** | Analiza qué pasó en el pasado |
| **Modelo predictivo** | Predice qué pasará usando ML sobre datos históricos |
| **Modelo prescriptivo** | Recomienda qué hacer para maximizar el resultado |
| **Modelo operacional** | Monitoriza operaciones diarias en tiempo real |
| **KDD** | Knowledge Discovery in Databases: marco de 5 etapas desde datos hasta conocimiento |
| **Minería de datos** | Aplicación de algoritmos ML/DL para descubrir patrones ocultos en los datos |
| **ERP** | Sistema que gestiona todos los recursos de la empresa (finanzas, RRHH, inventario) |
| **CRM** | Sistema de gestión de relaciones con clientes |
| **KPI** | Indicador clave de desempeño para medir el progreso hacia objetivos |
| **Prueba A/B** | Comparación de dos versiones de un modelo para determinar cuál es mejor |
| **Análisis de sensibilidad** | Estudio de cómo los cambios en variables de entrada afectan el resultado |
| **Validación cruzada** | Técnica de particionamiento de datos para evaluar modelos ML de forma robusta |
