# -*- coding: utf-8 -*-
u"""La ruta de analista funcional.

   Es la ruta mas dificil de armar del sitio, y conviene decir por que
   antes de mirarla: este oficio no se aprende con cursos. Se aprende
   con metodo y con anos de hablar con gente que no sabe explicar lo
   que necesita. No existe un "CS50 del analisis funcional".

   Lo que si existe, y es lo que esta aca, es el material de
   referencia con el que se trabaja: los marcos que todo el mundo usa,
   la notacion con la que se dibuja un proceso, y las dos habilidades
   tecnicas que separan a un analista funcional de alguien que toma
   notas -consultar una base y leer un tablero-.

   De donde sale:

   - La Guia Scrum y el Manifiesto Agil son los documentos originales,
     gratis y en espanol. Son cortos: eso es una virtud, no una falta.
   - Atlassian publica su guia de agilidad completa y abierta. Es la
     mejor explicacion gratuita que hay de historias de usuario,
     epicas y requisitos, y la escribio quien hace la herramienta que
     vas a usar.
   - Camunda publica la referencia de BPMN entera. BPMN es el idioma
     con el que se dibuja un proceso y se acuerda que hace.
   - Nielsen Norman Group para investigar con usuarios: es la
     autoridad del tema y publica sus articulos abiertos.
   - SQL y Power BI salen del material que el sitio ya usa en otras
     rutas. Un curso repetido en dos rutas no es un problema: el
     avance viaja con el curso, no con la ruta.

   Lo que NO esta y por que: BABOK, que es el cuerpo de conocimiento
   de referencia del oficio, no es gratis. Se dice en el pie.

   Uso: python build-funcional.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "airflow.html"
SALE = "funcional.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Cómo se trabaja", desc: "Los marcos que vas a encontrar en cualquier equipo" },
  { n: 2, title: "Escribir lo que se pide", desc: "De una charla a algo que alguien puede construir" },
  { n: 3, title: "Dibujar el proceso", desc: "BPMN, que es el idioma para acordar qué pasa" },
  { n: 4, title: "Lo técnico que sí hace falta", desc: "Consultar los datos y leer un tablero" }
];'''

C = [
 # ------------------------------------------- 1. como se trabaja
 ("f01", 1, "20 min", "law", True, "",
  u"El Manifiesto Ágil, el original",
  u"Cuatro valores y doce principios, en una página. Es corto a propósito, y es de donde salió todo lo que después te van a vender en cursos de tres días.",
  u"Terminas esta parte cuando reconoces qué de lo que hace tu equipo es ágil y qué es una reunión con otro nombre.",
  [u"El documento original, en español, gratis",
   u"Veinte minutos que te ahorran discusiones de años",
   u"Sirve para detectar cuándo alguien usa la palabra sin el contenido"],
  "https://agilemanifesto.org/iso/es/manifesto.html"),

 ("f02", 1, "2 h", "school", False, "",
  u"La Guía Scrum",
  u"El documento oficial: los roles, los eventos y los artefactos, sin interpretación de nadie. Trece páginas.",
  u"Terminas esta parte cuando distingues Scrum de lo que tu empresa llama Scrum.",
  [u"Qué es cada ceremonia y para qué existe de verdad",
   u"Dónde entra el analista funcional en ese marco",
   u"Es la fuente: todo curso pago de Scrum explica esto"],
  "https://scrumguides.org/scrum-guide.html"),

 ("f03", 1, "2 h", "flow", False, "",
  u"Scrum en la práctica",
  u"La guía de Atlassian: lo mismo pero contado por quienes hacen la herramienta donde vas a cargar los tickets. Con los problemas reales que la guía oficial no cuenta.",
  u"Terminas esta parte cuando sabes qué hacer cuando el sprint no entra.",
  [u"Cómo se ve el marco cuando lo aplica gente con apuro",
   u"El vocabulario de Jira, que es donde vas a trabajar",
   u"Los errores típicos, contados antes de que los cometas"],
  "https://www.atlassian.com/agile/scrum"),

 # ------------------------------------------- 2. escribir lo que se pide
 ("f04", 2, "2 h", "build", True, "",
  u"Historias de usuario",
  u"El corazón del oficio: pasar de «quiero que el sistema haga algo» a algo que un equipo puede construir y verificar. Quién, qué y para qué.",
  u"Terminas esta parte cuando escribes una historia que el desarrollador no tiene que venir a preguntarte.",
  [u"La forma de la historia, y por qué esa forma y no otra",
   u"Criterios de aceptación: cómo se sabe que está hecho",
   u"Es lo que te van a pedir escribir el primer día"],
  "https://www.atlassian.com/agile/project-management/user-stories"),

 ("f05", 2, "1 h 30", "chart", False, "",
  u"Épicas, historias y temas",
  u"Cómo se agrupa el trabajo cuando no entra en una historia. Es lo que evita el backlog de trescientos tickets sueltos.",
  u"Terminas esta parte cuando partes un pedido grande en piezas que se pueden entregar de a una.",
  [u"Partir sin romper: cada pieza tiene que servir sola",
   u"Los niveles, para poder hablar con negocio y con desarrollo",
   u"Ordenar un backlog en vez de acumularlo"],
  "https://www.atlassian.com/agile/project-management/epics-stories-themes"),

 ("f06", 2, "2 h", "search", False, "",
  u"Preguntar bien: investigación con usuarios",
  u"Nielsen Norman Group, que es la autoridad del tema. Qué método usar según lo que necesitas saber, y por qué preguntarle a la gente qué quiere casi nunca funciona.",
  u"Terminas esta parte cuando eliges cómo averiguar algo en vez de mandar una encuesta por defecto.",
  [u"Qué método sirve para qué pregunta",
   u"Por qué lo que la gente dice y lo que hace no coinciden",
   u"Es la diferencia entre tomar el pedido y entender el problema"],
  "https://www.nngroup.com/articles/which-ux-research-methods/"),

 # ------------------------------------------- 3. dibujar el proceso
 ("f07", 3, "3 h", "flow", True, "",
  u"BPMN, la referencia completa",
  u"El idioma con el que se dibuja un proceso: qué significa cada figura, y por qué un diagrama mal hecho esconde justamente lo que hay que discutir. Camunda publica la referencia entera.",
  u"Terminas esta parte cuando dibujas un proceso y el que lo lee entiende lo mismo que tú.",
  [u"Cada figura y qué quiere decir, sin ambigüedad",
   u"Dónde se esconden las excepciones, que es donde está el trabajo",
   u"Es notación estándar: lo lee cualquiera, en cualquier empresa"],
  "https://camunda.com/bpmn/reference/"),

 ("f08", 3, "1 h 30", "code", False, "",
  u"Casos de uso y UML",
  u"La notación anterior a BPMN, que sigue viva en la mitad de las empresas grandes. Vale conocerla porque te la vas a encontrar escrita.",
  u"Terminas esta parte cuando lees un diagrama de casos de uso ajeno sin traductor.",
  [u"Actores, casos y relaciones",
   u"Cuándo un caso de uso dice más que una historia",
   u"Poder trabajar donde ya está elegido"],
  "https://www.uml-diagrams.org/use-case-diagrams.html"),

 # ------------------------------------------- 4. lo tecnico que si hace falta
 ("f09", 4, "4 h 30", "sql", True, "",
  u"SQL: mirar los datos tú mismo",
  u"Es lo que separa a un analista funcional de alguien que toma notas. Poder responder «¿cuántos casos hay así?» sin pedirle a nadie que lo consulte.",
  u"Terminas esta parte cuando contestas una pregunta del negocio con una consulta, en el momento.",
  [u"SELECT, filtros y JOINs: alcanza para el noventa por ciento",
   u"Verificar un supuesto antes de escribir el requisito",
   u"Es la habilidad que más rápido te cambia el peso en una reunión"],
  "https://www.stratascratch.com/learn/comprehensive-sql/introduction-to-databases-and-sql"),

 ("f10", 4, "5 h", "chart", False, "",
  u"Power BI, del lado de quien pide",
  u"No para construir tableros, sino para saber qué se puede pedir, qué cuesta caro y por qué el dato no está como lo quieres.",
  u"Terminas esta parte cuando pides un tablero sabiendo qué implica cada cosa que pediste.",
  [u"Qué se puede y qué no, antes de prometerlo",
   u"El vocabulario para hablar con el equipo de datos",
   u"Gratis, en español, de Microsoft"],
  "https://learn.microsoft.com/es-es/training/paths/get-started-power-bi/"),
]

TEXTOS = [
 (u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""",
  u"""  /* Analista funcional. Terracota: es el unico calido de las
     diecinueve, y esta ruta es la unica que no es tecnica. */
  --accent:        #A94F2E;
  --accent-strong: #863D22;
  --accent-soft:   #FBEDE8;
  --accent-line:   #EFCCBE;""", 1),

 (u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""",
  u"""  --accent:        #E89571;
  --accent-strong: #F2B79C;
  --accent-soft:   #3A1B10;
  --accent-line:   #5E2E1C;""", 1),

 (u'<span class="brand-sub">/ Airflow</span>',
  u'<span class="brand-sub">/ Analista funcional</span>', 1),

 (u'<h1>Orquestar con <span class="grad">Airflow</span></h1>',
  u'<h1>Analista <span class="grad">funcional</span></h1>', 1),

 (u'<span class="dest">academy.astronomer.io</span>',
  u'<span class="dest">scrumguides.org</span>', 1),

 (u"los ocho pasos de Airflow", u"los diez pasos de analista funcional", 1),

 (u"Se desbloquea cuando cierres los ocho pasos del mapa. La certificación "
  u"oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para "
  u"aprender esto.",
  u"Se desbloquea cuando cierres los diez pasos del mapa. Las certificaciones "
  u"del oficio -CBAP del IIBA, las de Scrum- se pagan y no están acá: lo que "
  u"está es el material con el que se trabaja de verdad.", 1),

 (u"<h2>Tres tramos, ocho pasos</h2>", u"<h2>Cuatro tramos, diez pasos</h2>", 1),

 (u'id="startDest">Airflow 101<', u'id="startDest">el Manifiesto Ágil<', 1),

 (u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Los de Astronomer dejan constancia en su academia; los de Apache "
  u"son documentación y no dejan nada más que saberlo.",
  u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Ninguno deja credencial: son documentos oficiales y guías abiertas. "
  u"Las certificaciones de este oficio se pagan, y se dice cuáles.", 1),
]

