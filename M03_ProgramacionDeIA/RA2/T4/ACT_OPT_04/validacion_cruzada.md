# Validación cruzada

La **validación cruzada** (o *Cross-Validation*) es una técnica de evaluación descrita en el temario fundamental en IA para evaluar de forma fiable el rendimiento real de un modelo sobre datos no vistos, consistiendo en dividir el conjunto de entrenamiento de forma estratégica.

### Técnicas de Validación Cruzada:

**1. Holdout (División Simple)**
* **Descripción:** Se divide el dataset original en dos (o tres) subconjuntos estáticos: Entrenamiento, Validación y Prueba (ej. 70%-15%-15% u 80%-20%).
* **Cuándo es adecuado:** Para conjuntos de datos increíblemente grandes.
* **Ventajas:** Es el método más rápido, ya que el modelo se entrena una única vez y el coste computacional es bajo.
* **Inconvenientes:** La evaluación dependerá fuertemente de qué exactos datos caigan en el conjunto de validación o test. Existe un alto sesgo por casualidad en la partición.

**2. K-Fold Cross Validation**
* **Descripción:** El conjunto de datos original se baraja y se fragmenta (divide) en *K* subconjuntos del mismo tamaño (los "folds" o pliegues). El modelo se entrena iterativamente *K* veces. En cada iteración, un *fold* diferente se usa de Prueba y los *K-1* restantes se usan como conjunto de Entrenamiento.
* **Cuándo es adecuado:** En la inmensa mayoría de problemas convencionales de Machine Learning estructurado (ej. K=5 o K=10).
* **Ventajas:** Extremadamente fiable. Cada instancia del dataset es usada en prueba exactamente una vez. Minimiza el sesgo variacional que sufren modelos más simples.
* **Inconvenientes:** Computacionalmente demandante; puesto que requiere multiplicar por *K* los tiempos de entrenamiento.

**3. Leave-One-Out Cross Validation (LOOCV)**
* **Descripción:** Es un caso extremo de K-Fold donde *K* es exactamente el número total de muestras aportadas en el dataset.
* **Cuándo es adecuado:** Exclusivamente para datasets increíblemente limitados o con escasas filas (ej. de uso clínico extremadamente específico).
* **Ventajas:** Da la estimación menos sesgada posible, aprovechando al límite todos y cada uno de los valiosos datos.
* **Inconvenientes:** Impensable en grandes volúmenes. Coste computacional astronómico en datasets masivos (si tenemos 100,000 datos entrena 100,000 modelos).

---

### ¿Qué técnica sería más apropiada según la situación?

* **Si tu dataset es PEQUEÑO:**
  La técnica óptima será **K-Fold Cross-Validation** (con un *K* típicamente alto, e incluso escalando a **LOOCV** si el dataset es minúsculo). En un dataset pequeño necesitamos aprovechar cada minúsculo retazo de información para entrenar, pero también estar seguros de que no sobreentrena. K-fold nos garantiza que usaremos la mayoría de datos para aprender, rotando iterativamente para la validación sin quedarnos sin datos fijos de prueba.

* **Si tienes un TAMAÑO DE LOTE / DATASET MASIVO (Big Data):**
  La técnica más apropiada será **Holdout simple** (o, si la arquitectura lo tolera, un K-Fold con una *K* muy baja, digamos K=2 o 3). Con volúmenes gigantescos, una partición de "holdout" validacional es estadísticamente suficiente e invariable para representar a la muestra total. Aplicar *LOOCV* o un K muy grande aquí multiplicaría inútilmente las horas -o días- de cálculo, rebasando los márgenes computacionales que dictamina la industria.
