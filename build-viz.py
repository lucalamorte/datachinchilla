# -*- coding: utf-8 -*-
u"""La ruta de visualizacion y BI.

   El segundo hueco que medía contenido.py: visualizacion con cuatro
   pasos y veintisiete horas, contra un pedido de siete repartido en
   tres puestos -Data Analyst en 3, Data Scientist en 2, analista
   funcional en 2-. Y de esos cuatro pasos, tres son graficos con
   Python y R de la ruta de Data Science: para un Data Analyst que
   quiere hacer tableros no hay casi nada.

   Es raro que el tema mas flaco sea justo el del puesto mas buscado.

   La ruta se parte en dos mitades a proposito:

   - Primero como se lee un grafico, que es lo que no cambia. El libro
     de Claus Wilke esta entero y gratis en la web y es el mejor texto
     que hay del tema; el catalogo de visualizaciones esta en espanol
     y contesta "que grafico uso para esto"; y la guia de Storytelling
     with Data es la referencia de como se cuenta con un grafico.
   - Despues las herramientas. Power BI pesa mas porque Microsoft
     publica su formacion entera gratis y en espanol, y porque es la
     que mas aparece en los avisos en espanol. Looker Studio es gratis
     de verdad, Tableau publica su formacion en Tableau Public, y
     Metabase es de codigo abierto.

   Lo que no esta: los cursos de Tableau del sitio principal, que
   estan detras de un muro que devuelve 403. Los de Tableau Public
   son abiertos y son los que van.

   Uso: python build-viz.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "airflow.html"
SALE = "visualizacion.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Cómo se lee un gráfico", desc: "Lo que no cambia cuando cambia la herramienta" },
  { n: 2, title: "Power BI", desc: "La que más aparece en los avisos en español" },
  { n: 3, title: "Las otras", desc: "Gratis, abiertas, y las vas a encontrar puestas" }
];'''

C = [
 # ------------------------------------ 1. como se lee un grafico
 ("v01", 1, "8 h", "school", True, "",
  u"Fundamentos de visualización, el libro",
  u"Claus Wilke publicó el libro entero y gratis en la web. Por qué un gráfico se entiende o no: escalas, color, cuánta información tolera un ojo, y los errores que se repiten en todas las presentaciones.",
  u"Terminas esta parte cuando miras un gráfico ajeno y sabes decir qué está mal en él.",
  [u"Los principios, que sirven en cualquier herramienta",
   u"El catálogo de gráficos con qué hace bien cada uno",
   u"Gratis y completo: no es una muestra del libro pago"],
  "https://clauswilke.com/dataviz/"),

 ("v02", 1, "2 h", "chart", False, "",
  u"Qué gráfico uso para esto",
  u"El catálogo de visualizaciones, en español: entras por lo que quieres mostrar -una comparación, una parte de un todo, un cambio en el tiempo- y sales con los gráficos que sirven.",
  u"Terminas esta parte cuando eliges el gráfico por lo que quieres decir y no por costumbre.",
  [u"Entrar por la pregunta, no por el tipo de gráfico",
   u"Está en español, que en este tema es raro",
   u"Se consulta, no se recorre: queda de referencia"],
  "https://datavizcatalogue.com/ES/"),

 ("v03", 1, "2 h", "build", False, "",
  u"Contar algo con un gráfico",
  u"La guía de Storytelling with Data. Un gráfico correcto y un gráfico que convence no son lo mismo, y la diferencia es casi toda decisiones de qué sacar.",
  u"Terminas esta parte cuando tu gráfico se entiende sin que estés al lado explicándolo.",
  [u"Qué sacar, que es más importante que qué poner",
   u"Dirigir la mirada a lo que importa",
   u"Es lo que separa un tablero que se usa de uno que se abrió una vez"],
  "https://www.storytellingwithdata.com/chart-guide"),

 # ------------------------------------ 2. power bi
 ("v04", 2, "5 h", "data", True, "",
  u"Power BI, de cero",
  u"Conectar los datos, limpiarlos y hacer el primer informe. Microsoft publica su formación completa, gratis y en español.",
  u"Terminas esta parte cuando armas un informe con datos tuyos y lo compartes.",
  [u"De un archivo suelto a un informe que otro puede abrir",
   u"Limpiar los datos antes de graficarlos, que es la mitad del trabajo",
   u"Gratis, en español y sin cuenta para leerlo"],
  "https://learn.microsoft.com/es-es/training/paths/get-started-power-bi/"),

 ("v05", 2, "6 h", "data", False, "",
  u"Modelar los datos",
  u"El paso que separa un informe que anda de uno que aguanta: relaciones entre tablas, medidas y DAX. Es donde se traba todo el mundo.",
  u"Terminas esta parte cuando escribes una medida que suma bien sin importar cómo filtren.",
  [u"Relaciones entre tablas: por qué el total no da",
   u"DAX, lo suficiente para no copiar fórmulas de internet",
   u"Se cruza con modelado de datos, que ya está en el sitio"],
  "https://learn.microsoft.com/es-es/training/paths/model-power-bi/"),

 ("v06", 2, "5 h", "chart", False, "",
  u"Visualizaciones y análisis",
  u"Las visualizaciones que trae, cuándo usar cada una, y cómo se arma un tablero que la gente pueda recorrer sola.",
  u"Terminas esta parte cuando alguien encuentra su respuesta en tu tablero sin preguntarte.",
  [u"Filtros y segmentaciones que no confunden",
   u"Un tablero que se recorre, no una pila de gráficos",
   u"Con esto cierras el temario de la certificación PL-300"],
  "https://learn.microsoft.com/es-es/training/paths/perform-analytics-power-bi/"),

 # ------------------------------------ 3. las otras
 ("v07", 3, "3 h", "cloud", True, "",
  u"Looker Studio, de Google",
  u"Gratis de verdad, en el navegador y conectado a lo de Google. Es lo que vas a encontrar en empresas chicas y en marketing.",
  u"Terminas esta parte cuando publicas un tablero que se actualiza solo y se comparte con un link.",
  [u"Sin instalar nada y sin licencia",
   u"Conecta con Sheets, BigQuery y Analytics",
   u"Es la que más aparece cuando no hay presupuesto"],
  "https://support.google.com/looker-studio/answer/6283323"),

 ("v08", 3, "4 h", "search", False, "",
  u"Tableau, con Tableau Public",
  u"La herramienta que domina en las empresas grandes. Tableau Public es gratis y su formación es abierta: alcanza para saber trabajar en ella.",
  u"Terminas esta parte cuando abres un libro de Tableau ajeno y sabes qué hace.",
  [u"La otra mitad del mercado, la que Power BI no tiene",
   u"Tableau Public es gratis: lo pago es la versión de empresa",
   u"Poder trabajar donde ya está elegida"],
  "https://public.tableau.com/app/resources/learn"),

 ("v09", 3, "3 h", "code", False, "",
  u"Metabase, código abierto",
  u"La que se instala una empresa cuando no quiere pagar licencias. Preguntar en lenguaje casi natural sobre una base, y armar tableros arriba de SQL.",
  u"Terminas esta parte cuando dejas armado un tablero que el equipo consulta sin saber SQL.",
  [u"Tableros arriba de SQL, que es lo que ya sabes",
   u"De código abierto: se instala y no se paga",
   u"Es la puerta para que el resto del equipo consulte solo"],
  "https://www.metabase.com/learn/"),
]

TEXTOS = [
 (u'<a class="btn-quiet" href="https://academy.astronomer.io/" target="_blank" rel="noopener">',
  u'<a class="btn-quiet" href="https://clauswilke.com/dataviz/" target="_blank" rel="noopener">', 1),

 (u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""",
  u"""  /* Visualizacion. Ambar oscuro: es el color de un grafico y no lo
     usa ninguna de las otras veintiuna. */
  --accent:        #A16207;
  --accent-strong: #7F4E05;
  --accent-soft:   #FBF1DC;
  --accent-line:   #EBD4A4;""", 1),

 (u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""",
  u"""  --accent:        #E8B84B;
  --accent-strong: #F2CE78;
  --accent-soft:   #33260A;
  --accent-line:   #5A4413;""", 1),

 (u'<span class="brand-sub">/ Airflow</span>',
  u'<span class="brand-sub">/ Visualización</span>', 1),

 (u'<h1>Orquestar con <span class="grad">Airflow</span></h1>',
  u'<h1>Visualización y <span class="grad">tableros</span></h1>', 1),

 (u'<span class="dest">academy.astronomer.io</span>',
  u'<span class="dest">clauswilke.com</span>', 1),

 (u"los ocho pasos de Airflow", u"los nueve pasos de visualización", 1),

 (u"Se desbloquea cuando cierres los ocho pasos del mapa. La certificación "
  u"oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para "
  u"aprender esto.",
  u"Se desbloquea cuando cierres los nueve pasos del mapa. La certificación "
  u"PL-300 de Power BI es aparte y la cobra Microsoft: las tres partes de Power BI "
  u"de acá son su temario completo, y son gratis.", 1),

 (u"<h2>Tres tramos, ocho pasos</h2>", u"<h2>Tres tramos, nueve pasos</h2>", 1),

 (u'id="startDest">Airflow 101<', u'id="startDest">el libro de Claus Wilke<', 1),

 (u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Los de Astronomer dejan constancia en su academia; los de Apache "
  u"son documentación y no dejan nada más que saberlo.",
  u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Las tres partes de Power BI son el temario de la PL-300, que es la única "
  u"credencial del tema que se pide por nombre.", 1),
]

PIE = (u'<p class="hero-foot">Todo gratis. El libro de Claus Wilke está entero en la web, no es '
       u'una muestra; Microsoft publica su formación de Power BI completa y en español; Looker '
       u'Studio no tiene versión paga; Tableau Public es gratis y lo que cuesta es la versión de '
       u'empresa; Metabase es de código abierto. La certificación PL-300 sí se paga, y los tres '
       u'partes de Power BI de acá son exactamente su temario.</p>')

LEAD = (u'<p class="hero-lead">Un gráfico no es la respuesta: es cómo alguien más la entiende. '
        u'Acá va de por qué un gráfico se lee o no -que es lo que no cambia aunque cambie la '
        u'herramienta- a armar tableros en las cuatro que vas a encontrar puestas: Power BI, '
        u'Looker Studio, Tableau y Metabase.</p>')


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

    t = t.replace(u'var MI_RUTA = "airflow"', u'var MI_RUTA = "viz"')
    t = t.replace(u'var MI_CLAVE = "airflow"', u'var MI_CLAVE = "viz"')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 3 tramos" % (SALE, len(C)))


main()
