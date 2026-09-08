# -*- coding: utf-8 -*-
u"""La ruta de testing.

   De donde sale, y por que de ahi.

   Test Automation University tiene los mejores cursos gratuitos de
   testing que hay, y NO se usan aca. Su catalogo muestra hoy, en cada
   curso, un cartel que dice "Credits coming soon" con un numero de
   creditos al lado. O sea que estan por poner sus cursos detras de un
   sistema de creditos. Construir la ruta sobre eso es construirla
   sobre algo que anunciaron que va a cambiar, y este sitio promete
   que lo que ofrece no se paga. Si el dia de manana siguen abiertos,
   se agregan.

   Lo que se usa es documentacion oficial y abierta: Playwright,
   Cypress, pytest, Vitest, k6, GitHub Actions, Postman Learning
   Center y el W3C. No pide cuenta, no tiene creditos, y es a donde
   vas a volver a mirar cuando trabajes.

   Los dos que no son documentacion:

   - El silabo de ISTQB. Es el vocabulario que usa toda la industria
     para hablar de esto, se baja gratis en PDF y trae examenes de
     ejemplo gratis tambien. El examen de certificacion SI cuesta, y
     se dice en el pie del hero.
   - "The Practical Test Pyramid", de Martin Fowler. Es el articulo
     que explica que probar en cada nivel y por que; sin eso, alguien
     escribe cincuenta pruebas de interfaz para algo que se probaba
     con tres unitarias.

   Las duraciones: las de la documentacion van estimadas por el
   tamano de cada seccion, no inventadas al azar, y las paginas dicen
   "a tu ritmo" donde la fuente no publica horas.

   Se arma copiando airflow.html, que es la ruta con la estructura mas
   parecida: pocos tramos, fuente oficial, credencial paga aparte.

   Uso: python build-tester.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "airflow.html"
SALE = "testing.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Qué es probar", desc: "El vocabulario y qué probar en cada nivel" },
  { n: 2, title: "Probar el código", desc: "Unitarias, que es donde empieza todo" },
  { n: 3, title: "Probar la aplicación", desc: "El navegador y las APIs, de punta a punta" },
  { n: 4, title: "Que corra solo", desc: "En cada commit, y lo que no es funcional" }
];'''

# (id, acto, tiempo, icono, jefe, cert, titulo, resumen, objetivo, wins, url)
C = [
 # ---------------------------------------------- 1. que es probar
 ("t01", 1, "6 h", "school", True, "",
  u"El sílabo de ISTQB Foundation",
  u"El vocabulario con el que la industria habla de esto: qué es un defecto, qué es una prueba de caja negra, qué significa cobertura. Se baja gratis en PDF y trae exámenes de ejemplo, también gratis.",
  u"Terminas esta parte cuando entiendes qué te están pidiendo en una entrevista de QA sin traducir mentalmente.",
  [u"El vocabulario común: sin esto, cada equipo te lo explica distinto",
   u"Los niveles y tipos de prueba, que es lo que se pregunta siempre",
   u"Exámenes de ejemplo gratis para saber si te alcanza"],
  "https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/"),

 ("t02", 1, "45 min", "build", False, "",
  u"La pirámide de pruebas, de Martin Fowler",
  u"Qué probar en cada nivel y por qué. Es el artículo que evita el error más caro de todos: escribir cincuenta pruebas de interfaz para algo que se probaba con tres unitarias.",
  u"Terminas esta parte cuando, ante una funcionalidad nueva, sabes en qué nivel conviene probarla.",
  [u"Por qué una prueba de interfaz cuesta cien veces más que una unitaria",
   u"Dónde poner el esfuerzo cuando el tiempo no alcanza",
   u"El lenguaje que vas a escuchar en cualquier equipo que pruebe en serio"],
  "https://martinfowler.com/articles/practical-test-pyramid.html"),

 # ---------------------------------------------- 2. probar el codigo
 ("t03", 2, "3 h", "code", True, "",
  u"pytest, de cero",
  u"El framework de pruebas de Python. Instalarlo, escribir la primera prueba, entender qué pasa cuando falla y cómo se lee el error.",
  u"Terminas esta parte cuando escribes una prueba que falla, la lees, y arreglas el código en vez de la prueba.",
  [u"Escribir y correr pruebas sin ceremonia",
   u"Leer un fallo y saber qué te está diciendo",
   u"Es la base de todo lo demás: lo de arriba no reemplaza esto"],
  "https://docs.pytest.org/en/stable/getting-started.html"),

 ("t04", 2, "3 h", "flow", False, "",
  u"Fixtures: preparar y limpiar",
  u"Lo que separa un puñado de pruebas de una suite: cómo se prepara el estado que cada prueba necesita, y cómo se deja todo limpio después.",
  u"Terminas esta parte cuando tus pruebas no dependen del orden en que corren.",
  [u"Preparar datos sin copiar y pegar en cada prueba",
   u"Por qué una suite que depende del orden es una suite rota",
   u"Alcances: qué se arma una vez y qué se arma cada vez"],
  "https://docs.pytest.org/en/stable/how-to/fixtures.html"),

 ("t05", 2, "2 h", "code", False, "",
  u"Vitest, lo mismo en JavaScript",
  u"El equivalente del lado del navegador. Si vas a probar una aplicación web, las unitarias van acá.",
  u"Terminas esta parte cuando pruebas una función de tu frontend sin abrir el navegador.",
  [u"Las mismas ideas, en el otro lenguaje",
   u"Correr las pruebas mientras escribes, no al final",
   u"Simulacros: cómo se prueba algo que llama a un servidor"],
  "https://vitest.dev/guide/"),

 # ---------------------------------------------- 3. probar la aplicacion
 ("t06", 3, "2 h", "web", True, "",
  u"Playwright, la primera prueba",
  u"Automatizar el navegador de verdad: abrir la página, hacer clic, escribir, comprobar. Es la herramienta que se está llevando el mercado.",
  u"Terminas esta parte cuando una prueba tuya recorre tu aplicación sola y te dice si algo se rompió.",
  [u"Instalar y correr, que en esta herramienta es de verdad rápido",
   u"Escribir una prueba que hace lo que haría una persona",
   u"Ver la grabación de la prueba que falló, que es la mitad del trabajo"],
  "https://playwright.dev/docs/intro"),

 ("t07", 3, "2 h", "search", False, "",
  u"Encontrar elementos sin que se rompa mañana",
  u"El tema que decide si tu suite sobrevive un rediseño. Localizar por rol y por texto en vez de por la clase CSS que alguien va a cambiar.",
  u"Terminas esta parte cuando tus pruebas siguen pasando después de que el equipo toca el HTML.",
  [u"Localizadores que describen qué hace el elemento, no dónde está",
   u"Por qué el selector CSS es la causa número uno de pruebas frágiles",
   u"De paso, te obliga a mirar la accesibilidad de la página"],
  "https://playwright.dev/docs/locators"),

 ("t08", 3, "2 h", "web", False, "",
  u"Cypress, la otra escuela",
  u"La herramienta que muchos equipos ya tienen puesta. Conviene conocerla: no vas a elegir vos la que usa la empresa donde entres.",
  u"Terminas esta parte cuando lees una suite de Cypress ajena y sabes qué hace.",
  [u"El mismo problema resuelto con otra filosofía",
   u"Qué gana y qué pierde contra Playwright",
   u"Poder trabajar donde ya está elegida"],
  "https://docs.cypress.io/app/get-started/why-cypress"),

 ("t09", 3, "2 h", "cloud", True, "",
  u"Probar APIs",
  u"Lo que hay detrás de la pantalla. Escribir comprobaciones sobre las respuestas de un servicio: códigos, cuerpos, errores.",
  u"Terminas esta parte cuando una API rota se detecta antes de que alguien abra la aplicación.",
  [u"Comprobar respuestas, no solo mirarlas",
   u"Encadenar pedidos: usar lo que devolvió uno en el siguiente",
   u"Es la capa más barata de probar y la que más problemas encuentra"],
  "https://learning.postman.com/docs/writing-scripts/test-scripts/"),

 # ---------------------------------------------- 4. que corra solo
 ("t10", 4, "2 h", "flow", True, "",
  u"Que las pruebas corran en cada cambio",
  u"Una suite que hay que acordarse de correr no sirve. Acá se conecta a GitHub Actions para que corra sola en cada commit.",
  u"Terminas esta parte cuando un cambio que rompe algo no llega a la rama principal.",
  [u"Un flujo que corre tus pruebas sin que nadie apriete nada",
   u"Bloquear lo que rompe, que es el punto de todo esto",
   u"Es lo que separa 'tengo pruebas' de 'las pruebas me cuidan'"],
  "https://docs.github.com/en/actions/writing-workflows/quickstart"),

 ("t11", 4, "1 h 30", "clock", False, "",
  u"Playwright en integración continua",
  u"La parte específica: correr pruebas de navegador en un servidor que no tiene pantalla, y guardar la evidencia de lo que falló.",
  u"Terminas esta parte cuando puedes ver el video de la prueba que falló anoche.",
  [u"Navegador sin pantalla, que es donde todos se traban la primera vez",
   u"Guardar rastros y videos de lo que fallo",
   u"Correr en paralelo para que la suite no tarde una hora"],
  "https://playwright.dev/docs/ci-intro"),

 ("t12", 4, "3 h", "chart", False, "",
  u"Carga: qué pasa cuando entran mil",
  u"k6 es de código abierto y se escribe en JavaScript. Simular carga real y ver dónde se cae el sistema antes de que se caiga solo.",
  u"Terminas esta parte cuando sabes cuántos usuarios aguanta lo que probaste, con un número.",
  [u"Medir en vez de suponer",
   u"La diferencia entre lento y roto",
   u"Es lo que te preguntan cuando algo se cayó y nadie sabe por qué"],
  "https://grafana.com/docs/k6/latest/get-started/running-k6/"),

 ("t13", 4, "2 h", "user", True, "",
  u"Accesibilidad: probar que se pueda usar",
  u"La guía del W3C para evaluar accesibilidad. Es requisito legal en cada vez más lugares, y casi nadie lo prueba.",
  u"Terminas esta parte cuando encuentras los problemas de accesibilidad de un sitio con un método y no a ojo.",
  [u"Qué se puede comprobar automático y qué hay que mirar a mano",
   u"Es de las pocas habilidades de QA que se piden y no abundan",
   u"Se cruza con los localizadores: probar bien y ser accesible van juntos"],
  "https://www.w3.org/WAI/test-evaluate/"),
]

# El <head> no se toca: lo reescribe build-brand.py entero, y por eso
# la ruta se da de alta ahi y no aca.
TEXTOS = [
 (u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""",
  u"""  /* Testing. Verde: es el color del check que pasa, y no lo usa
     ninguna de las otras diecisiete. */
  --accent:        #15803D;
  --accent-strong: #106430;
  --accent-soft:   #E3F5E9;
  --accent-line:   #BCE3C9;""", 1),

 (u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""",
  u"""  --accent:        #4ADE80;
  --accent-strong: #86EFAC;
  --accent-soft:   #0B2E19;
  --accent-line:   #14532D;""", 1),

 (u'<span class="brand-sub">/ Airflow</span>',
  u'<span class="brand-sub">/ Testing</span>', 1),

 (u'<h1>Orquestar con <span class="grad">Airflow</span></h1>',
  u'<h1>Probar el <span class="grad">software</span></h1>', 1),

 (u'<span class="dest">academy.astronomer.io</span>',
  u'<span class="dest">playwright.dev</span>', 1),

 (u"los ocho pasos de Airflow",
  u"los trece pasos de testing", 1),

 # La nota del certificado. En airflow.html quedo con el texto de
 # Astronomer y el numero viejo: se reemplaza entera, que ademas es
 # donde va lo que si cuesta.
 (u"Se desbloquea cuando cierres los ocho pasos del mapa. La certificación "
  u"oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para "
  u"aprender esto.",
  u"Se desbloquea cuando cierres los trece pasos del mapa. La certificación "
  u"ISTQB es aparte y la cobra cada país por su cuenta: el sílabo con el "
  u"que se estudia es gratis, y es el que está acá.", 1),

 (u"<h2>Tres tramos, ocho pasos</h2>",
  u"<h2>Cuatro tramos, trece pasos</h2>", 1),

 (u'id="startDest">Airflow 101<',
  u'id="startDest">el sílabo de ISTQB<', 1),
]

