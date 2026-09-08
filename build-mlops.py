# -*- coding: utf-8 -*-
u"""La ruta de MLOps.

   Es el unico agujero que quedaba medido: contenido.py da MLOps con
   un paso y una hora, mientras ML Engineer lo pide en nivel 3 y AI
   Engineer en 1. Ese unico paso ademas no era de MLOps: es "The
   AI-Native SDLC Playbook" de la ruta de Claude, que quedo etiquetado
   ahi porque habla de poner cosas en produccion. Por eso ML Engineer
   se quedaba en 89% y era el peor cubierto de los diez puestos.

   De donde sale:

   - ml-ops.org y el articulo de arquitectura de Google Cloud son los
     dos textos de referencia del tema. El de Google define los
     niveles 0, 1 y 2 de madurez, que es el vocabulario con el que se
     habla de esto en una entrevista.
   - Made With ML, de Goku Mohandas, es el mejor curso gratuito de
     MLOps que existe y es abierto entero, sin cuenta.
   - MLflow, DVC y Evidently son de codigo abierto y su documentacion
     es la fuente. Las tres son herramientas que vas a encontrar
     puestas en cualquier equipo que haga esto en serio.

   No hay certificacion de MLOps que valga la pena y por eso no se
   nombra ninguna. Lo mas parecido son las credenciales de nube, que
   ya tienen su ruta aca.

   Uso: python build-mlops.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "airflow.html"
SALE = "mlops.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Qué cambia al salir del notebook", desc: "El vocabulario y los niveles de madurez" },
  { n: 2, title: "Que se pueda repetir", desc: "Experimentos, datos y modelos versionados" },
  { n: 3, title: "Ponerlo a correr", desc: "Del registro de modelos al servicio que responde" },
  { n: 4, title: "Que siga funcionando", desc: "Lo que nadie mira hasta que falla" }
];'''

C = [
 # ------------------------------------ 1. que cambia al salir del notebook
 ("m01", 1, "2 h", "school", True, "",
  u"Los principios de MLOps",
  u"Qué es MLOps y qué no: por qué un modelo que anda en un notebook no es un sistema, y qué hace falta agregarle para que lo sea. El texto de referencia del tema, abierto.",
  u"Terminas esta parte cuando explicas por qué el 80% de los modelos nunca llegan a producción.",
  [u"El vocabulario con el que se habla de esto",
   u"Qué se rompe cuando un modelo sale del notebook",
   u"Las tres partes que hay que versionar: código, datos y modelo"],
  "https://ml-ops.org/content/mlops-principles"),

 ("m02", 1, "2 h", "flow", False, "",
  u"Los niveles 0, 1 y 2, de Google",
  u"El artículo de arquitectura que define la escalera: hacerlo a mano, automatizar el entrenamiento, automatizar el pipeline entero. Es la respuesta a «dónde está tu equipo» en una entrevista.",
  u"Terminas esta parte cuando ubicas a tu equipo en un nivel y sabes cuál es el siguiente.",
  [u"Una escalera concreta en vez de una lista de herramientas",
   u"Qué automatizar primero, que es la pregunta cara",
   u"Es el documento que todos citan"],
  "https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning"),

 ("m03", 1, "3 h", "build", False, "",
  u"Diseñar el sistema, no el modelo",
  u"Made With ML arranca por donde hay que arrancar: qué problema resuelve, cómo se mide, y recién después qué modelo. Es el error más caro y el más común.",
  u"Terminas esta parte cuando escribes qué métrica de negocio tiene que mover tu modelo, antes de entrenarlo.",
  [u"Del problema del negocio a la métrica del modelo",
   u"Por qué empezar por el modelo es empezar por el final",
   u"El curso entero es abierto, sin cuenta"],
  "https://madewithml.com/courses/mlops/systems-design/"),

 # ------------------------------------ 2. que se pueda repetir
 ("m04", 2, "2 h", "code", True, "",
  u"MLflow, primeros pasos",
  u"La herramienta que vas a encontrar puesta en la mayoría de los equipos. Instalarla, correr el primer experimento y ver qué guarda.",
  u"Terminas esta parte cuando vuelves a un experimento de la semana pasada y sabes exactamente con qué lo corriste.",
  [u"Registrar qué corriste, con qué datos y qué dio",
   u"Comparar corridas en vez de acordarte",
   u"Es de código abierto: no hay nada que pagar"],
  "https://mlflow.org/docs/latest/getting-started/index.html"),

 ("m05", 2, "3 h", "chart", False, "",
  u"Seguimiento de experimentos",
  u"Parámetros, métricas y artefactos de cada corrida. Es lo que convierte «probé como veinte cosas» en una tabla que se puede mirar.",
  u"Terminas esta parte cuando eliges un modelo mostrando la comparación, no contándola.",
  [u"Qué registrar y qué no, que es la mitad del asunto",
   u"Comparar veinte corridas sin planillas",
   u"El registro es lo que después permite volver atrás"],
  "https://mlflow.org/docs/latest/ml/tracking/"),

 ("m06", 2, "2 h", "data", False, "",
  u"Versionar los datos, no sólo el código",
  u"DVC pone los datos y los modelos bajo control de versiones, junto al código. Sin esto, «el modelo de marzo» es una carpeta que ya nadie sabe cuál era.",
  u"Terminas esta parte cuando reproduces un resultado de hace tres meses con un comando.",
  [u"Git para archivos que no entran en Git",
   u"Reproducir de verdad, no de memoria",
   u"Es lo que falta cuando alguien dice que no puede repetir un número"],
  "https://dvc.org/doc/start"),

 ("m07", 2, "3 h", "search", False, "",
  u"Seguimiento, con el curso al lado",
  u"La misma idea contada por Made With ML, con el proyecto entero armándose alrededor. Sirve para ver cómo encaja en un flujo real.",
  u"Terminas esta parte cuando tu proyecto registra cada corrida sin que tengas que acordarte.",
  [u"La herramienta dentro de un proyecto, no suelta",
   u"Qué se automatiza y qué queda a mano",
   u"Código completo para copiar y adaptar"],
  "https://madewithml.com/courses/mlops/experiment-tracking/"),

 # ------------------------------------ 3. ponerlo a correr
 ("m08", 3, "2 h", "cloud", True, "",
  u"El registro de modelos",
  u"Dónde vive el modelo que está en producción, quién lo aprobó y cómo se pasa de la versión 3 a la 4 sin cortar el servicio.",
  u"Terminas esta parte cuando promueves un modelo a producción y puedes volver atrás en un minuto.",
  [u"Etapas: desarrollo, prueba, producción",
   u"Volver a la versión anterior sin drama, que es lo que te salva",
   u"Quién aprobó qué, que en algunos rubros te lo van a pedir"],
  "https://mlflow.org/docs/latest/ml/model-registry/"),

 ("m09", 3, "3 h", "flow", False, "",
  u"Servir el modelo",
  u"Que el modelo responda a un pedido: como servicio, por lotes o adentro de otra aplicación. Las tres formas y cuándo conviene cada una.",
  u"Terminas esta parte cuando tu modelo contesta por HTTP y sabes cuánto tarda.",
  [u"Las tres formas de servir, con sus costos",
   u"Latencia: la diferencia entre un modelo bueno y uno usable",
   u"Empaquetar el modelo con lo que necesita para correr"],
  "https://mlflow.org/docs/latest/ml/deployment/"),

 ("m10", 3, "3 h", "build", False, "",
  u"Que se despliegue solo",
  u"Integración y entrega continuas para modelos: que un cambio pase las pruebas, entrene y despliegue sin que nadie ejecute nada a mano.",
  u"Terminas esta parte cuando un cambio tuyo llega a producción sin que abras una terminal.",
  [u"El pipeline completo, del commit al modelo servido",
   u"Qué tiene que frenar el despliegue y qué no",
   u"Es el nivel 2 del artículo de Google, hecho"],
  "https://madewithml.com/courses/mlops/cicd/"),

 # ------------------------------------ 4. que siga funcionando
 ("m11", 4, "3 h", "warn", True, "",
  u"Monitoreo y deriva",
  u"Un modelo no se rompe: se degrada, en silencio, mientras el mundo cambia. Evidently mide esa deriva y avisa antes de que la note el negocio.",
  u"Terminas esta parte cuando tienes una alerta que salta cuando tu modelo empieza a fallar, no cuando ya falló.",
  [u"Deriva de datos y deriva de concepto, que no son lo mismo",
   u"Qué medir cuando no tienes las etiquetas reales todavía",
   u"Es la parte del trabajo que sólo se nota cuando falta"],
  "https://docs.evidentlyai.com/quickstart_ml"),

 ("m12", 4, "3 h", "check", False, "",
  u"Probar código, datos y modelo",
  u"Tres cosas distintas que se prueban distinto. Un modelo puede pasar todas las pruebas del código y estar entrenado con datos rotos.",
  u"Terminas esta parte cuando tus pruebas cubren las tres cosas y no sólo las funciones.",
  [u"Probar los datos, que es lo que nadie hace",
   u"Probar el comportamiento del modelo, no sólo su métrica",
   u"Se cruza con la ruta de testing que ya está acá"],
  "https://madewithml.com/courses/mlops/testing/"),

 ("m13", 4, "3 h", "search", False, "",
  u"Monitorear el sistema entero",
  u"La vuelta completa de Made With ML: qué mirar del sistema, no sólo del modelo, y cómo cerrar el ciclo para volver a entrenar.",
  u"Terminas esta parte cuando el sistema te dice solo cuándo hay que reentrenar.",
  [u"Del monitoreo al reentrenamiento, que es el ciclo entero",
   u"Qué mirar del sistema y no del modelo",
   u"Cierra la ruta con el proyecto funcionando de punta a punta"],
  "https://madewithml.com/courses/mlops/monitoring/"),
]

TEXTOS = [
 (u'<a class="btn-quiet" href="https://academy.astronomer.io/" target="_blank" rel="noopener">',
  u'<a class="btn-quiet" href="https://madewithml.com/" target="_blank" rel="noopener">', 1),

 (u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""",
  u"""  /* MLOps. Indigo: no lo usa ninguna de las otras veinte, y no se
     confunde con el violeta del sitio ni con el azul de la nube. */
  --accent:        #4338CA;
  --accent-strong: #362CA1;
  --accent-soft:   #EBEAFA;
  --accent-line:   #C9C6F0;""", 1),

 (u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""",
  u"""  --accent:        #A5A0F0;
  --accent-strong: #C3BFF6;
  --accent-soft:   #1B1840;
  --accent-line:   #322C6B;""", 1),

 (u'<span class="brand-sub">/ Airflow</span>',
  u'<span class="brand-sub">/ MLOps</span>', 1),

 (u'<h1>Orquestar con <span class="grad">Airflow</span></h1>',
  u'<h1>Modelos en <span class="grad">producción</span></h1>', 1),

 (u'<span class="dest">academy.astronomer.io</span>',
  u'<span class="dest">madewithml.com</span>', 1),

 (u"los ocho pasos de Airflow", u"los trece pasos de MLOps", 1),

 (u"Se desbloquea cuando cierres los ocho pasos del mapa. La certificación "
  u"oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para "
  u"aprender esto.",
  u"Se desbloquea cuando cierres los trece pasos del mapa. No hay certificación "
  u"de MLOps que valga la pena, así que no se nombra ninguna: lo más parecido son "
  u"las credenciales de nube, que tienen su propia ruta acá.", 1),

 (u"<h2>Tres tramos, ocho pasos</h2>", u"<h2>Cuatro tramos, trece pasos</h2>", 1),

 (u'id="startDest">Airflow 101<', u'id="startDest">los principios de MLOps<', 1),

 (u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Los de Astronomer dejan constancia en su academia; los de Apache "
  u"son documentación y no dejan nada más que saberlo.",
  u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Ninguno deja credencial: son documentación de herramientas abiertas y "
  u"un curso que su autor publica entero.", 1),
]

