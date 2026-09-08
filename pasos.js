/* ============================================================
   pasos.js

   Lo genera build-pasos.py leyendo el array NODES de cada ruta.
   No se edita a mano: se corre el script y queda al día.

   Existe para el planificador semanal, que necesita saber cuál
   es tu próximo paso y cuánto lleva sin abrir todas las páginas.
   ============================================================ */
var PASOS = [
 {
  "archivo": "sql-python.html",
  "clave": "sqlpy",
  "nombre": "SQL y Python",
  "actos": [
   "Comprehensive SQL",
   "Comprehensive Python"
  ],
  "pasos": [
   {
    "id": "q01",
    "t": "Fundamentos de SQL",
    "min": 240,
    "act": 1,
    "time": "4 h 30 min",
    "sum": "Ocho lecciones desde cero: qué es una base, SELECT, filtros, operadores lógicos, nulos, orden y límite.",
    "goal": "Terminas este módulo cuando escribes una consulta con filtros sin buscar la sintaxis.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-databases-and-sql",
    "boss": false,
    "wins": [
     "SELECT, FROM y WHERE sin dudar",
     "Los nulos, que no se comparan como el resto",
     "Patrones con LIKE, IN y BETWEEN"
    ]
   },
   {
    "id": "q02",
    "t": "Agrupar y agregar",
    "min": 180,
    "act": 1,
    "time": "3 h 25 min",
    "sum": "Contar, sumar y promediar por grupo, filtrar grupos con HAVING y agregar condicionalmente con CASE WHEN.",
    "goal": "Terminas este módulo cuando distingues WHERE de HAVING sin pensarlo.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-aggregate-functions",
    "boss": false,
    "wins": [
     "GROUP BY y las funciones de agregación",
     "HAVING, que filtra después de agrupar",
     "CASE WHEN adentro de un agregado"
    ]
   },
   {
    "id": "q03",
    "t": "Varias tablas",
    "min": 240,
    "act": 1,
    "time": "4 h 5 min",
    "sum": "El módulo más largo: UNION y los cinco tipos de JOIN, incluidos los que se hacen contra la misma tabla.",
    "goal": "Terminas este módulo cuando eliges el JOIN correcto por lo que necesitas, no por costumbre.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/understanding-table-relationships",
    "boss": false,
    "wins": [
     "INNER, LEFT, RIGHT, FULL y CROSS, con sus casos",
     "Self-joins, que aparecen en toda entrevista",
     "Encadenar varias tablas sin perderte"
    ]
   },
   {
    "id": "q04",
    "t": "Subconsultas y CTEs",
    "min": 120,
    "act": 1,
    "time": "2 h 20 min",
    "sum": "Partir una consulta grande en pasos con nombre. Es lo que separa una consulta legible de una ilegible.",
    "goal": "Terminas este módulo cuando reescribes una consulta anidada como una cadena de CTEs.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/understanding-subqueries",
    "boss": false,
    "wins": [
     "Subconsultas y dónde pueden ir",
     "WITH para armar la consulta por partes",
     "Los patrones que se repiten en entrevistas"
    ]
   },
   {
    "id": "q05",
    "t": "Fechas y texto",
    "min": 180,
    "act": 1,
    "time": "3 h 20 min",
    "sum": "Extraer partes de una fecha, hacer aritmética con ellas, y las funciones de texto que siempre piden.",
    "goal": "Terminas este módulo cuando resuelves una pregunta de rango de fechas sin googlear.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/date-time-data-types-and-extraction",
    "boss": false,
    "wins": [
     "Extraer año, mes y día, y truncar",
     "Aritmética de fechas y diferencias",
     "Funciones de texto y separación de cadenas"
    ]
   },
   {
    "id": "q06",
    "t": "Funciones de ventana",
    "min": 120,
    "act": 1,
    "time": "2 h 55 min",
    "sum": "El tema que decide muchas entrevistas: ranking, comparar con la fila anterior y acumulados sin perder el detalle.",
    "goal": "Terminas este módulo cuando resuelves un ranking por grupo de memoria.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-window-functions",
    "boss": true,
    "wins": [
     "PARTITION BY y las funciones de ranking",
     "LAG y LEAD para comparar filas vecinas",
     "Marcos de ventana, que es lo que casi nadie sabe"
    ]
   },
   {
    "id": "q07",
    "t": "Fundamentos de DataFrames",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "pandas desde cero: columnas, filtros, condiciones combinadas, datos faltantes y ordenamiento.",
    "goal": "Terminas este módulo cuando filtras un DataFrame por varias condiciones sin errores de sintaxis.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/introduction-to-python-and-pandas",
    "boss": false,
    "wins": [
     "Seleccionar y crear columnas",
     "Filtrar filas y combinar condiciones",
     "Datos faltantes, que en pandas tienen sus reglas"
    ]
   },
   {
    "id": "q08",
    "t": "Agrupar y agregar",
    "min": 120,
    "act": 2,
    "time": "2 h 50 min",
    "sum": "El equivalente en pandas de lo que hiciste en SQL: groupby, filtrado de grupos y agregación condicional.",
    "goal": "Terminas este módulo cuando traduces una consulta con GROUP BY a pandas de corrido.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/introduction-to-aggregate-methods",
    "boss": false,
    "wins": [
     "groupby y los métodos de agregación",
     "Filtrar grupos después de agrupar",
     "NaN en agregaciones, que no se comporta como cero"
    ]
   },
   {
    "id": "q09",
    "t": "Combinar DataFrames",
    "min": 120,
    "act": 2,
    "time": "2 h 45 min",
    "sum": "concat y los cinco tipos de merge, incluido el que se hace contra el mismo DataFrame.",
    "goal": "Terminas este módulo cuando eliges entre concat y merge sin dudar.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/understanding-dataframe-relationships",
    "boss": false,
    "wins": [
     "concat frente a merge, que no son lo mismo",
     "Los cinco tipos de merge",
     "Self-merges y varios DataFrames encadenados"
    ]
   },
   {
    "id": "q10",
    "t": "Análisis en varios pasos",
    "min": 120,
    "act": 2,
    "time": "2 h 55 min",
    "sum": "Encadenar transformaciones, el patrón transform, lógica propia con apply y remodelado de datos.",
    "goal": "Terminas este módulo cuando resuelves un problema en pasos encadenados y legibles.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/step-by-step-analysis",
    "boss": false,
    "wins": [
     "Encadenar sin crear diez variables intermedias",
     "transform, que es el groupby que no colapsa filas",
     "apply para lo que no cubre pandas"
    ]
   },
   {
    "id": "q11",
    "t": "Fechas, texto y lógica",
    "min": 120,
    "act": 2,
    "time": "2 h 40 min",
    "sum": "Lo mismo del módulo cinco de SQL, del lado de pandas: fechas, cadenas y patrones.",
    "goal": "Terminas este módulo cuando manipulas fechas en pandas sin pelearte con los tipos.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/datetime-extraction",
    "boss": false,
    "wins": [
     "Extraer y truncar fechas",
     "Métodos de texto de pandas",
     "Patrones y separación de cadenas"
    ]
   },
   {
    "id": "q12",
    "t": "Operaciones de ventana",
    "min": 60,
    "act": 2,
    "time": "1 h 40 min",
    "sum": "El cierre: ranking, comparación con filas vecinas y acumulados en pandas.",
    "goal": "Terminas este módulo cuando resuelves en pandas lo mismo que resolviste con funciones de ventana en SQL.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-python/introduction-to-window-operations",
    "boss": true,
    "wins": [
     "Ranking dentro de grupos",
     "Comparar con la fila anterior o siguiente",
     "Acumulados y promedios móviles"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "data-engineer.html",
  "clave": "de",
  "nombre": "Data Engineer",
  "actos": [],
  "pasos": [
   {
    "id": "d01",
    "t": "SQL",
    "min": 1800,
    "act": 0,
    "time": "6 semanas",
    "sum": "La herramienta que vas a usar todos los días de tu carrera, sin excepción.",
    "goal": "Cierras este nivel cuando escribes una consulta con ventanas y subconsultas sin buscar la sintaxis, y entiendes por qué una tarda diez veces más que otra.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Agrupar, filtrar agregados y ordenar sin dudar",
     "Funciones de ventana: ranking, acumulados y comparaciones contra la fila anterior",
     "Leer un plan de ejecución y saber dónde se va el tiempo",
     "Resolver una pregunta de entrevista sin pánico"
    ]
   },
   {
    "id": "d02",
    "t": "Python",
    "min": 1800,
    "act": 0,
    "time": "6 semanas",
    "sum": "El pegamento de todo lo demás: mover datos, llamar APIs y automatizar lo que se repite.",
    "goal": "Cierras este nivel cuando escribes un script que lee de una fuente, transforma y escribe en otra, con sus errores manejados.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Listas, diccionarios y comprensiones sin consultar la documentación",
     "Leer y escribir archivos y consumir una API",
     "pandas para explorar datos antes de meterlos en una base",
     "Entender un traceback y arreglarlo solo"
    ]
   },
   {
    "id": "d03",
    "t": "Data Modeling",
    "min": 1200,
    "act": 0,
    "time": "4 semanas",
    "sum": "El nivel que separa a quien mueve datos de quien diseña cómo se guardan. Casi nadie lo enseña gratis.",
    "goal": "Cierras este nivel cuando puedes dibujar el modelo de un negocio con sus hechos y sus dimensiones, y defender por qué lo partiste así.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Distinguir tablas de hechos de tablas de dimensiones",
     "Elegir la granularidad correcta, que es la decisión que después no se puede deshacer",
     "Manejar dimensiones que cambian con el tiempo",
     "Saber cuándo normalizar y cuándo repetir datos a propósito"
    ]
   },
   {
    "id": "d04",
    "t": "Platform",
    "min": 90,
    "act": 0,
    "time": "según la que elijas",
    "sum": "Una plataforma de datos hecha en serio. Elige una sola y hazla completa: la segunda después cuesta la mitad.",
    "goal": "Cierras este nivel cuando cargas, transformas y consultas datos en una plataforma, y entiendes qué te cobra y por qué.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Dominio real de una plataforma, no haberla tocado un rato",
     "Entender el modelo de costos, que es lo que te van a preguntar en el trabajo",
     "Una certificación en el perfil, si vas por Snowflake",
     "La base para pasar a cualquier otra en semanas"
    ]
   },
   {
    "id": "d05",
    "t": "dbt y Airflow",
    "min": 2400,
    "act": 0,
    "time": "40 h",
    "sum": "Las dos herramientas que aparecen en casi toda búsqueda de trabajo: una transforma, la otra orquesta.",
    "goal": "Cierras este nivel cuando tienes un proyecto de dbt con tests corriendo todos los días desde un DAG de Airflow.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Versionar transformaciones como se versiona el código, con tests y documentación",
     "Programar pipelines con dependencias, reintentos y alertas",
     "Encontrar la tarea que rompió sin adivinar",
     "Hablar el idioma de cualquier equipo de datos moderno"
    ]
   },
   {
    "id": "d06",
    "t": "Cloud",
    "min": 2400,
    "act": 0,
    "time": "8 semanas",
    "sum": "Todo lo anterior corre sobre alguna nube. Elige una, entiende sus servicios de datos y arma tu proyecto ahí.",
    "goal": "Cierras este nivel cuando tu pipeline corre solo en la nube y puedes explicar cuánto cuesta por mes.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": [
     "Almacenamiento, cómputo y permisos, que son los tres ladrillos de cualquier nube",
     "Un proyecto propio corriendo de punta a punta, que vale más que diez certificados",
     "Saber leer una factura y saber qué apagar",
     "El repositorio con README que vas a mostrar en la entrevista"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "snowpro.html",
  "clave": "__suelto__",
  "nombre": "SnowPro Core",
  "actos": [
   "Fundamentos",
   "Núcleo del examen",
   "Performance y costos",
   "Jefe final"
  ],
  "pasos": [
   {
    "id": "n01",
    "t": "Arquitectura y primeros conceptos",
    "min": 360,
    "act": 1,
    "time": "6 h",
    "sum": "El track oficial que explica cómo Snowflake separa almacenamiento, cómputo y servicios.",
    "goal": "Terminas este hito cuando puedes dibujar las tres capas de la arquitectura de memoria y explicar qué hace cada una cuando corres una consulta.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n02",
    "t": "Tu cuenta de prueba de 120 días",
    "min": 20,
    "act": 1,
    "time": "20 min",
    "sum": "Registro por el link de Hands-On Essentials, que da 120 días en vez de 30.",
    "goal": "Terminas este hito cuando entras a Snowsight con tu propia cuenta y ves el warehouse COMPUTE_WH corriendo.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n03",
    "t": "Hands-On Essentials",
    "min": 480,
    "act": 1,
    "time": "8 h",
    "sum": "Laboratorios con datasets reales: cargar archivos, consultar, crear roles y manejar warehouses.",
    "goal": "Terminas este hito cuando cargas un archivo a una tabla nueva y consultas el resultado sin copiar y pegar el ejercicio.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n04",
    "t": "Snowsight, SnowSQL e Information Schema",
    "min": 120,
    "act": 1,
    "time": "2 h",
    "sum": "Las tres formas de hablarle a Snowflake: interfaz web, línea de comandos y metadata.",
    "goal": "Terminas este hito cuando consultas el historial de queries por SQL en vez de buscarlo a mano en la interfaz.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n05",
    "t": "Seguridad, gobernanza y RBAC",
    "min": 240,
    "act": 2,
    "time": "4 h",
    "sum": "El segundo dominio más pesado del examen y el gran ausente del documento original.",
    "goal": "Terminas este hito cuando puedes ordenar de memoria la jerarquía de roles del sistema y decir quién le otorga privilegios a quién.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n06",
    "t": "Carga y descarga de datos",
    "min": 180,
    "act": 2,
    "time": "3 h",
    "sum": "Todo lo que pasa entre un archivo crudo y una tabla consultable, en los dos sentidos.",
    "goal": "Terminas este hito cuando eliges el stage y el file format correctos sin abrir la documentación.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n07",
    "t": "Pipelines: Snowpipe, Streams y Tasks",
    "min": 180,
    "act": 2,
    "time": "3 h",
    "sum": "La automatización que convierte cargas manuales en un flujo continuo.",
    "goal": "Terminas este hito cuando puedes explicar el patrón stream más task para procesar solo lo nuevo.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n08",
    "t": "Time Travel contra Fail-safe",
    "min": 120,
    "act": 2,
    "time": "2 h",
    "sum": "La confusión más común del examen. Dos mecanismos distintos, con dueños distintos.",
    "goal": "Terminas este hito cuando respondes sin dudar quién recupera los datos en cada ventana y cuánto dura cada una.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n09",
    "t": "Data Sharing y Marketplace",
    "min": 120,
    "act": 2,
    "time": "2 h",
    "sum": "Compartir datos sin copiarlos, la feature que define el Data Cloud.",
    "goal": "Terminas este hito cuando puedes explicar por qué el consumidor paga el cómputo y el proveedor el almacenamiento.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n16",
    "t": "Lo que el C03 agregó",
    "min": 300,
    "act": 2,
    "time": "5 h",
    "sum": "Cortex, Iceberg, dynamic tables, Snowpark y datos sin estructura: nada de esto existía en la versión anterior del examen.",
    "goal": "Terminas este hito cuando puedes explicar qué problema resuelve cada una de estas features y, sobre todo, cuándo no usarlas.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n10",
    "t": "Level Up: Performance Series",
    "min": 300,
    "act": 3,
    "time": "5 h",
    "sum": "El track oficial de optimización: warehouses, caché, query profile y control de gasto.",
    "goal": "Terminas este hito cuando lees un query profile y señalas dónde se va el tiempo.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n11",
    "t": "Micro-partitions y clustering",
    "min": 90,
    "act": 3,
    "time": "1.5 h",
    "sum": "Cómo guarda Snowflake los datos por dentro y por qué eso decide el costo de tus consultas.",
    "goal": "Terminas este hito cuando explicas el pruning con un ejemplo propio.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n12",
    "t": "Créditos y resource monitors",
    "min": 90,
    "act": 3,
    "time": "1.5 h",
    "sum": "Quién consume, cuánto cuesta y cómo cortar el gasto antes de que duela.",
    "goal": "Terminas este hito cuando creas un monitor que suspende un warehouse al llegar a un límite.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n13",
    "t": "SQL Scripting y automatización",
    "min": 120,
    "act": 3,
    "time": "2 h",
    "sum": "Bloques procedurales con variables, loops y manejo de errores dentro de Snowflake.",
    "goal": "Terminas este hito cuando escribes un bloque con una variable, una condición y un cursor.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n14",
    "t": "Simulacros y repaso activo",
    "min": 360,
    "act": 4,
    "time": "6 h",
    "sum": "El simulacro de esta página y los de YouTube, hasta que las respuestas salgan solas.",
    "goal": "Terminas este hito cuando pasas dos rondas completas del simulacro arriba del 80%.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": false,
    "wins": []
   },
   {
    "id": "n15",
    "t": "Study Guide oficial y registro al examen",
    "min": 60,
    "act": 4,
    "time": "1 h",
    "sum": "El documento que define qué entra. Úsalo como checklist final, tema por tema.",
    "goal": "Terminas este hito cuando cada línea del Study Guide te remite a un hito que ya cerraste. Ahí agendas la fecha.",
    "cert": "",
    "i": "",
    "u": "",
    "boss": true,
    "wins": []
   }
  ],
  "nivel": "Con SQL sabido",
  "nivelN": 1
 },
 {
  "archivo": "cs50.html",
  "clave": "cs50",
  "nombre": "CS50",
  "actos": [
   "Arrancar",
   "Lenguajes y datos",
   "Especializarse",
   "Para otros roles"
  ],
  "pasos": [
   {
    "id": "c01",
    "t": "CS50 Scratch",
    "min": 3000,
    "act": 1,
    "time": "10 semanas",
    "sum": "Programación visual, arrastrando bloques. Para quien nunca escribió una línea de código.",
    "goal": "Terminas este curso cuando armas un juego o una animación que funciona, sin haber tocado sintaxis.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/scratch/",
    "boss": false,
    "wins": [
     "Entender qué es un bucle, una condición y una variable sin pelear con puntos y comas",
     "Perderle el miedo a la idea de programar",
     "Tener algo hecho que se puede mostrar"
    ]
   },
   {
    "id": "c02",
    "t": "CS50x, introducción a las ciencias de la computación",
    "min": 3600,
    "act": 1,
    "time": "12 semanas",
    "sum": "El curso legendario. Pensamiento algorítmico y resolución de problemas, con C, Python y SQL de paso.",
    "goal": "Terminas este curso cuando puedes descomponer un problema y elegir la estructura de datos correcta antes de escribir nada.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/x/",
    "boss": true,
    "wins": [
     "Entender qué hace la computadora por debajo: memoria, punteros, complejidad",
     "Comparar algoritmos y saber por qué uno tarda más",
     "El proyecto final, que es tuyo y sirve de carta de presentación"
    ]
   },
   {
    "id": "c03",
    "t": "CS50 Python",
    "min": 3000,
    "act": 2,
    "time": "10 semanas",
    "sum": "Programar de verdad en Python, con tests, manejo de errores y librerías.",
    "goal": "Terminas este curso cuando escribes un programa con sus pruebas y sabes por qué falla cuando falla.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/python/",
    "boss": false,
    "wins": [
     "Funciones, clases y manejo de excepciones",
     "Escribir tests, que es lo que separa un script de un programa",
     "Expresiones regulares y manipulación de archivos"
    ]
   },
   {
    "id": "c04",
    "t": "CS50 SQL",
    "min": 2100,
    "act": 2,
    "time": "7 semanas",
    "sum": "Diseño de bases de datos, no solo consultas: normalización, índices y transacciones.",
    "goal": "Terminas este curso cuando diseñas un esquema desde cero y justificas cada tabla.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/sql/",
    "boss": false,
    "wins": [
     "Modelar entidades y relaciones antes de escribir la primera tabla",
     "Escribir consultas que no se arrastran, con índices donde corresponde",
     "Entender transacciones y qué pasa cuando dos personas escriben a la vez"
    ]
   },
   {
    "id": "c05",
    "t": "CS50 R",
    "min": 1800,
    "act": 2,
    "time": "6 semanas",
    "sum": "Estadística, análisis y visualización con R, que es el idioma de la investigación con datos.",
    "goal": "Terminas este curso cuando tomas un dataset crudo y sacas un gráfico que responde una pregunta.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/r/",
    "boss": false,
    "wins": [
     "Limpiar y transformar datos con criterio estadístico",
     "Visualizaciones que muestran lo que hay, no lo que uno quiere ver",
     "Un segundo lenguaje de datos, que amplía dónde puedes trabajar"
    ]
   },
   {
    "id": "c06",
    "t": "CS50 AI",
    "min": 2100,
    "act": 3,
    "time": "7 semanas",
    "sum": "Cómo funcionan por dentro la búsqueda, el aprendizaje automático y las redes neuronales.",
    "goal": "Terminas este curso cuando implementas un modelo y puedes explicar qué está optimizando.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/ai/",
    "boss": false,
    "wins": [
     "Algoritmos de búsqueda y juegos, que es donde empezó todo",
     "Aprendizaje supervisado y redes, con las matemáticas en su lugar",
     "Criterio para saber cuándo un problema no necesita machine learning"
    ]
   },
   {
    "id": "c07",
    "t": "CS50 Web",
    "min": 3600,
    "act": 3,
    "time": "12 semanas",
    "sum": "Aplicaciones completas con Python, JavaScript y SQL: del backend al navegador.",
    "goal": "Terminas este curso cuando publicas una aplicación con usuarios, base de datos y su interfaz.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/web/",
    "boss": false,
    "wins": [
     "Django y modelos de datos del lado del servidor",
     "JavaScript en el navegador y cómo hablan las dos puntas",
     "Desplegar algo que otra persona puede usar"
    ]
   },
   {
    "id": "c08",
    "t": "CS50 Cybersecurity",
    "min": 1500,
    "act": 3,
    "time": "5 semanas",
    "sum": "Encontrar vulnerabilidades y proteger datos, desde contraseñas hasta cifrado.",
    "goal": "Terminas este curso cuando miras un sistema y ves por dónde entraría alguien.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/cybersecurity/",
    "boss": false,
    "wins": [
     "Amenazas reales y cómo se explotan, para poder defender",
     "Cifrado, autenticación y manejo de secretos",
     "Criterio de seguridad que sirve en cualquier rol técnico"
    ]
   },
   {
    "id": "c09",
    "t": "CS50 Games",
    "min": 3600,
    "act": 3,
    "time": "12 semanas",
    "sum": "Desarrollo de juegos en dos dimensiones con Lua y Love2D.",
    "goal": "Terminas este curso cuando tienes varios juegos jugables hechos por ti.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/games/",
    "boss": false,
    "wins": [
     "Bucles de juego, física simple y detección de colisiones",
     "Diseño de niveles y de dificultad",
     "La forma más entretenida de practicar programación"
    ]
   },
   {
    "id": "c10",
    "t": "CS50 Business",
    "min": 1800,
    "act": 4,
    "time": "6 semanas",
    "sum": "Los fundamentos técnicos para quien dirige o funda, sin tener que programar.",
    "goal": "Terminas este curso cuando entiendes de qué habla tu equipo técnico y puedes decidir con criterio.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/business/",
    "boss": false,
    "wins": [
     "Vocabulario real de nube, datos y desarrollo",
     "Saber qué preguntas hacer antes de aprobar un presupuesto",
     "Distinguir una promesa técnica razonable de uno vendiendo humo"
    ]
   },
   {
    "id": "c11",
    "t": "CS50 for Lawyers",
    "min": 1500,
    "act": 4,
    "time": "5 semanas",
    "sum": "El lado técnico de la privacidad, la propiedad intelectual y la tecnología legal.",
    "goal": "Terminas este curso cuando puedes leer un caso con componente técnico sin depender de un traductor.",
    "cert": "",
    "i": "",
    "u": "https://cs50.harvard.edu/law/",
    "boss": false,
    "wins": [
     "Cómo funcionan los datos personales y su protección",
     "Criptografía y firmas, aplicadas a lo legal",
     "Vocabulario compartido con equipos de ingeniería"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "dbt.html",
  "clave": "dbt",
  "nombre": "dbt",
  "actos": [
   "Entender qué es",
   "Construir",
   "Hacerlo confiable",
   "Ir más lejos"
  ],
  "pasos": [
   {
    "id": "d01",
    "t": "Qué es dbt y para qué sirve",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "La charla de introducción de dbt Labs: qué problema resuelve y dónde encaja en el stack moderno.",
    "goal": "Terminas este paso cuando puedes explicarle a alguien por qué dbt no es solo \"SQL en archivos\".",
    "cert": "",
    "i": "",
    "u": "https://www.youtube.com/watch?v=M8oi7nSaWps",
    "boss": false,
    "wins": [
     "Entender qué es analytics engineering y por qué apareció el rol",
     "Ver dónde encaja dbt entre el warehouse y el reporte",
     "Saber la diferencia entre dbt Core y la plataforma antes de instalar nada"
    ]
   },
   {
    "id": "d02",
    "t": "dbt Fundamentals",
    "min": 360,
    "act": 1,
    "time": "6 horas",
    "sum": "El curso oficial y gratuito de dbt Labs. Modelos, fuentes, tests y documentación, con ejercicios.",
    "goal": "Terminas este paso cuando escribes un modelo, lo referencias desde otro y el linaje se dibuja solo.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/dbt-fundamentals",
    "boss": true,
    "wins": [
     "Modelos y la función ref, que es el corazón de dbt",
     "Fuentes declaradas, para que el linaje empiece en la tabla cruda",
     "Los primeros tests y la documentación que se genera sola"
    ]
   },
   {
    "id": "d03",
    "t": "Tu primer proyecto, paso a paso",
    "min": 120,
    "act": 2,
    "time": "2 horas",
    "sum": "Las guías oficiales: crear el proyecto, conectarlo a tu warehouse y correr el primer modelo.",
    "goal": "Terminas este paso cuando tienes un proyecto propio corriendo contra tu warehouse.",
    "cert": "",
    "i": "",
    "u": "https://docs.getdbt.com/guides?version=2",
    "boss": false,
    "wins": [
     "Conectar dbt a Snowflake, BigQuery, Databricks o Redshift sin adivinar",
     "Entender la estructura de carpetas y el archivo de configuración",
     "Correr, ver el resultado y saber dónde mirar cuando falla"
    ]
   },
   {
    "id": "d04",
    "t": "Jaffle Shop, el proyecto de práctica",
    "min": 180,
    "act": 2,
    "time": "3 horas",
    "sum": "El proyecto de ejemplo oficial de dbt Labs. Datos de una tienda ficticia para romper y arreglar sin miedo.",
    "goal": "Terminas este paso cuando modificas sus modelos y entiendes qué se rompe aguas abajo.",
    "cert": "",
    "i": "",
    "u": "https://github.com/dbt-labs/jaffle-shop",
    "boss": false,
    "wins": [
     "Leer un proyecto ajeno bien armado, que enseña más que empezar de cero",
     "Ver cómo se separan las capas de staging y de marts",
     "Tener un lugar donde probar cosas sin tocar nada real"
    ]
   },
   {
    "id": "d05",
    "t": "Jaffle Shop con DuckDB, todo local",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "La misma práctica sin cuenta en ningún warehouse: DuckDB corre en tu máquina.",
    "goal": "Terminas este paso cuando puedes practicar dbt Core sin depender de una cuenta en la nube.",
    "cert": "",
    "i": "",
    "u": "https://github.com/dbt-labs/jaffle_shop_duckdb",
    "boss": false,
    "wins": [
     "Un entorno local que arranca en minutos y no cuesta nada",
     "Practicar dbt Core, que es la versión que usan la mayoría de los equipos",
     "Poder experimentar sin miedo a la factura"
    ]
   },
   {
    "id": "d06",
    "t": "Curso intensivo de dbt Core",
    "min": 180,
    "act": 2,
    "time": "3 horas",
    "sum": "Recorrido práctico de punta a punta: instalación, modelos, materializaciones, tests y documentación.",
    "goal": "Terminas este paso cuando armas un proyecto entero sin seguir un tutorial.",
    "cert": "",
    "i": "",
    "u": "https://www.youtube.com/watch?v=toSAAgLUHuk",
    "boss": false,
    "wins": [
     "Ver a alguien resolver los problemas de instalación que te van a pasar a ti",
     "Las materializaciones explicadas con el proyecto corriendo delante",
     "Tests y documentación aplicados, no solo nombrados"
    ]
   },
   {
    "id": "d16",
    "t": "Git, lo justo para dbt",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "Curso oficial gratuito. Ramas, commits y pull requests, que es como se trabaja en dbt apenas hay alguien más en el proyecto.",
    "goal": "Terminas este paso cuando abres un pull request con un modelo nuevo y alguien te lo revisa.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/git-fundamentals",
    "boss": false,
    "wins": [
     "Ramas y pull requests, que es el flujo de trabajo de dbt",
     "Resolver un conflicto sin romper lo que ya andaba",
     "Por qué el entorno de desarrollo es tuyo y el de producción no"
    ]
   },
   {
    "id": "d07",
    "t": "Cómo se estructura un proyecto de verdad",
    "min": 240,
    "act": 3,
    "time": "4 horas",
    "sum": "La guía oficial de buenas prácticas: capas, convenciones de nombres y cuándo materializar cada cosa.",
    "goal": "Terminas este paso cuando puedes justificar por qué cada modelo está donde está.",
    "cert": "",
    "i": "",
    "u": "https://docs.getdbt.com/best-practices?version=2",
    "boss": true,
    "wins": [
     "Las capas staging, intermediate y marts, y qué va en cada una",
     "Convenciones de nombres que hacen que otro entienda tu proyecto",
     "Cuándo conviene vista, tabla o incremental, y por qué"
    ]
   },
   {
    "id": "d17",
    "t": "Refactorizar SQL heredado",
    "min": 180,
    "act": 3,
    "time": "3 horas",
    "sum": "Curso oficial gratuito con proyecto de práctica. Tomar una consulta larga que ya existe y partirla en modelos que se entienden solos.",
    "goal": "Terminas este paso cuando conviertes una consulta de trescientas líneas en modelos con nombre propio.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/refactoring-sql-for-modularity",
    "boss": false,
    "wins": [
     "El método para partir SQL viejo sin cambiar el resultado",
     "Comparar la salida vieja y la nueva, que es lo que da confianza",
     "Una consulta y un dataset de práctica para hacerlo tú"
    ]
   },
   {
    "id": "d08",
    "t": "Materializaciones",
    "min": 120,
    "act": 3,
    "time": "2 horas",
    "sum": "Curso oficial gratuito. Vista, tabla, incremental y efímera: qué hace cada una en el warehouse.",
    "goal": "Terminas este paso cuando eliges la materialización mirando el costo y la frescura, no por costumbre.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/materializations-fundamentals",
    "boss": false,
    "wins": [
     "Qué SQL genera dbt detrás de cada materialización",
     "Por qué una vista es gratis de construir y cara de consultar",
     "Cuándo una tabla deja de alcanzar"
    ]
   },
   {
    "id": "d09",
    "t": "Testing a fondo",
    "min": 180,
    "act": 3,
    "time": "3 horas",
    "sum": "Curso oficial gratuito. Tests genéricos, singulares y personalizados, y qué conviene testear.",
    "goal": "Terminas este paso cuando tus tests fallan por las razones correctas y no por ruido.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/advanced-testing",
    "boss": false,
    "wins": [
     "La diferencia entre un test genérico y uno singular",
     "Escribir tus propios tests como macros reutilizables",
     "Qué testear en cada capa: mucho arriba, poco abajo"
    ]
   },
   {
    "id": "d19",
    "t": "Unit tests",
    "min": 60,
    "act": 3,
    "time": "1 h 30 min",
    "sum": "Curso oficial gratuito. Distinto de los data tests: acá pruebas la lógica del modelo con datos que inventas, sin esperar a que corra sobre el warehouse.",
    "goal": "Terminas este paso cuando una regla rara del negocio tiene su test y no se rompe en silencio.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/unit-testing",
    "boss": false,
    "wins": [
     "Probar la lógica con datos de mentira, en segundos",
     "La diferencia entre un data test y un unit test",
     "Dónde poner cada uno para no probar dos veces lo mismo"
    ]
   },
   {
    "id": "d10",
    "t": "Jinja, macros y paquetes",
    "min": 180,
    "act": 3,
    "time": "3 horas",
    "sum": "Curso oficial gratuito. Dejar de repetir SQL y aprovechar lo que ya escribió la comunidad.",
    "goal": "Terminas este paso cuando reemplazas SQL repetido por una macro y el proyecto se achica.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/jinja-macros-and-packages",
    "boss": false,
    "wins": [
     "Jinja, que es lo que convierte a dbt en algo más que archivos .sql",
     "Escribir una macro propia y usarla en varios modelos",
     "dbt-utils y los paquetes que resuelven lo que ya está resuelto"
    ]
   },
   {
    "id": "d18",
    "t": "Seeds y analyses",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "Curso oficial gratuito. Dos cosas que dbt tiene y casi nadie usa: cargar CSV chicos como tablas versionadas, y guardar consultas de análisis que no son modelos.",
    "goal": "Terminas este paso cuando dejas de tener el CSV de mapeos suelto en el escritorio de alguien.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/analyses-and-seeds",
    "boss": false,
    "wins": [
     "Seeds para las tablas chicas que hoy viven en un Excel",
     "Analyses para las consultas que no van a producción",
     "Cuándo algo es un seed y cuándo tiene que ser una tabla de verdad"
    ]
   },
   {
    "id": "d11",
    "t": "Modelos incrementales",
    "min": 120,
    "act": 3,
    "time": "2 horas",
    "sum": "Curso oficial gratuito. Procesar solo lo nuevo en vez de reconstruir la tabla entera.",
    "goal": "Terminas este paso cuando un modelo que tardaba una hora corre en minutos.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/incremental-models",
    "boss": false,
    "wins": [
     "La estrategia incremental y la clave única que la sostiene",
     "Qué pasa con los datos que llegan tarde",
     "Cuándo conviene reconstruir todo igual"
    ]
   },
   {
    "id": "d12",
    "t": "Un proyecto de verdad, con el Zoomcamp",
    "min": 480,
    "act": 4,
    "time": "8 horas",
    "sum": "El módulo de analytics engineering del Data Engineering Zoomcamp: dbt dentro de un pipeline completo.",
    "goal": "Terminas este paso cuando tienes un proyecto tuyo, con datos reales, que podrías mostrar en una entrevista.",
    "cert": "",
    "i": "",
    "u": "https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/README.md",
    "boss": true,
    "wins": [
     "dbt dentro de un pipeline completo, no aislado",
     "Modelado dimensional sobre datos que no son de juguete",
     "Un proyecto terminado para el portfolio"
    ]
   },
   {
    "id": "d20",
    "t": "Despliegue a fondo",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "Curso oficial gratuito. Ambientes, corridas programadas y CI: que lo que se mergea corra solo y que lo que falla avise.",
    "goal": "Terminas este paso cuando un merge dispara la corrida y no tienes que apretar nada.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/advanced-deployment",
    "boss": false,
    "wins": [
     "Separar desarrollo de producción de verdad, no de palabra",
     "CI que corre los modelos que cambiaron y no todos",
     "Que un fallo te llegue antes que al que usa el reporte"
    ]
   },
   {
    "id": "d13",
    "t": "Snapshots",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "Curso oficial gratuito. Guardar la historia de algo que cambia: es el SCD tipo 2 de dbt.",
    "goal": "Terminas este paso cuando puedes reconstruir cómo era una dimensión en cualquier fecha pasada.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/snapshots",
    "boss": false,
    "wins": [
     "Por qué una tabla que se pisa pierde información que después hace falta",
     "Las dos estrategias, por timestamp y por columnas",
     "Cuándo un snapshot es la respuesta y cuándo es de más"
    ]
   },
   {
    "id": "d21",
    "t": "Exposures",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "Curso oficial gratuito. Declarar quién consume tus modelos -un dashboard, un notebook, una API- para que el lineage llegue hasta el final.",
    "goal": "Terminas este paso cuando sabes qué reporte se rompe antes de tocar un modelo.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/exposures",
    "boss": false,
    "wins": [
     "Saber a quién afecta un cambio antes de hacerlo",
     "El lineage completo, del origen al dashboard",
     "Documentación que se actualiza sola"
    ]
   },
   {
    "id": "d14",
    "t": "Semantic Layer",
    "min": 240,
    "act": 4,
    "time": "4 horas",
    "sum": "Definir métricas una sola vez para que todas las herramientas de reporte den el mismo número.",
    "goal": "Terminas este paso cuando entiendes por qué una métrica definida en tres dashboards da tres resultados.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/semantic-layer",
    "boss": false,
    "wins": [
     "Definir una métrica en un lugar y consumirla desde varias herramientas",
     "El problema real que resuelve: que ventas y finanzas dejen de discutir números",
     "Cuándo vale la pena y cuándo es infraestructura de más"
    ]
   },
   {
    "id": "d22",
    "t": "dbt Mesh",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "Curso oficial gratuito. Varios proyectos de dbt que se referencian entre sí, con contratos y versiones, para cuando un repo solo ya no alcanza.",
    "goal": "Terminas este paso cuando dos equipos comparten modelos sin pisarse.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/dbt-mesh",
    "boss": false,
    "wins": [
     "Contratos de modelo: prometer una forma y cumplirla",
     "Versionar un modelo para no romperle el trabajo a otro equipo",
     "Cuándo conviene partir y cuándo es complicarse al pedo"
    ]
   },
   {
    "id": "d23",
    "t": "dbt sobre Apache Iceberg",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Curso oficial gratuito. El formato de tabla abierto que están adoptando los warehouses, y cómo dbt materializa sobre él.",
    "goal": "Terminas este paso cuando entiendes qué cambia y qué no al materializar sobre Iceberg.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/dbt-and-apache-iceberg",
    "boss": false,
    "wins": [
     "Qué resuelve Iceberg y por qué aparece en todas las ofertas",
     "Materializar sobre Iceberg desde dbt",
     "Dónde conviene y dónde es una vuelta de más"
    ]
   },
   {
    "id": "d15",
    "t": "Prepararte para la certificación",
    "min": 90,
    "act": 4,
    "time": "a tu ritmo",
    "sum": "El camino oficial de dbt Labs hacia la certificación de developer, con todo lo que hay que repasar.",
    "goal": "Terminas este paso cuando rindes, o cuando decides que no te hace falta el papel.",
    "cert": "Prepara la certificación de dbt Labs",
    "i": "",
    "u": "https://learn.getdbt.com/learning-paths/dbt-certified-developer",
    "boss": false,
    "wins": [
     "Ver qué te falta contra el temario oficial",
     "Repasar lo que ya hiciste con la mirada del examen",
     "Decidir con información si la certificación te sirve"
    ]
   }
  ],
  "nivel": "Con SQL sabido",
  "nivelN": 1
 },
 {
  "archivo": "bigdata.html",
  "clave": "bigdata",
  "nombre": "Big Data",
  "actos": [
   "El panorama",
   "Hadoop",
   "Spark",
   "Spark para analítica",
   "Scala",
   "Operar el clúster"
  ],
  "pasos": [
   {
    "id": "b01",
    "t": "Big Data 101",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "El panorama: qué se considera Big Data, de dónde sale y por qué hizo falta otra forma de procesarlo.",
    "goal": "Terminas este curso cuando puedes usar el vocabulario sin repetir titulares.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/what-is-big-data",
    "boss": false,
    "wins": [
     "Las famosas uves, y cuáles importan de verdad",
     "Por qué una base tradicional deja de alcanzar",
     "Dónde encaja Hadoop en todo esto"
    ]
   },
   {
    "id": "b02",
    "t": "Hadoop 101",
    "min": 1200,
    "act": 2,
    "time": "20 horas",
    "sum": "El curso más largo de la ruta y el que sostiene todo lo demás: HDFS, el clúster y el procesamiento distribuido.",
    "goal": "Terminas este curso cuando entiendes qué pasa cuando un archivo se parte en bloques y se replica.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/introduction-to-hadoop",
    "boss": true,
    "wins": [
     "HDFS: cómo se guarda un archivo que no entra en una máquina",
     "Qué hace cada pieza del clúster",
     "Correr un trabajo distribuido y ver dónde mirar cuando falla"
    ]
   },
   {
    "id": "b03",
    "t": "MapReduce y YARN",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "El modelo de procesamiento original de Hadoop y el gestor de recursos que lo reemplazó como capa de control.",
    "goal": "Terminas este curso cuando puedes explicar qué hace un map, qué hace un reduce y quién reparte el trabajo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/mapreduce-and-yarn",
    "boss": false,
    "wins": [
     "El modelo map y reduce, que es la idea detrás de casi todo lo distribuido",
     "Qué problema vino a resolver YARN",
     "Por qué Spark después ganó"
    ]
   },
   {
    "id": "b04",
    "t": "Moving Data into Hadoop",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "Cómo entra el dato: comandos del shell, Sqoop desde bases relacionales y Flume para flujos.",
    "goal": "Terminas este curso cuando puedes traer una tabla de una base relacional al clúster.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/flume-sqoop-moving-data-into-hadoop",
    "boss": false,
    "wins": [
     "Sqoop, que es el puente con las bases de siempre",
     "Flume para datos que llegan continuamente",
     "Cuándo alcanza con un comando y cuándo hace falta una herramienta"
    ]
   },
   {
    "id": "b05",
    "t": "Kafka para pipelines de datos",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "Productores, consumidores, tópicos y brokers: la pieza que hoy mueve los datos en casi cualquier arquitectura.",
    "goal": "Terminas este curso cuando entiendes por qué un log distribuido resuelve el acople entre sistemas.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/simplifying-data-pipelines-with-apache-kafka",
    "boss": false,
    "wins": [
     "El vocabulario de Kafka, que aparece en toda entrevista de datos",
     "Por qué desacoplar productor y consumidor cambia todo",
     "Dónde encaja Kafka frente a Sqoop y Flume"
    ]
   },
   {
    "id": "b06",
    "t": "Hive: SQL sobre Hadoop",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "Consultar el clúster con SQL en vez de escribir código distribuido a mano.",
    "goal": "Terminas este curso cuando escribes una consulta sobre datos que viven en HDFS.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/accessing-hadoop-data-using-hive",
    "boss": false,
    "wins": [
     "Por qué poner SQL encima de Hadoop cambió quién podía usarlo",
     "Cómo se traduce una consulta a trabajo distribuido",
     "Particiones, que es donde se gana o se pierde el tiempo"
    ]
   },
   {
    "id": "b07",
    "t": "Spark Fundamentals I",
    "min": 240,
    "act": 3,
    "time": "4 horas",
    "sum": "Los conceptos centrales de Spark: RDDs, transformaciones, acciones y por qué es más rápido que MapReduce.",
    "goal": "Terminas este curso cuando entiendes qué significa que una transformación sea perezosa.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/what-is-spark",
    "boss": true,
    "wins": [
     "RDDs y el grafo de ejecución que Spark arma antes de correr nada",
     "Transformaciones contra acciones, que es la confusión número uno",
     "Por qué mantener los datos en memoria cambia el orden de magnitud"
    ]
   },
   {
    "id": "b08",
    "t": "Spark Fundamentals II",
    "min": 300,
    "act": 3,
    "time": "5 horas",
    "sum": "El siguiente escalón: operaciones sobre RDDs, particionado y cómo no arruinar el rendimiento sin darte cuenta.",
    "goal": "Terminas este curso cuando sabes por qué una operación cuesta un shuffle y otra no.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/spark-rdd",
    "boss": false,
    "wins": [
     "El shuffle, que es de donde sale casi todo el tiempo perdido",
     "Particionado y por qué importa dónde vive cada dato",
     "Persistencia y caché, y cuándo valen la pena"
    ]
   },
   {
    "id": "b09",
    "t": "Spark MLlib",
    "min": 300,
    "act": 4,
    "time": "1 semana",
    "sum": "La biblioteca de machine learning de Spark: clasificación, regresión, clustering y pipelines.",
    "goal": "Terminas este curso cuando entrenas un modelo sobre datos que no entran en una máquina.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/spark-mllib",
    "boss": false,
    "wins": [
     "Pipelines de ML sobre datos distribuidos",
     "Los algoritmos que trae y cuándo alcanzan",
     "Búsqueda de hiperparámetros aprovechando el clúster"
    ]
   },
   {
    "id": "b10",
    "t": "GraphX",
    "min": 180,
    "act": 4,
    "time": "3 horas",
    "sum": "Representar los datos como nodos y aristas, y correr algoritmos de grafos en paralelo.",
    "goal": "Terminas este curso cuando reconoces un problema de grafos disfrazado de tabla.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/spark-graphx",
    "boss": false,
    "wins": [
     "Cuándo un problema es de grafos y conviene tratarlo así",
     "Los operadores básicos y los algoritmos que ya vienen",
     "Casos reales: recomendación, fraude, linaje"
    ]
   },
   {
    "id": "b11",
    "t": "Spark desde R",
    "min": 180,
    "act": 4,
    "time": "3 horas",
    "sum": "SparkR: la misma potencia distribuida con la sintaxis de data frames que ya conoce quien usa R.",
    "goal": "Terminas este curso cuando corres un análisis en R sobre datos que no entrarían en tu memoria.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/analyzing-big-data-in-r-using-apache-spark",
    "boss": false,
    "wins": [
     "El puente entre R y el clúster",
     "Qué se puede y qué no desde SparkR",
     "Cuándo conviene R y cuándo Python o Scala"
    ]
   },
   {
    "id": "b12",
    "t": "Scala 101",
    "min": 360,
    "act": 5,
    "time": "6 horas",
    "sum": "El lenguaje en el que está escrito Spark: orientado a objetos y funcional al mismo tiempo, y compatible con Java.",
    "goal": "Terminas este curso cuando lees código Scala sin sentir que es otro idioma.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/introduction-to-scala",
    "boss": true,
    "wins": [
     "Programación funcional aplicada, no en abstracto",
     "Por qué Spark eligió Scala",
     "Colecciones e inmutabilidad, que es el corazón del lenguaje"
    ]
   },
   {
    "id": "b13",
    "t": "Spark con Scala",
    "min": 480,
    "act": 5,
    "time": "8 horas",
    "sum": "Spark visto desde su propio lenguaje: construir aplicaciones, RDDs y DataFrames con la API nativa.",
    "goal": "Terminas este curso cuando escribes una aplicación de Spark y la corres en un clúster.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/spark-overview-scala-analytics",
    "boss": false,
    "wins": [
     "La API de Spark como fue pensada originalmente",
     "DataFrames y cuándo convienen sobre RDDs",
     "Empaquetar y correr una aplicación de verdad"
    ]
   },
   {
    "id": "b14",
    "t": "Data Science con Scala",
    "min": 360,
    "act": 5,
    "time": "6 horas",
    "sum": "Los pipelines de machine learning de Spark desde Scala, con búsqueda de hiperparámetros sobre el clúster.",
    "goal": "Terminas este curso cuando ajustas un modelo aprovechando todo el clúster y sabes qué costó.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-science-scala",
    "boss": false,
    "wins": [
     "Pipelines de ML en la API nativa",
     "Ajuste de hiperparámetros distribuido",
     "Cerrar el círculo: Scala, Spark y modelos sobre Big Data"
    ]
   },
   {
    "id": "b15",
    "t": "Oozie",
    "min": 360,
    "act": 6,
    "time": "6 horas",
    "sum": "El programador de trabajos de Hadoop: encadenar pasos, ramificar según el resultado y correrlos en horario.",
    "goal": "Terminas este curso cuando armas un flujo con varios pasos y lo dejas corriendo solo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/controlling-hadoop-jobs-using-oozie",
    "boss": false,
    "wins": [
     "Un flujo de trabajo con dependencias entre pasos",
     "Bifurcaciones y uniones, para cuando el camino no es uno solo",
     "El coordinador, que es lo que lo hace correr sin ti"
    ]
   },
   {
    "id": "b16",
    "t": "ZooKeeper",
    "min": 240,
    "act": 6,
    "time": "4 horas",
    "sum": "Cómo se ponen de acuerdo las máquinas de un clúster: configuración compartida, nombres y quién manda.",
    "goal": "Terminas este curso cuando puedes explicar por qué un sistema distribuido necesita un árbitro.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/developing-distributed-applications-using-zookeeper",
    "boss": false,
    "wins": [
     "El problema de la coordinación, que aparece en todo lo distribuido",
     "Configuración que muchas máquinas leen igual",
     "Elección de líder, sin que quede nadie a medias"
    ]
   },
   {
    "id": "b17",
    "t": "Solr 101",
    "min": 180,
    "act": 6,
    "time": "3 horas",
    "sum": "Buscar de verdad dentro de lo que guardaste. El motor de búsqueda de Apache Lucene, servido y consultable.",
    "goal": "Terminas este curso cuando indexas un conjunto de documentos y los consultas por texto.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/solr",
    "boss": false,
    "wins": [
     "Qué es un índice invertido y por qué es rápido",
     "Indexar documentos y consultarlos",
     "Dónde conviene un buscador y dónde una consulta común"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "data-science.html",
  "clave": "data_science",
  "nombre": "Data Science",
  "actos": [
   "Qué es el oficio",
   "Con Python",
   "Con R",
   "Modelar"
  ],
  "pasos": [
   {
    "id": "s01",
    "t": "Data Science 101",
    "min": 660,
    "act": 1,
    "time": "11 horas",
    "sum": "Qué hace alguien de data science, contado por gente que lo hace. El curso más visto de CognitiveClass.",
    "goal": "Terminas este curso cuando puedes explicar el oficio sin recurrir a la palabra algoritmo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-science-101",
    "boss": true,
    "wins": [
     "Qué problemas resuelve y cuáles no",
     "En qué se diferencia de análisis y de ingeniería de datos",
     "Cómo entra alguien al campo, sin la versión de los avisos"
    ]
   },
   {
    "id": "s02",
    "t": "Data Science Methodology",
    "min": 240,
    "act": 1,
    "time": "4 horas",
    "sum": "El método: del problema de negocio a un modelo desplegado, con las diez etapas y qué se decide en cada una.",
    "goal": "Terminas este curso cuando puedes decir en qué etapa está un proyecto y qué falta para la siguiente.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-science-methodology-2",
    "boss": false,
    "wins": [
     "Empezar por la pregunta de negocio y no por el dato",
     "Preparación y modelado como etapas con criterio propio",
     "Evaluación y despliegue, que es donde casi todo se cae"
    ]
   },
   {
    "id": "s03",
    "t": "Data Science Tools",
    "min": 900,
    "act": 1,
    "time": "15 horas",
    "sum": "Las herramientas: notebooks, entornos, control de versiones y por qué el ecosistema se ve así.",
    "goal": "Terminas este curso cuando armas tu entorno y sabes qué hace cada pieza.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-science-hands-open-source-tools-2",
    "boss": false,
    "wins": [
     "Jupyter y los notebooks, con sus límites",
     "Los entornos y por qué reproducir importa",
     "El panorama de bibliotecas sin tener que probarlas todas"
    ]
   },
   {
    "id": "s04",
    "t": "Python para data science",
    "min": 1080,
    "act": 2,
    "time": "18 horas",
    "sum": "El lenguaje desde cero, orientado al análisis: estructuras, archivos y las bibliotecas con las que se trabaja.",
    "goal": "Terminas este curso cuando escribes tus propios scripts sin copiar el esqueleto de otro lado.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/python-for-data-science",
    "boss": true,
    "wins": [
     "Python de verdad, no solo la sintaxis",
     "Leer y escribir archivos y datos",
     "numpy y pandas, que es donde vive el trabajo"
    ]
   },
   {
    "id": "s05",
    "t": "Análisis de datos con Python",
    "min": 900,
    "act": 2,
    "time": "15 horas",
    "sum": "El trabajo sucio y el que más tiempo lleva: limpiar, cruzar, resumir y recién ahí sacar una conclusión.",
    "goal": "Terminas este curso cuando tomas un conjunto de datos crudo y llegas a una respuesta defendible.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-analysis-python",
    "boss": false,
    "wins": [
     "Limpieza y datos faltantes, que nunca son pocos",
     "Agrupar, cruzar y resumir con pandas",
     "Un primer modelo y qué tan lejos está de servir"
    ]
   },
   {
    "id": "s06",
    "t": "Visualización con Python",
    "min": 600,
    "act": 2,
    "time": "10 horas",
    "sum": "Mostrar el resultado de manera que se entienda sin que estés al lado explicándolo.",
    "goal": "Terminas este curso cuando eliges el gráfico por el dato que tienes, y no por el que sabes hacer.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-visualization-python",
    "boss": false,
    "wins": [
     "Qué gráfico corresponde a qué pregunta",
     "matplotlib y seaborn sin pelearse con ellos",
     "Mapas y gráficos interactivos"
    ]
   },
   {
    "id": "s11",
    "t": "Análisis exploratorio, en la práctica",
    "min": 45,
    "act": 2,
    "time": "45 min",
    "sum": "El proyecto guiado que cierra la parte de Python: mirar los datos antes de modelarlos, que es lo que casi nadie hace.",
    "goal": "Terminas este proyecto cuando detectas un problema en los datos antes de entrenar nada.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/exploratory-data-analysis-eda-for-data-science-and-ml",
    "boss": false,
    "wins": [
     "Calidad de datos y valores faltantes",
     "Los gráficos que sí dicen algo",
     "Primeras variables derivadas"
    ]
   },
   {
    "id": "s12",
    "t": "Métodos de clasificación",
    "min": 360,
    "act": 2,
    "time": "6 horas",
    "sum": "De la regresión logística a SVM y árboles, con scikit-learn y seaborn sobre problemas reales. Cierra Data Science Essentials.",
    "goal": "Terminas este curso cuando eliges el clasificador por el problema y puedes defender la elección.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/classification-methods-problems-and-solutions",
    "boss": false,
    "wins": [
     "Regresión logística, KNN y SVM, con sus límites",
     "Árboles y ensambles, que suelen ganar",
     "El badge de Data Science Essentials, al cerrar los cuatro"
    ]
   },
   {
    "id": "s07",
    "t": "R para data science",
    "min": 360,
    "act": 3,
    "time": "6 horas",
    "sum": "El otro lenguaje del oficio, el que viene de la estadística y sigue siendo el de la academia.",
    "goal": "Terminas este curso cuando cargas datos en R y los manipulas sin extrañar pandas.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/r-101",
    "boss": false,
    "wins": [
     "La sintaxis de R, que no se parece a nada más",
     "Data frames, que acá nacieron",
     "Cuándo conviene R y cuándo Python"
    ]
   },
   {
    "id": "s08",
    "t": "Visualización con R",
    "min": 360,
    "act": 3,
    "time": "6 horas",
    "sum": "ggplot2 y la gramática de gráficos: armar un gráfico por capas en vez de elegirlo de una lista.",
    "goal": "Terminas este curso cuando construyes un gráfico capa por capa y sabes qué hace cada una.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/data-visualization-with-r",
    "boss": false,
    "wins": [
     "La gramática de gráficos, que es otra forma de pensarlo",
     "ggplot2, que es la razón por la que mucha gente usa R",
     "Gráficos listos para publicar"
    ]
   },
   {
    "id": "s09",
    "t": "Modelado predictivo",
    "min": 360,
    "act": 4,
    "time": "6 horas",
    "sum": "Los fundamentos antes de las bibliotecas: qué es predecir, con qué se mide y por qué un modelo bueno en papel falla.",
    "goal": "Terminas este curso cuando puedes decir si un modelo sirve mirando algo más que el porcentaje de acierto.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/predictive-modeling-fundamentals",
    "boss": false,
    "wins": [
     "Entrenar y evaluar sin engañarse solo",
     "Sobreajuste, que es el error más caro",
     "Qué métrica corresponde a qué problema"
    ]
   },
   {
    "id": "s10",
    "t": "Machine learning con Python",
    "min": 1200,
    "act": 4,
    "time": "20 horas",
    "sum": "El curso largo del final: regresión, clasificación, agrupamiento y sistemas de recomendación con scikit-learn.",
    "goal": "Terminas este curso cuando eliges el algoritmo por el problema y puedes explicar la elección.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/machine-learning-with-python",
    "boss": true,
    "wins": [
     "Regresión y clasificación, con sus casos de uso reales",
     "Agrupamiento, cuando no hay respuesta correcta de antemano",
     "Un sistema de recomendación funcionando"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "arquitectura.html",
  "clave": "arquitectura",
  "nombre": "Arquitectura",
  "actos": [
   "Contenedores",
   "Sistemas reactivos",
   "Reactivos a fondo"
  ],
  "pasos": [
   {
    "id": "a01",
    "t": "Contenedores, Kubernetes y OpenShift",
    "min": 1080,
    "act": 1,
    "time": "18 horas",
    "sum": "Qué es un contenedor, en qué se diferencia de una máquina virtual, y cómo Kubernetes los orquesta.",
    "goal": "Terminas este curso cuando despliegas una aplicación en contenedores y entiendes qué hace el orquestador.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/kubernetes-course",
    "boss": true,
    "wins": [
     "Contenedores contra máquinas virtuales, con la diferencia real",
     "Docker y el ciclo de construir, publicar y correr",
     "Los objetos de Kubernetes y para qué está cada uno"
    ]
   },
   {
    "id": "a02",
    "t": "Microservicios con Istio",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "Cómo se comunican los microservicios en un clúster y qué agrega una malla de servicios.",
    "goal": "Terminas este curso cuando entiendes qué problema resuelve Istio que Kubernetes no resuelve solo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/get-started-with-microservices-istio-and-ibm-cloud-container-service",
    "boss": false,
    "wins": [
     "Qué es una malla de servicios y por qué apareció",
     "Enrutar tráfico entre versiones sin tocar el código",
     "Desplegar de a poco, que es el canario del mundo de contenedores"
    ]
   },
   {
    "id": "a03",
    "t": "Istio a fondo",
    "min": 300,
    "act": 1,
    "time": "1 día",
    "sum": "Control de tráfico, observabilidad y seguridad de la malla, con la práctica sobre un clúster real.",
    "goal": "Terminas este curso cuando puedes ver la salud de cada servicio y cortar el tráfico a uno sin desplegar nada.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/beyond-the-basics-istio-and-ibm-cloud-kubernetes-service",
    "boss": false,
    "wins": [
     "Observabilidad: ver qué servicio está rompiendo qué",
     "Seguridad entre servicios, que casi nadie configura",
     "Control fino del tráfico para pruebas y despliegues"
    ]
   },
   {
    "id": "a03a",
    "t": "AWS Application Networking Demonstrated",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "Una evaluación dentro de una cuenta de AWS de verdad: entregar la aplicación, optimizar su rendimiento y sostener la arquitectura que la aguanta.",
    "goal": "Terminas esto cuando resolviste el escenario y tienes la microcredencial en tu perfil.",
    "cert": "Microcredencial oficial de AWS",
    "i": "",
    "u": "https://skillbuilder.aws/learn/EM5GTXEQB6/aws-application-networking-demonstrated/GS9ZN623HY",
    "boss": true,
    "wins": [
     "Una credencial oficial de AWS, gratis desde abril de 2026",
     "Se rinde configurando y arreglando, no eligiendo opciones",
     "Entrega, rendimiento y arquitectura de aplicaciones"
    ]
   },
   {
    "id": "a07",
    "t": "Sistemas reactivos",
    "min": 300,
    "act": 2,
    "time": "5 horas",
    "sum": "De qué se habla cuando se dice reactivo: responder siempre, aguantar la falla y no bloquear esperando.",
    "goal": "Terminas este curso cuando puedes decir si un sistema es reactivo y por qué, sin repetir el manifiesto.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-introduction",
    "boss": true,
    "wins": [
     "Los cuatro rasgos, y cuál sostiene a los otros tres",
     "Por qué bloquear es caro cuando hay muchas máquinas",
     "Qué cambia respecto de una aplicación de una sola máquina"
    ]
   },
   {
    "id": "a08",
    "t": "Diseño guiado por el dominio",
    "min": 300,
    "act": 2,
    "time": "5 horas",
    "sum": "Dónde cortar el sistema. Contextos delimitados, lenguaje compartido y por qué el corte técnico suele ser el corte equivocado.",
    "goal": "Terminas este curso cuando puedes trazar los límites de un dominio y defender por dónde los pusiste.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-ddd",
    "boss": false,
    "wins": [
     "Contextos delimitados, que es de dónde salen los servicios",
     "Agregados y quién es dueño de qué dato",
     "El lenguaje del negocio dentro del código"
    ]
   },
   {
    "id": "a09",
    "t": "Microservicios reactivos",
    "min": 360,
    "act": 2,
    "time": "6 horas",
    "sum": "Los límites del dominio convertidos en servicios que se hablan sin quedarse esperando.",
    "goal": "Terminas este curso cuando un servicio sigue respondiendo aunque el de al lado esté caído.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-microservices",
    "boss": false,
    "wins": [
     "Aislamiento: que la falla de uno no sea la falla de todos",
     "Comunicación asincrónica entre servicios",
     "El estado, que es la parte difícil de repartir"
    ]
   },
   {
    "id": "a04",
    "t": "Sistemas escalables y el teorema CAP",
    "min": 360,
    "act": 3,
    "time": "6 horas",
    "sum": "Por qué en un sistema distribuido hay que elegir entre consistencia y disponibilidad, y qué implica cada elección.",
    "goal": "Terminas este curso cuando puedes decir qué eligió un sistema y qué perdió a cambio.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-building-scalable-systems",
    "boss": true,
    "wins": [
     "El teorema CAP explicado con consecuencias, no como trivia",
     "Las leyes de la escalabilidad y dónde está el techo",
     "Sharding y replicación, y qué rompe cada uno"
    ]
   },
   {
    "id": "a05",
    "t": "Mensajería distribuida",
    "min": 360,
    "act": 3,
    "time": "6 horas",
    "sum": "Los mensajes asincrónicos y sin bloqueo como base de un sistema reactivo, y qué garantiza cada modelo de entrega.",
    "goal": "Terminas este curso cuando eliges un modelo de entrega sabiendo qué duplicados vas a tener que manejar.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-dmp",
    "boss": false,
    "wins": [
     "Por qué asincrónico cambia el diseño entero, no solo el rendimiento",
     "Garantías de entrega y qué cuesta cada una",
     "El vínculo directo con Kafka y con los pipelines de datos"
    ]
   },
   {
    "id": "a06",
    "t": "CQRS y event sourcing",
    "min": 360,
    "act": 3,
    "time": "6 horas",
    "sum": "Separar el camino de escritura del de lectura, y guardar los hechos en vez del estado final.",
    "goal": "Terminas este curso cuando puedes decir qué gana y qué cuesta guardar eventos en lugar de estado.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reactive-architecture-cqrs",
    "boss": false,
    "wins": [
     "CQRS: por qué leer y escribir pueden querer modelos distintos",
     "Event sourcing y la historia completa como fuente de verdad",
     "El costo real: complejidad, consistencia eventual y migraciones"
    ]
   }
  ],
  "nivel": "Con experiencia",
  "nivelN": 3
 },
 {
  "archivo": "subir-nivel.html",
  "clave": "subirnivel",
  "nombre": "Subir de nivel",
  "actos": [
   "Respaldar dbt",
   "Orquestar de verdad",
   "Procesamiento distribuido",
   "Infraestructura como código",
   "Streaming"
  ],
  "pasos": [
   {
    "id": "x01",
    "t": "dbt Fundamentals",
    "min": 360,
    "act": 1,
    "time": "6 horas",
    "sum": "El curso oficial. Modelos, sources, tests y lineage: lo que convierte una carpeta de SQL en un proyecto.",
    "goal": "Terminas este curso cuando armas un proyecto de dbt de cero sin mirar un tutorial.",
    "cert": "Certificado de dbt Labs",
    "i": "",
    "u": "https://learn.getdbt.com/courses/dbt-fundamentals",
    "boss": true,
    "wins": [
     "Modelos y referencias, que es de donde sale el lineage",
     "Sources y tests, que es lo que evita el incidente del lunes",
     "El proyecto corriendo sobre tu propio warehouse"
    ]
   },
   {
    "id": "x02",
    "t": "Estructurar un proyecto real",
    "min": 240,
    "act": 1,
    "time": "4 horas",
    "sum": "La guía de dbt Labs sobre cómo se organiza un proyecto en capas: staging, intermedios y marts.",
    "goal": "Terminas este paso cuando defiendes por qué un modelo va en una capa y no en otra.",
    "cert": "",
    "i": "",
    "u": "https://docs.getdbt.com/best-practices?version=2",
    "boss": false,
    "wins": [
     "Staging, intermedios y marts, con el criterio de cada corte",
     "Convenciones de nombres que sobreviven al equipo",
     "Dónde poner la lógica de negocio para encontrarla después"
    ]
   },
   {
    "id": "x03",
    "t": "Materializaciones",
    "min": 120,
    "act": 1,
    "time": "2 horas",
    "sum": "Vista, tabla, incremental o efímero: qué cambia en costo y en tiempo según cuál elijas.",
    "goal": "Terminas este curso cuando eliges la materialización por el costo y puedes estimarlo.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/materializations-fundamentals",
    "boss": false,
    "wins": [
     "Las cuatro, con el caso donde conviene cada una",
     "Qué se recalcula y qué no en cada corrida",
     "El impacto en la factura, que en Snowflake se nota"
    ]
   },
   {
    "id": "x04",
    "t": "Testing a fondo",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "Más allá de not_null y unique: tests singulares, genéricos propios y paquetes de la comunidad.",
    "goal": "Terminas este curso cuando escribes un test que atrapa un error que ya te pasó.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/advanced-testing",
    "boss": false,
    "wins": [
     "Tests genéricos propios, reusables en todo el proyecto",
     "dbt-utils y dbt-expectations, para no reinventar",
     "Severidad y umbrales: cuándo frenar y cuándo avisar"
    ]
   },
   {
    "id": "x05",
    "t": "Jinja, macros y paquetes",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "Donde dbt deja de ser SQL con plantillas y pasa a ser código que genera SQL.",
    "goal": "Terminas este curso cuando escribes una macro que borra repetición real de tu proyecto.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/jinja-macros-and-packages",
    "boss": false,
    "wins": [
     "Jinja en dbt sin pelearse con la sintaxis",
     "Macros propias y cuándo son un exceso",
     "Paquetes: qué instalar y qué escribir tú"
    ]
   },
   {
    "id": "x06",
    "t": "Modelos incrementales",
    "min": 120,
    "act": 1,
    "time": "2 horas",
    "sum": "Procesar solo lo nuevo. Es la diferencia entre una corrida de tres minutos y una de tres horas.",
    "goal": "Terminas este curso cuando conviertes un modelo pesado en incremental sin perder datos.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/incremental-models",
    "boss": false,
    "wins": [
     "La estrategia incremental que corresponde a cada caso",
     "is_incremental y el filtro que define todo",
     "Cuándo hace falta reconstruir de cero"
    ]
   },
   {
    "id": "x07",
    "t": "Snapshots",
    "min": 120,
    "act": 1,
    "time": "2 horas",
    "sum": "SCD Tipo 2 resuelto por la herramienta. Si ya modelaste dimensiones que cambian, esto te va a resultar familiar.",
    "goal": "Terminas este curso cuando reemplazas una dimensión lenta hecha a mano por un snapshot.",
    "cert": "",
    "i": "",
    "u": "https://learn.getdbt.com/courses/snapshots",
    "boss": false,
    "wins": [
     "Snapshots como SCD Tipo 2, sin escribir el merge",
     "Las dos estrategias, timestamp y check",
     "Qué pasa cuando la fuente no tiene fecha de cambio"
    ]
   },
   {
    "id": "x08",
    "t": "Un proyecto de verdad, con el Zoomcamp",
    "min": 480,
    "act": 1,
    "time": "8 horas",
    "sum": "El módulo de analytics engineering del zoomcamp de DataTalksClub: dbt dentro de un pipeline completo, no en un tutorial.",
    "goal": "Terminas este paso cuando tienes un repositorio propio que alguien puede clonar y correr.",
    "cert": "",
    "i": "",
    "u": "https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/README.md",
    "boss": true,
    "wins": [
     "dbt como una pieza del pipeline y no como el pipeline",
     "El proyecto que se muestra en una entrevista",
     "Datos reales, con los problemas que traen"
    ]
   },
   {
    "id": "x09a",
    "t": "Los tutoriales oficiales de Airflow",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "La documentación del proyecto, que es de donde sale lo que después repiten los cursos. Cinco tutoriales que se hacen con Airflow corriendo al lado, no mirando.",
    "goal": "Terminas esto cuando tienes Airflow local y escribiste un pipeline leyendo la doc y no un video.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html",
    "boss": false,
    "wins": [
     "Airflow 101, tu primer workflow de punta a punta",
     "TaskFlow API, que es como se escriben los DAGs hoy",
     "Un pipeline de datos simple, armado por ti",
     "Object storage, que es por donde pasan los datos ahora",
     "Human-in-the-loop, para los pasos que aprueba una persona"
    ]
   },
   {
    "id": "x09",
    "t": "Airflow 101",
    "min": 150,
    "act": 2,
    "time": "2 horas y media",
    "sum": "Once módulos de Astronomer, la empresa que mantiene Airflow: conceptos, entorno local, la interfaz y tu primer DAG.",
    "goal": "Terminas este camino cuando tienes Airflow corriendo local y un DAG propio programado.",
    "cert": "Insignia de Astronomer",
    "i": "",
    "u": "https://academy.astronomer.io/path/airflow-101",
    "boss": false,
    "wins": [
     "Qué resuelve un orquestador y qué no",
     "Un DAG escrito por ti, corriendo en tu máquina",
     "Scheduling, XComs, sensores y conexiones"
    ]
   },
   {
    "id": "x10",
    "t": "DAG Authoring",
    "min": 135,
    "act": 2,
    "time": "2 horas y cuarto",
    "sum": "El camino oficial de preparación de la certificación: task mapping dinámico, DAGs dinámicos, TaskFlow API y TaskGroups.",
    "goal": "Terminas este camino cuando escribes DAGs que no se repiten y puedes rendir el examen.",
    "cert": "Prepara la certificación de Astronomer",
    "i": "",
    "u": "https://academy.astronomer.io/path/airflow-dag-authoring",
    "boss": true,
    "wins": [
     "Dynamic task mapping, para tareas que dependen del dato",
     "TaskFlow API, que es cómo se escribe hoy",
     "TaskGroups y branching, para DAGs que se leen"
    ]
   },
   {
    "id": "x11",
    "t": "Spark Fundamentals I",
    "min": 240,
    "act": 3,
    "time": "4 horas",
    "sum": "El salto: procesar algo que no entra en una máquina. RDDs, transformaciones y acciones.",
    "goal": "Terminas este curso cuando explicas por qué una operación dispara un shuffle y otra no.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/what-is-spark",
    "boss": false,
    "wins": [
     "Evaluación perezosa, que es toda la idea",
     "Transformaciones y acciones, con la diferencia clara",
     "Dónde se va el tiempo en un trabajo distribuido"
    ]
   },
   {
    "id": "x12",
    "t": "Spark Fundamentals II",
    "min": 300,
    "act": 3,
    "time": "5 horas",
    "sum": "DataFrames, Spark SQL y el ajuste de rendimiento: particionamiento, caching y joins.",
    "goal": "Terminas este curso cuando arreglas un trabajo lento mirando el plan y no probando al azar.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/spark-rdd",
    "boss": true,
    "wins": [
     "DataFrames y Spark SQL, que es la API que vas a usar",
     "Particionamiento y caching, con criterio",
     "Joins distribuidos y el broadcast que los salva"
    ]
   },
   {
    "id": "x13",
    "t": "Terraform sobre AWS",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "El tutorial oficial de HashiCorp: seis pasos para crear, cambiar y destruir infraestructura desde código.",
    "goal": "Terminas este paso cuando levantas y destruyes infraestructura sin tocar una consola.",
    "cert": "Prepara la Terraform Associate",
    "i": "",
    "u": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started",
    "boss": false,
    "wins": [
     "Providers, recursos y variables",
     "El state, que es donde se rompe todo al principio",
     "plan y apply, y por qué revisar el plan no es opcional"
    ]
   },
   {
    "id": "x13a",
    "t": "AWS Serverless Demonstrated",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Una evaluación dentro de una cuenta de AWS de verdad: Lambda, API Gateway, Step Functions y DynamoDB. No hay multiple choice, se configura y se arregla igual que en el trabajo.",
    "goal": "Terminas esto cuando resolviste el escenario y tienes la microcredencial en tu perfil.",
    "cert": "Microcredencial oficial de AWS",
    "i": "",
    "u": "https://skillbuilder.aws/learn/XV3B4RGA8Q/aws-serverless-demonstrated/BYD5SH8R5C",
    "boss": true,
    "wins": [
     "Una credencial oficial de AWS, gratis desde abril de 2026",
     "Se rinde haciendo, no eligiendo la opción correcta",
     "Lambda, API Gateway, Step Functions y DynamoDB"
    ]
   },
   {
    "id": "x13b",
    "t": "AWS Incident Response Demonstrated",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "La contracara de desplegar: encontrar, contener y arreglar un incidente de seguridad dentro de una cuenta de AWS de verdad. Lo que llega cuando lo que pusiste en producción se rompe y hay que responder.",
    "goal": "Terminas esto cuando contuviste el incidente y tienes la microcredencial en tu perfil.",
    "cert": "Microcredencial oficial de AWS",
    "i": "",
    "u": "https://skillbuilder.aws/learn/UQWKF19DT7/aws-incident-response-demonstrated/VH96JY5RJZ",
    "boss": true,
    "wins": [
     "Una credencial oficial de AWS, gratis desde abril de 2026",
     "Se rinde respondiendo a un incidente, no eligiendo opciones",
     "Detectar, contener y remediar los incidentes más comunes"
    ]
   },
   {
    "id": "x14",
    "t": "Kafka para pipelines",
    "min": 240,
    "act": 5,
    "time": "4 horas",
    "sum": "Salir del batch: topics, particiones, productores y consumidores, y qué garantiza cada configuración.",
    "goal": "Terminas este curso cuando puedes decir qué se pierde y qué se duplica en cada modo de entrega.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/simplifying-data-pipelines-with-apache-kafka",
    "boss": false,
    "wins": [
     "Topics y particiones, que es de donde sale la escala",
     "Grupos de consumidores y offsets",
     "Las garantías de entrega, que nunca son gratis"
    ]
   }
  ],
  "nivel": "Con experiencia",
  "nivelN": 3
 },
 {
  "archivo": "ai-fundamentos.html",
  "clave": "aifund",
  "nombre": "AI: fundamentos",
  "actos": [
   "Fundamentals of AI",
   "Machine Learning Basics",
   "Machine Learning with Python"
  ],
  "pasos": [
   {
    "id": "f01",
    "t": "Introducing AI",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "El panorama, sin jerga: qué es AI, dónde ya se usa y qué se puede esperar de ella.",
    "goal": "Terminas este curso cuando puedes separar lo que la AI hace de lo que se le atribuye.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/introducing-ai-09f5c2a8-b79c-443d-b09a-8227c40c2108",
    "boss": false,
    "wins": [
     "De dónde viene el campo y por qué explotó ahora",
     "Dónde ya está funcionando, con casos concretos",
     "Qué no hace, que es la mitad de entenderlo"
    ]
   },
   {
    "id": "f02",
    "t": "AI Concepts",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "El vocabulario: machine learning, deep learning y redes neuronales, y cómo se contienen entre sí.",
    "goal": "Terminas este curso cuando usas los tres términos sin mezclarlos.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/ai-concepts-ba67406f-972f-40ec-bd11-4c45a979f57d",
    "boss": false,
    "wins": [
     "Machine learning dentro de AI, deep learning dentro de machine learning",
     "Qué es una red neuronal, en una frase que se entienda",
     "NLP, visión y reconocimiento de voz: qué problema resuelve cada uno"
    ]
   },
   {
    "id": "f03",
    "t": "AI Ethics",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "Sesgo, privacidad, regulación y quién responde cuando el modelo se equivoca. Cierra la primera credencial.",
    "goal": "Terminas este curso cuando puedes decir por qué un modelo con buen puntaje igual puede ser inaceptable.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/ai-ethics-2f459a4d-fd9a-4fc6-aba8-e4f66cf33220",
    "boss": true,
    "wins": [
     "De dónde sale el sesgo, que casi siempre es de los datos",
     "Qué exige la regulación y a quién",
     "El badge de Fundamentals of AI, que se reclama al cerrar los tres"
    ]
   },
   {
    "id": "f04",
    "t": "Introducción a machine learning",
    "min": 180,
    "act": 2,
    "time": "3 horas",
    "sum": "El primer curso con código: qué es entrenar un modelo, con qué datos y cómo se mide si anda.",
    "goal": "Terminas este curso cuando entrenas un modelo y sabes leer si sirve o no.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/a-quick-introduction-to-machine-learning",
    "boss": false,
    "wins": [
     "Aprendizaje supervisado y no supervisado, con la diferencia clara",
     "Partir los datos en entrenamiento y prueba, y por qué",
     "Las métricas básicas y qué esconde cada una"
    ]
   },
   {
    "id": "f05",
    "t": "Refuerzo y deep learning, lo esencial",
    "min": 120,
    "act": 2,
    "time": "2 horas",
    "sum": "Los dos paradigmas que no entraron en el curso anterior: aprender por recompensa y aprender con redes.",
    "goal": "Terminas este curso cuando puedes plantear un problema como estado, acción y recompensa.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reinforcement-learning-and-deep-learning-essentials",
    "boss": false,
    "wins": [
     "Agente, entorno, estado y recompensa",
     "El dilema entre explorar y explotar",
     "Qué agrega una red neuronal sobre un modelo común"
    ]
   },
   {
    "id": "f06",
    "t": "Clasificar flores y tumores",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "El primer proyecto guiado: un clasificador entrenado por ti sobre dos conjuntos clásicos, en el navegador.",
    "goal": "Terminas este proyecto cuando tu clasificador predice sobre datos que no vio antes.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/precise-predictions-classification-for-flower-and-tumors",
    "boss": false,
    "wins": [
     "Un clasificador funcionando de punta a punta",
     "Qué mirar cuando acierta poco",
     "Sin instalar nada: corre en el navegador"
    ]
   },
   {
    "id": "f07",
    "t": "Predecir consumo y precios",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "El mismo ejercicio del otro lado: en vez de una categoría, un número. Consumo de un auto y precio de un diamante.",
    "goal": "Terminas este proyecto cuando puedes decir en qué se diferencia de clasificar.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/predictions-regression-for-car-mileage-and-diamond-price",
    "boss": false,
    "wins": [
     "Regresión, con dos casos que se entienden solos",
     "Cómo se mide el error cuando la respuesta es un número",
     "Cuándo el problema es de regresión y cuándo no"
    ]
   },
   {
    "id": "f08",
    "t": "Agrupar clientes con KMeans",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "El tercero, y el que cierra la credencial: agrupar sin etiquetas, que es de lo que se trata el no supervisado.",
    "goal": "Terminas este proyecto cuando explicas qué separa a un grupo del otro.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/customer-clustering-with-kmeans-to-boost-business-strategy",
    "boss": true,
    "wins": [
     "Agrupamiento sobre datos de clientes reales",
     "Elegir cuántos grupos, que es la parte difícil",
     "El badge de Machine Learning Basics, al cerrar los cinco"
    ]
   },
   {
    "id": "f09",
    "t": "Machine learning con Python",
    "min": 1200,
    "act": 3,
    "time": "20 horas",
    "sum": "El curso largo: regresión, clasificación, agrupamiento y sistemas de recomendación con scikit-learn.",
    "goal": "Terminas este curso cuando resuelves un problema de punta a punta sin seguir un tutorial.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/machine-learning-with-python",
    "boss": true,
    "wins": [
     "Regresión y clasificación, con los casos donde se usan",
     "Agrupamiento, cuando no hay respuesta correcta de antemano",
     "Un sistema de recomendación funcionando"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "claude.html",
  "clave": "claude",
  "nombre": "Trabajar con Claude",
  "actos": [
   "Qué es y qué no",
   "Usarlo todos los días",
   "Construir con él",
   "Conectarlo con lo tuyo",
   "Llevarlo a producción"
  ],
  "pasos": [
   {
    "id": "c01",
    "t": "AI Fluency: Framework & Foundations",
    "min": 240,
    "act": 1,
    "time": "4 horas",
    "sum": "El marco de las cuatro D -delegar, describir, discernir, diligencia- para trabajar con un modelo sin quedar a merced de lo que conteste. Acá empieza todo lo demás.",
    "goal": "Terminas esto cuando sabes decidir qué delegar y qué no, y por qué.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/ai-fluency-framework-foundations",
    "boss": true,
    "wins": [
     "Las cuatro D, que es el marco que usa el resto de los cursos",
     "Cómo funciona un modelo generativo, sin misterio",
     "Insignia de Anthropic al aprobar la evaluación final"
    ]
   },
   {
    "id": "c02",
    "t": "AI Capabilities and Limitations",
    "min": 180,
    "act": 1,
    "time": "3 h 30 min",
    "sum": "Las cuatro propiedades que explican todo lo que un modelo hace bien y todo lo que hace mal: predicción, conocimiento, memoria de trabajo y direccionabilidad.",
    "goal": "Terminas esto cuando ves una respuesta rara y sabes cuál de las cuatro falló.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/ai-capabilities-and-limitations",
    "boss": false,
    "wins": [
     "Diagnosticar una falla en vez de volver a pedir lo mismo",
     "Qué se arregla con contexto y qué no se arregla",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c03",
    "t": "Claude 101",
    "min": 120,
    "act": 2,
    "time": "2 h 30 min",
    "sum": "La herramienta entera: conversaciones, prompting, y después Projects, Artifacts, Skills y Connectors. Con ejemplos por rol, no en abstracto.",
    "goal": "Terminas esto cuando armaste un Project con tus documentos y lo usas todos los días.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-101",
    "boss": true,
    "wins": [
     "Projects y Artifacts, que es donde vive el trabajo largo",
     "Skills y Connectors para que traiga tus datos",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c04",
    "t": "Introduction to Claude Cowork",
    "min": 120,
    "act": 2,
    "time": "2 h 30 min",
    "sum": "Delegar trabajo de varios pasos: armar el espacio, darle contexto, dejarlo correr y revisar. Con tareas agendadas, instrucciones globales y cómo compartirlo con el equipo.",
    "goal": "Terminas esto cuando le dejas una tarea larga y el resultado te sirve sin rehacerlo.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/introduction-to-claude-cowork",
    "boss": false,
    "wins": [
     "Delegar un trabajo de varios pasos y que vuelva bien",
     "Tareas agendadas y trabajo compartido con el equipo",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c05",
    "t": "Claude Code 101",
    "min": 60,
    "act": 2,
    "time": "1 h 30 min",
    "sum": "El agente que trabaja en la terminal y en el editor: el bucle agéntico, la ventana de contexto, las herramientas y los permisos. Y cómo configurarlo para tu proyecto.",
    "goal": "Terminas esto cuando Claude Code toca tu repo y entiendes cada permiso que le diste.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-code-101",
    "boss": false,
    "wins": [
     "El bucle agéntico y por qué importa la ventana de contexto",
     "Los archivos de configuración de tu propio proyecto",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c06",
    "t": "Claude Code in Action",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "Sesiones largas sin perder el control: acotar el trabajo, escribir instrucciones que se cumplan, poner reglas con hooks, agendar corridas y revisar lo que hizo solo antes de mostrarlo.",
    "goal": "Terminas esto cuando dejas una tarea corriendo sola y confias en revisar el resultado.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-code-in-action",
    "boss": false,
    "wins": [
     "Hooks, que son reglas que el agente no puede saltarse",
     "Cómo verificar trabajo hecho sin supervisión",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c07",
    "t": "AI Fluency for Builders",
    "min": 180,
    "act": 3,
    "time": "3 horas",
    "sum": "Las cuatro D aplicadas a construir: qué sale confiable y qué no, y cómo revisar lo que genera, tanto el código como lo que ve el usuario.",
    "goal": "Terminas esto cuando sabes qué revisar antes de que algo generado salga a producción.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/ai-fluency-for-builders",
    "boss": false,
    "wins": [
     "Evaluar código generado sin leerlo línea por línea",
     "Dónde poner el control de calidad cuando el volumen sube",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c08",
    "t": "Claude Platform 101",
    "min": 60,
    "act": 3,
    "time": "1 h 30 min",
    "sum": "De usarlo a construir con él: la primera llamada a la API, el bucle del agente, el uso de herramientas y los agentes gestionados. Con elección de modelo y manejo de contexto.",
    "goal": "Terminas esto cuando tu primera aplicación hace una llamada real y devuelve lo que esperabas.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-platform-101",
    "boss": true,
    "wins": [
     "Tu primera llamada a la API, funcionando",
     "Elegir modelo por costo y por tarea, no por costumbre",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c09",
    "t": "Building with the Claude API",
    "min": 540,
    "act": 3,
    "time": "9 horas",
    "sum": "El curso largo: autenticación, prompting, RAG, uso de herramientas y sistemas basados en agentes. Se sale con un chatbot y automatizaciones andando.",
    "goal": "Terminas esto cuando tienes una aplicación tuya en producción, no un notebook.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/building-with-the-claude-api",
    "boss": false,
    "wins": [
     "RAG de punta a punta, que es lo que se pide en el trabajo",
     "Uso de herramientas y agentes, con código propio",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c10",
    "t": "Introduction to Model Context Protocol",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Servidores y clientes MCP en Python, con los tres primitivos -herramientas, recursos y prompts- que conectan el modelo con lo que ya existe en tu empresa.",
    "goal": "Terminas esto cuando tu propio servidor MCP responde y Claude lo usa.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/introduction-to-model-context-protocol",
    "boss": true,
    "wins": [
     "Los tres primitivos y cuándo va cada uno",
     "Un servidor MCP propio, andando",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c11",
    "t": "Model Context Protocol: Advanced Topics",
    "min": 60,
    "act": 4,
    "time": "1 h 30 min",
    "sum": "Lo que hace falta para que un servidor MCP aguante producción: sampling, notificaciones, roots, los transportes STDIO y StreamableHTTP, y cómo desplegarlo.",
    "goal": "Terminas esto cuando tu servidor está desplegado y no corriendo en tu máquina.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/model-context-protocol-advanced-topics",
    "boss": false,
    "wins": [
     "Elegir transporte según dónde vive el servidor",
     "Desplegarlo de forma que lo use alguien más",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c12",
    "t": "Introduction to Subagents",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "Partir un trabajo grande en subagentes que corren en paralelo y orquestarlos sin que el resultado dependa de la suerte. Y cuándo no conviene.",
    "goal": "Terminas esto cuando partiste una tarea tuya en subagentes y el resultado se repite.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/introduction-to-subagents",
    "boss": false,
    "wins": [
     "Cuándo un subagente ayuda y cuándo estorba",
     "Orquestar en paralelo con resultado predecible"
    ]
   },
   {
    "id": "c13",
    "t": "Introduction to Agent Skills",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Skills: instrucciones en markdown que se aplican solas cuando la tarea coincide. Cómo escribirlas, compartirlas y arreglarlas cuando no se disparan.",
    "goal": "Terminas esto cuando una skill tuya se aplica sola y el equipo la usa.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/introduction-to-agent-skills",
    "boss": false,
    "wins": [
     "Escribir una skill que se dispare cuando corresponde",
     "Compartirla, que es donde se nota"
    ]
   },
   {
    "id": "c14",
    "t": "Claude with Amazon Bedrock",
    "min": 480,
    "act": 5,
    "time": "8 horas",
    "sum": "Todo lo anterior sobre AWS: la API por Bedrock, uso de herramientas, RAG, agentes y aplicaciones listas para producción.",
    "goal": "Terminas esto cuando lo que construiste corre en la cuenta de AWS de tu trabajo.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-with-amazon-bedrock",
    "boss": true,
    "wins": [
     "Claude dentro de la nube donde ya está tu empresa",
     "RAG y agentes con los servicios de AWS",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c15",
    "t": "Claude with Google Cloud Vertex AI",
    "min": 480,
    "act": 5,
    "time": "8 h 30 min",
    "sum": "Lo mismo sobre Google Cloud: configuración, prompting, herramientas, RAG, MCP y agentes sobre Vertex AI.",
    "goal": "Terminas esto cuando lo tuyo corre en Vertex AI y no en tu máquina.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai",
    "boss": false,
    "wins": [
     "La alternativa a Bedrock, por si tu empresa está en GCP",
     "MCP y agentes sobre Vertex AI",
     "Insignia de Anthropic"
    ]
   },
   {
    "id": "c16",
    "t": "The AI-Native SDLC Playbook",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "Qué le pasa al ciclo de desarrollo cuando los agentes escriben la mayor parte del código: planificación, diseño, build, test, deploy y mantenimiento, y dónde poner el control.",
    "goal": "Terminas esto cuando sabes qué cambia en tu equipo, no solo en tu máquina.",
    "cert": "Insignia de Anthropic",
    "i": "",
    "u": "https://academy.claude.com/courses/ai-native-sdlc-playbook",
    "boss": false,
    "wins": [
     "Dónde aparecen los cuellos de botella nuevos",
     "Gobernanza para trabajo agéntico, sin frenarlo"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "deep-learning.html",
  "clave": "deeplearning",
  "nombre": "Deep learning",
  "actos": [
   "Deep Learning",
   "Mastering PyTorch",
   "PyTorch Projects",
   "Computer Vision Hands-on",
   "Image Processing y modelos generativos"
  ],
  "pasos": [
   {
    "id": "d01",
    "t": "Fundamentos de deep learning",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "Qué es una red neuronal por dentro y por qué necesitó tantos datos y tanta máquina para funcionar.",
    "goal": "Terminas este curso cuando puedes explicar qué aprende cada capa sin recurrir a la analogía del cerebro.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/introduction-deep-learning",
    "boss": false,
    "wins": [
     "Capas, pesos y funciones de activación",
     "Convolucionales, recurrentes y autoencoders: para qué es cada familia",
     "Por qué el campo estuvo dormido treinta años"
    ]
   },
   {
    "id": "d02",
    "t": "Deep learning con TensorFlow",
    "min": 180,
    "act": 1,
    "time": "3 horas",
    "sum": "El primer framework: armar, entrenar y evaluar una red con la biblioteca de Google.",
    "goal": "Terminas este curso cuando entrenas una red tuya y sabes qué mirar cuando no converge.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/deep-learning-with-tensorflow",
    "boss": false,
    "wins": [
     "El grafo de cómputo, que es la idea que sostiene todo",
     "Entrenar una red y leer la curva de pérdida",
     "Convolucionales y recurrentes en código"
    ]
   },
   {
    "id": "d03",
    "t": "Acelerar con GPUs",
    "min": 300,
    "act": 1,
    "time": "5 horas",
    "sum": "Por qué entrenar en GPU cambia el orden de magnitud, y qué hay que saber para aprovecharlo. Cierra la primera credencial.",
    "goal": "Terminas este curso cuando sabes si tu cuello de botella es la GPU, la memoria o los datos.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/tensorflow_gpu",
    "boss": true,
    "wins": [
     "Qué hace distinta a una GPU para esta cuenta",
     "Repartir el entrenamiento en varias placas",
     "El badge de Deep Learning, al cerrar los tres"
    ]
   },
   {
    "id": "d04",
    "t": "Tensores y datos",
    "min": 180,
    "act": 2,
    "time": "3 horas",
    "sum": "El punto de entrada: qué es un tensor, cómo se carga un conjunto de datos y cómo se lo aumenta.",
    "goal": "Terminas este curso cuando armas tu propio cargador de datos y lo alimentas a un modelo.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/pytorch-tensor-dataset-and-data-augmentation",
    "boss": false,
    "wins": [
     "Tensores y operaciones, que es toda la base",
     "Dataset y DataLoader, las dos piezas que vas a usar siempre",
     "Aumentación de datos, para cuando tienes pocos"
    ]
   },
   {
    "id": "d05",
    "t": "Regresión lineal con PyTorch",
    "min": 420,
    "act": 2,
    "time": "7 horas",
    "sum": "El modelo más simple, hecho a mano: es la excusa para entender descenso de gradiente y entrenamiento.",
    "goal": "Terminas este curso cuando escribes el bucle de entrenamiento sin copiarlo.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/linear-regression-with-pytorch",
    "boss": false,
    "wins": [
     "Descenso de gradiente, paso a paso",
     "El bucle de entrenamiento completo, escrito por ti",
     "Regresión múltiple y qué cambia"
    ]
   },
   {
    "id": "d06",
    "t": "Clasificación con PyTorch",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "Del número continuo a la categoría: regresión logística, softmax y las primeras redes densas.",
    "goal": "Terminas este curso cuando entrenas un clasificador y lees su matriz de confusión.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/classification-with-pytorch",
    "boss": false,
    "wins": [
     "Softmax y entropía cruzada, sin la fórmula suelta",
     "Redes densas para clasificar",
     "Evaluar de verdad, no solo mirar el acierto"
    ]
   },
   {
    "id": "d07",
    "t": "Armar una red neuronal",
    "min": 420,
    "act": 2,
    "time": "7 horas",
    "sum": "Cómo PyTorch construye y optimiza modelos: módulos, inicialización, regularización y las decisiones de entrenamiento.",
    "goal": "Terminas este curso cuando diagnosticas por qué una red no aprende.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-neural-network-with-pytorch",
    "boss": false,
    "wins": [
     "Módulos y cómo se compone un modelo",
     "Sobreajuste, dropout y regularización",
     "Elegir optimizador y tasa de aprendizaje con criterio"
    ]
   },
   {
    "id": "d08",
    "t": "Redes convolucionales",
    "min": 240,
    "act": 2,
    "time": "4 horas",
    "sum": "Visión por computadora: convolución, pooling, entrenamiento en GPU y transferencia de aprendizaje. Cierra Mastering PyTorch.",
    "goal": "Terminas este curso cuando reusas una red preentrenada para tu propio problema.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/convolutional-neural-networks-with-pytorch",
    "boss": true,
    "wins": [
     "Convolución y pooling, y qué ve cada filtro",
     "Transferencia de aprendizaje, que es lo que se usa en la práctica",
     "El badge de Mastering PyTorch, al cerrar los cinco"
    ]
   },
   {
    "id": "d09",
    "t": "Empezar con PyTorch",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "El proyecto de arranque: montar el entorno y entrenar un primer modelo de punta a punta.",
    "goal": "Terminas este proyecto cuando el modelo corre entero en tu máquina.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/getting-started-with-machine-learning-with-pytorch",
    "boss": false,
    "wins": [
     "El flujo completo, en una hora",
     "Sin instalar nada: corre en el navegador"
    ]
   },
   {
    "id": "d10",
    "t": "Predecir precios con LSTM",
    "min": 30,
    "act": 3,
    "time": "30 min",
    "sum": "Series de tiempo con redes recurrentes: predecir el valor de una acción a partir de su historia.",
    "goal": "Terminas este proyecto cuando puedes decir por qué una LSTM sirve acá y una red común no.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/predict-stock-prices-with-lstm-in-pytorch",
    "boss": false,
    "wins": [
     "Qué agrega la memoria en una red",
     "Datos de mercado reales, con sus trampas"
    ]
   },
   {
    "id": "d11",
    "t": "Desplegar visión sin servidor",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "Poner un modelo de visión a disposición de cualquiera, en un entorno serverless.",
    "goal": "Terminas este proyecto cuando tu modelo responde desde una URL pública.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/deploy-a-computer-vision-app-in-a-serverless-environment",
    "boss": false,
    "wins": [
     "De un notebook a algo que otros pueden usar",
     "Serverless: pagar solo cuando alguien lo llama"
    ]
   },
   {
    "id": "d12",
    "t": "Detección de objetos con Faster R-CNN",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "Detectar varios objetos en una foto y saber cuánta confianza tiene el modelo en cada uno.",
    "goal": "Terminas este proyecto cuando el modelo marca objetos por nombre en tus propias imágenes.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/object-detection-with-faster-r-cnn-and-pytorch",
    "boss": false,
    "wins": [
     "Detección con una red preentrenada sobre COCO",
     "La probabilidad de cada predicción, y por qué importa"
    ]
   },
   {
    "id": "d13",
    "t": "Segmentación médica con U-Net",
    "min": 30,
    "act": 3,
    "time": "30 min",
    "sum": "Segmentar imágenes biomédicas con U-Net, la misma arquitectura que está detrás de Stable Diffusion.",
    "goal": "Terminas este proyecto cuando entiendes qué separa segmentar de clasificar.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/medical-image-segmentation-with-pytorch-and-u-net",
    "boss": false,
    "wins": [
     "U-Net armada con capas de PyTorch",
     "Por qué esta arquitectura reaparece en todos lados"
    ]
   },
   {
    "id": "d14",
    "t": "Vision Transformers",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "La arquitectura que superó a las convolucionales en conjuntos grandes, con atención en vez de filtros.",
    "goal": "Terminas este proyecto cuando puedes decir cuándo conviene un transformer y cuándo una CNN.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/vision-transformers-for-image-classification-hands-on",
    "boss": false,
    "wins": [
     "Atención aplicada a partes de una imagen",
     "Dónde le gana a las convolucionales y dónde no"
    ]
   },
   {
    "id": "d15",
    "t": "Generar personajes con DCGAN",
    "min": 120,
    "act": 3,
    "time": "2 horas",
    "sum": "Redes generativas antagónicas: dos modelos compitiendo hasta que uno produce imágenes creíbles. Cierra PyTorch Projects.",
    "goal": "Terminas este proyecto cuando tu modelo genera imágenes que no existían.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/creating-anime-characters-using-dcgans-and-pytorch",
    "boss": true,
    "wins": [
     "Generador y discriminador, y por qué compiten",
     "El badge de PyTorch Projects, al cerrar los siete"
    ]
   },
   {
    "id": "d16",
    "t": "Retratos con U-2 Net",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "La red detrás de las apps que convierten una foto en un retrato dibujado.",
    "goal": "Terminas este proyecto cuando generas retratos a partir de fotos propias.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/human-portrait-drawing-with-u-squared-net-and-pytorch",
    "boss": false,
    "wins": [
     "U-2 Net y qué la hace buena para recortar figuras",
     "De una foto cualquiera a un retrato"
    ]
   },
   {
    "id": "d17",
    "t": "Vision Transformers",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "El mismo proyecto de la credencial anterior. Si ya lo hiciste, esta copia queda marcada sola.",
    "goal": "Terminas este proyecto cuando puedes decir cuándo conviene un transformer y cuándo una CNN.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/vision-transformers-for-image-classification-hands-on",
    "boss": false,
    "wins": [
     "Atención aplicada a partes de una imagen",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "d18",
    "t": "Desplegar visión sin servidor",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "También es parte de PyTorch Projects. Hacerlo una vez cuenta para las dos credenciales.",
    "goal": "Terminas este proyecto cuando tu modelo responde desde una URL pública.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/deploy-a-computer-vision-app-in-a-serverless-environment",
    "boss": false,
    "wins": [
     "De un notebook a algo que otros pueden usar",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "d19",
    "t": "Detección de cáncer en imágenes",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "Identificar tejido metastásico en recortes de escaneos de patología, con redes preentrenadas.",
    "goal": "Terminas este proyecto cuando el modelo distingue tejido sano del que no lo es.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/cancer-image-detection-with-pytorch-part-3-ibest-workshop",
    "boss": false,
    "wins": [
     "Transferencia de aprendizaje sobre imágenes médicas",
     "Preparar datos clínicos para entrenar"
    ]
   },
   {
    "id": "d20",
    "t": "Empezar con PyTorch",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "El mismo proyecto de arranque de PyTorch Projects. Si ya está hecho, aparece marcado.",
    "goal": "Terminas este proyecto cuando el modelo corre entero en tu máquina.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/getting-started-with-machine-learning-with-pytorch",
    "boss": false,
    "wins": [
     "El flujo completo, en una hora",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "d21",
    "t": "Generar personajes con DCGAN",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "También es parte de PyTorch Projects y de Image Processing: aparece en las tres.",
    "goal": "Terminas este proyecto cuando tu modelo genera imágenes que no existían.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/creating-anime-characters-using-dcgans-and-pytorch",
    "boss": false,
    "wins": [
     "Generador y discriminador, y por qué compiten",
     "Cuenta para las tres credenciales"
    ]
   },
   {
    "id": "d22",
    "t": "Detección de objetos con Faster R-CNN",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "El mismo de PyTorch Projects, y el que cierra Computer Vision.",
    "goal": "Terminas este proyecto cuando el modelo marca objetos por nombre en tus propias imágenes.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/object-detection-with-faster-r-cnn-and-pytorch",
    "boss": true,
    "wins": [
     "Detección con una red preentrenada sobre COCO",
     "El badge de Computer Vision, al cerrar los siete"
    ]
   },
   {
    "id": "d23",
    "t": "Clasificar con Hugging Face",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "Ajustar un transformer preentrenado de Hugging Face para clasificar imágenes de un dominio propio.",
    "goal": "Terminas este proyecto cuando ajustas un modelo ajeno a tus propias clases.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/image-classification-using-hugging-face-for-crypto-beans",
    "boss": false,
    "wins": [
     "Fine-tuning sobre un modelo del hub",
     "Cuándo conviene ajustar y cuándo entrenar de cero"
    ]
   },
   {
    "id": "d24",
    "t": "Entrenar un reconocedor de imágenes",
    "min": 40,
    "act": 5,
    "time": "40 min",
    "sum": "Entrenar un modelo que detecta si una foto tiene un objeto concreto. El ejemplo es un pancho, pero sirve para cualquier cosa.",
    "goal": "Terminas este proyecto cuando repites el proceso con un objeto elegido por ti.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/train-a-hotdog-image-recognition-model-with-python",
    "boss": false,
    "wins": [
     "Un clasificador binario de imágenes, entero",
     "El mismo procedimiento sirve para cualquier objeto"
    ]
   },
   {
    "id": "d25",
    "t": "Transferencia de estilo con CycleGAN",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "Convertir fotos en pinturas al estilo de Monet, con una arquitectura que aprende sin pares de ejemplo.",
    "goal": "Terminas este proyecto cuando entiendes por qué CycleGAN no necesita imágenes emparejadas.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-an-image-style-transfer-tool-using-cyclegans",
    "boss": false,
    "wins": [
     "CycleGAN por partes, sin magia",
     "Traducir entre dos dominios de imágenes"
    ]
   },
   {
    "id": "d26",
    "t": "Generar personajes con DCGAN",
    "min": 120,
    "act": 5,
    "time": "2 horas",
    "sum": "El tercero que comparte con las otras credenciales, y el que cierra esta.",
    "goal": "Terminas este proyecto cuando tu modelo genera imágenes que no existían.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/creating-anime-characters-using-dcgans-and-pytorch",
    "boss": true,
    "wins": [
     "Generador y discriminador, y por qué compiten",
     "El badge de Image Processing, al cerrar los cuatro"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "llm-agentes.html",
  "clave": "llmagentes",
  "nombre": "LLMs y agentes",
  "actos": [
   "Getting Started with LLMs",
   "Mastering RAG",
   "Fundamentals of AI Agents",
   "Agentic AI Hands-on"
  ],
  "pasos": [
   {
    "id": "l01",
    "t": "Prompt engineering",
    "min": 300,
    "act": 1,
    "time": "5 horas",
    "sum": "Cómo se le habla a un modelo de lenguaje para que devuelva algo usable, y por qué el contexto es la mitad del trabajo.",
    "goal": "Terminas este curso cuando un prompt tuyo resuelve la tarea sin quince intentos.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/prompt-engineering-for-everyone",
    "boss": false,
    "wins": [
     "Las técnicas que sirven y las que son superstición",
     "Contexto, ejemplos y formato de salida",
     "Dónde falla el modelo y cómo notarlo"
    ]
   },
   {
    "id": "l02",
    "t": "El oficio del prompt",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "El curso anterior llevado a código, con LangChain y un análisis de supervivencia en Python.",
    "goal": "Terminas este proyecto cuando armas prompts dentro de un programa y no en un chat.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/the-art-of-prompt-engineering",
    "boss": false,
    "wins": [
     "Prompts dentro de código, no sueltos",
     "Primer contacto con LangChain"
    ]
   },
   {
    "id": "l03",
    "t": "Tu propio chat con modelos abiertos",
    "min": 60,
    "act": 1,
    "time": "1 hora",
    "sum": "Armar un sitio tipo ChatGPT usando modelos de lenguaje abiertos, sin pagar por API.",
    "goal": "Terminas este proyecto cuando tu chat responde desde tu propia página.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/create-your-own-chatgpt-like-website-with-open-source-llms",
    "boss": false,
    "wins": [
     "Un chat funcionando de punta a punta",
     "Modelos abiertos en vez de un servicio pago"
    ]
   },
   {
    "id": "l04",
    "t": "Poner límites al modelo",
    "min": 120,
    "act": 1,
    "time": "2 horas",
    "sum": "Guardrails con herramientas abiertas: qué puede y qué no puede responder tu aplicación. Cierra la credencial.",
    "goal": "Terminas este proyecto cuando tu modelo se niega a lo que no corresponde.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-guardrails-for-your-ai-with-open-source",
    "boss": true,
    "wins": [
     "Filtros de entrada y de salida",
     "El badge de Getting Started with LLMs, al cerrar los cuatro"
    ]
   },
   {
    "id": "l05",
    "t": "Resumir documentos privados",
    "min": 45,
    "act": 2,
    "time": "45 min",
    "sum": "El primer RAG: partir un documento propio, indexarlo y hacer que el modelo responda sobre él.",
    "goal": "Terminas este proyecto cuando el modelo contesta sobre un documento que nunca vio en su entrenamiento.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/summarize-private-documents-using-rag-langchain-and-llms",
    "boss": false,
    "wins": [
     "Partir y vectorizar un documento",
     "Recuperar el fragmento correcto antes de responder"
    ]
   },
   {
    "id": "l06",
    "t": "Un agente de búsqueda con LlamaIndex",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "Indexar PDF, HTML y texto plano, y consultarlos con lenguaje natural.",
    "goal": "Terminas este proyecto cuando una sola consulta busca en formatos distintos.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/rag-with-llamaindex-build-a-retrieval-agent-using-llms",
    "boss": false,
    "wins": [
     "LlamaIndex sobre documentos mezclados",
     "Del PDF suelto a algo consultable"
    ]
   },
   {
    "id": "l07",
    "t": "Preguntas y respuestas con fundamento",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "Un agente que responde citando de dónde sacó cada cosa, en vez de inventar.",
    "goal": "Terminas este proyecto cuando cada respuesta viene con su fuente.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-grounded-q-a-agent-with-langchain-granite-and-rag",
    "boss": false,
    "wins": [
     "La cadena completa de recuperación y generación",
     "Respuestas que se pueden verificar"
    ]
   },
   {
    "id": "l08",
    "t": "RAG sobre datos de la web",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "Lo mismo pero con información que cambia todo el tiempo: traerla en el momento de la consulta.",
    "goal": "Terminas este proyecto cuando tu sistema responde sobre algo que pasó hoy.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-rag-system-for-web-data-with-langchain-and-llama-3-1",
    "boss": false,
    "wins": [
     "Recuperar contenido web al vuelo",
     "Cuándo conviene indexar y cuándo consultar en vivo"
    ]
   },
   {
    "id": "l09",
    "t": "Resumir videos de YouTube",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "Extraer la transcripción de un video, resumirla y poder preguntarle cosas.",
    "goal": "Terminas este proyecto cuando le preguntas a un video de una hora sin verlo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/ai-powered-youtube-summarizer-q-a-tool-with-rag-langchain",
    "boss": false,
    "wins": [
     "De la transcripción a un resumen útil",
     "Búsqueda por similitud sobre los fragmentos"
    ]
   },
   {
    "id": "l10",
    "t": "Un bot que rompe el hielo",
    "min": 40,
    "act": 2,
    "time": "40 min",
    "sum": "El último de la credencial: juntar datos de un perfil profesional y generar una conversación a medida.",
    "goal": "Terminas este proyecto cuando el bot arma un tema de charla con datos reales.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/create-an-ai-icebreaker-bot-with-watsonx-and-llamaindex",
    "boss": true,
    "wins": [
     "RAG sobre datos de una persona",
     "El badge de Mastering RAG, al cerrar los seis"
    ]
   },
   {
    "id": "l11",
    "t": "Un agente ReAct desde cero",
    "min": 90,
    "act": 3,
    "time": "90 min",
    "sum": "El patrón que hace que un modelo razone antes de actuar, escrito a mano para entender qué hay adentro.",
    "goal": "Terminas este proyecto cuando puedes explicar cada paso del ciclo sin mirar el código.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-simple-react-agent-from-scratch",
    "boss": false,
    "wins": [
     "Razonar, actuar y observar, en ese orden",
     "Escrito desde cero, sin framework"
    ]
   },
   {
    "id": "l12",
    "t": "Un asistente de matemática que no inventa",
    "min": 45,
    "act": 3,
    "time": "45 min",
    "sum": "Herramientas de LangChain para que el modelo calcule de verdad en vez de aproximar.",
    "goal": "Terminas este proyecto cuando el modelo deja de equivocarse en cuentas simples.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/how-to-build-ai-math-assistant-with-langchain-tool-calling",
    "boss": false,
    "wins": [
     "Definir herramientas que el modelo puede llamar",
     "Validación y manejo de errores"
    ]
   },
   {
    "id": "l13",
    "t": "Tus propias herramientas",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "Funciones que conectan el modelo con servicios externos, y control manual de cuándo se ejecutan.",
    "goal": "Terminas este proyecto cuando el modelo usa una herramienta escrita por ti.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-and-execute-your-own-tools-for-llms",
    "boss": false,
    "wins": [
     "Del modelo aislado al modelo con manos",
     "Decidir tú cuándo se ejecuta cada llamada"
    ]
   },
   {
    "id": "l14",
    "t": "Razonar y actuar con LangGraph",
    "min": 45,
    "act": 3,
    "time": "45 min",
    "sum": "El ciclo ReAct completo dentro de un framework, con observación y ajuste del plan.",
    "goal": "Terminas este proyecto cuando el agente cambia de estrategia al ver un resultado.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-reasoning-and-acting-ai-agents-with-react",
    "boss": false,
    "wins": [
     "El ciclo entero en LangGraph",
     "Consultas de varios pasos"
    ]
   },
   {
    "id": "l15",
    "t": "Que el agente revise su trabajo",
    "min": 45,
    "act": 3,
    "time": "45 min",
    "sum": "Reflexión: el modelo critica su propia respuesta y la mejora antes de entregarla.",
    "goal": "Terminas este proyecto cuando la segunda versión es mejor que la primera, sin que intervengas.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/make-your-ai-agents-smarter-with-reflection-in-langgraph",
    "boss": false,
    "wins": [
     "Autocrítica estructurada",
     "Iterar hasta que la respuesta sirva"
    ]
   },
   {
    "id": "l16",
    "t": "Reflexion, con validación externa",
    "min": 30,
    "act": 3,
    "time": "30 min",
    "sum": "Un paso más: además de criticarse, el agente busca información para verificar lo que dijo.",
    "goal": "Terminas este proyecto cuando el agente corrige un error suyo con una fuente.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/reflexion-agent-101",
    "boss": false,
    "wins": [
     "Reflexión más búsqueda",
     "Consejos que se pueden respaldar"
    ]
   },
   {
    "id": "l17",
    "t": "Un agente de investigación",
    "min": 45,
    "act": 3,
    "time": "45 min",
    "sum": "El más completo de la credencial: investiga, se critica y optimiza su propio desempeño.",
    "goal": "Terminas este proyecto cuando el agente resuelve una tarea de varios pasos sin guía.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-self-reflective-deep-research-agent-using-langgraph",
    "boss": true,
    "wins": [
     "Investigación autónoma con validación",
     "El badge de Fundamentals of AI Agents, al cerrar los siete"
    ]
   },
   {
    "id": "l18",
    "t": "Introducción a los agentes",
    "min": 180,
    "act": 4,
    "time": "3 horas",
    "sum": "El curso del tramo: qué es un agente, cómo funciona y por qué cambió la forma de construir con modelos.",
    "goal": "Terminas este curso cuando puedes decir qué separa un agente de una llamada a un modelo.",
    "cert": "Certificado de IBM",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/introduction-to-agentic-ai",
    "boss": false,
    "wins": [
     "Qué es un agente y qué no lo es",
     "Herramientas, memoria y planificación",
     "Dónde conviene y dónde es un exceso"
    ]
   },
   {
    "id": "l19",
    "t": "Varios agentes con CrewAI",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Una aplicación que analiza fotos de comida y arma recetas, con agentes especializados que se reparten el trabajo.",
    "goal": "Terminas este proyecto cuando dos agentes resuelven juntos algo que uno solo no podía.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/agentic-ai-build-a-multi-agent-app-with-crewai-gradio",
    "boss": false,
    "wins": [
     "Agentes con roles distintos",
     "Visión y lenguaje en la misma aplicación"
    ]
   },
   {
    "id": "l20",
    "t": "CrewAI de cero",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "El framework por dentro: analista, redactor y diseñador trabajando en secuencia sobre el mismo problema.",
    "goal": "Terminas este proyecto cuando armas tu propio equipo de agentes.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/crewai-101-building-multi-agent-ai-systems",
    "boss": false,
    "wins": [
     "Definir roles y tareas",
     "Orquestar el flujo entre ellos"
    ]
   },
   {
    "id": "l21",
    "t": "Un asistente de matemática que no inventa",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "También es parte de Fundamentals of AI Agents. Si ya lo hiciste, esta copia queda marcada sola.",
    "goal": "Terminas este proyecto cuando el modelo deja de equivocarse en cuentas simples.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/how-to-build-ai-math-assistant-with-langchain-tool-calling",
    "boss": false,
    "wins": [
     "Definir herramientas que el modelo puede llamar",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "l22",
    "t": "Tus propias herramientas",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "El mismo de la credencial anterior: hacerlo una vez cuenta para las dos.",
    "goal": "Terminas este proyecto cuando el modelo usa una herramienta escrita por ti.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-and-execute-your-own-tools-for-llms",
    "boss": false,
    "wins": [
     "Del modelo aislado al modelo con manos",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "l23",
    "t": "Un agente ReAct desde cero",
    "min": 90,
    "act": 4,
    "time": "90 min",
    "sum": "Compartido con Fundamentals of AI Agents. Aparece acá porque también forma parte de esta credencial.",
    "goal": "Terminas este proyecto cuando puedes explicar cada paso del ciclo sin mirar el código.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-a-simple-react-agent-from-scratch",
    "boss": false,
    "wins": [
     "Razonar, actuar y observar, en ese orden",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "l24",
    "t": "Patrones de flujo con LangGraph",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Las tres formas de coordinar agentes: en secuencia, por intención y en paralelo.",
    "goal": "Terminas este proyecto cuando eliges el patrón según el problema, no por costumbre.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/agentic-ai-workflow-design-patterns-with-langgraph",
    "boss": false,
    "wins": [
     "Secuencial, enrutado y paralelo",
     "Aplicaciones reales con cada uno"
    ]
   },
   {
    "id": "l25",
    "t": "Agentes para salud, con AutoGen",
    "min": 30,
    "act": 4,
    "time": "30 min",
    "sum": "Varios agentes que analizan síntomas y consultan fuentes médicas antes de sugerir algo.",
    "goal": "Terminas este proyecto cuando los agentes se corrigen entre sí.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-multiagent-chatbot-with-ag2-autogen-for-healthcare",
    "boss": false,
    "wins": [
     "AutoGen y la conversación entre agentes",
     "Un dominio donde equivocarse es caro"
    ]
   },
   {
    "id": "l26",
    "t": "Agentes con esquema, con PydanticAI",
    "min": 45,
    "act": 4,
    "time": "45 min",
    "sum": "Respuestas validadas contra un esquema: el agente no puede devolver cualquier cosa.",
    "goal": "Terminas este proyecto cuando una respuesta mal formada se rechaza sola.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/learn-pydanticai-by-building-a-customer-support-agent",
    "boss": false,
    "wins": [
     "Validación de estructura en la salida",
     "Atención al cliente como caso de prueba"
    ]
   },
   {
    "id": "l27",
    "t": "Conversar con tus documentos",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "El último: RAG con varios agentes que se corrigen entre ellos, sobre documentos propios.",
    "goal": "Terminas este proyecto cuando el sistema detecta y arregla su propia respuesta floja.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/chat-with-your-documents-via-agentic-rag-langgraph-docling",
    "boss": true,
    "wins": [
     "RAG con arquitectura de varios agentes",
     "El badge de Agentic AI Hands-on, al cerrar los diez"
    ]
   },
   {
    "id": "l27a",
    "t": "AWS Agentic AI Demonstrated",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Una evaluación práctica sobre agentes hechos con Amazon Bedrock: hay que arreglarlos, integrarlos y mejorarlos, que es lo que se hace cuando el agente ya existe y falla.",
    "goal": "Terminas esto cuando arreglaste el agente que te dan y tienes la microcredencial.",
    "cert": "Microcredencial oficial de AWS",
    "i": "",
    "u": "https://skillbuilder.aws/learn/32Y249P272/aws-agentic-ai-demonstrated/TTAJ5WKYTS",
    "boss": true,
    "wins": [
     "Una credencial oficial de AWS, gratis desde abril de 2026",
     "Depurar un agente ajeno, que es el trabajo real",
     "Integrar y mejorar agentes sobre Amazon Bedrock"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "ml-aplicado.html",
  "clave": "mlaplicado",
  "nombre": "ML aplicado",
  "actos": [
   "Unsupervised Machine Learning",
   "Recommendation Systems",
   "NLP y análisis de sentimiento",
   "Embeddable AI",
   "Reinforcement Learning",
   "Explainable AI"
  ],
  "pasos": [
   {
    "id": "a01",
    "t": "Kernel PCA",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Reducir dimensiones cuando la relación entre variables no es una línea recta.",
    "goal": "Terminas este proyecto cuando ves un patrón que PCA común no encontraba.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/use-kernel-pca-to-find-why-are-you-poor",
    "boss": false,
    "wins": [
     "PCA con kernel, para relaciones no lineales",
     "Qué se pierde al reducir y qué se gana"
    ]
   },
   {
    "id": "a02",
    "t": "Segmentar imágenes con Mean Shift",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Un algoritmo que encuentra grupos sin que le digas cuántos, aplicado a separar partes de una imagen.",
    "goal": "Terminas este proyecto cuando el algoritmo separa zonas que no marcaste.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/image-segmentation-with-mean-shift-clustering",
    "boss": false,
    "wins": [
     "Agrupamiento sin fijar la cantidad de grupos",
     "Segmentación como caso de uso"
    ]
   },
   {
    "id": "a03",
    "t": "Mezclas gaussianas",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Agrupar con probabilidades en vez de fronteras duras: cada punto pertenece a varios grupos en distinta medida.",
    "goal": "Terminas este proyecto cuando puedes decir por qué a veces conviene una pertenencia parcial.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/building-recommender-systems-with-gaussian-mixture-model",
    "boss": false,
    "wins": [
     "Agrupamiento probabilístico",
     "Detección de anomalías y segmentación"
    ]
   },
   {
    "id": "a04",
    "t": "DBSCAN",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Agrupar por densidad: encuentra grupos de forma irregular y marca lo que no entra en ninguno.",
    "goal": "Terminas este proyecto cuando distingues un caso raro de uno mal medido.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/unraveling-patterns-with-dbscan",
    "boss": false,
    "wins": [
     "Grupos de cualquier forma, no solo esferas",
     "El ruido como resultado válido"
    ]
   },
   {
    "id": "a05",
    "t": "PCA para reconocimiento facial",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Comprimir miles de píxeles en unas pocas componentes que igual permiten reconocer una cara.",
    "goal": "Terminas este proyecto cuando reconoces caras con una fracción de los datos.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/using-pca-to-improve-facial-recognition",
    "boss": false,
    "wins": [
     "De miles de píxeles a unas pocas componentes",
     "Qué representa cada componente"
    ]
   },
   {
    "id": "a06",
    "t": "Quitar el fondo de un video con SVD",
    "min": 45,
    "act": 1,
    "time": "45 min",
    "sum": "Descomposición en valores singulares aplicada a separar lo que se mueve de lo que no.",
    "goal": "Terminas este proyecto cuando separas figura y fondo sin marcar nada a mano.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/video-processing-subtracting-background-with-svd",
    "boss": false,
    "wins": [
     "SVD explicada por lo que hace, no por la fórmula",
     "Edición de video como excusa para entenderla"
    ]
   },
   {
    "id": "a07",
    "t": "Buscar imágenes con NMF",
    "min": 30,
    "act": 1,
    "time": "30 min",
    "sum": "Factorización no negativa para armar un buscador de imágenes parecidas. Cierra la credencial.",
    "goal": "Terminas este proyecto cuando tu buscador devuelve imágenes parecidas de verdad.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-an-image-retrieval-system-with-nmf-and-more",
    "boss": true,
    "wins": [
     "Factorizar de forma que los factores se entiendan",
     "El badge de Unsupervised ML, al cerrar los siete"
    ]
   },
   {
    "id": "a08",
    "t": "Recomendar por contenido",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "El más simple: recomendar cosas parecidas a las que ya te gustaron, mirando sus características.",
    "goal": "Terminas este proyecto cuando tu sistema recomienda sin saber nada de otros usuarios.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/creating-a-content-based-recommendation-system",
    "boss": false,
    "wins": [
     "Preparar los datos, que es la mitad del trabajo",
     "Similitud entre elementos"
    ]
   },
   {
    "id": "a09",
    "t": "Un recomendador tipo Netflix",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "Popularidad y contenido combinados, con KNN para encontrar títulos parecidos.",
    "goal": "Terminas este proyecto cuando puedes explicar por qué recomendó cada película.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-netflix-like-recommendation-systems-with-sklearn",
    "boss": false,
    "wins": [
     "KNN sobre géneros y tipos",
     "pandas y scikit-learn en un caso completo"
    ]
   },
   {
    "id": "a10",
    "t": "Filtrado colaborativo",
    "min": 25,
    "act": 2,
    "time": "25 min",
    "sum": "Recomendar por lo que hizo gente parecida a ti, sin mirar el contenido.",
    "goal": "Terminas este proyecto cuando entiendes la diferencia entre usuario a usuario y elemento a elemento.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-recommendation-systems-using-collaborative-filtering",
    "boss": false,
    "wins": [
     "Las dos formas de filtrado colaborativo",
     "Por qué funciona sin saber qué es cada cosa"
    ]
   },
   {
    "id": "a11",
    "t": "Elegir vino con NLP",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "Embeddings de Hugging Face sobre descripciones de vinos, para recomendar por gusto descrito en palabras.",
    "goal": "Terminas este proyecto cuando la recomendación entiende una descripción en lenguaje natural.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/find-your-best-bottle-of-wine-with-nlp",
    "boss": false,
    "wins": [
     "Texto convertido en vectores comparables",
     "Un buscador visual sobre esos vectores"
    ]
   },
   {
    "id": "a12",
    "t": "Agrupar cursos con BERT",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "Vectorizar texto con BERT, agrupar por similitud y visualizar los grupos en dos y tres dimensiones.",
    "goal": "Terminas este proyecto cuando encuentras cursos parecidos sin comparar títulos.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/mastering-nlp-and-clustering-find-best-courses-like-a-pro",
    "boss": false,
    "wins": [
     "BERT para representar texto",
     "Elegir la cantidad de grupos con criterio"
    ]
   },
   {
    "id": "a13",
    "t": "Recomendar perfumes con Sentence-BERT",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "Similitud semántica sobre notas de perfume: parecido por significado, no por palabras iguales.",
    "goal": "Terminas este proyecto cuando dos descripciones distintas con el mismo sentido quedan cerca.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/perfume-recommendation-with-sentence-bert",
    "boss": false,
    "wins": [
     "Sentence-BERT y similitud semántica",
     "Recomendar sobre texto descriptivo"
    ]
   },
   {
    "id": "a14",
    "t": "Mezclas gaussianas",
    "min": 30,
    "act": 2,
    "time": "30 min",
    "sum": "El mismo proyecto de Unsupervised ML: también sirve para segmentar usuarios y recomendar.",
    "goal": "Terminas este proyecto cuando puedes decir por qué a veces conviene una pertenencia parcial.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/building-recommender-systems-with-gaussian-mixture-model",
    "boss": false,
    "wins": [
     "Agrupamiento probabilístico aplicado a recomendación",
     "Cuenta para las dos credenciales"
    ]
   },
   {
    "id": "a15",
    "t": "Un recomendador completo con Django",
    "min": 60,
    "act": 2,
    "time": "1 hora",
    "sum": "El que cierra la credencial: una aplicación entera que guarda historial y recomienda películas.",
    "goal": "Terminas este proyecto cuando tienes una aplicación que otros pueden usar.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-your-movie-recommender-with-django",
    "boss": true,
    "wins": [
     "Del notebook a una aplicación web",
     "El badge de Recommendation Systems, al cerrar los ocho"
    ]
   },
   {
    "id": "a16",
    "t": "Transformers de Hugging Face",
    "min": 30,
    "act": 3,
    "time": "30 min",
    "sum": "El punto de entrada al NLP moderno: resumir, clasificar, traducir y generar con modelos ya entrenados.",
    "goal": "Terminas este proyecto cuando resuelves cuatro tareas distintas sin entrenar nada.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/natural-language-processing-with-hugging-face-transformers",
    "boss": false,
    "wins": [
     "Modelos preentrenados listos para usar",
     "Resumen, clasificación, traducción y extracción"
    ]
   },
   {
    "id": "a17",
    "t": "Sentimiento con Caikit",
    "min": 30,
    "act": 3,
    "time": "30 min",
    "sum": "Una aplicación en Python que consulta un modelo de Hugging Face a través de una API propia.",
    "goal": "Terminas este proyecto cuando tu aplicación clasifica texto por API.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/text-sentiment-analysis-using-caikit-and-hugging-face",
    "boss": false,
    "wins": [
     "Servir un modelo detrás de una API",
     "Caikit como capa de ejecución"
    ]
   },
   {
    "id": "a18",
    "t": "Clasificar reseñas de Yelp",
    "min": 60,
    "act": 3,
    "time": "1 hora",
    "sum": "Técnicas de NLP sobre reseñas reales para separar lo positivo de lo negativo.",
    "goal": "Terminas este proyecto cuando tu clasificador funciona sobre texto que nadie limpió.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/classification-of-yelp-reviews-using-sentiment-analysis",
    "boss": false,
    "wins": [
     "Preparar texto real, con su ruido",
     "Construir y evaluar el clasificador"
    ]
   },
   {
    "id": "a19",
    "t": "Una extensión que mide el ánimo",
    "min": 120,
    "act": 3,
    "time": "2 horas",
    "sum": "Análisis de sentimiento sobre publicaciones, dentro de una extensión de navegador. Cierra la credencial.",
    "goal": "Terminas este proyecto cuando la extensión corre en tu navegador.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/sentiment-analysis-extension-for-twitter",
    "boss": true,
    "wins": [
     "Una extensión de navegador funcionando",
     "El badge de NLP y Sentiment Analysis, al cerrar los cuatro"
    ]
   },
   {
    "id": "a20",
    "t": "Un asistente de voz",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Voz a texto y texto a voz combinados con un modelo de lenguaje, en una aplicación propia.",
    "goal": "Terminas este proyecto cuando le hablas a tu asistente y te responde.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/chatapp-powered-by-openai",
    "boss": false,
    "wins": [
     "Reconocimiento y síntesis de voz",
     "Un asistente que funciona de punta a punta"
    ]
   },
   {
    "id": "a21",
    "t": "Qué siente la gente sobre un producto",
    "min": 60,
    "act": 4,
    "time": "1 hora",
    "sum": "Clasificar emociones en reseñas de compradores y mostrar el resultado en una aplicación web.",
    "goal": "Terminas este proyecto cuando puedes leer el ánimo de cientos de reseñas de un vistazo.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/how-do-people-feel-about-a-product-use-ai-to-get-the-answer",
    "boss": false,
    "wins": [
     "Clasificación de emociones, más fina que positivo o negativo",
     "Extracción de reseñas y despliegue"
    ]
   },
   {
    "id": "a22",
    "t": "Atención al cliente por voz",
    "min": 50,
    "act": 4,
    "time": "50 min",
    "sum": "Una aplicación de pedidos con voz, desplegada con Flask.",
    "goal": "Terminas este proyecto cuando tomas un pedido hablando.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/improve-customer-support-with-ai-powered-voice-services",
    "boss": false,
    "wins": [
     "Servir un modelo con Flask",
     "Una interfaz que cualquiera puede usar"
    ]
   },
   {
    "id": "a23",
    "t": "Una extensión que mide el ánimo",
    "min": 120,
    "act": 4,
    "time": "2 horas",
    "sum": "El mismo de NLP: también forma parte de esta credencial.",
    "goal": "Terminas este proyecto cuando la extensión corre en tu navegador.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/sentiment-analysis-extension-for-twitter",
    "boss": true,
    "wins": [
     "Una extensión de navegador funcionando",
     "El badge de Embeddable AI, al cerrar los cuatro"
    ]
   },
   {
    "id": "a24",
    "t": "Un TicTacToe invencible",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "El primer agente que aprende jugando, con el método de Monte Carlo.",
    "goal": "Terminas este proyecto cuando tu agente deja de perder.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/build-your-own-unbeatable-tictactoe-ai",
    "boss": false,
    "wins": [
     "Agente, entorno, estado y recompensa",
     "Monte Carlo, explicado jugando"
    ]
   },
   {
    "id": "a25",
    "t": "TicTacToe con OpenAI Gym",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "El mismo juego con un entorno estándar y aprendizaje por diferencia temporal.",
    "goal": "Terminas este proyecto cuando entiendes qué aporta un entorno estandarizado.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/playing-tictactoe-with-reinforcement-learning-and-openai-gym",
    "boss": false,
    "wins": [
     "Diferencia temporal frente a Monte Carlo",
     "Gym como entorno de prueba"
    ]
   },
   {
    "id": "a26",
    "t": "Ganarle al blackjack",
    "min": 60,
    "act": 5,
    "time": "1 hora",
    "sum": "Entrenar un agente para jugar de forma óptima, y medir si de verdad le gana a la casa.",
    "goal": "Terminas este proyecto cuando puedes responder si se le gana a la casa o no.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/win-blackjack-with-reinforcement-learning",
    "boss": false,
    "wins": [
     "Entrenar y evaluar una política",
     "Analizar el desempeño con datos"
    ]
   },
   {
    "id": "a27",
    "t": "Atención al cliente por voz",
    "min": 50,
    "act": 5,
    "time": "50 min",
    "sum": "Compartido con Embeddable AI: es el que cierra las dos credenciales.",
    "goal": "Terminas este proyecto cuando tomas un pedido hablando.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/improve-customer-support-with-ai-powered-voice-services",
    "boss": true,
    "wins": [
     "Servir un modelo con Flask",
     "El badge de Reinforcement Learning, al cerrar los cuatro"
    ]
   },
   {
    "id": "a28",
    "t": "Por qué se va la gente de una empresa",
    "min": 45,
    "act": 6,
    "time": "45 min",
    "sum": "AIX360 sobre datos de recursos humanos: qué factores pesan de verdad en que alguien renuncie.",
    "goal": "Terminas este proyecto cuando puedes nombrar los tres factores que más pesan y por qué.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/learn-explainable-ai-employee-retention-use-case",
    "boss": false,
    "wins": [
     "SHAP para medir la influencia de cada variable",
     "Explicaciones que sirven para decidir"
    ]
   },
   {
    "id": "a29",
    "t": "Explicar un rechazo de crédito",
    "min": 60,
    "act": 6,
    "time": "1 hora",
    "sum": "Reglas legibles en vez de una caja negra, para un caso donde la persona tiene derecho a saber por qué.",
    "goal": "Terminas este proyecto cuando tu modelo entrega la razón junto con la decisión.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/from-data-to-decisions-explainable-ai-in-credit-approval",
    "boss": false,
    "wins": [
     "Modelos basados en reglas, interpretables de origen",
     "Tres miradas: quien modela, quien decide y quien recibe"
    ]
   },
   {
    "id": "a30",
    "t": "Qué mueve el precio de una casa",
    "min": 45,
    "act": 6,
    "time": "45 min",
    "sum": "Extraer reglas de decisión de datos de vivienda: ingreso, antigüedad y ubicación.",
    "goal": "Terminas este proyecto cuando explicas una tasación con tres reglas.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/explainable-ai-in-housing-markets-rule-based-analysis",
    "boss": false,
    "wins": [
     "Reglas extraídas de los datos",
     "Transparencia en un sector regulado"
    ]
   },
   {
    "id": "a31",
    "t": "Por qué a unos les va mejor",
    "min": 45,
    "act": 6,
    "time": "45 min",
    "sum": "Perfiles representativos de estudiantes con Protodash, para entender patrones sin señalar individuos.",
    "goal": "Terminas este proyecto cuando identificas perfiles y no casos sueltos.",
    "cert": "",
    "i": "",
    "u": "https://cognitiveclass.ai/courses/learn-explainable-ai-by-analyzing-student-performance",
    "boss": true,
    "wins": [
     "Protodash para encontrar ejemplos representativos",
     "El badge de Explainable AI, al cerrar los cuatro"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "web3.html",
  "clave": "web3",
  "nombre": "Web3",
  "actos": [
   "Qué es todo esto",
   "La base de código",
   "Construir en Ethereum",
   "Cuentas inteligentes"
  ],
  "pasos": [
   {
    "id": "w01",
    "t": "Introducción a blockchain",
    "min": 860,
    "act": 1,
    "time": "43 lecciones",
    "sum": "De la web de páginas a la web de contratos: qué es una cadena de bloques, qué es DeFi y qué problema dice resolver.",
    "goal": "Terminas este curso cuando puedes explicar qué hace una blockchain sin usar la palabra revolución.",
    "cert": "",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/intro-to-blockchain",
    "boss": false,
    "wins": [
     "Qué guarda una cadena de bloques y por qué cuesta cambiarla",
     "Wallets, claves y quién controla qué",
     "DeFi y NFTs, con lo que hacen y lo que no"
    ]
   },
   {
    "id": "w02",
    "t": "JavaScript desde cero",
    "min": 980,
    "act": 2,
    "time": "49 lecciones",
    "sum": "El curso de programación de Alchemy. Es prerrequisito declarado del bootcamp, así que no es opcional si vas a seguir.",
    "goal": "Terminas este curso cuando escribes y depuras tu propio código sin copiarlo.",
    "cert": "",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/js",
    "boss": false,
    "wins": [
     "La sintaxis y las estructuras de datos que vas a usar todo el tiempo",
     "Funciones, asincronía y promesas",
     "Suficiente para entrar al bootcamp sin ahogarte"
    ]
   },
   {
    "id": "w03",
    "t": "Solidity",
    "min": 220,
    "act": 2,
    "time": "11 lecciones",
    "sum": "El lenguaje de los contratos en cadenas EVM: tipos, funciones, modificadores y las trampas propias de escribir código que maneja plata.",
    "goal": "Terminas este curso cuando lees un contrato ajeno y entiendes qué hace cada función.",
    "cert": "",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/solidity",
    "boss": false,
    "wins": [
     "La sintaxis, que se parece a otras pero no se comporta igual",
     "Almacenamiento y gas: por qué cada línea cuesta",
     "Los errores clásicos que vacían un contrato"
    ]
   },
   {
    "id": "w04",
    "t": "Ethereum Bootcamp",
    "min": 1820,
    "act": 3,
    "time": "91 lecciones",
    "sum": "El curso grande: criptografía, contratos inteligentes y una aplicación descentralizada completa, con desafíos y proyectos semanales.",
    "goal": "Terminas este curso cuando entregas el proyecto final y te emiten el certificado.",
    "cert": "Certificado NFT de Alchemy",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/ethereum",
    "boss": true,
    "wins": [
     "De la criptografía a una aplicación que funciona",
     "Desafíos de código y proyectos semanales, no solo video",
     "Un proyecto final que es lo que se muestra"
    ]
   },
   {
    "id": "w05",
    "t": "Account Abstraction",
    "min": 180,
    "act": 4,
    "time": "3 horas",
    "sum": "El estándar ERC-4337: cuentas que son contratos, para que el usuario no tenga que entender de claves privadas ni de gas.",
    "goal": "Terminas este curso cuando puedes decir qué problema de experiencia de usuario resuelve.",
    "cert": "",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/erc4337",
    "boss": false,
    "wins": [
     "Por qué la cuenta común es un problema para quien recién llega",
     "Cómo funciona una cuenta que además es un contrato",
     "Quién paga el gas cuando el usuario no puede"
    ]
   },
   {
    "id": "w06",
    "t": "Cuentas modulares",
    "min": 90,
    "act": 4,
    "time": "video",
    "sum": "El estándar ERC-6900: cuentas inteligentes a las que se les agregan capacidades como si fueran módulos.",
    "goal": "Terminas este curso cuando entiendes cómo se extiende una cuenta sin reescribirla.",
    "cert": "",
    "i": "",
    "u": "https://www.alchemy.com/university/courses/erc6900",
    "boss": false,
    "wins": [
     "Módulos y por qué separan responsabilidades",
     "Qué se puede agregar y qué conviene dejar afuera",
     "El estado del estándar, que todavía se mueve"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "fullstack.html",
  "clave": "fullstack",
  "nombre": "Full Stack Open",
  "actos": [
   "La base de la web",
   "El servidor y las pruebas",
   "La aplicación completa",
   "Lo que pide el mercado",
   "Llevarlo a producción"
  ],
  "pasos": [
   {
    "id": "f00",
    "t": "Parte 0 &middot; Cómo funciona una app web",
    "min": 1020,
    "act": 1,
    "time": "17 horas",
    "sum": "Qué pasa de verdad entre que escribes una dirección y ves algo: pedidos, respuestas, y por qué las páginas dejaron de recargarse enteras.",
    "goal": "Terminas esta parte cuando puedes dibujar, sin ayuda, todo lo que ocurre al apretar un botón en una página.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part0",
    "boss": false,
    "wins": [
     "El ida y vuelta entre el navegador y el servidor, mirado con las herramientas del navegador",
     "Por qué existen las aplicaciones de una sola página y qué problema vinieron a resolver",
     "El vocabulario que el resto del curso da por sabido"
    ]
   },
   {
    "id": "f01",
    "t": "Parte 1 &middot; Introducción a React",
    "min": 1020,
    "act": 1,
    "time": "17 horas",
    "sum": "Componentes, propiedades y estado: las tres ideas sobre las que se apoya todo lo demás.",
    "goal": "Terminas esta parte cuando armas una interfaz que reacciona a lo que hace quien la usa, sin tocar el DOM a mano.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part1",
    "boss": false,
    "wins": [
     "Componentes que reciben datos y devuelven interfaz",
     "Estado: qué cambia, cuándo, y por qué la pantalla se redibuja sola",
     "Manejar eventos sin ensuciar el componente"
    ]
   },
   {
    "id": "f02",
    "t": "Parte 2 &middot; Hablar con el servidor",
    "min": 1020,
    "act": 1,
    "time": "17 horas",
    "sum": "Listas, formularios y el primer contacto con una API de verdad: traer datos, mandarlos y contar lo que salió mal.",
    "goal": "Terminas esta parte cuando tu aplicación lee y escribe contra un servidor y avisa bien cuando algo falla.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part2",
    "boss": true,
    "wins": [
     "Renderizar colecciones sin que React se queje de las claves",
     "Formularios controlados, que es como React quiere que se haga",
     "Pedidos al servidor y qué hacer con el error, que es la mitad del trabajo"
    ]
   },
   {
    "id": "f03",
    "t": "Parte 3 &middot; Un servidor con Node y Express",
    "min": 1020,
    "act": 2,
    "time": "17 horas",
    "sum": "Del otro lado del cable: tu propio servidor, con rutas, validación y una base de datos, puesto a andar en internet.",
    "goal": "Terminas esta parte cuando tu backend está desplegado y tu frontend le habla a él y no a un simulador.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part3",
    "boss": false,
    "wins": [
     "Express de cero: rutas, middleware y el manejo de errores",
     "Guardar de verdad, con validación antes de escribir",
     "Desplegarlo, que es donde aparecen los problemas que en tu máquina no existían"
    ]
   },
   {
    "id": "f04",
    "t": "Parte 4 &middot; Probar el servidor y manejar usuarios",
    "min": 1020,
    "act": 2,
    "time": "17 horas",
    "sum": "Pruebas del backend, y después lo que todo producto termina necesitando: cuentas, contraseñas y quién puede hacer qué.",
    "goal": "Terminas esta parte cuando tienes pruebas que corren solas y un inicio de sesión que no guarda contraseñas en claro.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part4",
    "boss": false,
    "wins": [
     "Pruebas de integración contra una base de prueba",
     "Usuarios y contraseñas guardadas como corresponde",
     "Autenticación con tokens, y por qué no alcanza con confiar en el frontend"
    ]
   },
   {
    "id": "f05",
    "t": "Parte 5 &middot; Probar el frontend y varias pantallas",
    "min": 1020,
    "act": 2,
    "time": "17 horas",
    "sum": "Pruebas de la interfaz y navegación entre pantallas. Con esta parte cierras el curso base: cinco créditos y el certificado.",
    "goal": "Terminas esta parte cuando tu aplicación tiene varias pantallas, pruebas que las cubren, y puedes bajar el certificado.",
    "cert": "Certificado de la Universidad de Helsinki",
    "i": "",
    "u": "https://fullstackopen.com/en/part5",
    "boss": true,
    "wins": [
     "Probar componentes como los usa una persona, no como los escribiste",
     "Varias pantallas con React Router, sin recargar nada",
     "El certificado de Helsinki: se baja al llegar, sin examen ni inscripción"
    ]
   },
   {
    "id": "f06",
    "t": "Parte 6 &middot; Estado que aguanta una app grande",
    "min": 1020,
    "act": 3,
    "time": "17 horas",
    "sum": "Cuando pasar datos de componente en componente deja de alcanzar: manejo de estado global y datos que vienen del servidor.",
    "goal": "Terminas esta parte cuando el estado de tu aplicación vive en un lugar y no repartido en diez componentes.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part6",
    "boss": false,
    "wins": [
     "Estado global, y cuándo de verdad hace falta",
     "Separar los datos del servidor del estado de la interfaz",
     "Reducers: cambios de estado que se pueden leer y probar"
    ]
   },
   {
    "id": "f07",
    "t": "Parte 7 &middot; Tus propias herramientas",
    "min": 1020,
    "act": 3,
    "time": "17 horas",
    "sum": "Hooks propios para no repetirte, y cómo se empaqueta todo esto para que llegue al navegador.",
    "goal": "Terminas esta parte cuando sacas lógica repetida a un hook tuyo y entiendes qué hace el empaquetador.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part7",
    "boss": true,
    "wins": [
     "Hooks propios: la forma de reusar lógica en React",
     "Qué hace un empaquetador y por qué tu código no llega tal cual lo escribiste",
     "Estilos, que hasta acá el curso había dejado de lado a propósito"
    ]
   },
   {
    "id": "f08",
    "t": "Parte 8 &middot; GraphQL",
    "min": 1020,
    "act": 4,
    "time": "17 horas",
    "sum": "La otra forma de pedirle datos a un servidor: el cliente dice exactamente qué quiere, en un solo pedido.",
    "goal": "Terminas esta parte cuando tienes un servidor GraphQL propio y un frontend que le consulta.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part8",
    "boss": false,
    "wins": [
     "Consultas y mutaciones, y en qué se diferencian de REST",
     "Un servidor GraphQL con Apollo",
     "Cuándo GraphQL ayuda de verdad y cuándo es complejidad de más"
    ]
   },
   {
    "id": "f09",
    "t": "Parte 9 &middot; TypeScript",
    "min": 1020,
    "act": 4,
    "time": "17 horas",
    "sum": "Tipos sobre JavaScript. Es lo que más aparece en las búsquedas de trabajo de los últimos años.",
    "goal": "Terminas esta parte cuando escribes frontend y backend tipados y el editor te avisa del error antes de correr nada.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part9",
    "boss": false,
    "wins": [
     "Los tipos que hacen falta de verdad, sin pelear con el compilador",
     "Tipar un backend de Express y un frontend de React",
     "Por qué el error atajado al escribir sale mucho más barato"
    ]
   },
   {
    "id": "f10",
    "t": "Parte 10 &middot; React Native",
    "min": 1020,
    "act": 4,
    "time": "17 horas",
    "sum": "Lo que ya sabes de React, aplicado a una app de teléfono de verdad.",
    "goal": "Terminas esta parte cuando corres tu aplicación en un teléfono y entiendes qué se comparte y qué no con la web.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part10",
    "boss": true,
    "wins": [
     "React Native con Expo, sin pelear con la instalación",
     "Qué cambia respecto de la web: navegación, estilos y formularios",
     "Una app móvil que consume tu propia API"
    ]
   },
   {
    "id": "f11",
    "t": "Parte 11 &middot; Integración y despliegue continuos",
    "min": 1020,
    "act": 5,
    "time": "17 horas",
    "sum": "Que cada cambio se pruebe y se publique solo. Es la parte que separa un proyecto personal de un trabajo en equipo.",
    "goal": "Terminas esta parte cuando un cambio tuyo pasa las pruebas y llega a producción sin que toques nada a mano.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part11",
    "boss": false,
    "wins": [
     "Un flujo que prueba, construye y despliega en cada cambio",
     "Por qué romper producción se vuelve difícil cuando esto está bien puesto",
     "Versionado y control de calidad automático"
    ]
   },
   {
    "id": "f12",
    "t": "Parte 12 &middot; Contenedores",
    "min": 1020,
    "act": 5,
    "time": "17 horas",
    "sum": "Empaquetar tu aplicación con todo lo que necesita, para que corra igual en tu máquina y en el servidor.",
    "goal": "Terminas esta parte cuando levantas tu aplicación entera, con su base, con un solo comando.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part12",
    "boss": false,
    "wins": [
     "Imágenes y contenedores, sin mitología",
     "Varios servicios levantados juntos y hablándose",
     "Contenedores para desarrollar, que es el uso que más se subestima"
    ]
   },
   {
    "id": "f13",
    "t": "Parte 13 &middot; Bases de datos relacionales",
    "min": 1020,
    "act": 5,
    "time": "17 horas",
    "sum": "El curso base usa una base de documentos. Acá vas a la relacional, que es la que vas a encontrar en la mayoría de los trabajos.",
    "goal": "Terminas esta parte cuando tu backend habla con Postgres y las migraciones están versionadas.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part13",
    "boss": false,
    "wins": [
     "Postgres desde Node, con y sin capa intermedia",
     "Relaciones entre tablas y consultas que las cruzan",
     "Migraciones: cambiar el esquema sin romper lo que ya hay"
    ]
   },
   {
    "id": "f14",
    "t": "Parte 14 &middot; Next.js",
    "min": 1020,
    "act": 5,
    "time": "17 horas",
    "sum": "El marco de trabajo sobre React que hoy usan muchas empresas: renderizado en el servidor y rutas por archivos.",
    "goal": "Terminas esta parte cuando entiendes qué resuelve Next.js que React solo no resuelve, y lo usas.",
    "cert": "",
    "i": "",
    "u": "https://fullstackopen.com/en/part14",
    "boss": true,
    "wins": [
     "Renderizado en el servidor y por qué volvió a importar",
     "Rutas por estructura de archivos",
     "Cuándo conviene un marco encima de React y cuándo estorba"
    ]
   }
  ],
  "nivel": "Con programación sabida",
  "nivelN": 2
 },
 {
  "archivo": "airflow.html",
  "clave": "airflow",
  "nombre": "Airflow",
  "actos": [
   "Los fundamentos",
   "Escribir DAGs que aguanten",
   "De la fuente"
  ],
  "pasos": [
   {
    "id": "g01",
    "t": "Airflow 101",
    "min": 90,
    "act": 1,
    "time": "a tu ritmo",
    "sum": "El camino de entrada de Astronomer, sobre Airflow 3. Qué es un DAG, cómo se programa y qué pasa cuando una tarea falla.",
    "goal": "Terminas esta parte cuando escribes un DAG, lo ves correr y entiendes por qué se ejecutó cuando se ejecutó.",
    "cert": "",
    "i": "",
    "u": "https://academy.astronomer.io/path/airflow-101",
    "boss": true,
    "wins": [
     "DAGs, tareas y dependencias: el vocabulario que todo lo demás da por sabido",
     "El planificador: por qué una tarea arranca cuando arranca",
     "Reintentos y alertas, que es la mitad de por qué se usa Airflow"
    ]
   },
   {
    "id": "g02",
    "t": "Airflow 101, versión Airflow 2",
    "min": 90,
    "act": 1,
    "time": "a tu ritmo",
    "sum": "El mismo camino para quien trabaja sobre Airflow 2. Hazlo sólo si tu empresa todavía está en esa versión: si empiezas de cero, ve directo a la 3.",
    "goal": "Terminas esta parte cuando reconoces qué cambió entre la 2 y la 3, y no te confunde la documentación.",
    "cert": "",
    "i": "",
    "u": "https://academy.astronomer.io/path/airflow-101-airflow-2",
    "boss": false,
    "wins": [
     "Lo mismo que la parte anterior, en la versión que todavía corre en producción en muchos lados",
     "Las diferencias que importan al leer código viejo",
     "Saltéala sin culpa si arrancas de cero"
    ]
   },
   {
    "id": "g03",
    "t": "DAG Authoring",
    "min": 90,
    "act": 2,
    "time": "a tu ritmo",
    "sum": "El camino avanzado de Astronomer: TaskFlow API, tareas dinámicas y plantillas. Es donde un DAG deja de ser un ejemplo.",
    "goal": "Terminas esta parte cuando escribes un DAG que genera tareas según lo que encuentre, sin repetir código.",
    "cert": "",
    "i": "",
    "u": "https://academy.astronomer.io/path/airflow-dag-authoring",
    "boss": true,
    "wins": [
     "TaskFlow API: DAGs que se leen como Python y no como configuración",
     "Tareas dinámicas, para cuando no sabes de antemano cuántas hay",
     "Plantillas y variables, que es como un DAG deja de estar hardcodeado"
    ]
   },
   {
    "id": "g04",
    "t": "Airflow 101: Building Your First Workflow",
    "min": 90,
    "act": 3,
    "time": "a tu ritmo",
    "sum": "El primer tutorial de la documentación oficial. Abierto, sin cuenta y sin registro.",
    "goal": "Terminas esta parte cuando tienes el primer flujo corriendo desde la documentación oficial.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html",
    "boss": false,
    "wins": [
     "El mismo arranque, contado por quien mantiene el proyecto",
     "La documentación oficial como fuente, que es a donde vas a volver siempre",
     "Sin cuenta y sin registro"
    ]
   },
   {
    "id": "g05",
    "t": "Pythonic DAGs con la TaskFlow API",
    "min": 90,
    "act": 3,
    "time": "a tu ritmo",
    "sum": "Escribir DAGs como funciones de Python en vez de como grafos armados a mano.",
    "goal": "Terminas esta parte cuando tus tareas se pasan datos entre sí sin que tengas que pensar en XComs.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html",
    "boss": false,
    "wins": [
     "Decoradores en vez de operadores para lo que hacés todos los días",
     "Cómo viajan los datos de una tarea a la siguiente",
     "Por qué el código queda más corto y más fácil de probar"
    ]
   },
   {
    "id": "g06",
    "t": "Un pipeline de datos simple",
    "min": 90,
    "act": 3,
    "time": "a tu ritmo",
    "sum": "El caso completo de punta a punta: traer datos, transformarlos y dejarlos donde alguien los use.",
    "goal": "Terminas esta parte cuando tienes un pipeline que corre solo y sabes dónde mirar cuando no corre.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html",
    "boss": false,
    "wins": [
     "El recorrido entero, no un fragmento",
     "Dónde se rompe un pipeline de verdad",
     "Qué mirar en la interfaz cuando algo falló anoche"
    ]
   },
   {
    "id": "g07",
    "t": "Flujos sobre almacenamiento de objetos",
    "min": 90,
    "act": 3,
    "time": "a tu ritmo",
    "sum": "Trabajar contra S3, GCS o Azure sin atarte a uno solo.",
    "goal": "Terminas esta parte cuando lees y escribes en la nube desde un DAG sin código específico del proveedor.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/objectstorage.html",
    "boss": false,
    "wins": [
     "Almacenamiento de objetos como si fuera un sistema de archivos",
     "El mismo DAG contra distintos proveedores",
     "Es lo que vas a usar en cualquier trabajo con datos en la nube"
    ]
   },
   {
    "id": "g08",
    "t": "Cuando hace falta una persona en el medio",
    "min": 90,
    "act": 3,
    "time": "a tu ritmo",
    "sum": "El operador que frena el flujo y espera que alguien apruebe. Es lo que piden los procesos que tocan plata o clientes.",
    "goal": "Terminas esta parte cuando un DAG espera una aprobación humana y sigue solo después.",
    "cert": "",
    "i": "",
    "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/hitl.html",
    "boss": true,
    "wins": [
     "Frenar un flujo hasta que alguien decida",
     "Por qué esto aparece en cuanto el pipeline toca algo sensible",
     "Cómo no dejar un flujo esperando para siempre"
    ]
   }
  ],
  "nivel": "Con Python sabido",
  "nivelN": 2
 },
 {
  "archivo": "testing.html",
  "clave": "testing",
  "nombre": "Testing y QA",
  "actos": [
   "Qué es probar",
   "Probar el código",
   "Probar la aplicación",
   "Que corra solo"
  ],
  "pasos": [
   {
    "id": "t01",
    "t": "El sílabo de ISTQB Foundation",
    "min": 360,
    "act": 1,
    "time": "6 h",
    "sum": "El vocabulario con el que la industria habla de esto: qué es un defecto, qué es una prueba de caja negra, qué significa cobertura. Se baja gratis en PDF y trae exámenes de ejemplo, también gratis.",
    "goal": "Terminas esta parte cuando entiendes qué te están pidiendo en una entrevista de QA sin traducir mentalmente.",
    "cert": "",
    "i": "",
    "u": "https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/",
    "boss": true,
    "wins": [
     "El vocabulario común: sin esto, cada equipo te lo explica distinto",
     "Los niveles y tipos de prueba, que es lo que se pregunta siempre",
     "Exámenes de ejemplo gratis para saber si te alcanza"
    ]
   },
   {
    "id": "t02",
    "t": "La pirámide de pruebas, de Martin Fowler",
    "min": 45,
    "act": 1,
    "time": "45 min",
    "sum": "Qué probar en cada nivel y por qué. Es el artículo que evita el error más caro de todos: escribir cincuenta pruebas de interfaz para algo que se probaba con tres unitarias.",
    "goal": "Terminas esta parte cuando, ante una funcionalidad nueva, sabes en qué nivel conviene probarla.",
    "cert": "",
    "i": "",
    "u": "https://martinfowler.com/articles/practical-test-pyramid.html",
    "boss": false,
    "wins": [
     "Por qué una prueba de interfaz cuesta cien veces más que una unitaria",
     "Dónde poner el esfuerzo cuando el tiempo no alcanza",
     "El lenguaje que vas a escuchar en cualquier equipo que pruebe en serio"
    ]
   },
   {
    "id": "t03",
    "t": "pytest, de cero",
    "min": 180,
    "act": 2,
    "time": "3 h",
    "sum": "El framework de pruebas de Python. Instalarlo, escribir la primera prueba, entender qué pasa cuando falla y cómo se lee el error.",
    "goal": "Terminas esta parte cuando escribes una prueba que falla, la lees, y arreglas el código en vez de la prueba.",
    "cert": "",
    "i": "",
    "u": "https://docs.pytest.org/en/stable/getting-started.html",
    "boss": true,
    "wins": [
     "Escribir y correr pruebas sin ceremonia",
     "Leer un fallo y saber qué te está diciendo",
     "Es la base de todo lo demás: lo de arriba no reemplaza esto"
    ]
   },
   {
    "id": "t04",
    "t": "Fixtures: preparar y limpiar",
    "min": 180,
    "act": 2,
    "time": "3 h",
    "sum": "Lo que separa un puñado de pruebas de una suite: cómo se prepara el estado que cada prueba necesita, y cómo se deja todo limpio después.",
    "goal": "Terminas esta parte cuando tus pruebas no dependen del orden en que corren.",
    "cert": "",
    "i": "",
    "u": "https://docs.pytest.org/en/stable/how-to/fixtures.html",
    "boss": false,
    "wins": [
     "Preparar datos sin copiar y pegar en cada prueba",
     "Por qué una suite que depende del orden es una suite rota",
     "Alcances: qué se arma una vez y qué se arma cada vez"
    ]
   },
   {
    "id": "t05",
    "t": "Vitest, lo mismo en JavaScript",
    "min": 120,
    "act": 2,
    "time": "2 h",
    "sum": "El equivalente del lado del navegador. Si vas a probar una aplicación web, las unitarias van acá.",
    "goal": "Terminas esta parte cuando pruebas una función de tu frontend sin abrir el navegador.",
    "cert": "",
    "i": "",
    "u": "https://vitest.dev/guide/",
    "boss": false,
    "wins": [
     "Las mismas ideas, en el otro lenguaje",
     "Correr las pruebas mientras escribes, no al final",
     "Simulacros: cómo se prueba algo que llama a un servidor"
    ]
   },
   {
    "id": "t06",
    "t": "Playwright, la primera prueba",
    "min": 120,
    "act": 3,
    "time": "2 h",
    "sum": "Automatizar el navegador de verdad: abrir la página, hacer clic, escribir, comprobar. Es la herramienta que se está llevando el mercado.",
    "goal": "Terminas esta parte cuando una prueba tuya recorre tu aplicación sola y te dice si algo se rompió.",
    "cert": "",
    "i": "",
    "u": "https://playwright.dev/docs/intro",
    "boss": true,
    "wins": [
     "Instalar y correr, que en esta herramienta es de verdad rápido",
     "Escribir una prueba que hace lo que haría una persona",
     "Ver la grabación de la prueba que falló, que es la mitad del trabajo"
    ]
   },
   {
    "id": "t07",
    "t": "Encontrar elementos sin que se rompa mañana",
    "min": 120,
    "act": 3,
    "time": "2 h",
    "sum": "El tema que decide si tu suite sobrevive un rediseño. Localizar por rol y por texto en vez de por la clase CSS que alguien va a cambiar.",
    "goal": "Terminas esta parte cuando tus pruebas siguen pasando después de que el equipo toca el HTML.",
    "cert": "",
    "i": "",
    "u": "https://playwright.dev/docs/locators",
    "boss": false,
    "wins": [
     "Localizadores que describen qué hace el elemento, no dónde está",
     "Por qué el selector CSS es la causa número uno de pruebas frágiles",
     "De paso, te obliga a mirar la accesibilidad de la página"
    ]
   },
   {
    "id": "t08",
    "t": "Cypress, la otra escuela",
    "min": 120,
    "act": 3,
    "time": "2 h",
    "sum": "La herramienta que muchos equipos ya tienen puesta. Conviene conocerla: no vas a elegir vos la que usa la empresa donde entres.",
    "goal": "Terminas esta parte cuando lees una suite de Cypress ajena y sabes qué hace.",
    "cert": "",
    "i": "",
    "u": "https://docs.cypress.io/app/get-started/why-cypress",
    "boss": false,
    "wins": [
     "El mismo problema resuelto con otra filosofía",
     "Qué gana y qué pierde contra Playwright",
     "Poder trabajar donde ya está elegida"
    ]
   },
   {
    "id": "t09",
    "t": "Probar APIs",
    "min": 120,
    "act": 3,
    "time": "2 h",
    "sum": "Lo que hay detrás de la pantalla. Escribir comprobaciones sobre las respuestas de un servicio: códigos, cuerpos, errores.",
    "goal": "Terminas esta parte cuando una API rota se detecta antes de que alguien abra la aplicación.",
    "cert": "",
    "i": "",
    "u": "https://learning.postman.com/docs/writing-scripts/test-scripts/",
    "boss": true,
    "wins": [
     "Comprobar respuestas, no solo mirarlas",
     "Encadenar pedidos: usar lo que devolvió uno en el siguiente",
     "Es la capa más barata de probar y la que más problemas encuentra"
    ]
   },
   {
    "id": "t10",
    "t": "Que las pruebas corran en cada cambio",
    "min": 120,
    "act": 4,
    "time": "2 h",
    "sum": "Una suite que hay que acordarse de correr no sirve. Acá se conecta a GitHub Actions para que corra sola en cada commit.",
    "goal": "Terminas esta parte cuando un cambio que rompe algo no llega a la rama principal.",
    "cert": "",
    "i": "",
    "u": "https://docs.github.com/en/actions/writing-workflows/quickstart",
    "boss": true,
    "wins": [
     "Un flujo que corre tus pruebas sin que nadie apriete nada",
     "Bloquear lo que rompe, que es el punto de todo esto",
     "Es lo que separa 'tengo pruebas' de 'las pruebas me cuidan'"
    ]
   },
   {
    "id": "t11",
    "t": "Playwright en integración continua",
    "min": 60,
    "act": 4,
    "time": "1 h 30",
    "sum": "La parte específica: correr pruebas de navegador en un servidor que no tiene pantalla, y guardar la evidencia de lo que falló.",
    "goal": "Terminas esta parte cuando puedes ver el video de la prueba que falló anoche.",
    "cert": "",
    "i": "",
    "u": "https://playwright.dev/docs/ci-intro",
    "boss": false,
    "wins": [
     "Navegador sin pantalla, que es donde todos se traban la primera vez",
     "Guardar rastros y videos de lo que fallo",
     "Correr en paralelo para que la suite no tarde una hora"
    ]
   },
   {
    "id": "t12",
    "t": "Carga: qué pasa cuando entran mil",
    "min": 180,
    "act": 4,
    "time": "3 h",
    "sum": "k6 es de código abierto y se escribe en JavaScript. Simular carga real y ver dónde se cae el sistema antes de que se caiga solo.",
    "goal": "Terminas esta parte cuando sabes cuántos usuarios aguanta lo que probaste, con un número.",
    "cert": "",
    "i": "",
    "u": "https://grafana.com/docs/k6/latest/get-started/running-k6/",
    "boss": false,
    "wins": [
     "Medir en vez de suponer",
     "La diferencia entre lento y roto",
     "Es lo que te preguntan cuando algo se cayó y nadie sabe por qué"
    ]
   },
   {
    "id": "t13",
    "t": "Accesibilidad: probar que se pueda usar",
    "min": 120,
    "act": 4,
    "time": "2 h",
    "sum": "Las herramientas para encontrar problemas de accesibilidad y las tecnologías que usa la gente que las necesita. Es requisito legal en cada vez más lugares y casi nadie lo prueba.",
    "goal": "Terminas esta parte cuando encuentras los problemas de accesibilidad de un sitio con un método y no a ojo.",
    "cert": "",
    "i": "",
    "u": "https://developer.mozilla.org/es/docs/Learn_web_development/Core/Accessibility",
    "boss": true,
    "wins": [
     "Qué se puede comprobar automático y qué hay que mirar a mano",
     "Es de las pocas habilidades de QA que se piden y no abundan",
     "Se cruza con los localizadores: probar bien y ser accesible van juntos"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "nube.html",
  "clave": "nube",
  "nombre": "Credenciales de nube",
  "actos": [
   "Qué es la nube",
   "AWS",
   "Datos en la nube",
   "Google"
  ],
  "pasos": [
   {
    "id": "n01",
    "t": "Conceptos de nube",
    "min": 300,
    "act": 1,
    "time": "5 h",
    "sum": "Qué es la nube y qué no: modelos de servicio, modelos de despliegue, en qué cambia pagar por uso. Es la mitad del examen AZ-900 y es lo único de todo esto que no depende del proveedor.",
    "goal": "Terminas esta parte cuando explicas la diferencia entre IaaS, PaaS y SaaS con un ejemplo tuyo.",
    "cert": "AZ-900",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
    "boss": true,
    "wins": [
     "El vocabulario que los tres proveedores comparten",
     "Por qué la nube cambia el costo de equivocarse, que es de lo que se trata",
     "Gratis, en español y sin cuenta para leerlo"
    ]
   },
   {
    "id": "n02",
    "t": "Arquitectura y servicios",
    "min": 360,
    "act": 1,
    "time": "6 h",
    "sum": "Las piezas concretas: regiones, zonas, cómputo, red y almacenamiento. Los nombres cambian entre proveedores, las piezas no.",
    "goal": "Terminas esta parte cuando dibujas dónde vive cada cosa de una aplicación en la nube.",
    "cert": "AZ-900",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/azure-fundamentals-describe-azure-architecture-services/",
    "boss": false,
    "wins": [
     "Regiones y zonas: por qué importa dónde está tu servidor",
     "Cómputo, red y almacenamiento, que es de lo que está hecho todo",
     "Aprender los conceptos en uno te sirve en los tres"
    ]
   },
   {
    "id": "n03",
    "t": "Administración y gobernanza",
    "min": 240,
    "act": 1,
    "time": "4 h",
    "sum": "Lo que nadie estudia y todos necesitan: cuánto va a costar, quién puede tocar qué, y cómo no llevarte una sorpresa a fin de mes.",
    "goal": "Terminas esta parte cuando puedes estimar el costo de algo antes de encenderlo.",
    "cert": "AZ-900",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/describe-azure-management-governance/",
    "boss": false,
    "wins": [
     "Calcular el costo antes, no después de la factura",
     "Permisos: quién puede hacer qué, que es la mitad de la seguridad",
     "Con esto cierras el temario completo de AZ-900"
    ]
   },
   {
    "id": "n04",
    "t": "AWS Cloud Practitioner Essentials",
    "min": 360,
    "act": 2,
    "time": "6 h",
    "sum": "El curso oficial y gratuito de AWS para su credencial de entrada. Los mismos conceptos del tramo anterior, con los nombres de AWS, que son los que aparecen en los avisos de trabajo.",
    "goal": "Terminas esta parte cuando lees un aviso que pide EC2, S3 y VPC y sabes de qué habla.",
    "cert": "AWS CCP",
    "i": "",
    "u": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
    "boss": true,
    "wins": [
     "Los nombres de AWS, que es lo que se pide por nombre",
     "El modelo de responsabilidad compartida, que entra en el examen y en la vida",
     "Es el curso oficial: no hay intermediario"
    ]
   },
   {
    "id": "n05",
    "t": "El mismo curso en Skill Builder",
    "min": 300,
    "act": 2,
    "time": "5 h",
    "sum": "La versión con seguimiento de avance y prácticas. Skill Builder tiene una parte paga; ésta no lo es. Pide crear una cuenta gratuita.",
    "goal": "Terminas esta parte cuando das el examen de práctica y te alcanza.",
    "cert": "AWS CCP",
    "i": "",
    "u": "https://explore.skillbuilder.aws/learn/courses/134/aws-cloud-practitioner-essentials",
    "boss": false,
    "wins": [
     "Ejercicios y examen de práctica, que es lo que falta para presentarse",
     "Tu avance queda guardado del lado de AWS",
     "Cuenta gratuita: lo pago de Skill Builder es otra cosa"
    ]
   },
   {
    "id": "n06",
    "t": "Fundamentos de datos en Azure",
    "min": 480,
    "act": 3,
    "time": "8 h",
    "sum": "DP-900: datos relacionales y no relacionales, analítica, y qué servicio se usa para qué. Es la credencial que más cruza con el resto de este sitio.",
    "goal": "Terminas esta parte cuando eliges entre una base relacional y una de documentos con un argumento.",
    "cert": "DP-900",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/courses/dp-900t00",
    "boss": true,
    "wins": [
     "Relacional contra no relacional, decidido y no adivinado",
     "Qué servicio hace qué, que es la pregunta de todos los días",
     "Se cruza con SQL y con modelado, que ya están acá"
    ]
   },
   {
    "id": "n07",
    "t": "Microsoft Fabric",
    "min": 240,
    "act": 3,
    "time": "4 h",
    "sum": "La plataforma con la que Microsoft juntó todo lo de datos en un solo lugar. Está apareciendo en los avisos y casi no hay material ordenado en español.",
    "goal": "Terminas esta parte cuando sabes qué reemplaza Fabric y qué no.",
    "cert": "",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/get-started-fabric/",
    "boss": false,
    "wins": [
     "Qué es y qué junta, sin el folleto",
     "Dónde encaja si ya sabes SQL y modelado",
     "Es reciente: saberlo distingue"
    ]
   },
   {
    "id": "n08",
    "t": "Empezar en ingeniería de datos",
    "min": 300,
    "act": 3,
    "time": "5 h",
    "sum": "El camino de Microsoft para el rol, con los servicios de datos en la nube. Es el puente entre esta ruta y la de Data Engineer.",
    "goal": "Terminas esta parte cuando entiendes cómo se arma un pipeline con servicios administrados en vez de con tu propio servidor.",
    "cert": "",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/get-started-data-engineering/",
    "boss": false,
    "wins": [
     "Pipelines sin mantener servidores",
     "Cómo se ve el trabajo de datos del lado de la nube",
     "Conecta con la ruta de Data Engineer que ya está acá"
    ]
   },
   {
    "id": "n09",
    "t": "Cloud Digital Leader, de Google",
    "min": 480,
    "act": 4,
    "time": "8 h",
    "sum": "La ruta oficial de Google para su credencial de entrada. Seis actividades sobre nube, datos e IA. Pide crear una cuenta gratuita para verla.",
    "goal": "Terminas esta parte cuando puedes comparar los tres proveedores sin repetir lo que dice cada folleto.",
    "cert": "Cloud Digital Leader",
    "i": "",
    "u": "https://skills.google/paths/9",
    "boss": true,
    "wins": [
     "El tercero de los tres grandes, con sus nombres",
     "Nube, datos e IA juntos, que es como Google la vende",
     "Cuenta gratuita: los laboratorios con créditos son aparte y no hacen falta acá"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 },
 {
  "archivo": "funcional.html",
  "clave": "funcional",
  "nombre": "Analista funcional",
  "actos": [
   "Cómo se trabaja",
   "Escribir lo que se pide",
   "Dibujar el proceso",
   "Lo técnico que sí hace falta"
  ],
  "pasos": [
   {
    "id": "f01",
    "t": "El Manifiesto Ágil, el original",
    "min": 20,
    "act": 1,
    "time": "20 min",
    "sum": "Cuatro valores y doce principios, en una página. Es corto a propósito, y es de donde salió todo lo que después te van a vender en cursos de tres días.",
    "goal": "Terminas esta parte cuando reconoces qué de lo que hace tu equipo es ágil y qué es una reunión con otro nombre.",
    "cert": "",
    "i": "",
    "u": "https://agilemanifesto.org/iso/es/manifesto.html",
    "boss": true,
    "wins": [
     "El documento original, en español, gratis",
     "Veinte minutos que te ahorran discusiones de años",
     "Sirve para detectar cuándo alguien usa la palabra sin el contenido"
    ]
   },
   {
    "id": "f02",
    "t": "La Guía Scrum",
    "min": 120,
    "act": 1,
    "time": "2 h",
    "sum": "El documento oficial: los roles, los eventos y los artefactos, sin interpretación de nadie. Trece páginas.",
    "goal": "Terminas esta parte cuando distingues Scrum de lo que tu empresa llama Scrum.",
    "cert": "",
    "i": "",
    "u": "https://scrumguides.org/scrum-guide.html",
    "boss": false,
    "wins": [
     "Qué es cada ceremonia y para qué existe de verdad",
     "Dónde entra el analista funcional en ese marco",
     "Es la fuente: todo curso pago de Scrum explica esto"
    ]
   },
   {
    "id": "f03",
    "t": "Scrum en la práctica",
    "min": 120,
    "act": 1,
    "time": "2 h",
    "sum": "La guía de Atlassian: lo mismo pero contado por quienes hacen la herramienta donde vas a cargar los tickets. Con los problemas reales que la guía oficial no cuenta.",
    "goal": "Terminas esta parte cuando sabes qué hacer cuando el sprint no entra.",
    "cert": "",
    "i": "",
    "u": "https://www.atlassian.com/agile/scrum",
    "boss": false,
    "wins": [
     "Cómo se ve el marco cuando lo aplica gente con apuro",
     "El vocabulario de Jira, que es donde vas a trabajar",
     "Los errores típicos, contados antes de que los cometas"
    ]
   },
   {
    "id": "f04",
    "t": "Historias de usuario",
    "min": 120,
    "act": 2,
    "time": "2 h",
    "sum": "El corazón del oficio: pasar de «quiero que el sistema haga algo» a algo que un equipo puede construir y verificar. Quién, qué y para qué.",
    "goal": "Terminas esta parte cuando escribes una historia que el desarrollador no tiene que venir a preguntarte.",
    "cert": "",
    "i": "",
    "u": "https://www.atlassian.com/agile/project-management/user-stories",
    "boss": true,
    "wins": [
     "La forma de la historia, y por qué esa forma y no otra",
     "Criterios de aceptación: cómo se sabe que está hecho",
     "Es lo que te van a pedir escribir el primer día"
    ]
   },
   {
    "id": "f05",
    "t": "Épicas, historias y temas",
    "min": 60,
    "act": 2,
    "time": "1 h 30",
    "sum": "Cómo se agrupa el trabajo cuando no entra en una historia. Es lo que evita el backlog de trescientos tickets sueltos.",
    "goal": "Terminas esta parte cuando partes un pedido grande en piezas que se pueden entregar de a una.",
    "cert": "",
    "i": "",
    "u": "https://www.atlassian.com/agile/project-management/epics-stories-themes",
    "boss": false,
    "wins": [
     "Partir sin romper: cada pieza tiene que servir sola",
     "Los niveles, para poder hablar con negocio y con desarrollo",
     "Ordenar un backlog en vez de acumularlo"
    ]
   },
   {
    "id": "f06",
    "t": "Preguntar bien: investigación con usuarios",
    "min": 120,
    "act": 2,
    "time": "2 h",
    "sum": "Nielsen Norman Group, que es la autoridad del tema. Qué método usar según lo que necesitas saber, y por qué preguntarle a la gente qué quiere casi nunca funciona.",
    "goal": "Terminas esta parte cuando eliges cómo averiguar algo en vez de mandar una encuesta por defecto.",
    "cert": "",
    "i": "",
    "u": "https://www.nngroup.com/articles/which-ux-research-methods/",
    "boss": false,
    "wins": [
     "Qué método sirve para qué pregunta",
     "Por qué lo que la gente dice y lo que hace no coinciden",
     "Es la diferencia entre tomar el pedido y entender el problema"
    ]
   },
   {
    "id": "f07",
    "t": "BPMN, la referencia completa",
    "min": 180,
    "act": 3,
    "time": "3 h",
    "sum": "El idioma con el que se dibuja un proceso: qué significa cada figura, y por qué un diagrama mal hecho esconde justamente lo que hay que discutir. Camunda publica la referencia entera.",
    "goal": "Terminas esta parte cuando dibujas un proceso y el que lo lee entiende lo mismo que tú.",
    "cert": "",
    "i": "",
    "u": "https://camunda.com/bpmn/reference/",
    "boss": true,
    "wins": [
     "Cada figura y qué quiere decir, sin ambigüedad",
     "Dónde se esconden las excepciones, que es donde está el trabajo",
     "Es notación estándar: lo lee cualquiera, en cualquier empresa"
    ]
   },
   {
    "id": "f08",
    "t": "Casos de uso y UML",
    "min": 60,
    "act": 3,
    "time": "1 h 30",
    "sum": "La notación anterior a BPMN, que sigue viva en la mitad de las empresas grandes. Vale conocerla porque te la vas a encontrar escrita.",
    "goal": "Terminas esta parte cuando lees un diagrama de casos de uso ajeno sin traductor.",
    "cert": "",
    "i": "",
    "u": "https://www.uml-diagrams.org/use-case-diagrams.html",
    "boss": false,
    "wins": [
     "Actores, casos y relaciones",
     "Cuándo un caso de uso dice más que una historia",
     "Poder trabajar donde ya está elegido"
    ]
   },
   {
    "id": "f09",
    "t": "SQL: mirar los datos tú mismo",
    "min": 240,
    "act": 4,
    "time": "4 h 30",
    "sum": "Es lo que separa a un analista funcional de alguien que toma notas. Poder responder «¿cuántos casos hay así?» sin pedirle a nadie que lo consulte.",
    "goal": "Terminas esta parte cuando contestas una pregunta del negocio con una consulta, en el momento.",
    "cert": "",
    "i": "",
    "u": "https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-databases-and-sql",
    "boss": true,
    "wins": [
     "SELECT, filtros y JOINs: alcanza para el noventa por ciento",
     "Verificar un supuesto antes de escribir el requisito",
     "Es la habilidad que más rápido te cambia el peso en una reunión"
    ]
   },
   {
    "id": "f10",
    "t": "Power BI, del lado de quien pide",
    "min": 300,
    "act": 4,
    "time": "5 h",
    "sum": "No para construir tableros, sino para saber qué se puede pedir, qué cuesta caro y por qué el dato no está como lo quieres.",
    "goal": "Terminas esta parte cuando pides un tablero sabiendo qué implica cada cosa que pediste.",
    "cert": "",
    "i": "",
    "u": "https://learn.microsoft.com/es-es/training/paths/get-started-power-bi/",
    "boss": false,
    "wins": [
     "Qué se puede y qué no, antes de prometerlo",
     "El vocabulario para hablar con el equipo de datos",
     "Gratis, en español, de Microsoft"
    ]
   }
  ],
  "nivel": "Desde cero",
  "nivelN": 0
 }
];
