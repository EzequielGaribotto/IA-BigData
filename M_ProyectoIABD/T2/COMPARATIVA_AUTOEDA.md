# Comparativa de herramientas de EDA automático

Comparación de seis librerías de *auto-EDA* aplicadas al dataset *E-Commerce Data* (541.909 filas, 8 columnas), y contraste con el EDA manual de [`eda_y_preparacion_ventas_diarias_ecommerce.ipynb`](eda_y_preparacion_ventas_diarias_ecommerce.ipynb), donde también se aplica la combinación recomendada en la sección 5. Los informes de esa combinación están en [`eda_reports/combinado/`](eda_reports/combinado/).

## 1. Herramientas evaluadas

| Herramienta | Versión | Salida | Tiempo (dataset completo) |
|---|---|---|---|
| **skimpy** | 0.0.21 | Tabla de texto en el notebook | 2,6 s |
| **ydata-profiling** | 4.18.4 | Informe HTML + API Python | 17,1 s |
| **Sweetviz** | 2.3.3 | Informe HTML (análisis y comparación) | 2,1 s (+2,2 s comparación) |
| **AutoViz** | 0.1.905 | Gráficos PNG/SVG + tabla de calidad | 70,1 s (muestra de 150.000 filas) |
| **D-Tale** | 3.22.0 | Aplicación web interactiva | 1,9 s (arranque) |
| **prism-eda** | 1.0.1 | Informes HTML por receta + API Python | 5,7 s perfil · 2,7 s anomalías · <1 s serie temporal y regresión |

## 2. Qué encuentra cada herramienta

Tomando como referencia los hallazgos del EDA manual:

| Hallazgo (EDA manual) | skimpy | ydata-profiling | Sweetviz | AutoViz | D-Tale | prism-eda |
|---|---|---|---|---|---|---|
| `CustomerID` nulo (24,9%) | ✅ | ✅ alerta | ✅ | ✅ (pero sugiere imputar con la media) | ✅ | ✅ issue |
| `Description` nula (0,27%) | ✅ | ⚠️ en estadísticas, sin alerta | ✅ | ✅ | ✅ | ✅ y además 58 nulos "disfrazados" (`?`…) |
| Filas duplicadas (5.268) | ❌ | ✅ alerta (cuenta 4.879: filas distintas repetidas) | ✅ 5.268 | ⚠️ 460 (solo en la muestra) | ✅ (acción manual) | ✅ issue |
| `Quantity` negativa (10.624 filas) | ⚠️ solo p0 negativo | ⚠️ `n_negative` en estadísticas, sin alerta | ⚠️ solo el mínimo | ⚠️ solo el mínimo | ⚠️ en *Describe* | ⚠️ como "colas" en anomalías |
| `UnitPrice` = 0 (2.515 filas) | ❌ | ⚠️ en estadísticas, sin alerta | ✅ "ZEROES" | ❌ | ⚠️ en *Describe* | ❌ |
| Pedido extremo de ±80.995 uds. | ✅ p0/p100 | ✅ mín./máx. | ✅ mín./máx. | ❌ fuera de la muestra (máx. 5.568) | ✅ | ✅ en distribuciones (anomalías usa muestra de 100.000) |
| Asimetría de `UnitPrice` | ⚠️ histograma | ✅ alerta | ✅ histograma | ✅ gráfico + nº de outliers | ✅ | ✅ colas (7,3%) |
| Asimetría de `Quantity` | ⚠️ histograma | ❌ (los outliers ± se compensan: γ₁ = −0,26) | ⚠️ histograma | ✅ nº de outliers | ✅ | ✅ colas (13,4%) |
| `Country` muy desequilibrado (91% UK) | ❌ | ✅ alerta | ✅ | ✅ "34 categorías raras" | ✅ | ✅ |
| Facturas `C…` = cancelaciones | ⚠️ se ve `C536379` como "longest" | ❌ | ❌ | ❌ | ❌ | ⚠️ "1,7% de `InvoiceNo` no es numérico", sin interpretarlo |
| Códigos que no son productos (`POST`, `M`, `AMAZONFEE`…) | ⚠️ se ve `BANK CHARGES` como "longest" | ❌ | ❌ | ❌ | ❌ | ⚠️ las filas `AMAZONFEE` son las primeras anomalías |
| Pedidos gigantes cancelados minutos después | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Nunca hay ventas en sábado / festivos | ❌ | ❌ | ❌ | ❌ | ⚠️ visible si se hace el gráfico | ✅ "69 periodos sin registro" (sin saber que son cierres) |
| Cambio de régimen en noviembre (campaña de Navidad) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ cambio de nivel +42% el 03/11/2011 |
| Estacionalidad semanal | ❌ | ❌ | ❌ | ❌ | ⚠️ manual | ✅ |
| Cambio de distribución train vs. test | ❌ | ⚠️ posible con `compare()` | ✅ `compare_intra` | ❌ | ❌ | ⚠️ `compare_datasets` (no probado) |
| Variable objetivo (ventas diarias) | ❌ | ⚠️ `tsmode` si se agrega a mano | ❌ | ❌ | ❌ | ⚠️ recetas `time_series` y `regression` si se agrega a mano |
| Fuga de datos (`n_invoices` del mismo día) | — | — | — | — | — | ❌ no la detecta |

