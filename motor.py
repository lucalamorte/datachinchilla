# -*- coding: utf-8 -*-
u"""Prueba el motor que lee el CV, sin abrir el navegador.

   cv.js decide que ruta te toca, y hasta ahora la unica forma de
   probarlo era cargar un CV a mano y mirar el resultado. Eso alcanza
   para ver que anda; no alcanza para ver que sigue andando despues de
   tocarlo.

   Los casos de abajo son de dos clases:

   - Lo que tiene que detectar. Un CV que dice Spark sabe Spark.
   - Lo que NO tiene que detectar. Un CV que dice que NO sabe Spark no
     sabe Spark, y ese era el agujero: "no tengo experiencia en Spark"
     y "cinco anos con Spark" valian igual.

   Los casos trampa son los que importan. Una regla de negacion mal
   puesta rompe mas de lo que arregla: "no solo Python" no niega
   Python, "sin problemas con Docker" tampoco, y un punto corta la
   frase.

   Corre con node, que ya hace falta para nada mas -humo.py usa
   Chrome-, asi que si no esta, esto avisa y no rompe nada.

   Uso: python motor.py
"""
import io, os, json, subprocess, sys

D = os.path.dirname(os.path.abspath(__file__))

# (texto, temas que tienen que salir, temas que NO tienen que salir)
CASOS = [
 # --- lo de siempre: que siga detectando -------------------------
 (u"Analista con 5 anios de Postgres, BigQuery y window functions.",
  ["sql"], []),
 (u"Desarrollo en Python con pandas y numpy. Notebooks a diario.",
  ["python"], []),
 (u"Orquesto pipelines con Airflow sobre AWS.",
  ["pipelines", "cloud"], []),
 (u"Entreno modelos, scikit-learn, validacion cruzada.",
  ["ml"], []),

 # --- "no ... ningun": un no con un ningun cerca es negacion -------
 #
 # La lista de frases tenia "no manejo" y no tenia "no puse". El
 # primero agarraba "No manejo ninguna herramienta de visualizacion";
 # el segundo dejaba pasar "No puse ninguno en produccion", asi que
 # al CV de un data scientist se le daba por sabido MLOps y se le
 # ofrecia AI: justo lo que ese CV dice que le falta.
 #
 # Enumerar verbos es perder contra el proximo, asi que la regla mira
 # el "ningun", que es lo que las dos frases tienen en comun, y pide
 # un "no" delante para no comerse "sin ningun problema con Kafka".
 (u"Data scientist. Python, scikit-learn, entreno modelos. "
  u"Estadistica y experimentos A/B. No puse ninguno en produccion.",
  ["ml", "python", "stats"], ["mlops"]),
 (u"No puse ningun modelo en produccion. Uso Docker y Kubernetes todos los dias.",
  ["cloud"], ["mlops"]),
 (u"Analista de negocio. Excel y SQL en Postgres. "
  u"No manejo ninguna herramienta de visualizacion ni tableros.",
  ["sql"], ["viz"]),
 # Y la trampa al reves: "sin ningun problema con X" no niega X.
 (u"Backend con Kafka. Sin ningun problema con Kafka en produccion, lo uso a diario.",
  ["pipelines"], []),
 # Que la regla no se coma lo que si esta.
 (u"Entreno modelos y los llevo a produccion con MLflow y Docker.",
  ["mlops"], []),

 # --- nombrar una herramienta no es haberla oido nombrar ----------
 #
 # El nivel salia de cuantas senales distintas toca el CV, y eso trata
 # igual a "software" que a "dbt". Un CV con dbt y Airflow daba
 # modelado 1 y pipelines 1 -"los oyo nombrar"- y el sitio le ofrecia
 # los cursos de dbt y de Airflow a alguien que los usa todos los dias.
 (u"Data Engineer. Modelo el warehouse en dbt y orquesto con Airflow.",
  ["modelado:2", "pipelines:2"], []),
 # Y un titulo de puesto afirma igual que un nombre propio: a un
 # senior developer le preguntabamos si programa.
 (u"Senior developer con 8 anos de experiencia.", ["prog:2"], []),
 # Lo generico sigue valiendo lo que vale.
 # Y que el piso no se le pegue a lo generico: estas siguen en 1.
 (u"Trabajo con software y consultas.", ["prog:1", "sql:1"], []),
 # Y el piso no le gana a la negacion. "No uso" estaba solo en pasado
 # -"no use"-, asi que "No uso dbt ni Airflow" no negaba nada, y con
 # el piso puesto pasaba de contar 1 a contar 2.
 (u"No uso dbt ni Airflow.", [], ["modelado", "pipelines"]),

 # --- lo nuevo: que deje de detectar lo que se niega --------------
 (u"No tengo experiencia en Spark.", [], ["bigdata"]),
 (u"No se Docker.", [], ["cloud"]),
 (u"Nunca use Airflow.", [], ["pipelines"]),
 (u"Sin conocimientos de Kubernetes.", [], ["cloud"]),
 (u"Desconozco Hadoop.", [], ["bigdata"]),
 (u"Cero Tableau.", [], ["viz"]),
 (u"Ganas de aprender Kubernetes.", [], ["cloud"]),
 (u"Me gustaria aprender Spark.", [], ["bigdata"]),
 (u"Spark es mi asignatura pendiente.", [], ["bigdata"]),
 (u"No manejo Snowflake todavia.", [], ["sql"]),
 (u"Sin experiencia en dbt.", [], ["modelado"]),

 # --- trampas: que NO se pase de listo ----------------------------
 (u"No solo Python, tambien R y Julia.",
  ["python"], []),
 (u"Sin problemas con Docker: lo uso todos los dias.",
  ["cloud"], []),
 (u"No termine la carrera. Python desde 2019.",
  ["python"], []),
 (u"No se Java. Postgres y BigQuery a diario.",
  ["sql"], []),
 (u"No se Docker avanzado, pero uso Docker a diario.",
  ["cloud"], []),
 (u"No uso Excel; armo pipelines con Airflow.",
  ["pipelines"], []),
 (u"Experiencia: Spark, Hadoop.\\nNo se Kubernetes.",
  ["bigdata"], ["cloud"]),

 # --- mezcla, que es lo que pasa de verdad ------------------------
 (u"Cinco anios de SQL en Postgres. Python con pandas. "
  u"No tengo experiencia en Spark ni en Kubernetes.",
  ["sql", "python"], ["bigdata", "cloud"]),
]

