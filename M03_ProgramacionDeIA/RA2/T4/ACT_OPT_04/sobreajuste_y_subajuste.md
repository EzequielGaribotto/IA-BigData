# Sobreajuste y subajuste

En el contexto del entrenamiento de modelos de IA, ambos son los dos problemas nodales que dictaminan que un modelo de inteligencia artificial no generaliza de forma fidedigna. 

### ¿Qué es cada concepto?

**Sobreajuste (Overfitting):**
Sucede cuando un modelo de IA se ajusta *demasiado* a los datos de entrenamiento. En este estado patológico, el modelo en lugar de aprender los patrones subyacentes útiles, **"memoriza"** los datos incluyendo fluctuaciones aleatorias, el ruido biológico y los atípicos del conjunto inicial. 
* Consecuencia: Rendimiento espectacular en entrenamiento, pero predicciones inútiles, inexactas y pésimas frente a nuevos datos de la vida real.

**Subajuste (Underfitting):**
Cuando un modelo es *demasiado simple* o rígido y no logra captar la complejidad esencial de los datos. 
* Consecuencia: El modelo resulta superficial, predice con lentitud y tiene unos índices de fallo altísimos **tanto con los datos de entrenamiento**, como en validación.

---

### ¿Cómo identificar estos problemas?
Visual y numéricamente estos problemas se identifican comprobando y confrontando las denominadas **Curvas de Aprendizaje**:

*   **Identificando Overfitting:** Si tabulamos el error a lo largo del tiempo, notaremos que el "error de entrenamiento" no para de encoger (tiende a casi cero), persiguiendo el ruido, mientras abruptamente el "error de validación" se estanca e incluso *empieza a aumentar/divergir*. 
*   **Identificando Underfitting:** Al tabular, observamos que las curvas de "error de entrenamiento" y "error de validación" se estancan y aplanan muy pronto de forma paralela en un número / porcentaje de error muy elevado y malo; o tardan eternamente bajo fluctuaciones irregulares.

---

### Técnicas para prevenir / mitigar

**Para Mitigar el Sobreajuste (Overfitting):**
1.  **Aumentar y enriquecer los datos:** Incluir más cantidad o aumentar el existente artificialmente (Data Augmentation en visión por computador, tal y como se estudió).
2.  **Regularización (L1/Lasso, L2/Ridge):** Penalizar algoritmos para que no otorguen pesos matemáticos demasiado grandes y descompensados a funciones.
3.  **Truncamientos Tempranos (Early Stopping):** Detener el entrenamiento del sistema apenas se detecta que el modelo deja de mejorar en los subconjuntos de testeo para evitar que comience a memorizar.
4.  **Dropout:** Apagar aleatoriamente neuronas durante el proceso de aprendizaje profundo forzando a aprender redes distribuidas que sean duraderas.
5.  **Simplificar el modelo:** En ocasiones el modelo resulta excesivamente complejo u orgánico, deberíamos disminuir la altura en árboles de decisión o reducir densidad y capas ocultas en redes neuronales.
6.  **Validación Cruzada (K-Fold):** Obliga a cambiar el dataset temporal de prueba convalidando todas las fases.

**Para Mitigar el Subajuste (Underfitting):**
1.  **Incrementar la Complejidad del Modelo:** Cambiar regresiones lineales por polinómicas, utilizar ensamblados en Cascada (Boosting) o dotar a la red neuronal de mayores capas y nodos matemáticos para ganar abstracción.
2.  **Mejorar Características (Feature Engineering):** El modelo no extrae la verdad porque esta no le ha sido presentada; debemos alimentar el sistema combinando atributos nuevos u omitiendo datos sesgados que no se correlacionen.
3.  **Extender el proceso de adaptación:** Ampliar métricas relativas el tiempo como aumentar el número de `Epochs` si el modelo se ahoga prematuramente o modificar `Learning Rates` estancados.