✅ lo detecta y lo destaca · ⚠️ el dato está, pero hay que buscarlo o interpretarlo · ❌ no lo detecta

## 3. Valoración de cada herramienta

### skimpy
- **A favor:** instantáneo, sale directamente en el notebook y cabe en una captura para la memoria. Incluye percentiles e histogramas en miniatura.
- **En contra:** solo es un resumen. No hay alertas, ni duplicados, ni correlaciones. Además fuerza **numpy 2**, incompatible con TensorFlow 2.16.
- **Uso recomendado:** primer vistazo de 5 segundos tras cargar un dataset.

### ydata-profiling
- **A favor:** el informe más completo (alertas, correlaciones, nulos, duplicados, interacciones). Es la única herramienta con **API programática**: `get_description()` devuelve alertas y estadísticas como objetos Python, lo que permite usarlas en el código o en tests de calidad de datos. Tiene un modo de **series temporales** (`tsmode`) con autocorrelación y estacionalidad.
- **En contra:** las alertas tienen umbrales fijos, así que la mayoría de problemas reales de este dataset (negativos, ceros, nulos en `Description`) quedan por debajo y no se señalan. Necesita **pandas 2.x** y `setuptools<81` (importa `pkg_resources`). Es la más lenta de las que procesan el dataset completo (17 s).
- **Uso recomendado:** informe de referencia del dataset y control de calidad automatizable.

### Sweetviz
- **A favor:** muy rápido y visual. Su función diferencial es **comparar dos subconjuntos** (`compare` / `compare_intra`), muy útil aquí para ver cómo cambian las distribuciones entre el periodo de entrenamiento y el de test (campaña de Navidad). Cuenta bien los duplicados y los ceros.
- **En contra:** no genera alertas. Redondea mucho las estadísticas (los cuartiles de `Quantity` aparecen como "0k"). No muestra cuántos valores son negativos.
- **Uso recomendado:** comparar train/validación/test o antes/después de la limpieza.

### AutoViz
- **A favor:** genera muchos gráficos sin configurar nada y una tabla de **calidad de datos** con una sugerencia por columna.
- **En contra:**
  - Por defecto analiza una **muestra aleatoria** de 150.000 filas, así que se le escapan los outliers más importantes.
  - Algunas sugerencias son incorrectas: imputar `CustomerID` (un identificador) con la media o la mediana.
  - Clasifica mal las variables: trata `Quantity` como categórica y genera gráficos sin sentido, como "Average UnitPrice by Quantity".
  - Es la más lenta (70 s).
  - Al importarse descarga **~440 MB de datos de NLTK** en `~/nltk_data`.
  - Fuerza un downgrade de xgboost a 1.6.2.
- **Uso recomendado:** solo como inspiración rápida de gráficos. No conviene seguir sus sugerencias sin revisarlas.

### D-Tale
- **A favor:** la más flexible. Es una interfaz interactiva con filtros, ordenación, análisis de nulos y duplicados, correlaciones y gráficos, y exporta cada acción como **código pandas**. Permite investigar a fondo (por ejemplo, filtrar las facturas que empiezan por `C`).
- **En contra:** no es automática: no da conclusiones, hay que saber qué buscar. Necesita un servidor en marcha y no deja nada en un informe estático, así que no sirve para documentar la memoria.
- **Uso recomendado:** exploración interactiva para confirmar hipótesis, como alternativa a escribir muchas celdas de pandas.

### prism-eda
- **A favor:**
  - Es la única herramienta **orientada a la tarea**. La receta `time_series` detecta los 69 días sin actividad, el cambio de nivel del +42% al empezar la campaña de Navidad y la estacionalidad semanal; también comprueba la estacionariedad con ADF y KPSS.
  - La receta `regression` propone acciones medidas: la transformación Yeo-Johnson deja la asimetría del target en ~0, avisa de que la tendencia `t` tiene una relación no lineal y señala filas influyentes.
  - Separa *issues* de *alertas* y da severidad, confianza y recomendación para cada hallazgo.
  - Encuentra **nulos disfrazados** (58 marcadores en `Description`).
  - Es rápida: menos de 6 s cada receta.