PIE = (u'<p class="hero-foot">Todo abierto y sin cuenta. Made With ML lo publica entero su '
       u'autor; MLflow, DVC y Evidently son de código abierto y lo que está acá es su propia '
       u'documentación; los dos textos de referencia -ml-ops.org y el artículo de arquitectura '
       u'de Google- son públicos. No hay certificación de MLOps que valga la pena y por eso no '
       u'se nombra ninguna.</p>')

LEAD = (u'<p class="hero-lead">Entrenar el modelo es la parte corta. Lo largo es que corra '
        u'todos los días, que se pueda repetir dentro de seis meses y que alguien se entere '
        u'cuando empieza a fallar. Acá va del notebook a un sistema que se despliega solo, se '
        u'monitorea y avisa antes de que lo note el negocio.</p>')


def nodo(c):
    cid, act, time, i, boss, cert, titulo, resumen, meta, wins, url = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s"%s,\n'
            u'    cert: "%s",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "%s"\n'
            u'  }' % (cid, act, time, i, u", boss: true" if boss else u"",
                      cert, titulo, resumen, meta, w, url))


def main():
    t = io.open(os.path.join(D, BASE), encoding="utf-8").read()

    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    v = re.search(r'<p class="hero-foot">.*?</p>', t, re.S)
    t = t[:v.start()] + PIE + t[v.end():]
    v2 = re.search(r'<p class="hero-lead">.*?</p>', t, re.S)
    t = t[:v2.start()] + LEAD + t[v2.end():]

    t = t.replace(u'var MI_RUTA = "airflow"', u'var MI_RUTA = "mlops"')
    t = t.replace(u'var MI_CLAVE = "airflow"', u'var MI_CLAVE = "mlops"')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 4 tramos" % (SALE, len(C)))


main()
