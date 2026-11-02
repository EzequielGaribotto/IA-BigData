---
title: Análisis de MovieLens 20M con PySpark
toc-title: Table of contents
---

**Actividad:** RA1 --- Comparación de Pandas, Polars y PySpark\
**Dataset:** `movielens_superdataset.csv` (columnas: userId, movieId,
rating, rating_timestamp, title, genres)

> Ejecutar las celdas **en orden de arriba a abajo**.

## Tareas

1.  Crear SparkSession y cargar el dataset
2.  Filtrar películas de género **Action** con `rating ≥ 4`
3.  Calcular **media y desviación estándar** de ratings por usuario
4.  Ordenar películas por **rating promedio** descendente
5.  Convertir `rating_timestamp` a fecha legible
6.  Medir tiempos de ejecución

## 0. Imports y SparkSession

Ejecuta esta celda primero --- define todas las dependencias y crea
`spark`.

::::: {.cell execution_count="1"}
``` {.python .cell-code}
# !pip install pyspark  # descomenta si no tienes pyspark

import os, zipfile, time
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("MovieLens-RA1")
    # --- Configuración de memoria ---
    .config("spark.driver.memory",          "6g")   # RAM para el driver
    .config("spark.executor.memory",        "6g")   # RAM para ejecutores (mismo proceso en local)
    .config("spark.driver.maxResultSize",   "2g")   # máximo para collect/show
    .config("spark.sql.shuffle.partitions", "4")    # menos particiones = menos overhead en local
    # Permite que Spark vuelque a disco si se queda sin RAM (más lento pero sin OOM)
    .config("spark.memory.offHeap.enabled", "true")
    .config("spark.memory.offHeap.size",    "2g")
    .getOrCreate()
)

print(f"Spark versión: {spark.version}")
print("SparkSession lista")
```

::: {.cell-output .cell-output-stderr}
    WARNING: Using incubator modules: jdk.incubator.vector
    Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
    26/06/15 10:55:54 WARN Utils: Your hostname, DESKTOP-HNSTSNV, resolves to a loopback address: 127.0.1.1; using 10.255.255.254 instead (on interface lo)
    26/06/15 10:55:54 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
    Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/06/15 10:55:54 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
:::

::: {.cell-output .cell-output-stdout}
    Spark versión: 4.1.2
    SparkSession lista
:::
:::::

## 0.1 Preparar el superdataset (ejecutar una sola vez)

Une `rating.csv` + `movie.csv` del zip y guarda
`movielens_superdataset.csv`.\
Las siguientes ejecuciones lo saltan si el archivo ya existe.

:::: {.cell execution_count="2"}
``` {.python .cell-code}
ZIP_PATH = "/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/archive.zip"
OUT_PATH = "/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv"

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
        ratings.merge(movies, on="movieId", how="left")
               .rename(columns={"timestamp": "rating_timestamp"})
    )
    superdataset.to_csv(OUT_PATH, index=False)
    print(f"Superdataset creado: {len(superdataset):,} filas")

DATA_PATH = OUT_PATH
print(f"DATA_PATH = {DATA_PATH}")
```

::: {.cell-output .cell-output-stdout}
    Ya existe: /home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv
    DATA_PATH = /home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/movielens_superdataset.csv
:::
::::

## 1. Cargar el dataset en Spark

:::::: {.cell execution_count="3"}
``` {.python .cell-code}
t0 = time.time()

df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)
df.cache()
count_total = df.count()  # acción que fuerza la carga y el cache

t_load = time.time() - t0

print(f"Filas totales: {count_total:,}")
print(f"Tiempo de carga + cache: {t_load:.3f} s")
df.printSchema()
df.show(5)
```

::: {.cell-output .cell-output-stderr}
    [Stage 2:==========================================>              (24 + 8) / 32]
:::

