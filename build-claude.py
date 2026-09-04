# -*- coding: utf-8 -*-
"""La ruta de Claude Academy.

   Anthropic publica veinticinco cursos gratuitos con insignia. Ocho
   son el mismo "AI Fluency" repetido para audiencias distintas
   -docentes, K-12, ONGs, pymes, estudiantes, trabajo creativo- y uno
   es de despliegue para un rol de IT. Nada de eso le sirve a quien
   entra a este sitio, asi que quedan dieciseis.

   Va como ruta propia y no repartida en "LLMs y agentes" porque
   tiene arco entero -entender que es, usarlo, construir con el,
   conectarlo, llevarlo a produccion- y porque esa ruta ya tiene
   veintiocho cursos, todos de CognitiveClass: sumarle una fuente con
   otra logica la volveria una bolsa.

   Las horas, la insignia y lo que cubre cada curso salen de la
   pagina de cada uno, no de mi cabeza.

   Se arma copiando ai-fundamentos.html, que es la ruta con la
   estructura mas parecida, y cambiando lo que es propio de la ruta.

   Uso: python build-claude.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "ai-fundamentos.html"
SALE = "claude.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Qué es y qué no", desc: "Para qué sirve de verdad y dónde falla" },
  { n: 2, title: "Usarlo todos los días", desc: "La herramienta, en el trabajo que ya tienes" },
  { n: 3, title: "Construir con él", desc: "De usarlo a que sea parte de lo que haces" },
  { n: 4, title: "Conectarlo con lo tuyo", desc: "MCP, subagentes y skills: que toque tus sistemas" },
  { n: 5, title: "Llevarlo a producción", desc: "En la nube donde ya trabajas, y cómo cambia el equipo" }
];'''

# (id, acto, tiempo, icono, jefe, titulo, resumen, objetivo, wins, slug)
C = [
 ("c01", 1, "4 horas", "brain", True,
  u"AI Fluency: Framework & Foundations",
  u"El marco de las cuatro D -delegar, describir, discernir, diligencia- para trabajar con un modelo sin quedar a merced de lo que conteste. Acá empieza todo lo demás.",
  u"Terminas esto cuando sabes decidir qué delegar y qué no, y por qué.",
  [u"Las cuatro D, que es el marco que usa el resto de los cursos",
   u"Cómo funciona un modelo generativo, sin misterio",
   u"Insignia de Anthropic al aprobar la evaluación final"],
  "ai-fluency-framework-foundations"),

 ("c02", 1, "3 h 30 min", "check", False,
  u"AI Capabilities and Limitations",
  u"Las cuatro propiedades que explican todo lo que un modelo hace bien y todo lo que hace mal: predicción, conocimiento, memoria de trabajo y direccionabilidad.",
  u"Terminas esto cuando ves una respuesta rara y sabes cuál de las cuatro falló.",
  [u"Diagnosticar una falla en vez de volver a pedir lo mismo",
   u"Qué se arregla con contexto y qué no se arregla",
   u"Insignia de Anthropic"],
  "ai-capabilities-and-limitations"),

 ("c03", 2, "2 h 30 min", "school", True,
  u"Claude 101",
  u"La herramienta entera: conversaciones, prompting, y después Projects, Artifacts, Skills y Connectors. Con ejemplos por rol, no en abstracto.",
  u"Terminas esto cuando armaste un Project con tus documentos y lo usas todos los días.",
  [u"Projects y Artifacts, que es donde vive el trabajo largo",
   u"Skills y Connectors para que traiga tus datos",
   u"Insignia de Anthropic"],
  "claude-101"),

 ("c04", 2, "2 h 30 min", "flow", False,
  u"Introduction to Claude Cowork",
  u"Delegar trabajo de varios pasos: armar el espacio, darle contexto, dejarlo correr y revisar. Con tareas agendadas, instrucciones globales y cómo compartirlo con el equipo.",
  u"Terminas esto cuando le dejas una tarea larga y el resultado te sirve sin rehacerlo.",
  [u"Delegar un trabajo de varios pasos y que vuelva bien",
   u"Tareas agendadas y trabajo compartido con el equipo",
   u"Insignia de Anthropic"],
  "introduction-to-claude-cowork"),

 ("c05", 2, "1 h 30 min", "code", False,
  u"Claude Code 101",
  u"El agente que trabaja en la terminal y en el editor: el bucle agéntico, la ventana de contexto, las herramientas y los permisos. Y cómo configurarlo para tu proyecto.",
  u"Terminas esto cuando Claude Code toca tu repo y entiendes cada permiso que le diste.",
  [u"El bucle agéntico y por qué importa la ventana de contexto",
   u"Los archivos de configuración de tu propio proyecto",
   u"Insignia de Anthropic"],
  "claude-code-101"),

 ("c06", 2, "1 hora", "build", False,
  u"Claude Code in Action",
  u"Sesiones largas sin perder el control: acotar el trabajo, escribir instrucciones que se cumplan, poner reglas con hooks, agendar corridas y revisar lo que hizo solo antes de mostrarlo.",
  u"Terminas esto cuando dejas una tarea corriendo sola y confias en revisar el resultado.",
  [u"Hooks, que son reglas que el agente no puede saltarse",
   u"Cómo verificar trabajo hecho sin supervisión",
   u"Insignia de Anthropic"],
  "claude-code-in-action"),

 ("c07", 3, "3 horas", "brain", False,
  u"AI Fluency for Builders",
  u"Las cuatro D aplicadas a construir: qué sale confiable y qué no, y cómo revisar lo que genera, tanto el código como lo que ve el usuario.",
  u"Terminas esto cuando sabes qué revisar antes de que algo generado salga a producción.",
  [u"Evaluar código generado sin leerlo línea por línea",
   u"Dónde poner el control de calidad cuando el volumen sube",
   u"Insignia de Anthropic"],
  "ai-fluency-for-builders"),

 ("c08", 3, "1 h 30 min", "code", True,
  u"Claude Platform 101",
  u"De usarlo a construir con él: la primera llamada a la API, el bucle del agente, el uso de herramientas y los agentes gestionados. Con elección de modelo y manejo de contexto.",
  u"Terminas esto cuando tu primera aplicación hace una llamada real y devuelve lo que esperabas.",
  [u"Tu primera llamada a la API, funcionando",
   u"Elegir modelo por costo y por tarea, no por costumbre",
   u"Insignia de Anthropic"],
  "claude-platform-101"),

 ("c09", 3, "9 horas", "build", False,
  u"Building with the Claude API",
  u"El curso largo: autenticación, prompting, RAG, uso de herramientas y sistemas basados en agentes. Se sale con un chatbot y automatizaciones andando.",
  u"Terminas esto cuando tienes una aplicación tuya en producción, no un notebook.",
  [u"RAG de punta a punta, que es lo que se pide en el trabajo",
   u"Uso de herramientas y agentes, con código propio",
   u"Insignia de Anthropic"],
  "building-with-the-claude-api"),

 ("c10", 4, "1 hora", "flow", True,
  u"Introduction to Model Context Protocol",
  u"Servidores y clientes MCP en Python, con los tres primitivos -herramientas, recursos y prompts- que conectan el modelo con lo que ya existe en tu empresa.",
  u"Terminas esto cuando tu propio servidor MCP responde y Claude lo usa.",
  [u"Los tres primitivos y cuándo va cada uno",
   u"Un servidor MCP propio, andando",
   u"Insignia de Anthropic"],
  "introduction-to-model-context-protocol"),

 ("c11", 4, "1 h 30 min", "cloud", False,
  u"Model Context Protocol: Advanced Topics",
  u"Lo que hace falta para que un servidor MCP aguante producción: sampling, notificaciones, roots, los transportes STDIO y StreamableHTTP, y cómo desplegarlo.",
  u"Terminas esto cuando tu servidor está desplegado y no corriendo en tu máquina.",
  [u"Elegir transporte según dónde vive el servidor",
   u"Desplegarlo de forma que lo use alguien más",
   u"Insignia de Anthropic"],
  "model-context-protocol-advanced-topics"),

 ("c12", 4, "45 min", "flow", False,
  u"Introduction to Subagents",
  u"Partir un trabajo grande en subagentes que corren en paralelo y orquestarlos sin que el resultado dependa de la suerte. Y cuándo no conviene.",
  u"Terminas esto cuando partiste una tarea tuya en subagentes y el resultado se repite.",
  [u"Cuándo un subagente ayuda y cuándo estorba",
   u"Orquestar en paralelo con resultado predecible"],
  "introduction-to-subagents"),

 ("c13", 4, "1 hora", "build", False,
  u"Introduction to Agent Skills",
  u"Skills: instrucciones en markdown que se aplican solas cuando la tarea coincide. Cómo escribirlas, compartirlas y arreglarlas cuando no se disparan.",
  u"Terminas esto cuando una skill tuya se aplica sola y el equipo la usa.",
  [u"Escribir una skill que se dispare cuando corresponde",
   u"Compartirla, que es donde se nota"],
  "introduction-to-agent-skills"),

 ("c14", 5, "8 horas", "cloud", True,
  u"Claude with Amazon Bedrock",
  u"Todo lo anterior sobre AWS: la API por Bedrock, uso de herramientas, RAG, agentes y aplicaciones listas para producción.",
  u"Terminas esto cuando lo que construiste corre en la cuenta de AWS de tu trabajo.",
  [u"Claude dentro de la nube donde ya está tu empresa",
   u"RAG y agentes con los servicios de AWS",
   u"Insignia de Anthropic"],
  "claude-with-amazon-bedrock"),

 ("c15", 5, "8 h 30 min", "cloud", False,
  u"Claude with Google Cloud Vertex AI",
  u"Lo mismo sobre Google Cloud: configuración, prompting, herramientas, RAG, MCP y agentes sobre Vertex AI.",
  u"Terminas esto cuando lo tuyo corre en Vertex AI y no en tu máquina.",
  [u"La alternativa a Bedrock, por si tu empresa está en GCP",
   u"MCP y agentes sobre Vertex AI",
   u"Insignia de Anthropic"],
  "claude-with-google-cloud-s-vertex-ai"),

 ("c16", 5, "1 hora", "school", False,
  u"The AI-Native SDLC Playbook",
  u"Qué le pasa al ciclo de desarrollo cuando los agentes escriben la mayor parte del código: planificación, diseño, build, test, deploy y mantenimiento, y dónde poner el control.",
  u"Terminas esto cuando sabes qué cambia en tu equipo, no solo en tu máquina.",
  [u"Dónde aparecen los cuellos de botella nuevos",
   u"Gobernanza para trabajo agéntico, sin frenarlo"],
  "ai-native-sdlc-playbook"),
]


# Lo que es propio de la ruta y no sale de los NODES: los textos, el
# acento y los enlaces de la plantilla que hablan de la otra ruta.
# (viejo, nuevo, cuantas veces tiene que aparecer)
TEXTOS = [
 (u"<title>AI: fundamentos, gratis y en orden · DataChinchilla</title>",
  u"<title>Trabajar con Claude, gratis y en orden · DataChinchilla</title>", 1),

 (u'content="Nueve cursos gratuitos de CognitiveClass en tres credenciales: '
  u'qué es la AI, cómo se entrena un modelo y machine learning con Python."',
  u'content="Dieciséis cursos gratuitos de Anthropic con insignia: usar Claude, '
  u'construir con la API, conectar tus sistemas con MCP y llevarlo a producción."', 3),

 (u'content="AI: fundamentos, en orden"',
  u'content="Trabajar con Claude, en orden"', 2),


 # El acento: la plantilla trae el violeta de ai-fundamentos y dos
 # rutas del mismo color se leen como la misma. Va el coral de
 # Anthropic, que es de donde salen los cursos. Medido contra los
 # fondos de verdad: 4.96:1 en claro, 8.12:1 en oscuro.
 (u"""  /* AI: fundamentos */
  --accent:        #7E22CE;
  --accent-strong: #6B21A8;
  --accent-soft:   #F6EDFD;
  --accent-line:   #DFC6F4;""",
  u"""  /* Trabajar con Claude */
  --accent:        #B5451F;
  --accent-strong: #9A3A19;
  --accent-soft:   #FDF0EB;
  --accent-line:   #F3D2C2;""", 1),

 (u"""  --accent:        #C084FC;
  --accent-strong: #D8B4FE;
  --accent-soft:   #2E1065;
  --accent-line:   #4C1D95;""",
  u"""  --accent:        #E0997B;
  --accent-strong: #EDB49A;
  --accent-soft:   #3B1C10;
  --accent-line:   #5E2E1B;""", 1),

 (u'<span class="brand-sub">/ AI: fundamentos</span>',
  u'<span class="brand-sub">/ Trabajar con Claude</span>', 1),

 (u'<h1>AI: <span class="grad">fundamentos</span></h1>',
  u'<h1>Trabajar con <span class="grad">Claude</span></h1>', 1),

 (u'<p class="hero-lead">Tres credenciales de CognitiveClass, una atrás de la otra. '
  u'Cada tramo del mapa es un learning path entero: al cerrarlo te dan el badge, no queda '
  u'a mitad de camino. No hace falta saber programar para empezar, sí para el último tramo.</p>',
  u'<p class="hero-lead">De usar la herramienta a construir con ella. Empieza por qué hace '
  u'y qué no, sigue por usarla todos los días, y termina con tu propio servidor MCP '
  u'corriendo en la nube donde ya trabajas. Los dieciséis son gratis y dejan insignia.</p>', 1),

 (u'<span class="dest" id="startDest">Introducing AI</span>',
  u'<span class="dest" id="startDest">el marco de las cuatro D</span>', 1),

 (u'<a class="btn-quiet" href="https://cognitiveclass.ai/" target="_blank" rel="noopener">',
  u'<a class="btn-quiet" href="https://academy.claude.com/" target="_blank" rel="noopener">', 1),

 # El texto del boton, no solo su destino: cambiar uno y no el otro
 # deja al que lee sin saber adonde va.
 (u'<span class="dest">cognitiveclass.ai</span>',
  u'<span class="dest">academy.claude.com</span>', 1),

 (u'<p class="hero-foot">Los nueve cursos son de CognitiveClass, la plataforma abierta de IBM. '
  u'Yo no los doy: esta página los agrupa por credencial y enlaza directo. El orden dentro de '
  u'cada tramo es el que publica CognitiveClass, no uno mío.</p>',
  u'<p class="hero-foot">Los dieciséis cursos son de Anthropic y se hacen en su academia. '
  u'Yo no los doy: esta página elige cuáles de los veinticinco te sirven y en qué orden. '
  u'Quedan afuera las ocho versiones de AI Fluency para otras audiencias y el de despliegue '
  u'para equipos de IT.</p>', 1),

 (u"<h2>Tres credenciales, nueve cursos</h2>",
  u"<h2>Cinco tramos, dieciséis cursos</h2>", 1),

 (u'<p>Cada tramo es un learning path completo: al cerrarlo entero te dan el badge. '
  u'Lo que ya hayas hecho en otra ruta aparece marcado solo.</p>',
  u'<p>Toca cualquiera para ver qué te llevas y por qué está acá. '
  u'Casi todos dejan insignia de Anthropic al terminarlos.</p>', 1),

 (u"los nueve cursos de los fundamentos de AI.",
  u"los dieciséis cursos de trabajar con Claude.", 1),

 (u"Se desbloquea cuando cierres los nueve cursos del mapa.",
  u"Se desbloquea cuando cierres los dieciséis cursos del mapa.", 1),

 (u'"Los nueve cursos"', u'"Los dieciséis cursos"', 1),
]


def nodo(c):
    cid, act, time, i, boss, titulo, resumen, meta, wins, slug = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s"%s,\n'
            u'    cert: "Insignia de Anthropic",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "https://academy.claude.com/courses/%s"\n'
            u'  }' % (cid, act, time, i, u", boss: true" if boss else u"",
                      titulo, resumen, meta, w, slug))


def main():
    p = os.path.join(D, BASE)
    if not os.path.exists(p):
        print("  ABORTA: no encuentro %s" % BASE); sys.exit(1)
    t = io.open(p, encoding="utf-8").read()

    # Con lambda y no con el texto directo: re.sub lee los \ del
    # reemplazo como escapes, y un "é" o una barra en cualquier
    # resumen lo haria explotar o, peor, entrar mal.
    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    # Los textos propios. Cada uno declara cuantas veces tiene que
    # aparecer: si la plantilla cambia, esto aborta en vez de dejar
    # media pagina hablando de la otra ruta.
    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r aparece %d veces, esperaba %d"
                  % (viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d cursos en 5 tramos, %d textos propios"
          % (SALE, len(C), len(TEXTOS)))


main()
