# -*- coding: utf-8 -*-
"""temas.js: los temas, los puestos y que paso ensena que.

   Es la pieza de fondo del path desde el CV. El ROADMAP lo dice en el
   punto 3 del item 10: sin una definicion de cada puesto, cualquier
   analisis devuelve algo generico. Esto es esa definicion.

   Tres cosas viven aca:

   1. TEMAS   - el vocabulario. Cada tema trae las senales con las que
                se lo reconoce en un CV (como lo escribe la gente, no
                como nos gustaria que lo escriba).
   2. PUESTOS - que temas pide cada puesto y con cuanta profundidad.
                Son los roles del gimnasio de entrevistas, con la misma
                taxonomia a proposito: dos listas de puestos distintas
                serian dos productos distintos.
   3. El indice tema -> pasos, que se calcula leyendo pasos.js.

   Los puestos y las senales se escriben a mano y se revisan. El
   indice se genera, porque las rutas cambian.
"""
import io, os, json, sys, unicodedata

AQUI = u"C:/Users/Luca/Desktop/snowflake path/"

# ---------------------------------------------------------------- temas
# (clave, nombre, [senales de CV], [reglas sobre el titulo del paso])
# Todo ya normalizado: sin acentos y en minuscula.
# Las senales que AFIRMAN, en vez de mencionar. Son de dos clases y
# valen igual:
#
#   - Nombres propios de herramientas. Nadie escribe "Airflow" en su CV
#     sin haber tocado Airflow.
#   - Titulos de puesto. Decir que sos desarrollador es decir que
#     programas; decir que sos data scientist es decir que entrenas
#     modelos.
#
# Las genericas -"pipeline", "software", "consultas"- no dicen nada
# parecido: aparecen en cualquier CV. Por eso esta lista existe y no es
# simplemente "todas las senales".
FUERTES = [
 "postgres", "mysql", "sql server", "oracle", "bigquery", "redshift",
 "snowflake", "plsql", "pandas", "numpy", "jupyter", "django", "flask",
 "fastapi", "scipy", "leetcode", "git", "javascript", "java", "scratch",
 "dbt", "kimball", "inmon", "star schema", "data vault", "airflow",
 "dagster", "prefect", "kafka", "nifi", "scrum", "bpmn", "jira",
 "kanban", "pytest", "great expectations", "aws", "azure", "gcp",
 "google cloud", "lambda", "terraform", "docker", "kubernetes",
 "openshift", "hadoop", "spark", "pyspark", "mapreduce", "hive",
 "hbase", "yarn", "databricks", "flink", "scikit", "sklearn", "xgboost",
 "random forest", "tensorflow", "pytorch", "keras", "cnn", "rnn", "gpt",
 "openai", "claude", "langchain", "rag", "bedrock", "mlflow",
 "kubeflow", "sagemaker", "feature store", "tableau", "power bi",
 "powerbi", "looker", "metabase", "superset", "matplotlib", "seaborn",
 "plotly", "typescript", "react", "angular", "vue", "svelte", "next.js",
 "nextjs", "tailwind", "jquery", "redux", "sass", "webpack", "vite",
 "react native", "flutter", "bootstrap", "graphql", "node", "nodejs",
 "node.js", "express", "spring", "spring boot", ".net", "laravel",
 "rails", "nestjs", "jwt", "oauth", "solidity", "ethereum", "defi",
 "desarrollador", "developer", "programador", "software engineer",
 "ingeniero de software", "full stack", "fullstack", "data scientist",
 "cientifico de datos", "analista funcional",
]

