# -*- coding: utf-8 -*-
"""Full Stack Open, de la Universidad de Helsinki.

   El sitio dice "el camino completo para trabajar en tech" y en los
   hechos solo servia a perfiles de datos. Quien entra siendo o
   queriendo ser desarrollador web cargaba su CV y recibia dbt y
   Snowflake. Esta es la primera ruta que no es de datos.

   Full Stack Open es la eleccion obvia para empezar: es gratis, la
   dicta una universidad publica, da certificado sin examen y sin
   inscripcion, y cubre el oficio entero -React, Node, pruebas,
   TypeScript, contenedores, CI/CD y base de datos- en una sola
   fuente con un orden pensado.

   Las quince partes, los creditos y las horas salen de la propia
   pagina del curso, no de mi cabeza:
     https://fullstackopen.com/en/part0/general_info
   Helsinki estima una parte por semana, 15 a 20 horas cada una. Se
   usa 17, el punto medio, y la pagina dice que es su estimacion y no
   una medicion mia.

   Las partes 0 a 5 son el curso base: cinco creditos y el
   certificado. Las demas son extensiones, y por eso el mapa las
   separa en tramos distintos.

   Se arma copiando claude.html, que tiene la misma estructura de
   cinco tramos.

   Uso: python build-fullstack.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "claude.html"
SALE = "fullstack.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "La base de la web", desc: "Cómo funciona una app web, y React de cero" },
  { n: 2, title: "El servidor y las pruebas", desc: "Node, Express, usuarios y tests: acá termina el curso base" },
  { n: 3, title: "La aplicación completa", desc: "Estado que escala y tus propias herramientas" },
  { n: 4, title: "Lo que pide el mercado", desc: "GraphQL, TypeScript y móvil" },
  { n: 5, title: "Llevarlo a producción", desc: "CI/CD, contenedores, base de datos y Next.js" }
];'''

# (id, acto, tiempo, icono, jefe, cert, titulo, resumen, objetivo, wins, parte)
C = [
 ("f00", 1, "17 horas", "web", False, "",
  u"Parte 0 &middot; Cómo funciona una app web",
  u"Qué pasa de verdad entre que escribes una dirección y ves algo: pedidos, respuestas, y por qué las páginas dejaron de recargarse enteras.",
  u"Terminas esta parte cuando puedes dibujar, sin ayuda, todo lo que ocurre al apretar un botón en una página.",
  [u"El ida y vuelta entre el navegador y el servidor, mirado con las herramientas del navegador",
   u"Por qué existen las aplicaciones de una sola página y qué problema vinieron a resolver",
   u"El vocabulario que el resto del curso da por sabido"], "part0"),

 ("f01", 1, "17 horas", "code", False, "",
  u"Parte 1 &middot; Introducción a React",
  u"Componentes, propiedades y estado: las tres ideas sobre las que se apoya todo lo demás.",
  u"Terminas esta parte cuando armas una interfaz que reacciona a lo que hace quien la usa, sin tocar el DOM a mano.",
  [u"Componentes que reciben datos y devuelven interfaz",
   u"Estado: qué cambia, cuándo, y por qué la pantalla se redibuja sola",
   u"Manejar eventos sin ensuciar el componente"], "part1"),

 ("f02", 1, "17 horas", "flow", True, "",
  u"Parte 2 &middot; Hablar con el servidor",
  u"Listas, formularios y el primer contacto con una API de verdad: traer datos, mandarlos y contar lo que salió mal.",
  u"Terminas esta parte cuando tu aplicación lee y escribe contra un servidor y avisa bien cuando algo falla.",
  [u"Renderizar colecciones sin que React se queje de las claves",
   u"Formularios controlados, que es como React quiere que se haga",
   u"Pedidos al servidor y qué hacer con el error, que es la mitad del trabajo"], "part2"),

 ("f03", 2, "17 horas", "build", False, "",
  u"Parte 3 &middot; Un servidor con Node y Express",
  u"Del otro lado del cable: tu propio servidor, con rutas, validación y una base de datos, puesto a andar en internet.",
  u"Terminas esta parte cuando tu backend está desplegado y tu frontend le habla a él y no a un simulador.",
  [u"Express de cero: rutas, middleware y el manejo de errores",
   u"Guardar de verdad, con validación antes de escribir",
   u"Desplegarlo, que es donde aparecen los problemas que en tu máquina no existían"], "part3"),

 ("f04", 2, "17 horas", "user", False, "",
  u"Parte 4 &middot; Probar el servidor y manejar usuarios",
  u"Pruebas del backend, y después lo que todo producto termina necesitando: cuentas, contraseñas y quién puede hacer qué.",
  u"Terminas esta parte cuando tienes pruebas que corren solas y un inicio de sesión que no guarda contraseñas en claro.",
  [u"Pruebas de integración contra una base de prueba",
   u"Usuarios y contraseñas guardadas como corresponde",
   u"Autenticación con tokens, y por qué no alcanza con confiar en el frontend"], "part4"),

 ("f05", 2, "17 horas", "check", True,
  u"Certificado de la Universidad de Helsinki",
  u"Parte 5 &middot; Probar el frontend y varias pantallas",
  u"Pruebas de la interfaz y navegación entre pantallas. Con esta parte cierras el curso base: cinco créditos y el certificado.",
  u"Terminas esta parte cuando tu aplicación tiene varias pantallas, pruebas que las cubren, y puedes bajar el certificado.",
  [u"Probar componentes como los usa una persona, no como los escribiste",
   u"Varias pantallas con React Router, sin recargar nada",
   u"El certificado de Helsinki: se baja al llegar, sin examen ni inscripción"], "part5"),

 ("f06", 3, "17 horas", "brain", False, "",
  u"Parte 6 &middot; Estado que aguanta una app grande",
  u"Cuando pasar datos de componente en componente deja de alcanzar: manejo de estado global y datos que vienen del servidor.",
  u"Terminas esta parte cuando el estado de tu aplicación vive en un lugar y no repartido en diez componentes.",
  [u"Estado global, y cuándo de verdad hace falta",
   u"Separar los datos del servidor del estado de la interfaz",
   u"Reducers: cambios de estado que se pueden leer y probar"], "part6"),

 ("f07", 3, "17 horas", "code", True, "",
  u"Parte 7 &middot; Tus propias herramientas",
  u"Hooks propios para no repetirte, y cómo se empaqueta todo esto para que llegue al navegador.",
  u"Terminas esta parte cuando sacas lógica repetida a un hook tuyo y entiendes qué hace el empaquetador.",
  [u"Hooks propios: la forma de reusar lógica en React",
   u"Qué hace un empaquetador y por qué tu código no llega tal cual lo escribiste",
   u"Estilos, que hasta acá el curso había dejado de lado a propósito"], "part7"),

 ("f08", 4, "17 horas", "flow", False, "",
  u"Parte 8 &middot; GraphQL",
  u"La otra forma de pedirle datos a un servidor: el cliente dice exactamente qué quiere, en un solo pedido.",
  u"Terminas esta parte cuando tienes un servidor GraphQL propio y un frontend que le consulta.",
  [u"Consultas y mutaciones, y en qué se diferencian de REST",
   u"Un servidor GraphQL con Apollo",
   u"Cuándo GraphQL ayuda de verdad y cuándo es complejidad de más"], "part8"),

 ("f09", 4, "17 horas", "shield", False, "",
  u"Parte 9 &middot; TypeScript",
  u"Tipos sobre JavaScript. Es lo que más aparece en las búsquedas de trabajo de los últimos años.",
  u"Terminas esta parte cuando escribes frontend y backend tipados y el editor te avisa del error antes de correr nada.",
  [u"Los tipos que hacen falta de verdad, sin pelear con el compilador",
   u"Tipar un backend de Express y un frontend de React",
   u"Por qué el error atajado al escribir sale mucho más barato"], "part9"),

 ("f10", 4, "17 horas", "web", True, "",
  u"Parte 10 &middot; React Native",
  u"Lo que ya sabes de React, aplicado a una app de teléfono de verdad.",
  u"Terminas esta parte cuando corres tu aplicación en un teléfono y entiendes qué se comparte y qué no con la web.",
  [u"React Native con Expo, sin pelear con la instalación",
   u"Qué cambia respecto de la web: navegación, estilos y formularios",
   u"Una app móvil que consume tu propia API"], "part10"),

 ("f11", 5, "17 horas", "build", False, "",
  u"Parte 11 &middot; Integración y despliegue continuos",
  u"Que cada cambio se pruebe y se publique solo. Es la parte que separa un proyecto personal de un trabajo en equipo.",
  u"Terminas esta parte cuando un cambio tuyo pasa las pruebas y llega a producción sin que toques nada a mano.",
  [u"Un flujo que prueba, construye y despliega en cada cambio",
   u"Por qué romper producción se vuelve difícil cuando esto está bien puesto",
   u"Versionado y control de calidad automático"], "part11"),

 ("f12", 5, "17 horas", "cloud", False, "",
  u"Parte 12 &middot; Contenedores",
  u"Empaquetar tu aplicación con todo lo que necesita, para que corra igual en tu máquina y en el servidor.",
  u"Terminas esta parte cuando levantas tu aplicación entera, con su base, con un solo comando.",
  [u"Imágenes y contenedores, sin mitología",
   u"Varios servicios levantados juntos y hablándose",
   u"Contenedores para desarrollar, que es el uso que más se subestima"], "part12"),

 ("f13", 5, "17 horas", "sql", False, "",
  u"Parte 13 &middot; Bases de datos relacionales",
  u"El curso base usa una base de documentos. Acá vas a la relacional, que es la que vas a encontrar en la mayoría de los trabajos.",
  u"Terminas esta parte cuando tu backend habla con Postgres y las migraciones están versionadas.",
  [u"Postgres desde Node, con y sin capa intermedia",
   u"Relaciones entre tablas y consultas que las cruzan",
   u"Migraciones: cambiar el esquema sin romper lo que ya hay"], "part13"),

 ("f14", 5, "17 horas", "build", True, "",
  u"Parte 14 &middot; Next.js",
  u"El marco de trabajo sobre React que hoy usan muchas empresas: renderizado en el servidor y rutas por archivos.",
  u"Terminas esta parte cuando entiendes qué resuelve Next.js que React solo no resuelve, y lo usas.",
  [u"Renderizado en el servidor y por qué volvió a importar",
   u"Rutas por estructura de archivos",
   u"Cuándo conviene un marco encima de React y cuándo estorba"], "part14"),
]

TEXTOS = [
 (u"<title>Trabajar con Claude, gratis y en orden · DataChinchilla</title>",
  u"<title>Full Stack Open, gratis y en orden · DataChinchilla</title>", 1),

 (u'content="Dieciséis cursos gratuitos de Anthropic con insignia: usar Claude, '
  u'construir con la API, conectar tus sistemas con MCP y llevarlo a producción."',
  u'content="Las quince partes del curso gratuito de la Universidad de Helsinki: React, '
  u'Node, pruebas, TypeScript, contenedores y CI/CD, con certificado y sin examen."', 3),

 (u'content="Trabajar con Claude, en orden"',
  u'content="Full Stack Open, en orden"', 2),

 # El acento: azul, medido contra los fondos de verdad y no contra
 # blanco. Claro 5.76:1 sobre --bg-2, que es el fondo mas claro que lo
 # toca; oscuro 7.90:1 sobre --surface.
 (u"""  /* Trabajar con Claude */
  --accent:        #B5451F;
  --accent-strong: #9A3A19;
  --accent-soft:   #FDF0EB;
  --accent-line:   #F3D2C2;""",
  u"""  /* Full Stack Open */
  --accent:        #1D5C99;
  --accent-strong: #17497A;
  --accent-soft:   #E8F1F9;
  --accent-line:   #C3DAEE;""", 1),

 (u"""  --accent:        #E0997B;
  --accent-strong: #EDB49A;
  --accent-soft:   #3B1C10;
  --accent-line:   #5E2E1B;""",
  u"""  --accent:        #7FB4E8;
  --accent-strong: #A3CBF0;
  --accent-soft:   #10263B;
  --accent-line:   #1D4A73;""", 1),

 (u'<span class="brand-sub">/ Trabajar con Claude</span>',
  u'<span class="brand-sub">/ Full Stack Open</span>', 1),

 (u'<h1>Trabajar con <span class="grad">Claude</span></h1>',
  u'<h1>Full Stack <span class="grad">Open</span></h1>', 1),

 (u'<p class="hero-lead">De usar la herramienta a construir con ella. Empieza por qué hace '
  u'y qué no, sigue por usarla todos los días, y termina con tu propio servidor MCP '
  u'corriendo en la nube donde ya trabajas. Los dieciséis son gratis y dejan insignia.</p>',
  u'<p class="hero-lead">El curso de la Universidad de Helsinki, entero y en orden. '
  u'Las partes 0 a 5 son el curso base: al cerrarlas bajas el certificado, sin examen y sin '
  u'inscribirte. Las otras nueve son las extensiones, y son las que te ponen a la par de lo '
  u'que piden los avisos: TypeScript, contenedores, CI/CD y Next.js. Helsinki calcula una '
  u'parte por semana, entre quince y veinte horas cada una; acá figuran diecisiete, que es '
  u'su punto medio y no una medición mía.</p>', 1),

 (u'<span class="dest" id="startDest">el marco de las cuatro D</span>',
  u'<span class="dest" id="startDest">cómo funciona una app web</span>', 1),

 (u'<a class="btn-quiet" href="https://academy.claude.com/" target="_blank" rel="noopener">',
  u'<a class="btn-quiet" href="https://fullstackopen.com/en/" target="_blank" rel="noopener">', 1),

 (u'<span class="dest">academy.claude.com</span>',
  u'<span class="dest">fullstackopen.com</span>', 1),

 (u'class="cert-linea">completó esta ruta:<br>los dieciséis cursos de trabajar con Claude.',
  u'class="cert-linea">completó esta ruta:<br>las quince partes de Full Stack Open.', 1),

 (u'class="cert-nota">Se desbloquea cuando cierres los dieciséis cursos del mapa.',
  u'class="cert-nota">Se desbloquea cuando cierres las quince partes del mapa. El certificado '
  u'de verdad, el de Helsinki, lo bajas de su sitio al cerrar la parte 5.', 1),
]


def nodo(c):
    cid, act, time, i, boss, cert, titulo, resumen, meta, wins, parte = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s"%s,\n'
            u'    cert: "%s",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "https://fullstackopen.com/en/%s"\n'
            u'  }' % (cid, act, time, i, u", boss: true" if boss else u"",
                      cert, titulo, resumen, meta, w, parte))


def main():
    p = os.path.join(D, BASE)
    if not os.path.exists(p):
        print("  ABORTA: no encuentro %s" % BASE)
        sys.exit(1)
    t = io.open(p, encoding="utf-8").read()

    # Con lambda: re.sub lee los backslash del reemplazo como escapes.
    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r aparece %d veces, esperaba %d"
                  % (viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d partes en 5 tramos, %d textos propios"
          % (SALE, len(C), len(TEXTOS)))


main()