- **En contra:**
  - No entiende el negocio: ve los sábados como "periodos nunca registrados" y pregunta si son fallos de recogida.
  - No detecta fugas de datos temporales (`n_invoices` pasó sin aviso).
  - Algunas recomendaciones hay que descartarlas: convertir `InvoiceNo` y `CustomerID` a número.
  - Con los datos originales llega a una conclusión contradictoria (*"the level is falling"* junto a un salto del +42%). Con los datos limpios dice *"rising"*, lo que demuestra que conviene ejecutarla **después** de la limpieza.
  - La detección de anomalías usa una muestra de 100.000 filas.
  - Es muy reciente (agosto de 2026), de un único autor, y tiene algún fallo menor de texto ("0.3%, not 0.3%").
- **Uso recomendado:** después de la limpieza y de construir la serie diaria, para validar si está lista para forecasting y regresión.

## 4. Comparación global

| Criterio | skimpy | ydata-profiling | Sweetviz | AutoViz | D-Tale | prism-eda |
|---|---|---|---|---|---|---|
| Profundidad del análisis | Baja | **Alta** | Media | Media | Alta (manual) | **Alta** |
| Alertas / avisos automáticos | No | **Sí** | No | Sí (poco fiables) | No | **Sí, con severidad y recomendación** |
| Orientado al tipo de problema | No | No | No | No | No | **Sí** (series, regresión, clasificación, clustering) |
| Comparar subconjuntos | No | Sí | **Sí (mejor)** | No | No | Sí (`compare_datasets`) |
| Series temporales | No | Sí (`tsmode`) | No | No | Sí (manual) | **Sí (la más completa)** |
| Uso desde código | No | **Sí** | No | Parcial | Parcial | **Sí** |
| Sirve para la memoria | Captura | **HTML / capturas** | HTML / capturas | PNG | No | HTML / tablas de hallazgos |
| Velocidad | **Muy alta** | Media | **Muy alta** | Baja | Alta | **Muy alta** |
| Fricción de instalación | Media (numpy 2) | Media (pandas 2) | **Baja** | Alta (xgboost, NLTK) | Baja | **Baja** (sin dependencias nuevas) |
| Madurez | Media | **Alta** | Alta | Media | Alta | Baja (v1.0, 2026) |

## 5. Conclusiones

1. **Ninguna herramienta sustituye al EDA manual.** Todas detectan problemas *genéricos* (nulos, duplicados, asimetría, desequilibrio), pero ninguna detecta los problemas *de negocio*, que son los que más afectan a la predicción de ventas: cancelaciones, códigos no comerciales, pedidos anulados y días sin actividad.
2. **Mostrar un dato no es detectarlo.** Las 10.624 cantidades negativas aparecen en todos los informes, pero ninguno las señala como problema ni sugiere que sean devoluciones. Sigue siendo necesario interpretar los resultados.
3. **Las sugerencias automáticas hay que revisarlas.** El caso de AutoViz (imputar un identificador con la media, analizar solo una muestra) demuestra que seguir los consejos al pie de la letra puede empeorar los datos.
4. **Las herramientas orientadas a la tarea van un paso más allá.** prism-eda es la única que encuentra los días sin actividad, el cambio de régimen de noviembre y la estacionalidad semanal. Es lo más relevante para predecir el periodo de test. Aun así, sigue sin entender el negocio ni detectar fugas temporales.
5. **Combinación recomendada para este proyecto:**
   - **ydata-profiling** como informe de referencia del dataset original.
   - **EDA manual** (`eda_y_preparacion_ventas_diarias_ecommerce.ipynb`) para los hallazgos de negocio y las decisiones de limpieza.
   - **Sweetviz `compare`** para documentar el efecto de la limpieza y el cambio de distribución entre train y test.
   - **prism-eda `time_series` y `regression`** sobre la serie diaria **ya limpia**, para validar que está lista para modelar. Sustituye al `tsmode` de ydata-profiling, que aporta mucho menos.
   - **D-Tale** opcionalmente, para explorar de forma interactiva antes de escribir el código definitivo.

## 6. Notas de entorno

Las herramientas se instalaron en un entorno separado, **`venv_autoeda`** (Python 3.12, kernel `venv_autoeda (3.12)`). Instalarlas en `venv_iabd` habría provocado estos cambios:

- ydata-profiling: pandas 3.0.1 → 2.3.3, además de scipy y matplotlib.
- skimpy y klib: numpy 1.26 → 2.x, lo que rompe TensorFlow 2.16.
- AutoViz: xgboost 3.2 → 1.6.2.
