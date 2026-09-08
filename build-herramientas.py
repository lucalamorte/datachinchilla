# -*- coding: utf-8 -*-
u"""Nombrar una herramienta no es haberla oido nombrar.

   El nivel de un tema sale de cuantas senales distintas toca el CV:
   una mencion es 1, tres o mas es 3. Eso trata igual a "software" que
   a "dbt", y no son lo mismo. Nadie escribe "Airflow" en su CV sin
   haber tocado Airflow; "software" lo escribe cualquiera.

   Con el conteo pelado pasaba esto:

   - Un CV con dbt y Airflow daba modelado 1 y pipelines 1, o sea "los
     oyo nombrar", y el sitio le recomendaba los cursos de dbt y de
     Airflow. A alguien que los usa todos los dias.
   - Un CV que dice "senior developer" no tocaba ninguna senal de
     programacion, asi que despues le preguntabamos si programa.

   La regla: si lo que toco es el nombre de una herramienta -un
   producto con nombre propio-, el nivel arranca en 2. No en 3: usar
   dbt no es dominar el modelado de datos, y el tercer nivel se lo
   sigue ganando quien menciona varias cosas del tema.

   Las genericas -"pipeline", "software", "consultas"- siguen valiendo
   1, que es lo que valen: son palabras que aparecen en cualquier CV.

   Y se agregan los titulos de puesto que afirman un tema entero, como
   ya se hizo con "data scientist" para machine learning. Decir que
   sos desarrollador es decir que programas.

   Uso: python build-herramientas.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

# Nombres propios. Si aparece uno, lo usaste.
HERRAMIENTAS = [
 # sql
 "postgres", "mysql", "sql server", "oracle", "bigquery", "redshift",
 "snowflake", "plsql",
 # python
 "pandas", "numpy", "jupyter", "django", "flask", "fastapi", "scipy",
 # programacion
 "leetcode", "git", "javascript", "java", "scratch",
 # modelado
 "dbt", "kimball", "inmon", "star schema", "data vault",
 # pipelines
 "airflow", "dagster", "prefect", "kafka", "nifi",
 # producto
 "scrum", "bpmn", "jira", "kanban",
 # calidad
 "pytest", "great expectations",
 # nube
 "aws", "azure", "gcp", "google cloud", "lambda", "terraform", "docker",
 "kubernetes", "openshift",
 # big data
 "hadoop", "spark", "pyspark", "mapreduce", "hive", "hbase", "yarn",
 "databricks", "flink",
 # machine learning
 "scikit", "sklearn", "xgboost", "random forest",
 # deep learning
 "tensorflow", "pytorch", "keras", "cnn", "rnn",
 # llm
 "gpt", "openai", "claude", "langchain", "rag", "bedrock",
 # mlops
 "mlflow", "kubeflow", "sagemaker", "feature store",
 # visualizacion
 "tableau", "power bi", "powerbi", "looker", "metabase", "superset",
 "matplotlib", "seaborn", "plotly",
 # web
 "typescript", "react", "angular", "vue", "svelte", "next.js", "nextjs",
 "tailwind", "jquery", "redux", "sass", "webpack", "vite", "react native",
 "flutter", "bootstrap",
 # backend
 "graphql", "node", "nodejs", "node.js", "express", "spring", "spring boot",
 ".net", "laravel", "rails", "nestjs", "jwt", "oauth",
 # web3
 "solidity", "ethereum", "defi",
]


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# ------------------------------------------- 1. los titulos que faltaban
P = os.path.join(D, "build-temas.py")
t = io.open(P, encoding="utf-8").read()
if u"HERRAMIENTAS" in t:
    print(u"  ya estaba"); sys.exit(1)

t = cambiar(t,
u'''  ["algoritmo", "estructura de datos", "leetcode", "complejidad", "big o",
   "programacion", "software", "git", "javascript", "java", "scratch"],''',
u'''  # Los titulos de puesto afirman el tema entero, igual que "data
  # scientist" para machine learning: decir que sos desarrollador es
  # decir que programas. Sin esto, a un senior developer le
  # preguntabamos si programa.
  ["algoritmo", "estructura de datos", "leetcode", "complejidad", "big o",
   "programacion", "software", "git", "javascript", "java", "scratch",
   "desarrollador", "developer", "programador", "software engineer",
   "ingeniero de software", "full stack", "fullstack"],''',
u"los titulos de programacion", "build-temas.py")

# ------------------------------------------- 2. la lista, a temas.js
t = cambiar(t,
u'''    salida = {
        "temas": [{"id": c, "nombre": n, "senales": s} for c, n, s, g in TEMAS],''',
u'''    salida = {
        "temas": [{"id": c, "nombre": n, "senales": s} for c, n, s, g in TEMAS],
        # Cuales de esas senales son nombres propios. Van aparte y no
        # dentro de cada tema porque la regla no es del tema, es de la
        # palabra: si un CV nombra una herramienta, la uso.
        "herramientas": HERRAMIENTAS,''',
u"la lista en la salida", "build-temas.py")

t = cambiar(t,
u'''TEMAS = [''',
u'''# Nombres propios. Si aparece uno en un CV, lo usaste: nadie escribe
# "Airflow" sin haber tocado Airflow. Las palabras genericas -"pipeline",
# "software", "consultas"- no dicen nada parecido, y por eso esta lista
# existe y no es simplemente "todas las senales".
#
# La escribe build-herramientas.py y se puede extender a mano.
HERRAMIENTAS = %s

TEMAS = [''' % repr(HERRAMIENTAS).replace("', '", "', '"),
u"la lista de herramientas", "build-temas.py")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"build-temas.py: %d herramientas y los titulos de desarrollador" % len(HERRAMIENTAS))


# ------------------------------------------- 3. y el piso, en el motor
C = os.path.join(D, "cv.js")
c = io.open(C, encoding="utf-8").read()
c = cambiar(c,
u'''      if(vistas.length){
        out[tema.id] = {
          nivel: Math.min(3, vistas.length),   /* 1 mención es 1; 3 o más, 3 */
          senales: vistas
        };
      }''',
u'''      if(vistas.length){
        /* Nombrar una herramienta no es haberla oido nombrar.

           El nivel salia de cuantas senales distintas toca el CV, y
           eso trata igual a "software" que a "dbt". Un CV con dbt y
           Airflow daba modelado 1 y pipelines 1 -"los oyo nombrar"- y
           el sitio le ofrecia los cursos de dbt y de Airflow a alguien
           que los usa todos los dias.

           Si lo que toco es un nombre propio, el nivel arranca en 2.
           No en 3: usar dbt no es dominar el modelado, y el tercer
           nivel se lo sigue ganando quien nombra varias cosas del
           tema. */
        var conHerramienta = false, h;
        for(h=0;h<vistas.length && !conHerramienta;h++){
          if(HERRAMIENTA[vistas[h]]) conHerramienta = true;
        }
        out[tema.id] = {
          nivel: Math.min(3, Math.max(vistas.length, conHerramienta ? 2 : 0)),
          senales: vistas
        };
      }''',
u"el piso por herramienta", "cv.js")

c = cambiar(c,
u'''  /* Qué temas asoma el CV, y con cuánta insistencia. */
  function leer(texto){''',
u'''  /* Las senales que son nombres propios, en un objeto para no
     recorrer la lista por cada una. */
  var HERRAMIENTA = (function(){
    var m = {}, l = (typeof TEMAS !== "undefined" && TEMAS.herramientas) || [], i;
    for(i=0;i<l.length;i++) m[l[i]] = true;
    return m;
  })();

  /* Qué temas asoma el CV, y con cuánta insistencia. */
  function leer(texto){''',
u"el indice de herramientas", "cv.js")

io.open(C, "w", encoding="utf-8", newline="").write(c)
print(u"cv.js: una herramienta nombrada vale 2, no 1")
