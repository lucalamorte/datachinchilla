# -*- coding: utf-8 -*-
u"""La ruta para quien no sabe todavia a donde va.

   Es la ruta que le faltaba al sitio, y se nota en como esta armado
   todo lo demas: el flujo del CV arranca preguntando "a que puesto
   apuntas", y hay gente -mucha, y la que mas ayuda necesita- cuya
   pregunta es justamente esa. Un estudiante de sistemas en segundo
   ano no sabe si quiere backend, datos o nube, y no lo va a saber
   leyendo descripciones de puestos: lo va a saber escribiendo codigo.

   Entonces esta ruta no termina en un puesto. Termina en poder
   elegirlo, que es un final distinto y hay que decirlo de frente.

   DE DONDE SALE. De un camino que Luca le armo a mano a su primo,
   porque la pagina no le servia. Eso es el mejor dato que puede dar
   un sitio sobre si mismo.

   COMO ESTA ARMADA. Los cuatro primeros pasos son rutas enteras que
   el sitio ya tiene -CS50x, Python, SQL, Full Stack Open- y no se
   copian: cada paso lleva a su ruta. Copiarlas seria tener el mismo
   curso en dos mapas con dos avances distintos, que es exactamente el
   problema que acabamos de arreglar con las claves compartidas.

   Los dos ultimos no son cursos y es a proposito. Despues de un ano
   de fundamentos, lo que falta no es otro curso general: es tocar
   cada area lo suficiente para saber cual te gusta. Un paso que dice
   "hace un proyecto chico de cada una" es mas honesto que cinco
   cursos mas.

   EL ORDEN tiene una razon y esta escrita en cada paso: primero
   pensar como programador -CS50x-, despues una herramienta que sirve
   para todo -Python-, despues datos -SQL, que es la mitad de
   cualquier trabajo-, despues algo completo y publicado -Full Stack
   Open-, y recien ahi nube, que es donde eso que hiciste vive.

   Uso: python build-empezar.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "funcional.html"
SALE = "empezar.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Pensar como programador", desc: "Lo que no cambia aunque cambie el lenguaje" },
  { n: 2, title: "Construir algo entero", desc: "De un ejercicio a algo que funciona y se publica" },
  { n: 3, title: "Probar y elegir", desc: "Tocar cada área y recién ahí decidir" }
];'''

# (id, acto, tiempo, icono, boss, cert, titulo, resumen, meta, wins, url)
C = [
 # ---------------------------------------- 1. pensar como programador
 ("e01", 1, "60 horas", "school", True, "Certificado gratis de CS50",
  u"CS50x, de Harvard",
  u"El curso de introducción a las ciencias de la computación de Harvard, entero y gratis. Arranca moviendo bloques y termina con vos escribiendo C, Python y SQL. No es un curso de lenguajes: es el que te enseña a pensar un problema antes de escribir una línea.",
  u"Terminas este paso cuando entregas el proyecto final: algo tuyo, con lo que aprendiste.",
  [u"Es el mejor punto de partida que existe, y es gratis",
   u"Te deja pensando en problemas, no memorizando sintaxis",
   u"En el sitio está partido en once semanas con su proyecto, para que entre en tu agenda"],
  "cs50.html"),

 ("e02", 1, "50 horas", "code", False, "Certificado gratis de CS50",
  u"CS50 Python",
  u"Python de cero a orientación a objetos, del mismo equipo. Después de CS50x se entiende el doble: ya sabés qué está pasando abajo, así que esto es aprender a decirlo cómodo.",
  u"Terminas este paso cuando entregas su proyecto final en Python.",
  [u"El lenguaje que más puertas abre: datos, backend, scripts, IA",
   u"Nueve semanas y un proyecto, cada una con su ejercicio",
   u"Es la herramienta que vas a usar en cualquiera de los caminos que elijas después"],
  "cs50.html"),

 ("e03", 1, "35 horas", "sql", False, "Certificado gratis de CS50",
  u"CS50 SQL",
  u"Consultar, diseñar y escribir en una base de datos. Es la mitad del trabajo de casi cualquier puesto técnico, y la que más gente saltea por parecer aburrida.",
  u"Terminas este paso cuando podés diseñar un esquema y consultarlo sin mirar apuntes.",
  [u"Siete semanas, una por verbo: consultar, relacionar, diseñar, escribir",
   u"Sirve igual si terminás en datos, en backend o en producto",
   u"Es lo que separa pedirle los datos a alguien de ir a buscarlos"],
  "cs50.html"),

 # ---------------------------------------- 2. construir algo entero
 ("e04", 2, "255 horas", "web", True, "Certificado gratis de la Universidad de Helsinki",
  u"Full Stack Open, de Helsinki",
  u"La aplicación entera: React adelante, Node atrás, base de datos, tests y despliegue. Está en español y lo publica la Universidad de Helsinki.",
  u"Terminas este paso cuando tenés una aplicación tuya publicada y andando, con su base de datos.",
  [u"Es el salto de 'hice ejercicios' a 'hice algo que funciona'",
   u"Lo primero que podés mostrar en una entrevista",
   u"Quince partes, con certificado de la universidad al terminar"],
  "fullstack.html"),

 ("e05", 2, "5 horas", "cloud", False, "Insignia de Google Cloud",
  u"Google Cloud: fundamentos de la nube",
  u"Dónde vive eso que acabás de construir. Qué es una máquina virtual, un contenedor y una base administrada, y por qué una empresa paga por no tener servidores propios.",
  u"Terminas este paso cuando entendés qué pasa entre que alguien escribe tu dirección y tu aplicación responde.",
  [u"Después de publicar algo, esto deja de ser abstracto",
   u"Insignia de Google al terminar",
   u"Es la base común de nube, DevOps y data engineering"],
  "https://www.skills.google/course_templates/153"),

 # ---------------------------------------- 3. probar y elegir
 ("e06", 3, "40 horas", "build", False, "",
  u"Un proyecto chico de cada área",
  u"Acá se terminan los cursos generales. Elegí cuatro áreas que te den curiosidad -datos, IA, backend, sistemas, lo que sea- y hacé un proyecto de fin de semana de cada una. Chico de verdad: algo que funcione, no algo que impresione.",
  u"Terminas este paso cuando tenés cuatro cosas hechas y podés decir cuál te dio ganas de seguir.",
  [u"Ningún curso te va a decir qué te gusta: lo dice hacerlo",
   u"Cuatro fines de semana valen más que cuatro cursos más",
   u"Lo que no te gusta también es información, y se descubre rápido"],
  ""),

 ("e07", 3, "1 h", "boss", True, "",
  u"Elegir a dónde vas",
  u"Ahora sí la pregunta tiene respuesta. Con un año de fundamentos y cuatro proyectos encima, elegí el camino: backend, data engineering, IA, nube, frontend, testing. El sitio tiene una ruta para cada uno.",
  u"Terminas este paso cuando sumás a tu semana la ruta del camino que elegiste.",
  [u"Es el único paso del sitio que no es estudiar, es decidir",
   u"Elegís con información propia, no con descripciones de puestos",
   u"Y si te equivocás, lo de abajo no se pierde: los fundamentos sirven para todas"],
  "index.html#rutas"),
]

TEXTOS = [
 (u"<title>Analista funcional, gratis y en orden · DataChinchilla</title>",
  u"<title>No sé qué seguir: el camino de cero · DataChinchilla</title>", 1),
 (u'<meta property="og:title" content="Analista funcional, en orden">',
  u'<meta property="og:title" content="No sé qué seguir: el camino de cero">', 1),
 (u'<meta name="twitter:title" content="Analista funcional, en orden">',
  u'<meta name="twitter:title" content="No sé qué seguir: el camino de cero">', 1),
 (u'<span class="brand-sub">/ Analista funcional</span>',
  u'<span class="brand-sub">/ No sé qué seguir</span>', 1),
]


def nodo(c):
    cid, act, time, i, boss, cert, titulo, resumen, meta, wins, url = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    interno = url.endswith(".html") or url.startswith("index.html")
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s"%s,\n'
            u'    cert: "%s",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "%s"%s\n'
            u'  }' % (cid, act, time, i, u", boss: true" if boss else u"",
                      cert, titulo, resumen, meta, w, url,
                      u",\n    interno: true" if interno else u""))


def main():
    p = os.path.join(D, BASE)
    if not os.path.exists(p):
        print(u"  ABORTA: no encuentro %s" % BASE); sys.exit(1)
    t = io.open(p, encoding="utf-8").read()

    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r x%d, esperaba %d" % (viejo[:48], n, veces)); sys.exit(1)
        t = t.replace(viejo, nuevo)

    # --- los textos largos
    LEAD = (u'<p class="hero-lead">Si no sabés qué camino seguir, éste es el camino. '
            u'Un año de fundamentos en orden -pensar como programador, una herramienta que '
            u'sirve para todo, datos, y algo entero publicado- y después cuatro proyectos '
            u'chicos para tocar cada área. Al final de esto la pregunta "¿qué me gusta?" '
            u'tiene respuesta, y es tuya.</p>')
    PIE = (u'<p class="hero-foot">Esta ruta no termina en un puesto: termina en poder elegirlo. '
           u'Son unas 445 horas: a diez horas por semana es casi un año. Los cuatro primeros pasos son rutas completas de este sitio y cada uno te '
           u'lleva a la suya, así que el avance se marca allá y no se duplica. CS50 y Full Stack '
           u'Open dejan certificado gratis; Google Cloud deja insignia. El anteúltimo paso no es '
           u'un curso a propósito.</p>')
    v = re.search(r'<p class="hero-foot">.*?</p>', t, re.S)
    t = t[:v.start()] + PIE + t[v.end():]
    v2 = re.search(r'<p class="hero-lead">.*?</p>', t, re.S)
    t = t[:v2.start()] + LEAD + t[v2.end():]

    t = re.sub(r'<h1>.*?</h1>',
               u'<h1>No sé qué seguir: <span class="grad">el camino de cero</span></h1>',
               t, count=1, flags=re.S)
    t = re.sub(r'<h2>[^<]*tramos[^<]*</h2>', u'<h2>Tres tramos, siete pasos</h2>',
               t, count=1)
    t = re.sub(r'id="startDest">[^<]*<', u'id="startDest">CS50x<', t, count=1)

    # --- LA IDENTIDAD. Son cinco cosas y es la quinta vez que una
    #     copia se trae alguna: se cambian todas y despues se
    #     comprueba que no quede ni una de la pagina base.
    t = t.replace(u'var MI_RUTA = "funcional"',  u'var MI_RUTA = "empezar"')
    t = t.replace(u'var MI_CLAVE = "funcional"', u'var MI_CLAVE = "empezar"')
    t = t.replace(u"p.funcional = cs;",          u"p.empezar = cs;")
    t = t.replace(u"p.funcional && typeof p.funcional",
                  u"p.empezar && typeof p.empezar")
    t = t.replace(u"cs = { done: p.funcional.done || {} };",
                  u"cs = { done: p.empezar.done || {} };")
    t = t.replace(u'"funcional-path/v1/anon"',   u'"empezar-path/v1/anon"')
    t = t.replace(u'"funcional-path/v1/migrado"', u'"empezar-path/v1/migrado"')

    # la migracion del cajon compartido no aplica: esta ruta nace limpia
    t = re.sub(r"\n/\* El avance que estaba en el cajon compartido\..*?\n\}\n",
               u"\n", t, count=1, flags=re.S)
    t = t.replace(u"  migrarDelCajonCompartido(p);\n", u"")

    # --- lo que queda de la pagina base y no es la identidad de
    #     arriba. Es la quinta vez que una copia se trae algo, asi
    #     que va explicito y despues se comprueba.
    t = t.replace(u'href="https://datachinchilla.com/funcional"',
                  u'href="https://datachinchilla.com/empezar"')
    t = t.replace(u'content="https://datachinchilla.com/funcional"',
                  u'content="https://datachinchilla.com/empezar"')
    t = t.replace(u"los diez pasos de analista funcional.",
                  u"los siete pasos del camino de cero.")
    # Y la nota de la constancia, que tambien traia el numero y
    # ademas hablaba de certificaciones de otro oficio. cuentas.py
    # lo caza, pero es mejor no escribirlo mal.
    t = re.sub(r'<p class="cert-nota">.*?</p>',
               u'<p class="cert-nota">Se desbloquea cuando cierres los siete pasos '
               u'del mapa. No es una credencial: es tuya y dice lo que hiciste. Las '
               u'de verdad las dejan los cursos, y acá son tres: CS50, Full Stack '
               u'Open y Google Cloud.</p>',
               t, count=1, flags=re.S)

    # --- color propio. Indigo: no lo usa ninguna otra ruta, y entre
    #     el violeta de la marca y los verdes azulados de nube y big
    #     data es el unico frio que quedaba libre.
    t = re.sub(r"/\* Analista funcional\..*?\*/",
               u"/* El camino de cero, en indigo: es el unico frio libre. */",
               t, count=1, flags=re.S)
    t = t.replace(u"--accent:        #A94F2E;", u"--accent:        #4338CA;")
    t = t.replace(u"--accent:        #E89571;", u"--accent:        #818CF8;")

    # El boton del medio del hero llevaba al sitio de Scrum, de la
    # pagina base. Aca no hay "un sitio": los cuatro primeros pasos
    # son rutas de este sitio. Se cambia por el catalogo, que es a
    # donde lleva el ultimo paso y lo que uno quiere ver si entra sin
    # saber que elegir.
    t = t.replace(u'<a class="btn-quiet" href="https://scrumguides.org/" target="_blank" rel="noopener">',
                  u'<a class="btn-quiet" href="index.html#rutas">')
    t = t.replace(u'<span class="verb">Ir al sitio de</span><span class="dest">scrumguides.org</span>',
                  u'<span class="verb">O mirá</span><span class="dest">las 23 rutas</span>')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)

    quedan = [x for x in ("funcional",) if x in re.sub(r'<!--.*?-->', '', t, flags=re.S)
              and ("MI_RUTA" in t or True)]
    rastros = len(re.findall(r'funcional', t))
    print(u"%s: %d pasos en 3 tramos" % (SALE, len(C)))
    if rastros:
        print(u"  OJO: quedan %d apariciones de 'funcional' en el archivo" % rastros)


main()
