---
title: Análisis de MovieLens 20M con Polars
toc-title: Table of contents
---

**Actividad:** RA1 --- Comparación de Pandas, Polars y PySpark\
**Dataset:** `movielens_superdataset.csv` (columnas: userId, movieId,
rating, rating_timestamp, title, genres)

Se implementan **dos modos**: Eager (ejecución inmediata) y
**LazyFrame** (optimización antes de ejecutar).

## Tareas

1.  Cargar el dataset
2.  Filtrar películas de género **Action** con `rating ≥ 4`
3.  Calcular **media y desviación estándar** de ratings por usuario
4.  Ordenar películas por **rating promedio** descendente
5.  Convertir `rating_timestamp` a fecha legible
6.  Medir tiempos de ejecución de cada operación (eager vs lazy)

## 0. Instalación y configuración

## 0.1 Preparar el superdataset desde archive.zip

Ejecuta esta celda **una sola vez** para generar
`movielens_superdataset.csv`.\
Las siguientes ejecuciones la saltarán si el archivo ya existe.

:::: {.cell execution_count="1"}
``` {.python .cell-code}
import os, zipfile
import polars as pl

ZIP_PATH = "/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/archive.zip"
OUT_PATH = os.path.join(os.path.dirname(ZIP_PATH), "movielens_superdataset.csv")

if os.path.exists(OUT_PATH):
    print(f"Ya existe: {OUT_PATH}")
else:
    print("Extrayendo y combinando rating.csv + movie.csv...")
    with zipfile.ZipFile(ZIP_PATH) as z:
        with z.open("rating.csv") as f:
            ratings = pl.read_csv(f)
        with z.open("movie.csv") as f:
            movies = pl.read_csv(f)

    superdataset = (
        ratings
        .join(movies, on="movieId", how="left")
        .rename({"timestamp": "rating_timestamp"})
    )
    superdataset.write_csv(OUT_PATH)
    print(f"Superdataset creado: {superdataset.shape[0]:,} filas -> {OUT_PATH}")

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
# Si no tienes polars instalado:
# !pip install polars

import time
import polars as pl

print(f"Polars versión: {pl.__version__}")
```

::: {.cell-output .cell-output-stdout}
    Polars versión: 1.41.2
:::
::::

## 1. Cargar el dataset --- Modo Eager

Ajusta `DATA_PATH` a la ruta donde tengas el archivo CSV.

::::: {.cell execution_count="3"}
``` {.python .cell-code}
# DATA_PATH ya está definido arriba por la celda de preparación

# --- EAGER ---
t0 = time.time()
df = pl.read_csv(DATA_PATH)
t_load_eager = time.time() - t0

print(f"[EAGER] Filas: {df.shape[0]:,}  |  Columnas: {df.shape[1]}")
print(f"[EAGER] Tiempo de carga: {t_load_eager:.3f} s")
print(df.schema)
df.head()
```

::: {.cell-output .cell-output-stdout}
    [EAGER] Filas: 20,000,263  |  Columnas: 6
    [EAGER] Tiempo de carga: 0.634 s
    Schema([('userId', Int64), ('movieId', Int64), ('rating', Float64), ('rating_timestamp', String), ('title', String), ('genres', String)])
:::