PUENTE = u"""
const fs = require("fs");
const path = require("path");
const D = %s;
function carga(a){
  const src = fs.readFileSync(path.join(D, a), "utf8");
  (0, eval)(src);
}
/* El eval indirecto corre en el ambito global, asi que temas.js y
   cv.js dejan TEMAS y CV en globalThis. Declararlos aca con var los
   taparia con undefined. */
globalThis.window = globalThis;
carga("temas.js");
carga("cv.js");
const casos = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const salida = casos.map(function(c){
  const det = globalThis.CV.leer(c);
  const out = {};
  Object.keys(det).forEach(function(k){
    if(!det[k].deducido) out[k] = det[k].nivel;
  });
  return out;
});
process.stdout.write(JSON.stringify(salida));
"""


def main():
    try:
        subprocess.check_output(["node", "--version"], stderr=subprocess.STDOUT)
    except Exception:
        print(u"no encuentro node: esta prueba lo necesita")
        return 0

    tmp = os.path.join(D, "_motor_casos.json")
    pnt = os.path.join(D, "_motor_puente.js")
    io.open(tmp, "w", encoding="utf-8").write(
        json.dumps([c[0] for c in CASOS], ensure_ascii=False))
    io.open(pnt, "w", encoding="utf-8").write(
        PUENTE % json.dumps(D.replace("\\", "/")))

    try:
        crudo = subprocess.check_output(["node", pnt, tmp],
                                        stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(u"node no pudo cargar el motor:")
        print(e.output.decode("utf-8", "replace"))
        return 1
    finally:
        for f in (tmp, pnt):
            try: os.remove(f)
            except OSError: pass

    vistos = json.loads(crudo.decode("utf-8"))
    mal = 0
    for (texto, deben, no_deben), salio in zip(CASOS, vistos):
        # "sql" pide que este; "sql:2" pide ademas que llegue a ese
        # nivel. Sin el nivel, un caso sobre cuanto pesa una senal no
        # prueba nada: el tema aparece igual valiendo 1 que valiendo 2,
        # y el caso pasa con la regla puesta y sin ella.
        faltan, flojos = [], []
        for d in deben:
            k, piso = (d.split(":") + ["0"])[:2]
            piso = int(piso)
            if k not in salio:
                faltan.append(k)
            elif salio[k] < piso:
                flojos.append(u"%s en %d, esperaba %d" % (k, salio[k], piso))
        sobran = [t for t in no_deben if t in salio]
        if not faltan and not sobran and not flojos:
            continue
        mal += 1
        print(u'  %s' % texto.replace("\\n", " / "))
        if faltan:
            print(u"      no detecto: %s" % ", ".join(faltan))
        if flojos:
            print(u"      se queda corto: %s" % ", ".join(flojos))
        if sobran:
            print(u"      detecto de mas: %s   (salio: %s)"
                  % (", ".join(sobran), ", ".join(sorted(salio))))

    print()
    print(u"los %d casos pasan" % len(CASOS) if not mal else
          u"%d de %d casos fallan" % (mal, len(CASOS)))
    return 1 if mal else 0


sys.exit(main())