PIE = (u'<p class="hero-foot">Hay que decirlo de frente: este oficio no se aprende con cursos. '
       u'Se aprende con método y con años de hablar con gente que no sabe explicar lo que '
       u'necesita, y no existe un CS50 del análisis funcional. Lo que está acá es el material '
       u'de referencia con el que se trabaja: los documentos originales de Scrum y del '
       u'manifiesto, la guía de agilidad de Atlassian, la referencia de BPMN de Camunda y los '
       u'métodos de Nielsen Norman. El BABOK, que es el cuerpo de conocimiento de referencia '
       u'del oficio, no es gratis y por eso no está.</p>')

LEAD = (u'<p class="hero-lead">El analista funcional es quien traduce: de lo que el negocio '
        u'necesita a algo que un equipo puede construir, y de vuelta. Acá va de los marcos que '
        u'vas a encontrar en cualquier equipo a escribir un requisito que nadie tenga que venir '
        u'a preguntarte, más las dos habilidades técnicas que cambian tu peso en una reunión: '
        u'consultar los datos tú mismo y saber qué se le puede pedir a un tablero.</p>')


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

    t = t.replace(u'var MI_RUTA = "airflow"', u'var MI_RUTA = "funcional"')
    t = t.replace(u'var MI_CLAVE = "airflow"', u'var MI_CLAVE = "funcional"')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 4 tramos" % (SALE, len(C)))


main()
