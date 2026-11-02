---
title: Análisis de MovieLens 20M con Pandas
toc-title: Table of contents
---

**Actividad:** RA1 --- Comparación de Pandas, Polars y PySpark\
**Dataset:** `movielens_superdataset.csv` (columnas: userId, movieId,
rating, rating_timestamp, title, genres)

## Tareas

1.  Cargar el dataset
2.  Filtrar películas de género **Action** con `rating ≥ 4`
3.  Calcular **media y desviación estándar** de ratings por usuario
4.  Ordenar películas por **rating promedio** descendente
5.  Convertir `rating_timestamp` a fecha legible
6.  Medir tiempos de ejecución de cada operación

## 0. Instalación y configuración

## 0.1 Preparar el superdataset desde archive.zip

Ejecuta esta celda **una sola vez** para generar
`movielens_superdataset.csv`.\
Las siguientes ejecuciones la saltarán si el archivo ya existe.

:::: {.cell execution_count="1"}
``` {.python .cell-code}
import os, zipfile, io
import pandas as pd

ZIP_PATH = "/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/archive.zip"
OUT_PATH = os.path.join(os.path.dirname(ZIP_PATH), "movielens_superdataset.csv")

if os.path.exists(OUT_PATH):
    print(f"Ya existe: {OUT_PATH}")
else:
    print("Extrayendo y combinando rating.csv + movie.csv...")
    with zipfile.ZipFile(ZIP_PATH) as z:
        with z.open("rating.csv") as f:
            ratings = pd.read_csv(f)
        with z.open("movie.csv") as f:
            movies = pd.read_csv(f)

    superdataset = (
        ratings
        .merge(movies, on="movieId", how="left")
        .rename(columns={"timestamp": "rating_timestamp"})
    )
    superdataset.to_csv(OUT_PATH, index=False)
    print(f"Superdataset creado: {len(superdataset):,} filas -> {OUT_PATH}")

DATA_PATH = OUT_PATH
print(f"DATA_PATH = {DATA_PATH}")
```

::: {.cell-output .cell-output-stdout}
    Ya existe: /home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv
    DATA_PATH = /home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv
:::
::::

:::: {.cell execution_count="2"}
``` {.python .cell-code}
# Si no tienes pandas instalado:
# !pip install pandas

import time
import pandas as pd

print(f"Pandas versión: {pd.__version__}")
```

::: {.cell-output .cell-output-stdout}
    Pandas versión: 3.0.1
:::
::::

## 1. Cargar el dataset

Ajusta `DATA_PATH` a la ruta donde tengas el archivo CSV.

::::: {.cell execution_count="3"}
``` {.python .cell-code}
# DATA_PATH ya está definido arriba por la celda de preparación
# Si saltaste esa celda, defínelo manualmente:
# DATA_PATH = "/ruta/a/movielens_superdataset.csv"

t0 = time.time()
df = pd.read_csv(DATA_PATH)
t_load = time.time() - t0

print(f"Filas: {len(df):,}  |  Columnas: {df.shape[1]}")
print(f"Tiempo de carga: {t_load:.3f} s")
df.head()
```

::: {.cell-output .cell-output-stdout}
    Filas: 20,000,263  |  Columnas: 6
    Tiempo de carga: 11.921 s
:::

