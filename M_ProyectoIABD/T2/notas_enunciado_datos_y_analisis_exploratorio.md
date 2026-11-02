# Notas del enunciado: datos del proyecto y análisis exploratorio

Dataset: [/home/eze/IA-BigData/M_ProyectoIABD/T2/data.csv](/home/eze/IA-BigData/M_ProyectoIABD/T2/data.csv)

- Datos para entrenamiento y validación: Todas las filas del dataset de e-commerce que
  corresponden a datos entre el 1 de diciembre de 2010 y el 8 de noviembre de 2011.
- Datos  para  test  (evaluación  final):  Todas  las  filas  del  dataset  de  e-commerce  que
  corresponden a datos entre el 9 de noviembre de 2011 y el 9 de diciembre de 2011.
- Variable objetivo a predecir: Valor total de las ventas por día, para cada día entre el 9
  de noviembre de 2011 y el 9 de diciembre de 2011.


Análisis  exploratorio  de  los  datos  y  su  calidad:  La  idea  de  este  paso  es  estudiar  el 

conjunto  de  datos  y  entender  bien  cada  una  de  las  columnas  y  sus  valores  antes  de 

ejecutar alguna acción sobre ellos. Algunas recomendaciones a estudiar son las 

siguientes: 


○ Entendimiento de los datos: Estudia los valores de cada columna, con funciones 

como  head o  unique.  Debes  observar  por  ejemplo  que  hay  transacciones  con 

valores  0  o  negativos  (que  podemos  deducir  que  corresponden  a  regalos, 

cambios o devoluciones). 

○ Búsqueda de valores faltantes, duplicados o erróneos: Estudia los valores que 

faltan o son incoherentes para cada columna, e intenta entender por qué faltan. 

Utiliza funciones de Pandas como isnull, describe o value_counts para hacerte 

una idea. Debes observar, por ejemplo, que hay transacciones (filas) en que no 

hay cliente y/o descripción 


○ Búsqueda de outliers: Encuentra para cada columna valores de magnitud muy 

diferente que pueden distorsionar el entrenamiento del modelo. Utiliza 

funciones  de  Pandas  como  describe  o  nunique  para  ver  la  distribución  de 

valores  y  discriminar  los más  comunes  y  los  menos  comunes.  Debes  observar 

por  ejemplo  que  hay  valores  de  ventas  extremadamente  altos,  o  que  hay 

códigos de stock o descripciones que no siguen los patrones habituales. 

○ Creación  de  gráficos  auxiliares:  Siempre  que  sea  posible,  utiliza  gráficos  para 

cada uno de los pasos anteriores, para entender mejor las variables y también 

para  mostrar  de  manera  gráfica  los  pasos  realizados  en  la  memoria  al  final. 

Utiliza  librerías  como  Seaborn  o  Matplotlib  para  ejecutar  los  gráficos  más 

habituales (gráficos de columnas, barras o circulares).
