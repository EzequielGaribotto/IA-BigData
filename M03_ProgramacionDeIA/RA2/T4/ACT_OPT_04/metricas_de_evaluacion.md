# Métricas de evaluación

Para analizar correctamente cómo se evaluaría el éxito en un problema de clasificación real, plantemos un caso de **Detección de Imágenes de Enfermedades Clínicas (Cáncer Tumoral Binario)**. 

### ¿Qué ocurre en este contexto?
En este escenario (1=Enfermedad detectada / Tumor, 0=Sano), las consecuencias de un error del modelo tienen impactos radicalmente diferentes para la vida humana.

1. **Falso Negativo:** Decirle al paciente que está "sano" y que su tumor no es peligroso cuando **SÍ** está enfermo. Esto causará un infarto fatal por omitir tratamiento vital (Fallo gravísimo).
2. **Falso Positivo:** Decirle que "está gravemente enfermo" cuando en realidad era apenas un tejido sano. Se enviará a biopsias que resultarán inocuas (Fallo moderado/leve).

---

### ¿Cuáles serían las métricas más relevantes?

Por todo lo establecido:
1. **Recall o Exhaustividad (Sensibilidad / Tasa de Verdaderos Positivos):** 
Calculado sobre el número total de *reales* enfermos. La métrica reina en el área médica, detecta estadísticamente qué fracción íntegra de todos los pacientes que sí estaban enfermos ha sido "recordada" (detectada) de entre la masa total de casos reales. Si un modelo consigue un `Recall` del 99,5%, significa que rarísimamente el sistema omitirá derivar a un paciente en grave riesgo a cuidados médicos directos.

2. **F1-Score:** 
Es la media armónica entre ambos el Recall (que es vital) y la Precisión (que mide si no te pasaste derivando personas sanas). Evalúa qué tan "equilibrado" fue el modelo frente a métricas aisladas. El F1 asienta penalizaciones severas si alguno de los valores decae demasiado, por lo que su alta puntuación nos valida científicamente que el modelo tiene alto índice de eficacia.

---

### Y, ¿qué ocurriría si los datos están drásticamente desbalanceados?

Imaginemos que por cada paciente que posee tumores extraños en el Dataset evaluativo encontramos *10,000 personas sanas* en los datos hospitalarios. Las métricas debían ajustarse obligatoriamente de la siguiente manera dadas estas circunstancias especiales:

1. **La Exactitud ("Accuracy") se vuelve inútil y peligrosa:**
   Si la base predice que *"todos los humanos del planeta están siempre sanos"*, acertará en el 99.9% de los casos (de esas 10,000 personas sanas) y su `Accuracy` será enorme y perfecta en apariencia, pero habrá condenado a muerte al único enfermo por un fallo sistemático.

2. **Precisión Predictiva vs Recall (Curva PR - AUC_PR):** 
En datasets de desbalance salvaje, la métrica estándar como la Curva de Característica Operativa ("ROC-AUC") resultaría muy errónea porque cuenta todos los *Verdaderos Negativos*, es decir, suma aplausos al algoritmo por acertar con los miles de pacientes sanos obvios. En su defecto, se aplica la **Curva Area Under Precision-Recall (PR-AUC)** la cual obvia por completo la abultada masa total de personas libres de enfermedad para focalizar qué tan eficiente y sensible detecta al puñado de enfermos.

3. **Matriz de Confusión Explicada (Confusion Matrix):** 
Aunque no es un porcentaje numérico como tal, la matriz cruza una tabla en crudo de predicciones frente la realidad. Nos permite ver la cifra exacta a pie desnudo de los Falsos Positivos vs Falsos Negativos. En desbalances graves, ver reflejados 5 enfermos no detectados es mil veces más esclarecedor desde la matriz para una presentación de negocio que un % de métrica F1 que esconda lo que está fallando al no segregar las predicciones de los modelos IA.