TEMAS = [
 ("sql", u"SQL",
  ["sql", "postgres", "mysql", "sql server", "oracle", "bigquery", "redshift",
   "snowflake", "consultas", "queries", "stored procedure", "plsql"],
  ["sql", "consulta", "subconsulta", "cte", "join", "agrupar", "agregar",
   "ventana", "window", "information schema", "snowsql"]),

 ("python", u"Python",
  ["python", "pandas", "numpy", "jupyter", "notebook", "django", "flask",
   "fastapi", "scipy"],
  ["python", "pandas", "numpy", "jupyter", "dataframe"]),

 ("prog", u"Fundamentos de programación",
  # Los titulos de puesto afirman el tema entero, igual que "data
  # scientist" para machine learning: decir que sos desarrollador es
  # decir que programas. Sin esto, a un senior developer le
  # preguntabamos si programa.
  ["algoritmo", "estructura de datos", "leetcode", "complejidad", "big o",
   "programacion", "software", "git", "javascript", "java", "scratch",
   "desarrollador", "developer", "programador", "software engineer",
   "ingeniero de software", "full stack", "fullstack"],
  ["cs50", "scratch", "algoritmo", "estructura", "javascript", "programacion",
   "introduccion a las ciencias"]),

 ("modelado", u"Modelado de datos",
  # "warehouse", "staging" y "marts" sueltos. Un CV que dice "Modelo
  # el warehouse en dbt sobre Snowflake: capas staging, intermediate y
  # marts, con tests, documentacion y snapshots" tocaba una sola senal
  # -"dbt"- porque "modelado" no esta en "Modelo" y "data warehouse"
  # no esta en "el warehouse". Quedaba en nivel 1, o sea alguien que
  # oyo hablar de modelar datos, y por eso a un data engineer con
  # cuatro anios se le ofrecia la ruta de dbt, que es la herramienta
  # que usa todos los dias.
  ["modelado", "data model", "star schema", "kimball", "inmon", "normalizacion",
   "dimensional", "data warehouse", "datawarehouse", "dwh", "data vault", "dbt",
   "warehouse", "staging", "marts"],
  ["modeling", "modelado", "dbt", "jaffle", "materializacion", "dimension",
   "esquema", "warehouse", "semantic", "jinja", "macro"]),

 ("pipelines", u"Pipelines y orquestación",
  # "dag" y "dags": es como se nombra lo que uno arma en Airflow, y
  # el CV de prueba dice "con DAGs que corren a diario" sin que nadie
  # lo contara. Con airflow y etl nomas quedaba en nivel 2, o sea que
  # a alguien que mantiene pipelines todos los dias se le ofrecia la
  # ruta de Airflow.
  ["airflow", "etl", "elt", "pipeline", "ingesta", "orquestacion", "dagster",
   "prefect", "kafka", "nifi", "streaming", "batch", "dag", "dags"],
  ["airflow", "pipeline", "kafka", "ingesta", "moving data", "streaming",
   "orquest", "etl", "elt", "snowpipe", "carga"]),

 ("producto", u"Producto y requisitos",
  ["requerimiento", "requisito", "historia de usuario", "backlog", "scrum",
   "product owner", "analista funcional", "bpmn", "casos de uso", "stakeholder",
   "relevamiento", "jira", "kanban", "agile", "ágil"],
  ["requisito", "historia", "backlog", "scrum", "proceso", "negocio",
   "bpmn", "producto", "relevamiento"]),

 ("calidad", u"Calidad y testing",
  ["testing", "test unitario", "pytest", "calidad de datos", "great expectations",
   "data quality", "observabilidad", "monitoreo"],
  ["testing", "test", "calidad", "observabilidad", "monitoreo"]),

 ("cloud", u"Nube e infraestructura",
  ["aws", "azure", "gcp", "google cloud", "cloud", "lambda", "terraform",
   "docker", "kubernetes", "openshift", "serverless", "microservicio",
   "devops"],
  ["contenedor", "kubernetes", "openshift", "istio", "microservicio", "cloud",
   "serverless", "docker", "arquitectura", "reactivo", "dominio", "sistemas",
   "gobernanza", "rbac", "seguridad"]),

 ("bigdata", u"Big data",
  ["hadoop", "spark", "pyspark", "mapreduce", "hive", "hbase", "yarn",
   "big data", "databricks", "flink"],
  ["hadoop", "spark", "mapreduce", "yarn", "big data", "hive", "hbase",
   "distribuid"]),

 ("stats", u"Estadística y experimentos",
  ["estadistica", "statistics", "ab testing", "experimento", "hipotesis",
   "regresion", "probabilidad", "inferencia", "significancia"],
  # "experimento" esta en la lista del CV y NO en la de los titulos.
  # En un CV, "diseñe experimentos" quiere decir estadistica. En el
  # titulo de un curso quiere decir otra cosa: "Seguimiento de
  # experimentos", de la ruta de MLOps, es registrar corridas de
  # entrenamiento, y con esa senal la ruta de MLOps quedaba cubriendo
  # estadistica. Es el mismo tipo de contaminacion que ya nos paso con
  # "react" en "sistemas reactivos".
  ["estadistica", "hipotesis", "probabilidad", "inferencia",
   "regresion lineal", "metodologia"]),

 ("ml", u"Machine learning",
  # "entreno modelos" y el titulo del puesto. Un CV que dice "Data
  # scientist. Python, scikit-learn, entreno modelos" tocaba una sola
  # senal -"scikit"- y quedaba en nivel 1, o sea alguien que apenas
  # oyo hablar de machine learning. Con eso, a un ML Engineer se le
  # ofrecia AI: fundamentos -aprende ML y Python- en vez de MLOps, que
  # es lo unico que ese CV dice que le falta.
  #
  # Entrenar modelos es hacer machine learning, y decir que sos data
  # scientist tambien. Las dos son afirmaciones directas, y si vienen
  # negadas las agarra la maquinaria de negacion como cualquier otra.
  ["machine learning", "scikit", "sklearn", "xgboost", "random forest",
   "clasificacion", "clustering", "modelo predictivo", "feature engineering",
   "entreno modelos", "entrenar modelos", "entrenamiento de modelos",
   "data scientist", "cientifico de datos"],
  ["machine learning", "clasific", "clustering", "regresion", "pca", "kmeans",
   "k-means", "dbscan", "mean shift", "gaussian", "arbol", "bosque", "svm",
   "supervisado", "no supervisado", "recomend"]),

 ("deep", u"Deep learning",
  ["deep learning", "tensorflow", "pytorch", "keras", "red neuronal",
   "neural network", "cnn", "rnn", "transformer", "computer vision", "nlp"],
  ["deep learning", "tensorflow", "pytorch", "keras", "neuronal", "tensor",
   "cnn", "rnn", "gpu", "vision", "imagen"]),

 ("llm", u"LLMs y agentes",
  ["llm", "gpt", "openai", "claude", "langchain", "rag", "prompt", "embedding",
   "vector", "agente", "bedrock", "generativa", "genai"],
  ["prompt", "llm", "modelo abierto", "agente", "rag", "embedding", "vectorial",
   "chat", "documento privado", "resumir", "token", "fine",
   # Los cursos de Anthropic tienen el titulo en ingles y ninguna de
   # las de arriba les pegaba: quedaban sin tema.
   "claude", "agent", "subagent", "mcp", "model context protocol",
   "ai fluency", "bedrock", "copilot"]),

 ("mlops", u"MLOps y puesta en producción",
  ["mlops", "mlflow", "kubeflow", "sagemaker", "model serving", "deploy",
   "produccion", "inferencia", "drift", "feature store"],
  ["produccion", "serving", "deploy", "mlops", "inferencia", "api del modelo"]),

 ("viz", u"Visualización",
  ["tableau", "power bi", "powerbi", "looker", "metabase", "superset",
   "matplotlib", "seaborn", "plotly", "dashboard", "visualizacion"],
  ["visualiza", "dashboard", "grafico", "tableau", "power bi"]),

 ("web", u"Desarrollo web",
  ["javascript", "typescript", "react", "angular", "vue", "svelte", "html",
   "css", "frontend", "front-end", "front end", "next.js", "nextjs", "tailwind",
   "jquery", "redux", "sass", "webpack", "vite", "spa", "responsive",
   "react native", "flutter", "bootstrap"],
  # Sin reglas de titulo, a proposito: el matcheo es por subcadena y
  # "react" agarraba "sistemas reactivos" y "un agente ReAct desde
  # cero". La ruta de web declara su tema por tramo en POR_TRAMO, que
  # es explicito; aca estas reglas solo podian ensuciar otras rutas.
  []),

 ("backend", u"Backend y APIs",
  ["api", "rest", "restful", "graphql", "node", "nodejs", "node.js", "express",
   "backend", "back-end", "back end", "endpoint", "spring", "spring boot",
   ".net", "laravel", "rails", "nestjs", "jwt", "oauth", "autenticacion",
   "microservicios", "http"],
  # Idem: "api" agarraba "Building with the Claude API" y "servidor"
  # agarraba "Desplegar vision sin servidor".
  []),

 ("web3", u"Blockchain y Web3",
  ["blockchain", "solidity", "ethereum", "web3", "smart contract",
   "cripto", "defi", "wallet"],
  ["blockchain", "solidity", "ethereum", "web3", "contrato",
   "account abstraction", "cripto"]),
]