::: {.cell-output .cell-output-stdout}
    Filas totales: 20,000,263
    Tiempo de carga + cache: 9.005 s
    root
     |-- userId: integer (nullable = true)
     |-- movieId: integer (nullable = true)
     |-- rating: double (nullable = true)
     |-- rating_timestamp: timestamp (nullable = true)
     |-- title: string (nullable = true)
     |-- genres: string (nullable = true)

    +------+-------+------+-------------------+--------------------+--------------------+
    |userId|movieId|rating|   rating_timestamp|               title|              genres|
    +------+-------+------+-------------------+--------------------+--------------------+
    |     1|      2|   3.5|2005-04-02 23:53:47|      Jumanji (1995)|Adventure|Childre...|
    |     1|     29|   3.5|2005-04-02 23:31:16|City of Lost Chil...|Adventure|Drama|F...|
    |     1|     32|   3.5|2005-04-02 23:33:39|Twelve Monkeys (a...|Mystery|Sci-Fi|Th...|
    |     1|     47|   3.5|2005-04-02 23:32:07|Seven (a.k.a. Se7...|    Mystery|Thriller|
    |     1|     50|   3.5|2005-04-02 23:29:40|Usual Suspects, T...|Crime|Mystery|Thr...|
    +------+-------+------+-------------------+--------------------+--------------------+
    only showing top 5 rows
:::

::: {.cell-output .cell-output-stderr}
                                                                                    
:::
::::::

## 2. Filtrar Action con rating ≥ 4

> `filter` es una **transformación** --- no se ejecuta hasta que llegue
> una **acción** como `count()` o `show()`.

:::: {.cell execution_count="4"}
``` {.python .cell-code}
t0 = time.time()

df_action = df.filter(
    F.col("genres").contains("Action") &
    (F.col("rating") >= 4)
)

count_action = df_action.count()

t_filter = time.time() - t0

print(f"Filas tras filtro Action ≥4: {count_action:,}")
print(f"Tiempo filtrado: {t_filter:.3f} s")
df_action.show(5)
```

::: {.cell-output .cell-output-stdout}
    Filas tras filtro Action ≥4: 2,583,646
    Tiempo filtrado: 0.614 s
    +------+-------+------+-------------------+--------------------+--------------------+
    |userId|movieId|rating|   rating_timestamp|               title|              genres|
    +------+-------+------+-------------------+--------------------+--------------------+
    |     1|    151|   4.0|2004-09-10 03:08:54|      Rob Roy (1995)|Action|Drama|Roma...|
    |     1|    260|   4.0|2005-04-02 23:33:46|Star Wars: Episod...|Action|Adventure|...|
    |     1|    293|   4.0|2005-04-02 23:31:43|Léon: The Profess...|Action|Crime|Dram...|
    |     1|    541|   4.0|2005-04-02 23:30:03| Blade Runner (1982)|Action|Sci-Fi|Thr...|
    |     1|   1036|   4.0|2005-04-02 23:44:40|     Die Hard (1988)|Action|Crime|Thri...|
    +------+-------+------+-------------------+--------------------+--------------------+
    only showing top 5 rows
:::
::::

:::: {.cell execution_count="5"}
``` {.python .cell-code}
# Plan físico de ejecución
df_action.explain()
```

::: {.cell-output .cell-output-stdout}
    == Physical Plan ==
    *(1) Filter (((isnotnull(genres#22) AND isnotnull(rating#19)) AND Contains(genres#22, Action)) AND (rating#19 >= 4.0))
    +- InMemoryTableScan [userId#17, movieId#18, rating#19, rating_timestamp#20, title#21, genres#22], [isnotnull(genres#22), isnotnull(rating#19), Contains(genres#22, Action), (rating#19 >= 4.0)]
          +- InMemoryRelation [userId#17, movieId#18, rating#19, rating_timestamp#20, title#21, genres#22], StorageLevel(disk, memory, deserialized, 1 replicas)
                +- FileScan csv [userId#17,movieId#18,rating#19,rating_timestamp#20,title#21,genres#22] Batched: false, DataFilters: [], Format: CSV, Location: InMemoryFileIndex(1 paths)[file:/home/eze/IA-BigData/M05_BigDataAplicado/RA1/obligatorias/moviele..., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<userId:int,movieId:int,rating:double,rating_timestamp:timestamp,title:string,genres:string>
:::
::::

## 3. Media y desviación estándar de ratings por usuario

:::: {.cell execution_count="6"}
``` {.python .cell-code}
t0 = time.time()

stats_por_usuario = (
    df.groupBy("userId")
    .agg(
        F.avg("rating").alias("rating_mean"),
        F.stddev("rating").alias("rating_std"),
        F.count("rating").alias("num_ratings")
    )
    .orderBy("userId")
)

stats_por_usuario.show(10)

t_agg = time.time() - t0

print(f"Tiempo agregación por usuario: {t_agg:.3f} s")
print(f"Usuarios únicos: {stats_por_usuario.count():,}")
```

::: {.cell-output .cell-output-stdout}
    +------+------------------+-------------------+-----------+
    |userId|       rating_mean|         rating_std|num_ratings|
    +------+------------------+-------------------+-----------+
    |     1| 3.742857142857143|0.38228420724211504|        175|
    |     2|               4.0|  1.064581294844754|         61|
    |     3| 4.122994652406417|  0.910426825916061|        187|
    |     4|3.5714285714285716| 0.7901510136288029|         28|
    |     5|4.2727272727272725| 0.9694638414402775|         66|
    |     6|              3.75| 1.0733936430981312|         24|
    |     7| 3.289855072463768| 0.8587762841347901|        276|
    |     8|               3.8| 0.9720738327060778|         70|
    |     9| 3.057142857142857| 1.1361145639947623|         35|
    |    10|3.8947368421052633| 0.6058040751966705|         38|
    +------+------------------+-------------------+-----------+
    only showing top 10 rows
    Tiempo agregación por usuario: 0.576 s
    Usuarios únicos: 138,493
:::
::::

## 4. Ordenar películas por rating promedio

:::: {.cell execution_count="7"}
``` {.python .cell-code}
t0 = time.time()

rating_por_pelicula = (
    df.groupBy("title")
    .agg(
        F.count("rating").alias("num_ratings"),
        F.avg("rating").alias("avg_rating")
    )
    .filter(F.col("num_ratings") >= 50)
    .orderBy(F.col("avg_rating").desc())
)

rating_por_pelicula.show(10)

t_sort = time.time() - t0

print(f"Tiempo ordenación: {t_sort:.3f} s")
```

::: {.cell-output .cell-output-stdout}
    +--------------------+-----------+-----------------+
    |               title|num_ratings|       avg_rating|
    +--------------------+-----------+-----------------+
    |Shawshank Redempt...|      63366|4.446990499637029|
    |Godfather, The (1...|      41355|4.364732196832306|
    |Usual Suspects, T...|      47006|4.334372207803259|
    |Schindler's List ...|      50054|4.310175010988133|
    |Godfather: Part I...|      27398|4.275640557704942|
    |Seven Samurai (Sh...|      11611|  4.2741796572216|
    |  Rear Window (1954)|      17449|4.271333600779414|
    |Band of Brothers ...|       4305|4.263182346109176|
    |   Casablanca (1942)|      24349|4.258326830670664|
    |Sunset Blvd. (a.k...|       6525|4.256934865900383|
    +--------------------+-----------+-----------------+
    only showing top 10 rows
    Tiempo ordenación: 0.708 s
:::
::::

## 5. Convertir rating_timestamp a fecha

:::: {.cell execution_count="8"}
``` {.python .cell-code}
t0 = time.time()

# El timestamp viene como string 'YYYY-MM-DD HH:MM:SS'
df_con_fecha = df.withColumn(
    "fecha_rating",
    F.to_timestamp(F.col("rating_timestamp"), "yyyy-MM-dd HH:mm:ss")
)

df_con_fecha.select(
    "userId", "title", "rating", "rating_timestamp", "fecha_rating"
).show(10, truncate=False)

t_ts = time.time() - t0

print(f"Tiempo conversión timestamp: {t_ts:.3f} s")
```

::: {.cell-output .cell-output-stdout}
    +------+---------------------------------------------------------------+------+-------------------+-------------------+
    |userId|title                                                          |rating|rating_timestamp   |fecha_rating       |
    +------+---------------------------------------------------------------+------+-------------------+-------------------+
    |1     |Jumanji (1995)                                                 |3.5   |2005-04-02 23:53:47|2005-04-02 23:53:47|
    |1     |City of Lost Children, The (Cité des enfants perdus, La) (1995)|3.5   |2005-04-02 23:31:16|2005-04-02 23:31:16|
    |1     |Twelve Monkeys (a.k.a. 12 Monkeys) (1995)                      |3.5   |2005-04-02 23:33:39|2005-04-02 23:33:39|
    |1     |Seven (a.k.a. Se7en) (1995)                                    |3.5   |2005-04-02 23:32:07|2005-04-02 23:32:07|
    |1     |Usual Suspects, The (1995)                                     |3.5   |2005-04-02 23:29:40|2005-04-02 23:29:40|
    |1     |Rumble in the Bronx (Hont faan kui) (1995)                     |3.5   |2004-09-10 03:09:00|2004-09-10 03:09:00|
    |1     |Rob Roy (1995)                                                 |4.0   |2004-09-10 03:08:54|2004-09-10 03:08:54|
    |1     |Clerks (1994)                                                  |4.0   |2005-04-02 23:46:13|2005-04-02 23:46:13|
    |1     |Interview with the Vampire: The Vampire Chronicles (1994)      |4.0   |2005-04-02 23:35:40|2005-04-02 23:35:40|
    |1     |Star Wars: Episode IV - A New Hope (1977)                      |4.0   |2005-04-02 23:33:46|2005-04-02 23:33:46|
    +------+---------------------------------------------------------------+------+-------------------+-------------------+
    only showing top 10 rows
    Tiempo conversión timestamp: 0.074 s
:::
::::

## 6. Resumen de tiempos

:::: {.cell execution_count="9"}
``` {.python .cell-code}
tiempos = pd.DataFrame({
    "Operación": [
        "Carga CSV + cache",
        "Filtro Action ≥4",
        "Agregación por usuario",
        "Ordenación por rating",
        "Conversión timestamp"
    ],
    "Tiempo PySpark (s)": [t_load, t_filter, t_agg, t_sort, t_ts]
})

print(tiempos.to_string(index=False))
print(f"\nTotal: {tiempos['Tiempo PySpark (s)'].sum():.3f} s")
```

::: {.cell-output .cell-output-stdout}
                 Operación  Tiempo PySpark (s)
         Carga CSV + cache            9.004626
          Filtro Action ≥4            0.614190
    Agregación por usuario            0.575526
     Ordenación por rating            0.707681
      Conversión timestamp            0.073586

    Total: 10.976 s
:::
::::

## 7. Spark SQL (alternativa declarativa)

:::: {.cell execution_count="10"}
``` {.python .cell-code}
df.createOrReplaceTempView("movielens")

spark.sql("""
    SELECT title, COUNT(*) AS num_ratings, ROUND(AVG(rating),3) AS avg_rating
    FROM movielens
    WHERE genres LIKE '%Action%' AND rating >= 4
    GROUP BY title HAVING COUNT(*) >= 50
    ORDER BY avg_rating DESC LIMIT 10
""").show(truncate=False)
```

::: {.cell-output .cell-output-stdout}
    +-----------------------------------------------------+-----------+----------+
    |title                                                |num_ratings|avg_rating|
    +-----------------------------------------------------+-----------+----------+
    |Band of Brothers (2001)                              |3560       |4.592     |
    |Star Wars: Episode IV - A New Hope (1977)            |42612      |4.584     |
    |Seven Samurai (Shichinin no samurai) (1954)          |9525       |4.584     |
    |Fight Club (1999)                                    |32094      |4.575     |
    |Matrix, The (1999)                                   |40163      |4.564     |
    |Lord of the Rings: The Return of the King, The (2003)|24042      |4.561     |
    |Princess Bride, The (1987)                           |25273      |4.554     |
    |Star Wars: Episode V - The Empire Strikes Back (1980)|35743      |4.553     |
    |Blade Runner (1982)                                  |23007      |4.547     |
    |Braveheart (1995)                                    |38390      |4.538     |
    +-----------------------------------------------------+-----------+----------+
:::
::::

:::: {.cell execution_count="11"}
``` {.python .cell-code}
spark.sql("""
    SELECT userId,
           ROUND(AVG(rating),3)    AS rating_mean,
           ROUND(STDDEV(rating),3) AS rating_std,
           COUNT(*) AS num_ratings
    FROM movielens
    GROUP BY userId ORDER BY userId LIMIT 10
""").show()
```

::: {.cell-output .cell-output-stdout}
    +------+-----------+----------+-----------+
    |userId|rating_mean|rating_std|num_ratings|
    +------+-----------+----------+-----------+
    |     1|      3.743|     0.382|        175|
    |     2|        4.0|     1.065|         61|
    |     3|      4.123|      0.91|        187|
    |     4|      3.571|      0.79|         28|
    |     5|      4.273|     0.969|         66|
    |     6|       3.75|     1.073|         24|
    |     7|       3.29|     0.859|        276|
    |     8|        3.8|     0.972|         70|
    |     9|      3.057|     1.136|         35|
    |    10|      3.895|     0.606|         38|
    +------+-----------+----------+-----------+
:::
::::

## 8. Preguntas de reflexión

**P1. ¿Qué diferencias de rendimiento observas entre Pandas, Polars y
PySpark?**\
\> PySpark tiene overhead de inicio (JVM, SparkSession) que lo hace más
lento en datasets pequeños en RAM. Su ventaja es la escala horizontal:
en un clúster distribuye el trabajo entre nodos y procesa datos que
superan la RAM de cualquier máquina individual.

**P2. ¿Qué mejora aporta la lazy evaluation de Spark?**\
\> Spark construye un DAG con las transformaciones y solo lo ejecuta al
llegar una acción. El Catalyst optimizer puede reordenar operaciones,
hacer predicate pushdown y eliminar columnas innecesarias antes de
ejecutar.

**P3. ¿Cómo escalaría con datasets más grandes?**\
\> Añadiendo más nodos al clúster. El mismo código corre sin cambios
sobre 20M o 20B de filas --- Spark reparte las particiones
automáticamente.

**P4. ¿Qué uso tiene en la industria?**\
\> ETL a gran escala (pipelines de TB/día), análisis de logs, data
warehouses y feature engineering para ML. Plataformas como Databricks,
Google Dataproc y Amazon EMR están construidas sobre Spark.

:::: {.cell execution_count="12"}
``` {.python .cell-code}
# Liberar recursos al terminar (no ejecutar hasta haber terminado todo)
spark.stop()
print("SparkSession cerrada")
```

::: {.cell-output .cell-output-stdout}
    SparkSession cerrada
:::
::::
