# -*- coding: utf-8 -*-
"""La ruta de Airflow.

   Estaba en el catalogo como tarjeta bloqueada -"Todavia no existe"-
   diciendo que Airflow vivia como un curso pago dentro del nivel 5 de
   Data Engineer. Ya no: hay material gratis y bueno.

   De donde sale cada cosa, y que es gratis de verdad:

   - Astronomer Academy publica sus learning paths gratis. Piden
     crear una cuenta para verlos, y eso se dice en la pagina.
     Airflow 101 esta en dos versiones, para Airflow 3 y para Airflow
     2, porque muchas empresas siguen en la 2.

   - La certificacion de Astronomer NO es gratis: son 150 dolares por
     intento. No entra como paso y se dice en el pie del hero, porque
     un sitio que promete que todo es gratis tiene que ser el primero
     en avisar donde empieza a costar.

   - Los cinco tutoriales oficiales de Apache son abiertos, sin
     cuenta. Los titulos salen de su propia pagina.

   Las duraciones van como "a tu ritmo" y no inventadas: ni Astronomer
   ni Apache publican horas por leccion, y poner un numero seria
   decorar. build-pasos.py cuenta 90 minutos para eso.

   Se arma copiando fullstack.html, que es la ruta con la estructura
   mas parecida.

   Uso: python build-airflow.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "fullstack.html"
SALE = "airflow.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Los fundamentos", desc: "Qué es un DAG y cómo se ejecuta" },
  { n: 2, title: "Escribir DAGs que aguanten", desc: "Lo que separa un ejemplo de algo que corre todas las noches" },
  { n: 3, title: "De la fuente", desc: "Los tutoriales oficiales de Apache, sin cuenta" }
];'''

# (id, acto, tiempo, icono, jefe, cert, titulo, resumen, objetivo, wins, url)
C = [
 ("g01", 1, "a tu ritmo", "flow", True, "",
  u"Airflow 101",
  u"El camino de entrada de Astronomer, sobre Airflow 3. Qué es un DAG, cómo se programa y qué pasa cuando una tarea falla.",
  u"Terminas esta parte cuando escribes un DAG, lo ves correr y entiendes por qué se ejecutó cuando se ejecutó.",
  [u"DAGs, tareas y dependencias: el vocabulario que todo lo demás da por sabido",
   u"El planificador: por qué una tarea arranca cuando arranca",
   u"Reintentos y alertas, que es la mitad de por qué se usa Airflow"],
  "https://academy.astronomer.io/path/airflow-101"),

 ("g02", 1, "a tu ritmo", "clock", False, "",
  u"Airflow 101, versión Airflow 2",
  u"El mismo camino para quien trabaja sobre Airflow 2. Hazlo sólo si tu empresa todavía está en esa versión: si empiezas de cero, ve directo a la 3.",
  u"Terminas esta parte cuando reconoces qué cambió entre la 2 y la 3, y no te confunde la documentación.",
  [u"Lo mismo que la parte anterior, en la versión que todavía corre en producción en muchos lados",
   u"Las diferencias que importan al leer código viejo",
   u"Saltéala sin culpa si arrancas de cero"],
  "https://academy.astronomer.io/path/airflow-101-airflow-2"),

 ("g03", 2, "a tu ritmo", "build", True, "",
  u"DAG Authoring",
  u"El camino avanzado de Astronomer: TaskFlow API, tareas dinámicas y plantillas. Es donde un DAG deja de ser un ejemplo.",
  u"Terminas esta parte cuando escribes un DAG que genera tareas según lo que encuentre, sin repetir código.",
  [u"TaskFlow API: DAGs que se leen como Python y no como configuración",
   u"Tareas dinámicas, para cuando no sabes de antemano cuántas hay",
   u"Plantillas y variables, que es como un DAG deja de estar hardcodeado"],
  "https://academy.astronomer.io/path/airflow-dag-authoring"),

 ("g04", 3, "a tu ritmo", "code", False, "",
  u"Airflow 101: Building Your First Workflow",
  u"El primer tutorial de la documentación oficial. Abierto, sin cuenta y sin registro.",
  u"Terminas esta parte cuando tienes el primer flujo corriendo desde la documentación oficial.",
  [u"El mismo arranque, contado por quien mantiene el proyecto",
   u"La documentación oficial como fuente, que es a donde vas a volver siempre",
   u"Sin cuenta y sin registro"],
  "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html"),

 ("g05", 3, "a tu ritmo", "code", False, "",
  u"Pythonic DAGs con la TaskFlow API",
  u"Escribir DAGs como funciones de Python en vez de como grafos armados a mano.",
  u"Terminas esta parte cuando tus tareas se pasan datos entre sí sin que tengas que pensar en XComs.",
  [u"Decoradores en vez de operadores para lo que hacés todos los días",
   u"Cómo viajan los datos de una tarea a la siguiente",
   u"Por qué el código queda más corto y más fácil de probar"],
  "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html"),

 ("g06", 3, "a tu ritmo", "data", False, "",
  u"Un pipeline de datos simple",
  u"El caso completo de punta a punta: traer datos, transformarlos y dejarlos donde alguien los use.",
  u"Terminas esta parte cuando tienes un pipeline que corre solo y sabes dónde mirar cuando no corre.",
  [u"El recorrido entero, no un fragmento",
   u"Dónde se rompe un pipeline de verdad",
   u"Qué mirar en la interfaz cuando algo falló anoche"],
  "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html"),

 ("g07", 3, "a tu ritmo", "cloud", False, "",
  u"Flujos sobre almacenamiento de objetos",
  u"Trabajar contra S3, GCS o Azure sin atarte a uno solo.",
  u"Terminas esta parte cuando lees y escribes en la nube desde un DAG sin código específico del proveedor.",
  [u"Almacenamiento de objetos como si fuera un sistema de archivos",
   u"El mismo DAG contra distintos proveedores",
   u"Es lo que vas a usar en cualquier trabajo con datos en la nube"],
  "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/objectstorage.html"),

 ("g08", 3, "a tu ritmo", "user", True, "",
  u"Cuando hace falta una persona en el medio",
  u"El operador que frena el flujo y espera que alguien apruebe. Es lo que piden los procesos que tocan plata o clientes.",
  u"Terminas esta parte cuando un DAG espera una aprobación humana y sigue solo después.",
  [u"Frenar un flujo hasta que alguien decida",
   u"Por qué esto aparece en cuanto el pipeline toca algo sensible",
   u"Cómo no dejar un flujo esperando para siempre"],
  "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/hitl.html"),
]

TEXTOS = [
 (u"<title>Full Stack Open, gratis y en orden · DataChinchilla</title>",
  u"<title>Airflow, gratis y en orden · DataChinchilla</title>", 1),

 (u'content="Las quince partes del curso gratuito de la Universidad de Helsinki: React, '
  u'Node, pruebas, TypeScript, contenedores y CI/CD, con certificado y sin examen."',
  u'content="Orquestación con Apache Airflow, gratis: los caminos de Astronomer Academy '
  u'y los tutoriales oficiales de Apache, en orden y sin pagar nada."', 3),

 (u'content="Full Stack Open, en orden"',
  u'content="Airflow, en orden"', 2),

 (u"""  /* Full Stack Open */
  --accent:        #1D5C99;
  --accent-strong: #17497A;
  --accent-soft:   #E8F1F9;
  --accent-line:   #C3DAEE;""",
  u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""", 1),

 (u"""  --accent:        #7FB4E8;
  --accent-strong: #A3CBF0;
  --accent-soft:   #10263B;
  --accent-line:   #1D4A73;""",
  u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""", 1),

 (u'<span class="brand-sub">/ Full Stack Open</span>',
  u'<span class="brand-sub">/ Airflow</span>', 1),

 (u'<h1>Full Stack <span class="grad">Open</span></h1>',
  u'<h1>Orquestar con <span class="grad">Airflow</span></h1>', 1),

 (u'<span class="dest" id="startDest">cómo funciona una app web</span>',
  u'<span class="dest" id="startDest">Airflow 101</span>', 1),

 (u'<a class="btn-quiet" href="https://fullstackopen.com/en/" target="_blank" rel="noopener">',
  u'<a class="btn-quiet" href="https://academy.astronomer.io/" target="_blank" rel="noopener">', 1),

 (u'<span class="dest">fullstackopen.com</span>',
  u'<span class="dest">academy.astronomer.io</span>', 1),

 (u'class="cert-linea">completó esta ruta:<br>las quince partes de Full Stack Open.',
  u'class="cert-linea">completó esta ruta:<br>los ocho pasos de Airflow.', 1),

 (u'class="cert-nota">Se desbloquea cuando cierres las quince partes del mapa. El certificado '
  u'de verdad, el de Helsinki, lo bajas de su sitio al cerrar la parte 5.',
  u'class="cert-nota">Se desbloquea cuando cierres los ocho pasos del mapa. La certificación '
  u'oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para aprender esto.', 1),

 (u"<h2>Cinco tramos, quince partes</h2>",
  u"<h2>Tres tramos, ocho pasos</h2>", 1),

 (u'<span class="dest" id="startDest">Airflow 101</span>',
  u'<span class="dest" id="startDest">Airflow 101</span>', 1),
]


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
    p = os.path.join(D, BASE)
    if not os.path.exists(p):
        print("  ABORTA: no encuentro %s" % BASE)
        sys.exit(1)
    t = io.open(p, encoding="utf-8").read()

    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    # el pie del hero: de donde sale el material y donde empieza a costar
    v = re.search(r'<p class="hero-foot">.*?</p>', t, re.S)
    if not v:
        print(u"  ABORTA: no encuentro el pie del hero"); sys.exit(1)
    nuevo_pie = (u'<p class="hero-foot">Los tres primeros pasos son de Astronomer Academy y '
                 u'piden crear una cuenta gratuita. Los cinco siguientes son la documentación '
                 u'oficial de Apache: abierta, sin cuenta y sin registro. La certificación de '
                 u'Astronomer cuesta 150 dólares y no entra acá: se aprende igual sin ella.</p>')
    t = t[:v.start()] + nuevo_pie + t[v.end():]

    # el lead
    v2 = re.search(r'<p class="hero-lead">.*?</p>', t, re.S)
    nuevo_lead = (u'<p class="hero-lead">Airflow es lo que hace que un pipeline corra todas las '
                  u'noches sin que nadie lo mire. Acá va de qué es un DAG a escribir uno que '
                  u'genere sus tareas solo, primero con los caminos de Astronomer y después con '
                  u'la documentación oficial, que es a donde vas a volver siempre.</p>')
    t = t[:v2.start()] + nuevo_lead + t[v2.end():]

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 3 tramos" % (SALE, len(C)))


main()