::: {.cell-output .cell-output-display execution_count="3"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (5, 6)</small>

  userId   movieId   rating   rating_timestamp          title                                 genres
  -------- --------- -------- ------------------------- ------------------------------------- ----------------------------------------
  i64      i64       f64      str                       str                                   str
  1        2         3.5      \"2005-04-02 23:53:47\"   \"Jumanji (1995)\"                    \"Adventure\|Children\|Fantasy\"
  1        29        3.5      \"2005-04-02 23:31:16\"   \"City of Lost Children, The (Ci...   \"Adventure\|Drama\|Fantasy\|Myster...
  1        32        3.5      \"2005-04-02 23:33:39\"   \"Twelve Monkeys (a.k.a. 12 Monk...   \"Mystery\|Sci-Fi\|Thriller\"
  1        47        3.5      \"2005-04-02 23:32:07\"   \"Seven (a.k.a. Se7en) (1995)\"       \"Mystery\|Thriller\"
  1        50        3.5      \"2005-04-02 23:29:40\"   \"Usual Suspects, The (1995)\"        \"Crime\|Mystery\|Thriller\"

</div>
:::
:::::

## 2. Filtrar Action con rating ≥ 4

### 2a. Eager

::::: {.cell execution_count="4"}
``` {.python .cell-code}
t0 = time.time()

df_action_eager = df.filter(
    pl.col("genres").str.contains("Action") &
    (pl.col("rating") >= 4)
)

t_filter_eager = time.time() - t0

print(f"[EAGER] Filas tras filtro: {len(df_action_eager):,}")
print(f"[EAGER] Tiempo filtrado: {t_filter_eager:.3f} s")
df_action_eager.head()
```

::: {.cell-output .cell-output-stdout}
    [EAGER] Filas tras filtro: 2,583,646
    [EAGER] Tiempo filtrado: 0.110 s
:::

::: {.cell-output .cell-output-display execution_count="4"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (5, 6)</small>

  userId   movieId   rating   rating_timestamp          title                                 genres
  -------- --------- -------- ------------------------- ------------------------------------- ------------------------------------
  i64      i64       f64      str                       str                                   str
  1        151       4.0      \"2004-09-10 03:08:54\"   \"Rob Roy (1995)\"                    \"Action\|Drama\|Romance\|War\"
  1        260       4.0      \"2005-04-02 23:33:46\"   \"Star Wars: Episode IV - A New ...   \"Action\|Adventure\|Sci-Fi\"
  1        293       4.0      \"2005-04-02 23:31:43\"   \"Léon: The Professional (a.k.a....   \"Action\|Crime\|Drama\|Thriller\"
  1        541       4.0      \"2005-04-02 23:30:03\"   \"Blade Runner (1982)\"               \"Action\|Sci-Fi\|Thriller\"
  1        1036      4.0      \"2005-04-02 23:44:40\"   \"Die Hard (1988)\"                   \"Action\|Crime\|Thriller\"

</div>
:::
:::::

### 2b. LazyFrame

::::: {.cell execution_count="5"}
``` {.python .cell-code}
# Con scan_csv el archivo no se carga todavía — se construye un plan
t0 = time.time()

df_action_lazy = (
    pl.scan_csv(DATA_PATH)
    .filter(
        pl.col("genres").str.contains("Action") &
        (pl.col("rating") >= 4)
    )
    .collect()  # <- aquí se ejecuta todo
)

t_filter_lazy = time.time() - t0

print(f"[LAZY] Filas tras filtro: {len(df_action_lazy):,}")
print(f"[LAZY] Tiempo filtrado (scan+filter+collect): {t_filter_lazy:.3f} s")
df_action_lazy.head()
```

::: {.cell-output .cell-output-stdout}
    [LAZY] Filas tras filtro: 2,583,646
    [LAZY] Tiempo filtrado (scan+filter+collect): 0.834 s
:::

::: {.cell-output .cell-output-display execution_count="5"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (5, 6)</small>

  userId   movieId   rating   rating_timestamp          title                                 genres
  -------- --------- -------- ------------------------- ------------------------------------- ------------------------------------
  i64      i64       f64      str                       str                                   str
  1        151       4.0      \"2004-09-10 03:08:54\"   \"Rob Roy (1995)\"                    \"Action\|Drama\|Romance\|War\"
  1        260       4.0      \"2005-04-02 23:33:46\"   \"Star Wars: Episode IV - A New ...   \"Action\|Adventure\|Sci-Fi\"
  1        293       4.0      \"2005-04-02 23:31:43\"   \"Léon: The Professional (a.k.a....   \"Action\|Crime\|Drama\|Thriller\"
  1        541       4.0      \"2005-04-02 23:30:03\"   \"Blade Runner (1982)\"               \"Action\|Sci-Fi\|Thriller\"
  1        1036      4.0      \"2005-04-02 23:44:40\"   \"Die Hard (1988)\"                   \"Action\|Crime\|Thriller\"

</div>
:::
:::::

:::: {.cell execution_count="6"}
``` {.python .cell-code}
# Ver el plan optimizado que Polars genera
plan = (
    pl.scan_csv(DATA_PATH)
    .filter(
        pl.col("genres").str.contains("Action") &
        (pl.col("rating") >= 4)
    )
)
print(plan.explain(optimized=True))
```

::: {.cell-output .cell-output-stdout}
    Csv SCAN [/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv]
    PROJECT */6 COLUMNS
    SELECTION: [([(col("rating")) >= (4.0)]) & (col("genres").str.contains(["Action"]))]
    ESTIMATED ROWS: 23192989
:::
::::

## 3. Media y desviación estándar de ratings por usuario

### 3a. Eager

::::: {.cell execution_count="7"}
``` {.python .cell-code}
t0 = time.time()

stats_eager = (
    df.group_by("userId")
    .agg([
        pl.col("rating").mean().alias("rating_mean"),
        pl.col("rating").std().alias("rating_std")
    ])
    .sort("userId")
)

t_agg_eager = time.time() - t0

print(f"[EAGER] Usuarios únicos: {len(stats_eager):,}")
print(f"[EAGER] Tiempo agregación: {t_agg_eager:.3f} s")
stats_eager.head(10)
```

::: {.cell-output .cell-output-stdout}
    [EAGER] Usuarios únicos: 138,493
    [EAGER] Tiempo agregación: 0.270 s
:::

::: {.cell-output .cell-output-display execution_count="7"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (10, 3)</small>

  userId   rating_mean   rating_std
  -------- ------------- ------------
  i64      f64           f64
  1        3.742857      0.382284
  2        4.0           1.064581
  3        4.122995      0.910427
  4        3.571429      0.790151
  5        4.272727      0.969464
  6        3.75          1.073394
  7        3.289855      0.858776
  8        3.8           0.972074
  9        3.057143      1.136115
  10       3.894737      0.605804

</div>
:::
:::::

### 3b. LazyFrame

::::: {.cell execution_count="8"}
``` {.python .cell-code}
t0 = time.time()

stats_lazy = (
    pl.scan_csv(DATA_PATH)
    .group_by("userId")
    .agg([
        pl.col("rating").mean().alias("rating_mean"),
        pl.col("rating").std().alias("rating_std")
    ])
    .sort("userId")
    .collect()
)

t_agg_lazy = time.time() - t0

print(f"[LAZY] Tiempo agregación: {t_agg_lazy:.3f} s")
stats_lazy.head(10)
```

::: {.cell-output .cell-output-stdout}
    [LAZY] Tiempo agregación: 0.540 s
:::

::: {.cell-output .cell-output-display execution_count="8"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (10, 3)</small>

  userId   rating_mean   rating_std
  -------- ------------- ------------
  i64      f64           f64
  1        3.742857      0.382284
  2        4.0           1.064581
  3        4.122995      0.910427
  4        3.571429      0.790151
  5        4.272727      0.969464
  6        3.75          1.073394
  7        3.289855      0.858776
  8        3.8           0.972074
  9        3.057143      1.136115
  10       3.894737      0.605804

</div>
:::
:::::

## 4. Ordenar películas por rating promedio

### 4a. Eager

::::: {.cell execution_count="9"}
``` {.python .cell-code}
t0 = time.time()

rating_pelicula_eager = (
    df.group_by("title")
    .agg([
        pl.col("rating").count().alias("num_ratings"),
        pl.col("rating").mean().alias("avg_rating")
    ])
    .filter(pl.col("num_ratings") >= 50)
    .sort("avg_rating", descending=True)
)

t_sort_eager = time.time() - t0

print(f"[EAGER] Tiempo ordenación: {t_sort_eager:.3f} s")
rating_pelicula_eager.head(10)
```

::: {.cell-output .cell-output-stdout}
    [EAGER] Tiempo ordenación: 0.530 s
:::

::: {.cell-output .cell-output-display execution_count="9"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (10, 3)</small>

  title                                 num_ratings   avg_rating
  ------------------------------------- ------------- ------------
  str                                   u32           f64
  \"Shawshank Redemption, The (199...   63366         4.44699
  \"Godfather, The (1972)\"             41355         4.364732
  \"Usual Suspects, The (1995)\"        47006         4.334372
  \"Schindler\'s List (1993)\"          50054         4.310175
  \"Godfather: Part II, The (1974)\"    27398         4.275641
  \"Seven Samurai (Shichinin no sa...   11611         4.27418
  \"Rear Window (1954)\"                17449         4.271334
  \"Band of Brothers (2001)\"           4305          4.263182
  \"Casablanca (1942)\"                 24349         4.258327
  \"Sunset Blvd. (a.k.a. Sunset Bo...   6525          4.256935

</div>
:::
:::::

### 4b. LazyFrame

::::: {.cell execution_count="10"}
``` {.python .cell-code}
t0 = time.time()

rating_pelicula_lazy = (
    pl.scan_csv(DATA_PATH)
    .group_by("title")
    .agg([
        pl.col("rating").count().alias("num_ratings"),
        pl.col("rating").mean().alias("avg_rating")
    ])
    .filter(pl.col("num_ratings") >= 50)
    .sort("avg_rating", descending=True)
    .collect()
)

t_sort_lazy = time.time() - t0

print(f"[LAZY] Tiempo ordenación: {t_sort_lazy:.3f} s")
rating_pelicula_lazy.head(10)
```

::: {.cell-output .cell-output-stdout}
    [LAZY] Tiempo ordenación: 0.936 s
:::

::: {.cell-output .cell-output-display execution_count="10"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (10, 3)</small>

  title                                 num_ratings   avg_rating
  ------------------------------------- ------------- ------------
  str                                   u32           f64
  \"Shawshank Redemption, The (199...   63366         4.44699
  \"Godfather, The (1972)\"             41355         4.364732
  \"Usual Suspects, The (1995)\"        47006         4.334372
  \"Schindler\'s List (1993)\"          50054         4.310175
  \"Godfather: Part II, The (1974)\"    27398         4.275641
  \"Seven Samurai (Shichinin no sa...   11611         4.27418
  \"Rear Window (1954)\"                17449         4.271334
  \"Band of Brothers (2001)\"           4305          4.263182
  \"Casablanca (1942)\"                 24349         4.258327
  \"Sunset Blvd. (a.k.a. Sunset Bo...   6525          4.256935

</div>
:::
:::::

## 5. Convertir rating_timestamp a fecha

### 5a. Eager

::::: {.cell execution_count="11"}
``` {.python .cell-code}
t0 = time.time()

# El timestamp ya viene como string 'YYYY-MM-DD HH:MM:SS' — convertir a Datetime
df_con_fecha = df.with_columns(
    pl.col("rating_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S").alias("fecha_rating")
)

t_ts_eager = time.time() - t0

print(f"[EAGER] Tiempo conversión timestamp: {t_ts_eager:.3f} s")
df_con_fecha.select(["userId", "title", "rating", "rating_timestamp", "fecha_rating"]).head()
```

::: {.cell-output .cell-output-stdout}
    [EAGER] Tiempo conversión timestamp: 0.103 s
:::

::: {.cell-output .cell-output-display execution_count="11"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (5, 5)</small>

  userId   title                                 rating   rating_timestamp          fecha_rating
  -------- ------------------------------------- -------- ------------------------- ---------------------
  i64      str                                   f64      str                       datetime\[μs\]
  1        \"Jumanji (1995)\"                    3.5      \"2005-04-02 23:53:47\"   2005-04-02 23:53:47
  1        \"City of Lost Children, The (Ci...   3.5      \"2005-04-02 23:31:16\"   2005-04-02 23:31:16
  1        \"Twelve Monkeys (a.k.a. 12 Monk...   3.5      \"2005-04-02 23:33:39\"   2005-04-02 23:33:39
  1        \"Seven (a.k.a. Se7en) (1995)\"       3.5      \"2005-04-02 23:32:07\"   2005-04-02 23:32:07
  1        \"Usual Suspects, The (1995)\"        3.5      \"2005-04-02 23:29:40\"   2005-04-02 23:29:40

</div>
:::
:::::

### 5b. LazyFrame

::::: {.cell execution_count="12"}
``` {.python .cell-code}
t0 = time.time()

df_con_fecha_lazy = (
    pl.scan_csv(DATA_PATH)
    .with_columns(
        pl.col("rating_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S").alias("fecha_rating")
    )
    .select(["userId", "title", "rating", "rating_timestamp", "fecha_rating"])
    .collect()
)

t_ts_lazy = time.time() - t0

print(f"[LAZY] Tiempo conversión timestamp: {t_ts_lazy:.3f} s")
df_con_fecha_lazy.head()
```

::: {.cell-output .cell-output-stdout}
    [LAZY] Tiempo conversión timestamp: 0.674 s
:::

::: {.cell-output .cell-output-display execution_count="12"}
<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (5, 5)</small>

  userId   title                                 rating   rating_timestamp          fecha_rating
  -------- ------------------------------------- -------- ------------------------- ---------------------
  i64      str                                   f64      str                       datetime\[μs\]
  1        \"Jumanji (1995)\"                    3.5      \"2005-04-02 23:53:47\"   2005-04-02 23:53:47
  1        \"City of Lost Children, The (Ci...   3.5      \"2005-04-02 23:31:16\"   2005-04-02 23:31:16
  1        \"Twelve Monkeys (a.k.a. 12 Monk...   3.5      \"2005-04-02 23:33:39\"   2005-04-02 23:33:39
  1        \"Seven (a.k.a. Se7en) (1995)\"       3.5      \"2005-04-02 23:32:07\"   2005-04-02 23:32:07
  1        \"Usual Suspects, The (1995)\"        3.5      \"2005-04-02 23:29:40\"   2005-04-02 23:29:40

</div>
:::
:::::

## 6. Comparación de tiempos: Eager vs LazyFrame

:::: {.cell execution_count="13"}
``` {.python .cell-code}
import polars as pl

comparativa = pl.DataFrame({
    "Operación": [
        "Carga / scan_csv",
        "Filtro Action ≥4",
        "Agregación por usuario",
        "Ordenación por rating",
        "Conversión timestamp"
    ],
    "Eager (s)": [t_load_eager, t_filter_eager, t_agg_eager, t_sort_eager, t_ts_eager],
    "Lazy (s)": [None, t_filter_lazy, t_agg_lazy, t_sort_lazy, t_ts_lazy]
})

print(comparativa)
```

::: {.cell-output .cell-output-stdout}
    shape: (5, 3)
    ┌────────────────────────┬───────────┬──────────┐
    │ Operación              ┆ Eager (s) ┆ Lazy (s) │
    │ ---                    ┆ ---       ┆ ---      │
    │ str                    ┆ f64       ┆ f64      │
    ╞════════════════════════╪═══════════╪══════════╡
    │ Carga / scan_csv       ┆ 0.634315  ┆ null     │
    │ Filtro Action ≥4       ┆ 0.109747  ┆ 0.833987 │
    │ Agregación por usuario ┆ 0.270017  ┆ 0.540137 │
    │ Ordenación por rating  ┆ 0.52992   ┆ 0.936424 │
    │ Conversión timestamp   ┆ 0.102744  ┆ 0.674459 │
    └────────────────────────┴───────────┴──────────┘
:::
::::

## 7. Preguntas de reflexión

**P1. ¿Qué diferencias de rendimiento observas?**\
\> Polars es significativamente más rápido que Pandas en la mayoría de
operaciones sobre grandes volúmenes gracias a su implementación en Rust
y al paralelismo automático. La diferencia se hace especialmente notoria
en agregaciones sobre columnas numéricas y filtros sobre strings.

**P2. ¿Qué mejora aporta LazyFrame?**\
\> LazyFrame permite a Polars construir un plan de ejecución y
optimizarlo antes de lanzarlo. Esto incluye *predicate pushdown*
(aplicar filtros lo antes posible para leer menos datos), *projection
pushdown* (leer solo las columnas necesarias) y eliminación de pasos
redundantes. El resultado es generalmente más rápido y menos uso de
memoria que el modo eager cuando hay múltiples operaciones encadenadas.

**P3. ¿Cómo escalaría con datasets más grandes?**\
\> Polars en modo LazyFrame puede procesar archivos más grandes que la
RAM gracias a la lectura en streaming. Sin embargo, sigue siendo un
único nodo. Para datos que superan la capacidad de un nodo (cientos de
GB o TB), PySpark con un clúster es la solución adecuada.

**P4. ¿Qué uso tiene en la industria?**\
\> Polars está ganando popularidad rápidamente como alternativa a Pandas
en análisis de datos a escala de un solo servidor. Es especialmente
valorado en ciencia de datos donde se trabaja con datos de decenas de
GB. Para producción a gran escala, PySpark sigue siendo el estándar.