PIE = (u'<p class="hero-foot">Todo lo de acá es documentación oficial y abierta: no pide '
       u'cuenta, no tiene créditos y no caduca. Falta a propósito Test Automation University, '
       u'que tiene los mejores cursos gratuitos de testing que existen: hoy anuncia en cada uno '
       u'"Credits coming soon", y una ruta no se arma sobre algo que avisaron que va a cambiar. '
       u'El examen de ISTQB cuesta; el sílabo con el que se estudia, no.</p>')

LEAD = (u'<p class="hero-lead">Probar no es apretar botones hasta que algo se rompa: es saber '
        u'qué probar en cada nivel y dejarlo corriendo solo. Acá va del vocabulario que usa la '
        u'industria a una suite que se ejecuta en cada cambio y avisa antes de que el problema '
        u'llegue a producción.</p>')


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
        print(u"  ABORTA: no encuentro %s" % BASE); sys.exit(1)
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

    v = re.search(r'<p class="hero-foot">.*?</p>', t, re.S)
    if not v:
        print(u"  ABORTA: no encuentro el pie del hero"); sys.exit(1)
    t = t[:v.start()] + PIE + t[v.end():]

    v2 = re.search(r'<p class="hero-lead">.*?</p>', t, re.S)
    t = t[:v2.start()] + LEAD + t[v2.end():]

    # la clave de la ruta: se hereda de la copiada y no se ve mirando
    t = t.replace(u'var MI_RUTA = "airflow"', u'var MI_RUTA = "testing"')
    t = t.replace(u'var MI_CLAVE = "airflow"', u'var MI_CLAVE = "testing"')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 4 tramos" % (SALE, len(C)))


main()