::: {.cell-output .cell-output-display execution_count="3"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

      userId   movieId   rating   rating_timestamp      title                                                genres
  --- -------- --------- -------- --------------------- ---------------------------------------------------- --------------------------------------------
  0   1        2         3.5      2005-04-02 23:53:47   Jumanji (1995)                                       Adventure\|Children\|Fantasy
  1   1        29        3.5      2005-04-02 23:31:16   City of Lost Children, The (Cité des enfants p\...   Adventure\|Drama\|Fantasy\|Mystery\|Sci-Fi
  2   1        32        3.5      2005-04-02 23:33:39   Twelve Monkeys (a.k.a. 12 Monkeys) (1995)            Mystery\|Sci-Fi\|Thriller
  3   1        47        3.5      2005-04-02 23:32:07   Seven (a.k.a. Se7en) (1995)                          Mystery\|Thriller
  4   1        50        3.5      2005-04-02 23:29:40   Usual Suspects, The (1995)                           Crime\|Mystery\|Thriller

</div>
:::
:::::

::::: {.cell execution_count="4"}
``` {.python .cell-code}
# Inspección rápida
df.info()
df.describe()
```

::: {.cell-output .cell-output-stdout}
    <class 'pandas.DataFrame'>
    RangeIndex: 20000263 entries, 0 to 20000262
    Data columns (total 6 columns):
     #   Column            Dtype  
    ---  ------            -----  
     0   userId            int64  
     1   movieId           int64  
     2   rating            float64
     3   rating_timestamp  str    
     4   title             str    
     5   genres            str    
    dtypes: float64(1), int64(2), str(3)
    memory usage: 2.1 GB
:::

::: {.cell-output .cell-output-display execution_count="4"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

          userId         movieId        rating
  ------- -------------- -------------- --------------
  count   2.000026e+07   2.000026e+07   2.000026e+07
  mean    6.904587e+04   9.041567e+03   3.525529e+00
  std     4.003863e+04   1.978948e+04   1.051989e+00
  min     1.000000e+00   1.000000e+00   5.000000e-01
  25%     3.439500e+04   9.020000e+02   3.000000e+00
  50%     6.914100e+04   2.167000e+03   3.500000e+00
  75%     1.036370e+05   4.770000e+03   4.000000e+00
  max     1.384930e+05   1.312620e+05   5.000000e+00

</div>
:::
:::::

## 2. Filtrar Action con rating ≥ 4

::::: {.cell execution_count="5"}
``` {.python .cell-code}
t0 = time.time()

# genres contiene strings como "Action|Adventure|Sci-Fi"
# Filtramos filas que contengan "Action" y tengan rating >= 4
df_action = df[
    df["genres"].str.contains("Action", na=False) &
    (df["rating"] >= 4)
]

t_filter = time.time() - t0

print(f"Filas tras filtro: {len(df_action):,}")
print(f"Tiempo filtrado: {t_filter:.3f} s")
df_action.head()
```

::: {.cell-output .cell-output-stdout}
    Filas tras filtro: 2,583,646
    Tiempo filtrado: 1.024 s
:::

::: {.cell-output .cell-output-display execution_count="5"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

       userId   movieId   rating   rating_timestamp      title                                                genres
  ---- -------- --------- -------- --------------------- ---------------------------------------------------- --------------------------------
  6    1        151       4.0      2004-09-10 03:08:54   Rob Roy (1995)                                       Action\|Drama\|Romance\|War
  9    1        260       4.0      2005-04-02 23:33:46   Star Wars: Episode IV - A New Hope (1977)            Action\|Adventure\|Sci-Fi
  10   1        293       4.0      2005-04-02 23:31:43   Léon: The Professional (a.k.a. The Professiona\...   Action\|Crime\|Drama\|Thriller
  15   1        541       4.0      2005-04-02 23:30:03   Blade Runner (1982)                                  Action\|Sci-Fi\|Thriller
  22   1        1036      4.0      2005-04-02 23:44:40   Die Hard (1988)                                      Action\|Crime\|Thriller

</div>
:::
:::::

## 3. Media y desviación estándar de ratings por usuario

::::: {.cell execution_count="6"}
``` {.python .cell-code}
t0 = time.time()

stats_por_usuario = (
    df.groupby("userId")["rating"]
    .agg(rating_mean="mean", rating_std="std")
    .reset_index()
)

t_agg = time.time() - t0

print(f"Usuarios únicos: {len(stats_por_usuario):,}")
print(f"Tiempo agregación: {t_agg:.3f} s")
stats_por_usuario.head(10)
```

::: {.cell-output .cell-output-stdout}
    Usuarios únicos: 138,493
    Tiempo agregación: 0.287 s
:::

::: {.cell-output .cell-output-display execution_count="6"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

      userId   rating_mean   rating_std
  --- -------- ------------- ------------
  0   1        3.742857      0.382284
  1   2        4.000000      1.064581
  2   3        4.122995      0.910427
  3   4        3.571429      0.790151
  4   5        4.272727      0.969464
  5   6        3.750000      1.073394
  6   7        3.289855      0.858776
  7   8        3.800000      0.972074
  8   9        3.057143      1.136115
  9   10       3.894737      0.605804

</div>
:::
:::::

## 4. Ordenar películas por rating promedio

::::: {.cell execution_count="7"}
``` {.python .cell-code}
t0 = time.time()

# Rating promedio por película (título)
rating_por_pelicula = (
    df.groupby("title")["rating"]
    .agg(num_ratings="count", avg_rating="mean")
    .reset_index()
    .sort_values("avg_rating", ascending=False)
)

t_sort = time.time() - t0

print(f"Tiempo ordenación: {t_sort:.3f} s")
# Mostrar solo películas con al menos 50 ratings para que el promedio sea significativo
rating_por_pelicula[rating_por_pelicula["num_ratings"] >= 50].head(10)
```

::: {.cell-output .cell-output-stdout}
    Tiempo ordenación: 0.552 s
:::

::: {.cell-output .cell-output-display execution_count="7"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

          title                                           num_ratings   avg_rating
  ------- ----------------------------------------------- ------------- ------------
  20779   Shawshank Redemption, The (1994)                63366         4.446990
  9586    Godfather, The (1972)                           41355         4.364732
  24967   Usual Suspects, The (1995)                      47006         4.334372
  20317   Schindler\'s List (1993)                        50054         4.310175
  9587    Godfather: Part II, The (1974)                  27398         4.275641
  20600   Seven Samurai (Shichinin no samurai) (1954)     11611         4.274180
  19203   Rear Window (1954)                              17449         4.271334
  2072    Band of Brothers (2001)                         4305          4.263182
  4236    Casablanca (1942)                               24349         4.258327
  22420   Sunset Blvd. (a.k.a. Sunset Boulevard) (1950)   6525          4.256935

</div>
:::
:::::

## 5. Convertir rating_timestamp a fecha

::::: {.cell execution_count="8"}
``` {.python .cell-code}
t0 = time.time()

# El timestamp ya viene como string 'YYYY-MM-DD HH:MM:SS'
df["fecha_rating"] = pd.to_datetime(df["rating_timestamp"], format="%Y-%m-%d %H:%M:%S")

t_ts = time.time() - t0

print(f"Tiempo conversión timestamp: {t_ts:.3f} s")
df[["userId", "title", "rating", "rating_timestamp", "fecha_rating"]].head()
```

::: {.cell-output .cell-output-stdout}
    Tiempo conversión timestamp: 15.706 s
:::

::: {.cell-output .cell-output-display execution_count="8"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

      userId   title                                                rating   rating_timestamp      fecha_rating
  --- -------- ---------------------------------------------------- -------- --------------------- ---------------------
  0   1        Jumanji (1995)                                       3.5      2005-04-02 23:53:47   2005-04-02 23:53:47
  1   1        City of Lost Children, The (Cité des enfants p\...   3.5      2005-04-02 23:31:16   2005-04-02 23:31:16
  2   1        Twelve Monkeys (a.k.a. 12 Monkeys) (1995)            3.5      2005-04-02 23:33:39   2005-04-02 23:33:39
  3   1        Seven (a.k.a. Se7en) (1995)                          3.5      2005-04-02 23:32:07   2005-04-02 23:32:07
  4   1        Usual Suspects, The (1995)                           3.5      2005-04-02 23:29:40   2005-04-02 23:29:40

</div>
:::
:::::

## 6. Resumen de tiempos

:::: {.cell execution_count="9"}
``` {.python .cell-code}
tiempos = pd.DataFrame({
    "Operación": ["Carga CSV", "Filtro Action ≥4", "Agregación por usuario", "Ordenación por rating", "Conversión timestamp"],
    "Tiempo (s)": [t_load, t_filter, t_agg, t_sort, t_ts]
})

print(tiempos.to_string(index=False))
print(f"\nTotal: {tiempos['Tiempo (s)'].sum():.3f} s")
```

::: {.cell-output .cell-output-stdout}
                 Operación  Tiempo (s)
                 Carga CSV   11.921296
          Filtro Action ≥4    1.023706
    Agregación por usuario    0.286896
     Ordenación por rating    0.551849
      Conversión timestamp   15.705937

    Total: 29.490 s
:::
::::

## 7. Preguntas de reflexión

**P1. ¿Qué diferencias de rendimiento observas entre Pandas, Polars y
PySpark?**\
\> Pandas carga todo en memoria y ejecuta operación a operación. Para
datasets que caben en RAM es cómodo, pero con 20M de filas puede
volverse lento (especialmente en la carga y las agregaciones). Polars es
más rápido gracias a su motor en Rust con paralelismo automático.
PySpark añade overhead de inicio, pero escala horizontalmente a datos
que no caben en memoria.

**P2. ¿Qué mejora aporta el LazyFrame de Polars?**\
\> En Pandas no existe este concepto. Cada operación se ejecuta
inmediatamente. Un LazyFrame en Polars o un DAG en Spark permite que el
motor optimice el orden y evite cálculos innecesarios antes de ejecutar.

**P3. ¿Cómo escalaría con datasets más grandes?**\
\> Pandas tiene el límite de la RAM disponible. Con datasets que superen
la memoria, Pandas falla. Polars mejora con sus LazyFrames y uso
eficiente de memoria, pero sigue siendo un solo nodo. PySpark distribuye
el trabajo entre múltiples máquinas.

**P4. ¿Qué uso tiene cada herramienta en la industria?**\
\> Pandas: análisis exploratorio, prototipado, ciencia de datos en
local. Polars: sustituto moderno de Pandas en pipelines de un solo nodo.
PySpark: ETL y análisis a escala de producción (GB/TB de datos).