# Rutas que no entran al indice del CV. La de Data Engineer es un mapa
# de areas, no una lista de cursos: sus nodos duran veinte y cuarenta
# horas porque cada uno resume una ruta entera que ya esta desglosada
# en otro lado.
SIN_INDICE = {"de"}

# Cuando el titulo no delata nada, el paso hereda el tema de su tramo,
# y si el tramo no dice nada, el de la ruta entera. El tramo importa:
# en "SQL y Python" el acto 1 es SQL y el 2 es Python, y heredar de la
# ruta le ponia los dos temas a todos los pasos.
# Se etiqueta lo que el tramo ENSENA, no lo que toca.
#
# Paso al reves y costo caro: las rutas nuevas quedaron etiquetadas
# con todo lo que rozaban -testing con web, backend y cloud porque se
# prueban aplicaciones web, APIs y se corre en GitHub Actions- y la
# ruta de testing termino cubriendo cinco de los cinco temas que pide
# Cloud Engineer. Un CV de sysadmin que decia "nunca use la nube"
# recibia la ruta de testing en vez de la de la nube.
#
# Aprender Playwright no es aprender desarrollo web. Si etiquetas lo
# que roza, la ruta empieza a competir por puestos que no sirve.
POR_TRAMO = {
 ("sqlpy", 1):        ["sql"],
 ("sqlpy", 2):        ["python"],
 ("data_science", 1): ["stats"],
 ("data_science", 2): ["python"],
 ("data_science", 3): ["viz", "stats"],
 ("data_science", 4): ["ml"],
 # Trabajar con Claude: cada tramo ensena algo distinto, asi que una
 # sola etiqueta para los cinco seria mentir sobre lo que cubre.
 ("claude", 1):       ["llm"],
 ("claude", 2):       ["llm", "prog"],
 ("claude", 3):       ["llm", "python"],
 ("claude", 4):       ["llm", "python"],
 ("claude", 5):       ["llm", "cloud", "mlops"],
 # Full Stack Open: cada tramo ensena algo distinto y los titulos
 # estan en espanol pero no usan el vocabulario de datos, asi que
 # sin esto los quince pasos caerian en el mismo saco.
 # Testing: cada tramo suma calidad, que es lo suyo, y ademas el
 # mundo sobre el que se prueba en ese tramo.
 # Credenciales de nube: los tres primeros tramos son nube pura, y
 # el de datos cruza con lo que el sitio ya ensena.
 # Analista funcional. El tema "producto" es nuevo: el metodo de
 # traducir lo que el negocio necesita no encajaba en ninguno de los
 # diecisiete que habia, y meterlo en "calidad" o en "modelado"
 # habria sido acomodarlo para no crear uno.
 # MLOps: los cuatro tramos son mlops, y los que tocan nube y
 # pruebas lo dicen tambien, porque es lo que de verdad ensenan.
 ("mlops", 1):        ["mlops"],
 ("mlops", 2):        ["mlops"],
 ("mlops", 3):        ["mlops"],
 ("mlops", 4):        ["mlops", "calidad"],

 # Visualizacion: el primer tramo son principios, los otros dos
 # herramientas. El de Power BI suma modelado, que es la mitad.
 ("viz", 1):          ["viz"],
 ("viz", 2):          ["viz", "modelado"],
 ("viz", 3):          ["viz"],

 ("funcional", 1):    ["producto"],
 ("funcional", 2):    ["producto"],
 ("funcional", 3):    ["producto"],
 ("funcional", 4):    ["sql", "viz"],

 ("nube", 1):         ["cloud"],
 ("nube", 2):         ["cloud"],
 ("nube", 3):         ["cloud", "modelado", "pipelines"],
 ("nube", 4):         ["cloud"],

 ("testing", 1):      ["calidad"],
 ("testing", 2):      ["calidad", "prog"],
 ("testing", 3):      ["calidad"],
 ("testing", 4):      ["calidad"],

 ("fullstack", 1):    ["web", "prog"],
 ("fullstack", 2):    ["backend", "calidad"],
 ("fullstack", 3):    ["web"],
 ("fullstack", 4):    ["web", "backend"],
 ("fullstack", 5):    ["cloud", "backend", "sql"],
}

