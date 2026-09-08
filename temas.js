/* ============================================================
   temas.js

   Lo genera build-temas.py. No se edita a mano.

   Los temas y los puestos se definen alla y se revisan; el
   indice de que paso ensena que se calcula desde pasos.js.
   ============================================================ */
var TEMAS = {
 "temas": [
  {
   "id": "sql",
   "nombre": "SQL",
   "senales": [
    "sql",
    "postgres",
    "mysql",
    "sql server",
    "oracle",
    "bigquery",
    "redshift",
    "snowflake",
    "consultas",
    "queries",
    "stored procedure",
    "plsql"
   ]
  },
  {
   "id": "python",
   "nombre": "Python",
   "senales": [
    "python",
    "pandas",
    "numpy",
    "jupyter",
    "notebook",
    "django",
    "flask",
    "fastapi",
    "scipy"
   ]
  },
  {
   "id": "prog",
   "nombre": "Fundamentos de programación",
   "senales": [
    "algoritmo",
    "estructura de datos",
    "leetcode",
    "complejidad",
    "big o",
    "programacion",
    "software",
    "git",
    "javascript",
    "java",
    "scratch"
   ]
  },
  {
   "id": "modelado",
   "nombre": "Modelado de datos",
   "senales": [
    "modelado",
    "data model",
    "star schema",
    "kimball",
    "inmon",
    "normalizacion",
    "dimensional",
    "data warehouse",
    "datawarehouse",
    "dwh",
    "data vault",
    "dbt"
   ]
  },
  {
   "id": "pipelines",
   "nombre": "Pipelines y orquestación",
   "senales": [
    "airflow",
    "etl",
    "elt",
    "pipeline",
    "ingesta",
    "orquestacion",
    "dagster",
    "prefect",
    "kafka",
    "nifi",
    "streaming",
    "batch"
   ]
  },
  {
   "id": "calidad",
   "nombre": "Calidad y testing",
   "senales": [
    "testing",
    "test unitario",
    "pytest",
    "calidad de datos",
    "great expectations",
    "data quality",
    "observabilidad",
    "monitoreo"
   ]
  },
  {
   "id": "cloud",
   "nombre": "Nube e infraestructura",
   "senales": [
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "cloud",
    "lambda",
    "terraform",
    "docker",
    "kubernetes",
    "openshift",
    "serverless",
    "microservicio",
    "devops"
   ]
  },
  {
   "id": "bigdata",
   "nombre": "Big data",
   "senales": [
    "hadoop",
    "spark",
    "pyspark",
    "mapreduce",
    "hive",
    "hbase",
    "yarn",
    "big data",
    "databricks",
    "flink"
   ]
  },
  {
   "id": "stats",
   "nombre": "Estadística y experimentos",
   "senales": [
    "estadistica",
    "statistics",
    "ab testing",
    "experimento",
    "hipotesis",
    "regresion",
    "probabilidad",
    "inferencia",
    "significancia"
   ]
  },
  {
   "id": "ml",
   "nombre": "Machine learning",
   "senales": [
    "machine learning",
    "scikit",
    "sklearn",
    "xgboost",
    "random forest",
    "clasificacion",
    "clustering",
    "modelo predictivo",
    "feature engineering"
   ]
  },
  {
   "id": "deep",
   "nombre": "Deep learning",
   "senales": [
    "deep learning",
    "tensorflow",
    "pytorch",
    "keras",
    "red neuronal",
    "neural network",
    "cnn",
    "rnn",
    "transformer",
    "computer vision",
    "nlp"
   ]
  },
  {
   "id": "llm",
   "nombre": "LLMs y agentes",
   "senales": [
    "llm",
    "gpt",
    "openai",
    "claude",
    "langchain",
    "rag",
    "prompt",
    "embedding",
    "vector",
    "agente",
    "bedrock",
    "generativa",
    "genai"
   ]
  },
  {
   "id": "mlops",
   "nombre": "MLOps y puesta en producción",
   "senales": [
    "mlops",
    "mlflow",
    "kubeflow",
    "sagemaker",
    "model serving",
    "deploy",
    "produccion",
    "inferencia",
    "drift",
    "feature store"
   ]
  },
  {
   "id": "viz",
   "nombre": "Visualización",
   "senales": [
    "tableau",
    "power bi",
    "powerbi",
    "looker",
    "metabase",
    "superset",
    "matplotlib",
    "seaborn",
    "plotly",
    "dashboard",
    "visualizacion"
   ]
  },
  {
   "id": "web",
   "nombre": "Desarrollo web",
   "senales": [
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "svelte",
    "html",
    "css",
    "frontend",
    "front-end",
    "front end",
    "next.js",
    "nextjs",
    "tailwind",
    "jquery",
    "redux",
    "sass",
    "webpack",
    "vite",
    "spa",
    "responsive",
    "react native",
    "flutter",
    "bootstrap"
   ]
  },
  {
   "id": "backend",
   "nombre": "Backend y APIs",
   "senales": [
    "api",
    "rest",
    "restful",
    "graphql",
    "node",
    "nodejs",
    "node.js",
    "express",
    "backend",
    "back-end",
    "back end",
    "endpoint",
    "spring",
    "spring boot",
    ".net",
    "laravel",
    "rails",
    "nestjs",
    "jwt",
    "oauth",
    "autenticacion",
    "microservicios",
    "http"
   ]
  },
  {
   "id": "web3",
   "nombre": "Blockchain y Web3",
   "senales": [
    "blockchain",
    "solidity",
    "ethereum",
    "web3",
    "smart contract",
    "cripto",
    "defi",
    "wallet"
   ]
  }
 ],
 "puestos": [
  {
   "id": "tester",
   "nombre": "QA / Tester",
   "resumen": "Encontrar lo que se rompe antes que el usuario, y dejarlo comprobado solo.",
   "temas": {
    "calidad": 3,
    "prog": 2,
    "web": 2,
    "backend": 2,
    "cloud": 1,
    "sql": 1
   }
  },
  {
   "id": "data_engineer",
   "nombre": "Data Engineer",
   "resumen": "Construir y sostener los pipelines y el modelo de datos del que vive todo el resto.",
   "temas": {
    "sql": 3,
    "python": 3,
    "modelado": 3,
    "pipelines": 3,
    "cloud": 2,
    "calidad": 2,
    "bigdata": 2,
    "prog": 1
   }
  },
  {
   "id": "data_analyst",
   "nombre": "Data Analyst",
   "resumen": "Responder preguntas del negocio con datos y dejar claro qué significa la respuesta.",
   "temas": {
    "sql": 3,
    "viz": 3,
    "stats": 2,
    "python": 2,
    "modelado": 1,
    "prog": 1
   }
  },
  {
   "id": "data_scientist",
   "nombre": "Data Scientist",
   "resumen": "Estadística, experimentos y modelos predictivos para decidir con evidencia.",
   "temas": {
    "stats": 3,
    "ml": 3,
    "python": 3,
    "sql": 2,
    "viz": 2,
    "deep": 1,
    "prog": 1
   }
  },
  {
   "id": "ml_engineer",
   "nombre": "ML Engineer",
   "resumen": "Llevar modelos a producción y que sigan funcionando cuando nadie los mira.",
   "temas": {
    "ml": 3,
    "mlops": 3,
    "python": 3,
    "deep": 2,
    "cloud": 2,
    "prog": 2,
    "pipelines": 2,
    "sql": 1
   }
  },
  {
   "id": "ai_engineer",
   "nombre": "AI Engineer",
   "resumen": "Aplicaciones sobre modelos de lenguaje: recuperación, agentes y sus límites.",
   "temas": {
    "llm": 3,
    "python": 3,
    "prog": 2,
    "cloud": 2,
    "ml": 1,
    "deep": 1,
    "mlops": 1
   }
  },
  {
   "id": "fullstack",
   "nombre": "Desarrollador Full Stack",
   "resumen": "Construir la aplicación entera: la pantalla, el servidor que la alimenta y lo que hace falta para publicarla.",
   "temas": {
    "web": 3,
    "backend": 3,
    "prog": 2,
    "calidad": 2,
    "sql": 2,
    "cloud": 2
   }
  },
  {
   "id": "frontend",
   "nombre": "Desarrollador Frontend",
   "resumen": "La parte que la gente toca: que se entienda, que responda y que funcione en cualquier pantalla.",
   "temas": {
    "web": 3,
    "prog": 2,
    "calidad": 2,
    "backend": 1
   }
  },
  {
   "id": "backend_dev",
   "nombre": "Desarrollador Backend",
   "resumen": "Lo que hay detrás de la pantalla: las APIs, los datos y que aguante cuando entra gente de verdad.",
   "temas": {
    "backend": 3,
    "prog": 2,
    "sql": 2,
    "calidad": 2,
    "cloud": 2
   }
  }
 ],
 "pasosPorTema": {
  "sql": [
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q01",
    "t": "Fundamentos de SQL",
    "min": 240
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q02",
    "t": "Agrupar y agregar",
    "min": 180
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q03",
    "t": "Varias tablas",
    "min": 240
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q04",
    "t": "Subconsultas y CTEs",
    "min": 120
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q05",
    "t": "Fechas y texto",
    "min": 180
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q06",
    "t": "Funciones de ventana",
    "min": 120
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q08",
    "t": "Agrupar y agregar",
    "min": 120
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q12",
    "t": "Operaciones de ventana",
    "min": 60
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n02",
    "t": "Tu cuenta de prueba de 120 días",
    "min": 20
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n03",
    "t": "Hands-On Essentials",
    "min": 480
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n04",
    "t": "Snowsight, SnowSQL e Information Schema",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n08",
    "t": "Time Travel contra Fail-safe",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n09",
    "t": "Data Sharing y Marketplace",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n16",
    "t": "Lo que el C03 agregó",
    "min": 300
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n10",
    "t": "Level Up: Performance Series",
    "min": 300
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n12",
    "t": "Créditos y resource monitors",
    "min": 90
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n13",
    "t": "SQL Scripting y automatización",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n14",
    "t": "Simulacros y repaso activo",
    "min": 360
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n15",
    "t": "Study Guide oficial y registro al examen",
    "min": 60
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c04",
    "t": "CS50 SQL",
    "min": 2100
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d17",
    "t": "Refactorizar SQL heredado",
    "min": 180
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b06",
    "t": "Hive: SQL sobre Hadoop",
    "min": 240
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f08",
    "t": "Agrupar clientes con KMeans",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a12",
    "t": "Agrupar cursos con BERT",
    "min": 60
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f11",
    "t": "Parte 11 &middot; Integración y despliegue continuos",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f13",
    "t": "Parte 13 &middot; Bases de datos relacionales",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f14",
    "t": "Parte 14 &middot; Next.js",
    "min": 1020
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n06",
    "t": "Fundamentos de datos en Azure",
    "min": 480
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n07",
    "t": "Microsoft Fabric",
    "min": 240
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n08",
    "t": "Empezar en ingeniería de datos",
    "min": 300
   }
  ],
  "python": [
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q07",
    "t": "Fundamentos de DataFrames",
    "min": 240
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q09",
    "t": "Combinar DataFrames",
    "min": 120
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q10",
    "t": "Análisis en varios pasos",
    "min": 120
   },
   {
    "ruta": "sqlpy",
    "archivo": "sql-python.html",
    "id": "q11",
    "t": "Fechas, texto y lógica",
    "min": 120
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c03",
    "t": "CS50 Python",
    "min": 3000
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s04",
    "t": "Python para data science",
    "min": 1080
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s05",
    "t": "Análisis de datos con Python",
    "min": 900
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s06",
    "t": "Visualización con Python",
    "min": 600
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s11",
    "t": "Análisis exploratorio, en la práctica",
    "min": 45
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s10",
    "t": "Machine learning con Python",
    "min": 1200
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f09",
    "t": "Machine learning con Python",
    "min": 1200
   },
   {
    "ruta": "airflow",
    "archivo": "airflow.html",
    "id": "g05",
    "t": "Pythonic DAGs con la TaskFlow API",
    "min": 90
   }
  ],
  "cloud": [
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n01",
    "t": "Arquitectura y primeros conceptos",
    "min": 360
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n02",
    "t": "Tu cuenta de prueba de 120 días",
    "min": 20
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n03",
    "t": "Hands-On Essentials",
    "min": 480
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n05",
    "t": "Seguridad, gobernanza y RBAC",
    "min": 240
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n08",
    "t": "Time Travel contra Fail-safe",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n09",
    "t": "Data Sharing y Marketplace",
    "min": 120
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n16",
    "t": "Lo que el C03 agregó",
    "min": 300
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n10",
    "t": "Level Up: Performance Series",
    "min": 300
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n12",
    "t": "Créditos y resource monitors",
    "min": 90
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n14",
    "t": "Simulacros y repaso activo",
    "min": 360
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n15",
    "t": "Study Guide oficial y registro al examen",
    "min": 60
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a01",
    "t": "Contenedores, Kubernetes y OpenShift",
    "min": 1080
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a02",
    "t": "Microservicios con Istio",
    "min": 180
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a03",
    "t": "Istio a fondo",
    "min": 300
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a03a",
    "t": "AWS Application Networking Demonstrated",
    "min": 60
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a07",
    "t": "Sistemas reactivos",
    "min": 300
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a08",
    "t": "Diseño guiado por el dominio",
    "min": 300
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a09",
    "t": "Microservicios reactivos",
    "min": 360
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a04",
    "t": "Sistemas escalables y el teorema CAP",
    "min": 360
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a06",
    "t": "CQRS y event sourcing",
    "min": 360
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x13a",
    "t": "AWS Serverless Demonstrated",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c15",
    "t": "Claude with Google Cloud Vertex AI",
    "min": 480
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c16",
    "t": "The AI-Native SDLC Playbook",
    "min": 60
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f11",
    "t": "Parte 11 &middot; Integración y despliegue continuos",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f12",
    "t": "Parte 12 &middot; Contenedores",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f13",
    "t": "Parte 13 &middot; Bases de datos relacionales",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f14",
    "t": "Parte 14 &middot; Next.js",
    "min": 1020
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t10",
    "t": "Que las pruebas corran en cada cambio",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t11",
    "t": "Playwright en integración continua",
    "min": 60
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t13",
    "t": "Accesibilidad: probar que se pueda usar",
    "min": 120
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n01",
    "t": "Conceptos de nube",
    "min": 300
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n02",
    "t": "Arquitectura y servicios",
    "min": 360
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n03",
    "t": "Administración y gobernanza",
    "min": 240
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n04",
    "t": "AWS Cloud Practitioner Essentials",
    "min": 360
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n05",
    "t": "El mismo curso en Skill Builder",
    "min": 300
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n06",
    "t": "Fundamentos de datos en Azure",
    "min": 480
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n07",
    "t": "Microsoft Fabric",
    "min": 240
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n08",
    "t": "Empezar en ingeniería de datos",
    "min": 300
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n09",
    "t": "Cloud Digital Leader, de Google",
    "min": 480
   }
  ],
  "pipelines": [
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n06",
    "t": "Carga y descarga de datos",
    "min": 180
   },
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n07",
    "t": "Pipelines: Snowpipe, Streams y Tasks",
    "min": 180
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b04",
    "t": "Moving Data into Hadoop",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b05",
    "t": "Kafka para pipelines de datos",
    "min": 240
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x09a",
    "t": "Los tutoriales oficiales de Airflow",
    "min": 240
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x09",
    "t": "Airflow 101",
    "min": 150
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x14",
    "t": "Kafka para pipelines",
    "min": 240
   },
   {
    "ruta": "airflow",
    "archivo": "airflow.html",
    "id": "g01",
    "t": "Airflow 101",
    "min": 90
   },
   {
    "ruta": "airflow",
    "archivo": "airflow.html",
    "id": "g02",
    "t": "Airflow 101, versión Airflow 2",
    "min": 90
   },
   {
    "ruta": "airflow",
    "archivo": "airflow.html",
    "id": "g04",
    "t": "Airflow 101: Building Your First Workflow",
    "min": 90
   },
   {
    "ruta": "airflow",
    "archivo": "airflow.html",
    "id": "g06",
    "t": "Un pipeline de datos simple",
    "min": 90
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t12",
    "t": "Carga: qué pasa cuando entran mil",
    "min": 180
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n06",
    "t": "Fundamentos de datos en Azure",
    "min": 480
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n07",
    "t": "Microsoft Fabric",
    "min": 240
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n08",
    "t": "Empezar en ingeniería de datos",
    "min": 300
   }
  ],
  "ml": [
   {
    "ruta": "__suelto__",
    "archivo": "snowpro.html",
    "id": "n11",
    "t": "Micro-partitions y clustering",
    "min": 90
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s12",
    "t": "Métodos de clasificación",
    "min": 360
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s10",
    "t": "Machine learning con Python",
    "min": 1200
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f01",
    "t": "Introducing AI",
    "min": 60
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f02",
    "t": "AI Concepts",
    "min": 60
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f03",
    "t": "AI Ethics",
    "min": 60
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f04",
    "t": "Introducción a machine learning",
    "min": 180
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f06",
    "t": "Clasificar flores y tumores",
    "min": 30
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f07",
    "t": "Predecir consumo y precios",
    "min": 30
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f08",
    "t": "Agrupar clientes con KMeans",
    "min": 30
   },
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f09",
    "t": "Machine learning con Python",
    "min": 1200
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d05",
    "t": "Regresión lineal con PyTorch",
    "min": 420
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d06",
    "t": "Clasificación con PyTorch",
    "min": 240
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d23",
    "t": "Clasificar con Hugging Face",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a01",
    "t": "Kernel PCA",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a02",
    "t": "Segmentar imágenes con Mean Shift",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a03",
    "t": "Mezclas gaussianas",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a04",
    "t": "DBSCAN",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a05",
    "t": "PCA para reconocimiento facial",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a06",
    "t": "Quitar el fondo de un video con SVD",
    "min": 45
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a08",
    "t": "Recomendar por contenido",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a09",
    "t": "Un recomendador tipo Netflix",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a10",
    "t": "Filtrado colaborativo",
    "min": 25
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a11",
    "t": "Elegir vino con NLP",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a13",
    "t": "Recomendar perfumes con Sentence-BERT",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a14",
    "t": "Mezclas gaussianas",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a15",
    "t": "Un recomendador completo con Django",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a16",
    "t": "Transformers de Hugging Face",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a17",
    "t": "Sentimiento con Caikit",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a18",
    "t": "Clasificar reseñas de Yelp",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a19",
    "t": "Una extensión que mide el ánimo",
    "min": 120
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a20",
    "t": "Un asistente de voz",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a21",
    "t": "Qué siente la gente sobre un producto",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a22",
    "t": "Atención al cliente por voz",
    "min": 50
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a23",
    "t": "Una extensión que mide el ánimo",
    "min": 120
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a24",
    "t": "Un TicTacToe invencible",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a25",
    "t": "TicTacToe con OpenAI Gym",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a26",
    "t": "Ganarle al blackjack",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a27",
    "t": "Atención al cliente por voz",
    "min": 50
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a28",
    "t": "Por qué se va la gente de una empresa",
    "min": 45
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a29",
    "t": "Explicar un rechazo de crédito",
    "min": 60
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a30",
    "t": "Qué mueve el precio de una casa",
    "min": 45
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a31",
    "t": "Por qué a unos les va mejor",
    "min": 45
   }
  ],
  "prog": [
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c01",
    "t": "CS50 Scratch",
    "min": 3000
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c02",
    "t": "CS50x, introducción a las ciencias de la computación",
    "min": 3600
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c03",
    "t": "CS50 Python",
    "min": 3000
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c04",
    "t": "CS50 SQL",
    "min": 2100
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c05",
    "t": "CS50 R",
    "min": 1800
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c06",
    "t": "CS50 AI",
    "min": 2100
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c07",
    "t": "CS50 Web",
    "min": 3600
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c08",
    "t": "CS50 Cybersecurity",
    "min": 1500
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c09",
    "t": "CS50 Games",
    "min": 3600
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c10",
    "t": "CS50 Business",
    "min": 1800
   },
   {
    "ruta": "cs50",
    "archivo": "cs50.html",
    "id": "c11",
    "t": "CS50 for Lawyers",
    "min": 1500
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d07",
    "t": "Cómo se estructura un proyecto de verdad",
    "min": 240
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x02",
    "t": "Estructurar un proyecto real",
    "min": 240
   },
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w02",
    "t": "JavaScript desde cero",
    "min": 980
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f00",
    "t": "Parte 0 &middot; Cómo funciona una app web",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f01",
    "t": "Parte 1 &middot; Introducción a React",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f02",
    "t": "Parte 2 &middot; Hablar con el servidor",
    "min": 1020
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t04",
    "t": "Fixtures: preparar y limpiar",
    "min": 180
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t05",
    "t": "Vitest, lo mismo en JavaScript",
    "min": 120
   }
  ],
  "modelado": [
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d01",
    "t": "Qué es dbt y para qué sirve",
    "min": 60
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d02",
    "t": "dbt Fundamentals",
    "min": 360
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d03",
    "t": "Tu primer proyecto, paso a paso",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d04",
    "t": "Jaffle Shop, el proyecto de práctica",
    "min": 180
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d05",
    "t": "Jaffle Shop con DuckDB, todo local",
    "min": 60
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d06",
    "t": "Curso intensivo de dbt Core",
    "min": 180
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d16",
    "t": "Git, lo justo para dbt",
    "min": 60
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d08",
    "t": "Materializaciones",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d10",
    "t": "Jinja, macros y paquetes",
    "min": 180
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d18",
    "t": "Seeds y analyses",
    "min": 60
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d11",
    "t": "Modelos incrementales",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d12",
    "t": "Un proyecto de verdad, con el Zoomcamp",
    "min": 480
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d20",
    "t": "Despliegue a fondo",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d13",
    "t": "Snapshots",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d21",
    "t": "Exposures",
    "min": 45
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d14",
    "t": "Semantic Layer",
    "min": 240
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d22",
    "t": "dbt Mesh",
    "min": 120
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d23",
    "t": "dbt sobre Apache Iceberg",
    "min": 60
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d15",
    "t": "Prepararte para la certificación",
    "min": 90
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s09",
    "t": "Modelado predictivo",
    "min": 360
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x01",
    "t": "dbt Fundamentals",
    "min": 360
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x03",
    "t": "Materializaciones",
    "min": 120
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x05",
    "t": "Jinja, macros y paquetes",
    "min": 180
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x06",
    "t": "Modelos incrementales",
    "min": 120
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x07",
    "t": "Snapshots",
    "min": 120
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x08",
    "t": "Un proyecto de verdad, con el Zoomcamp",
    "min": 480
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x10",
    "t": "DAG Authoring",
    "min": 135
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x13",
    "t": "Terraform sobre AWS",
    "min": 120
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x13b",
    "t": "AWS Incident Response Demonstrated",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l26",
    "t": "Agentes con esquema, con PydanticAI",
    "min": 45
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n06",
    "t": "Fundamentos de datos en Azure",
    "min": 480
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n07",
    "t": "Microsoft Fabric",
    "min": 240
   },
   {
    "ruta": "nube",
    "archivo": "nube.html",
    "id": "n08",
    "t": "Empezar en ingeniería de datos",
    "min": 300
   }
  ],
  "calidad": [
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d09",
    "t": "Testing a fondo",
    "min": 180
   },
   {
    "ruta": "dbt",
    "archivo": "dbt.html",
    "id": "d19",
    "t": "Unit tests",
    "min": 60
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x04",
    "t": "Testing a fondo",
    "min": 180
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f03",
    "t": "Parte 3 &middot; Un servidor con Node y Express",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f04",
    "t": "Parte 4 &middot; Probar el servidor y manejar usuarios",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f05",
    "t": "Parte 5 &middot; Probar el frontend y varias pantallas",
    "min": 1020
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t01",
    "t": "El sílabo de ISTQB Foundation",
    "min": 360
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t02",
    "t": "La pirámide de pruebas, de Martin Fowler",
    "min": 45
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t03",
    "t": "pytest, de cero",
    "min": 180
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t04",
    "t": "Fixtures: preparar y limpiar",
    "min": 180
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t05",
    "t": "Vitest, lo mismo en JavaScript",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t06",
    "t": "Playwright, la primera prueba",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t07",
    "t": "Encontrar elementos sin que se rompa mañana",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t08",
    "t": "Cypress, la otra escuela",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t09",
    "t": "Probar APIs",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t10",
    "t": "Que las pruebas corran en cada cambio",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t11",
    "t": "Playwright en integración continua",
    "min": 60
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t13",
    "t": "Accesibilidad: probar que se pueda usar",
    "min": 120
   }
  ],
  "bigdata": [
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b01",
    "t": "Big Data 101",
    "min": 180
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b02",
    "t": "Hadoop 101",
    "min": 1200
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b03",
    "t": "MapReduce y YARN",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b04",
    "t": "Moving Data into Hadoop",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b06",
    "t": "Hive: SQL sobre Hadoop",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b07",
    "t": "Spark Fundamentals I",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b08",
    "t": "Spark Fundamentals II",
    "min": 300
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b09",
    "t": "Spark MLlib",
    "min": 300
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b10",
    "t": "GraphX",
    "min": 180
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b11",
    "t": "Spark desde R",
    "min": 180
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b12",
    "t": "Scala 101",
    "min": 360
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b13",
    "t": "Spark con Scala",
    "min": 480
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b14",
    "t": "Data Science con Scala",
    "min": 360
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b15",
    "t": "Oozie",
    "min": 360
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b16",
    "t": "ZooKeeper",
    "min": 240
   },
   {
    "ruta": "bigdata",
    "archivo": "bigdata.html",
    "id": "b17",
    "t": "Solr 101",
    "min": 180
   },
   {
    "ruta": "arquitectura",
    "archivo": "arquitectura.html",
    "id": "a05",
    "t": "Mensajería distribuida",
    "min": 360
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x11",
    "t": "Spark Fundamentals I",
    "min": 240
   },
   {
    "ruta": "subirnivel",
    "archivo": "subir-nivel.html",
    "id": "x12",
    "t": "Spark Fundamentals II",
    "min": 300
   }
  ],
  "stats": [
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s01",
    "t": "Data Science 101",
    "min": 660
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s02",
    "t": "Data Science Methodology",
    "min": 240
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s03",
    "t": "Data Science Tools",
    "min": 900
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s07",
    "t": "R para data science",
    "min": 360
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d05",
    "t": "Regresión lineal con PyTorch",
    "min": 420
   }
  ],
  "viz": [
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s06",
    "t": "Visualización con Python",
    "min": 600
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s07",
    "t": "R para data science",
    "min": 360
   },
   {
    "ruta": "data_science",
    "archivo": "data-science.html",
    "id": "s08",
    "t": "Visualización con R",
    "min": 360
   }
  ],
  "deep": [
   {
    "ruta": "aifund",
    "archivo": "ai-fundamentos.html",
    "id": "f05",
    "t": "Refuerzo y deep learning, lo esencial",
    "min": 120
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d01",
    "t": "Fundamentos de deep learning",
    "min": 180
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d02",
    "t": "Deep learning con TensorFlow",
    "min": 180
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d03",
    "t": "Acelerar con GPUs",
    "min": 300
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d04",
    "t": "Tensores y datos",
    "min": 180
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d05",
    "t": "Regresión lineal con PyTorch",
    "min": 420
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d06",
    "t": "Clasificación con PyTorch",
    "min": 240
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d07",
    "t": "Armar una red neuronal",
    "min": 420
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d08",
    "t": "Redes convolucionales",
    "min": 240
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d09",
    "t": "Empezar con PyTorch",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d10",
    "t": "Predecir precios con LSTM",
    "min": 30
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d11",
    "t": "Desplegar visión sin servidor",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d12",
    "t": "Detección de objetos con Faster R-CNN",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d13",
    "t": "Segmentación médica con U-Net",
    "min": 30
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d14",
    "t": "Vision Transformers",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d15",
    "t": "Generar personajes con DCGAN",
    "min": 120
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d16",
    "t": "Retratos con U-2 Net",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d17",
    "t": "Vision Transformers",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d18",
    "t": "Desplegar visión sin servidor",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d19",
    "t": "Detección de cáncer en imágenes",
    "min": 45
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d20",
    "t": "Empezar con PyTorch",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d21",
    "t": "Generar personajes con DCGAN",
    "min": 120
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d22",
    "t": "Detección de objetos con Faster R-CNN",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d24",
    "t": "Entrenar un reconocedor de imágenes",
    "min": 40
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d25",
    "t": "Transferencia de estilo con CycleGAN",
    "min": 60
   },
   {
    "ruta": "deeplearning",
    "archivo": "deep-learning.html",
    "id": "d26",
    "t": "Generar personajes con DCGAN",
    "min": 120
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a02",
    "t": "Segmentar imágenes con Mean Shift",
    "min": 30
   },
   {
    "ruta": "mlaplicado",
    "archivo": "ml-aplicado.html",
    "id": "a07",
    "t": "Buscar imágenes con NMF",
    "min": 30
   }
  ],
  "llm": [
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c01",
    "t": "AI Fluency: Framework & Foundations",
    "min": 240
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c02",
    "t": "AI Capabilities and Limitations",
    "min": 180
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c03",
    "t": "Claude 101",
    "min": 120
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c04",
    "t": "Introduction to Claude Cowork",
    "min": 120
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c05",
    "t": "Claude Code 101",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c06",
    "t": "Claude Code in Action",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c07",
    "t": "AI Fluency for Builders",
    "min": 180
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c08",
    "t": "Claude Platform 101",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c09",
    "t": "Building with the Claude API",
    "min": 540
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c10",
    "t": "Introduction to Model Context Protocol",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c11",
    "t": "Model Context Protocol: Advanced Topics",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c12",
    "t": "Introduction to Subagents",
    "min": 45
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c13",
    "t": "Introduction to Agent Skills",
    "min": 60
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c14",
    "t": "Claude with Amazon Bedrock",
    "min": 480
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c15",
    "t": "Claude with Google Cloud Vertex AI",
    "min": 480
   },
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c16",
    "t": "The AI-Native SDLC Playbook",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l01",
    "t": "Prompt engineering",
    "min": 300
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l02",
    "t": "El oficio del prompt",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l03",
    "t": "Tu propio chat con modelos abiertos",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l04",
    "t": "Poner límites al modelo",
    "min": 120
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l05",
    "t": "Resumir documentos privados",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l06",
    "t": "Un agente de búsqueda con LlamaIndex",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l07",
    "t": "Preguntas y respuestas con fundamento",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l08",
    "t": "RAG sobre datos de la web",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l09",
    "t": "Resumir videos de YouTube",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l10",
    "t": "Un bot que rompe el hielo",
    "min": 40
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l11",
    "t": "Un agente ReAct desde cero",
    "min": 90
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l12",
    "t": "Un asistente de matemática que no inventa",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l13",
    "t": "Tus propias herramientas",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l14",
    "t": "Razonar y actuar con LangGraph",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l15",
    "t": "Que el agente revise su trabajo",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l16",
    "t": "Reflexion, con validación externa",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l17",
    "t": "Un agente de investigación",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l18",
    "t": "Introducción a los agentes",
    "min": 180
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l19",
    "t": "Varios agentes con CrewAI",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l20",
    "t": "CrewAI de cero",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l21",
    "t": "Un asistente de matemática que no inventa",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l22",
    "t": "Tus propias herramientas",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l23",
    "t": "Un agente ReAct desde cero",
    "min": 90
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l24",
    "t": "Patrones de flujo con LangGraph",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l25",
    "t": "Agentes para salud, con AutoGen",
    "min": 30
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l26",
    "t": "Agentes con esquema, con PydanticAI",
    "min": 45
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l27",
    "t": "Conversar con tus documentos",
    "min": 60
   },
   {
    "ruta": "llmagentes",
    "archivo": "llm-agentes.html",
    "id": "l27a",
    "t": "AWS Agentic AI Demonstrated",
    "min": 60
   }
  ],
  "mlops": [
   {
    "ruta": "claude",
    "archivo": "claude.html",
    "id": "c16",
    "t": "The AI-Native SDLC Playbook",
    "min": 60
   }
  ],
  "web3": [
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w01",
    "t": "Introducción a blockchain",
    "min": 860
   },
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w03",
    "t": "Solidity",
    "min": 220
   },
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w04",
    "t": "Ethereum Bootcamp",
    "min": 1820
   },
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w05",
    "t": "Account Abstraction",
    "min": 180
   },
   {
    "ruta": "web3",
    "archivo": "web3.html",
    "id": "w06",
    "t": "Cuentas modulares",
    "min": 90
   }
  ],
  "web": [
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f00",
    "t": "Parte 0 &middot; Cómo funciona una app web",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f01",
    "t": "Parte 1 &middot; Introducción a React",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f02",
    "t": "Parte 2 &middot; Hablar con el servidor",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f06",
    "t": "Parte 6 &middot; Estado que aguanta una app grande",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f07",
    "t": "Parte 7 &middot; Tus propias herramientas",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f08",
    "t": "Parte 8 &middot; GraphQL",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f09",
    "t": "Parte 9 &middot; TypeScript",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f10",
    "t": "Parte 10 &middot; React Native",
    "min": 1020
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t06",
    "t": "Playwright, la primera prueba",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t07",
    "t": "Encontrar elementos sin que se rompa mañana",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t08",
    "t": "Cypress, la otra escuela",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t09",
    "t": "Probar APIs",
    "min": 120
   }
  ],
  "backend": [
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f03",
    "t": "Parte 3 &middot; Un servidor con Node y Express",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f04",
    "t": "Parte 4 &middot; Probar el servidor y manejar usuarios",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f05",
    "t": "Parte 5 &middot; Probar el frontend y varias pantallas",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f08",
    "t": "Parte 8 &middot; GraphQL",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f09",
    "t": "Parte 9 &middot; TypeScript",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f10",
    "t": "Parte 10 &middot; React Native",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f11",
    "t": "Parte 11 &middot; Integración y despliegue continuos",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f13",
    "t": "Parte 13 &middot; Bases de datos relacionales",
    "min": 1020
   },
   {
    "ruta": "fullstack",
    "archivo": "fullstack.html",
    "id": "f14",
    "t": "Parte 14 &middot; Next.js",
    "min": 1020
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t06",
    "t": "Playwright, la primera prueba",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t07",
    "t": "Encontrar elementos sin que se rompa mañana",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t08",
    "t": "Cypress, la otra escuela",
    "min": 120
   },
   {
    "ruta": "testing",
    "archivo": "testing.html",
    "id": "t09",
    "t": "Probar APIs",
    "min": 120
   }
  ]
 }
};
