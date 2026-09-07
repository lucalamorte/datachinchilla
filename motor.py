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
  return Object.keys(det).filter(function(k){ return !det[k].deducido; });
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
        faltan = [t for t in deben if t not in salio]
        sobran = [t for t in no_deben if t in salio]
        if not faltan and not sobran:
            continue
        mal += 1
        print(u'  %s' % texto.replace("\\n", " / "))
        if faltan:
            print(u"      no detecto: %s" % ", ".join(faltan))
        if sobran:
            print(u"      detecto de mas: %s   (salio: %s)"
                  % (", ".join(sobran), ", ".join(salio)))

    print()
    print(u"los %d casos pasan" % len(CASOS) if not mal else
          u"%d de %d casos fallan" % (mal, len(CASOS)))
    return 1 if mal else 0


sys.exit(main())