POR_RUTA = {
 "sqlpy":        ["sql", "python"],
 "de":           ["pipelines", "modelado"],
 "__suelto__":   ["cloud", "sql"],
 "cs50":         ["prog"],
 "dbt":          ["modelado"],
 "bigdata":      ["bigdata"],
 "data_science": ["stats", "python"],
 "arquitectura": ["cloud"],
 "subirnivel":   ["modelado"],
 "aifund":       ["ml"],
 "deeplearning": ["deep"],
 "llmagentes":   ["llm"],
 "claude":       ["llm"],
 "mlaplicado":   ["ml"],
 "web3":         ["web3"],
 "fullstack":    ["web", "backend"],
}

# -------------------------------------------------------------- puestos
# Cuanto pide cada puesto de cada tema: 3 es el dia a dia, 2 se usa
# seguido, 1 se toca. Lo que no figura, no se pide.
PUESTOS = [
 {"id": "data_engineer", "nombre": u"Data Engineer",
  "resumen": u"Construir y sostener los pipelines y el modelo de datos del que vive todo el resto.",
  "distingue": u"Mueve y ordena los datos para que otros los usen. No los analiza ni entrena modelos con ellos.",
  "temas": {"sql": 3, "python": 3, "modelado": 3, "pipelines": 3, "cloud": 2,
            "calidad": 2, "bigdata": 2, "prog": 1}},

 {"id": "data_analyst", "nombre": u"Data Analyst",
  "resumen": u"Responder preguntas del negocio con datos y dejar claro qué significa la respuesta.",
  "distingue": u"Usa los datos que otro preparó. Su producto es una respuesta, no un sistema que queda corriendo.",
  "temas": {"sql": 3, "viz": 3, "stats": 2, "python": 2, "modelado": 1,
            "prog": 1}},

 {"id": "data_scientist", "nombre": u"Data Scientist",
  "resumen": u"Estadística, experimentos y modelos predictivos para decidir con evidencia.",
  "distingue": u"Investiga y prueba hipótesis. Llevar a producción lo que encuentra es trabajo del ML Engineer.",
  "temas": {"stats": 3, "ml": 3, "python": 3, "sql": 2, "viz": 2, "deep": 1,
            "prog": 1}},

 {"id": "ml_engineer", "nombre": u"ML Engineer",
  "resumen": u"Llevar modelos a producción y que sigan funcionando cuando nadie los mira.",
  "distingue": u"Lo que el científico entrenó, éste lo hace correr todos los días y avisar cuando falla.",
  "temas": {"ml": 3, "mlops": 3, "python": 3, "deep": 2, "cloud": 2, "prog": 2,
            "pipelines": 2, "sql": 1}},

 {"id": "ai_engineer", "nombre": u"AI Engineer",
  "resumen": u"Aplicaciones sobre modelos de lenguaje: recuperación, agentes y sus límites.",
  "distingue": u"No entrena modelos: usa los que ya existen y arma algo alrededor que resuelva un problema.",
  "temas": {"llm": 3, "python": 3, "prog": 2, "cloud": 2, "ml": 1, "deep": 1,
            "mlops": 1}},

 {"id": "bigdata_engineer", "nombre": u"Big Data Engineer",
  "resumen": u"Procesar datos que no entran en una m\u00e1quina: Spark, streaming y sistemas distribuidos.",
  "distingue": u"Es Data Engineer cuando el volumen ya no deja hacerlo de la forma simple.",
  "temas": {"bigdata": 3, "sql": 3, "python": 3, "cloud": 2,
            "pipelines": 2, "modelado": 2, "prog": 1}},

 {"id": "cloud_engineer", "nombre": u"Cloud Engineer",
  "resumen": u"Sostener la infraestructura sobre la que corre todo lo dem\u00e1s, y que no cueste una fortuna.",
  "distingue": u"No escribe la aplicaci\u00f3n: hace que tenga d\u00f3nde correr, que aguante y que se pueda pagar.",
  "temas": {"cloud": 3, "prog": 2, "calidad": 2, "backend": 1,
            "pipelines": 1}},

 {"id": "fullstack", "nombre": u"Desarrollador Full Stack",
  "resumen": u"Construir la aplicación entera: la pantalla, el servidor que la alimenta y lo que hace falta para publicarla.",
  "distingue": u"Toca las dos mitades. Sabe menos de cada una que el especialista, y llega solo hasta el final.",
  "temas": {"web": 3, "backend": 3, "prog": 2, "calidad": 2, "sql": 2,
            "cloud": 2}},

 {"id": "frontend", "nombre": u"Desarrollador Frontend",
  "resumen": u"La parte que la gente toca: que se entienda, que responda y que funcione en cualquier pantalla.",
  "distingue": u"Termina donde empieza el servidor. Su problema es que se entienda y funcione en cualquier pantalla.",
  "temas": {"web": 3, "prog": 2, "calidad": 2, "backend": 1}},

 {"id": "backend_dev", "nombre": u"Desarrollador Backend",
  "resumen": u"Lo que hay detrás de la pantalla: las APIs, los datos y que aguante cuando entra gente de verdad.",
  "distingue": u"Nunca se ve, y si falla se nota en todo. Su problema es que aguante y que los datos estén bien.",
  "temas": {"backend": 3, "prog": 2, "sql": 2, "calidad": 2, "cloud": 2}},

 {"id": "web3_dev", "nombre": u"Desarrollador Web3",
  "resumen": u"Contratos inteligentes y aplicaciones sobre blockchain, de Solidity para arriba.",
  "distingue": u"Es desarrollo backend donde un error no se arregla con otro deploy: el contrato ya est\u00e1 publicado.",
  "temas": {"web3": 3, "prog": 3, "web": 2, "backend": 2, "calidad": 2,
            "cloud": 1}},

 {"id": "tester", "nombre": u"QA / Tester",
  "resumen": u"Encontrar lo que se rompe antes que el usuario, y dejarlo comprobado solo.",
  "distingue": u"No construye: rompe a propósito, y deja escrito cómo se rompió para que no vuelva a pasar.",
  "temas": {"calidad": 3, "prog": 2, "web": 2, "backend": 2, "cloud": 1,
            "sql": 1}},

 {"id": "analista_funcional", "nombre": u"Analista funcional",
  "resumen": u"Traducir lo que el negocio necesita a algo que un equipo puede construir, y de vuelta.",
  "distingue": u"No programa. Su trabajo es que lo que se construya sea lo que hacía falta.",
  "temas": {"producto": 3, "sql": 2, "viz": 2, "modelado": 1, "calidad": 1}},
]



def limpiar(s):
    """Sin acentos y en minuscula, que es como conviene comparar."""
    s = unicodedata.normalize("NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def temas_de(titulo, clave_ruta, acto):
    t = limpiar(titulo)
    out = []
    for clave, _n, _senales, reglas in TEMAS:
        for r in reglas:
            if r in t:
                out.append(clave)
                break
    if not out:
        out = list(POR_TRAMO.get((clave_ruta, acto)) or POR_RUTA.get(clave_ruta, []))
    return out


def main():
    p = AQUI + u"pasos.js"
    if not os.path.exists(p):
        print("  ABORTA: falta pasos.js, corre build-pasos.py primero")
        sys.exit(1)
    crudo = io.open(p, encoding="utf-8").read()
    rutas = json.loads(crudo[crudo.index("["):crudo.rindex(";")])

    indice, sin_tema, total = {}, [], 0
    for r in rutas:
        for paso in r["pasos"]:
            total += 1
            ts = temas_de(paso["t"], r["clave"], paso.get("act", 0))
            if r["clave"] in SIN_INDICE:
                continue
            if not ts:
                sin_tema.append((r["clave"], paso["t"]))
            for t in ts:
                indice.setdefault(t, []).append({
                    "ruta": r["clave"], "archivo": r["archivo"],
                    "id": paso["id"], "t": paso["t"], "min": paso["min"],
                })

    # Un tema sin un solo paso es un tema que no podemos ensenar: mejor
    # saberlo aca que descubrirlo cuando alguien lo necesite.
    vacios = [c for c, n, s, g in TEMAS if not indice.get(c)]

    # Y un tema que un puesto pide pero no existe seria un hueco mudo.
    claves = set(c for c, n, s, g in TEMAS)
    for pu in PUESTOS:
        falta = [t for t in pu["temas"] if t not in claves]
        if falta:
            print("  ABORTA: %s pide temas que no existen: %s" % (pu["id"], falta))
            sys.exit(1)

    salida = {
        "temas": [{"id": c, "nombre": n, "senales": s} for c, n, s, g in TEMAS],
        # Cuales de esas senales afirman en vez de mencionar. Van
        # aparte y no dentro de cada tema porque la regla no es del
        # tema, es de la palabra.
        "fuertes": FUERTES,
        "puestos": PUESTOS,
        "pasosPorTema": indice,
    }
    js = (u"/* ============================================================\n"
          u"   temas.js\n\n"
          u"   Lo genera build-temas.py. No se edita a mano.\n\n"
          u"   Los temas y los puestos se definen alla y se revisan; el\n"
          u"   indice de que paso ensena que se calcula desde pasos.js.\n"
          u"   ============================================================ */\n"
          u"var TEMAS = " + json.dumps(salida, ensure_ascii=False, indent=1) + u";\n")
    io.open(AQUI + u"temas.js", "w", encoding="utf-8", newline="").write(js)

    print(u"%d pasos leidos, %d temas, %d puestos" % (total, len(TEMAS), len(PUESTOS)))
    for c, n, s, g in TEMAS:
        print(u"  %-10s %-32s %3d pasos" % (c, n, len(indice.get(c, []))))
    if vacios:
        print(u"\n  OJO, temas sin ningun paso: %s" % ", ".join(vacios))
    if sin_tema:
        print(u"\n  %d pasos sin tema:" % len(sin_tema))
        for r, t in sin_tema[:10]:
            print(u"    %-14s %s" % (r, t))
    print(u"\ntemas.js escrito")


main()
