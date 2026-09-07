# -*- coding: utf-8 -*-
u"""Las preguntas, para todo el sitio y no solo para datos.

   Las cuatro preguntas se escribieron cuando el sitio eran tres rutas
   de datos: programas, SQL, datos en un trabajo, nube. Hoy hay
   diecisiete rutas y ocho puestos, y la mitad no toca una base de
   datos en su vida. A alguien que eligio "Desarrollador Frontend" se
   le preguntaba si armo pipelines: es preguntarle por el trabajo de
   otro, y encima las respuestas no le sumaban nada al puesto que
   eligio.

   Las cinco de ahora cubren el ancho del sitio: programar, la
   pantalla, el servidor, los datos y la infraestructura. Un data
   engineer contesta las cinco igual que antes contestaba las cuatro,
   y un frontend por fin contesta algo suyo.

   Los temas que suma cada respuesta salen de temas.js, que ya tiene
   web, backend y web3 desde que entraron las rutas de desarrollo:
   las preguntas eran lo unico que se habia quedado atras.

   El texto de "cuatro preguntas" tambien cambia, en los dos lugares
   donde se decia.

   Uso: python build-preguntas-tech.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r x%d, esperaba %d"
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-18s %d cambios" % (archivo, len(cambios)))


VIEJAS = u'''  var PREGUNTAS = [
    { id: "prog", texto: "¿Programas?",
      ayuda: "En cualquier lenguaje, aunque sea para automatizar algo tuyo.",
      opciones: [
        { t: "Nunca escribí código", temas: {} },
        { t: "Algo, scripts sueltos", temas: { prog: 1, python: 1 } },
        { t: "Sí, es parte de mi trabajo", temas: { prog: 2, python: 2 } },
        { t: "Vengo del desarrollo", temas: { prog: 3, python: 2 } }
      ] },
    { id: "sql", texto: "¿Y SQL?",
      ayuda: "La pregunta real es hasta dónde llegas sin buscar en Google.",
      opciones: [
        { t: "No lo usé nunca", temas: {} },
        { t: "Consultas simples y algún JOIN", temas: { sql: 1 } },
        { t: "Subconsultas, CTEs y ventanas", temas: { sql: 3 } },
        { t: "Optimizo consultas ajenas", temas: { sql: 3, modelado: 1 } }
      ] },
    { id: "datos", texto: "¿Trabajaste con datos en un trabajo?",
      ayuda: "Cuenta cualquier cosa que alguien más haya usado para decidir.",
      opciones: [
        { t: "Todavía no", temas: {} },
        { t: "Reportes y planillas", temas: { viz: 1 } },
        { t: "Dashboards o análisis para otros", temas: { viz: 2, sql: 1 } },
        { t: "Pipelines o modelos en producción", temas: { pipelines: 2, modelado: 2 } }
      ] },
    { id: "nube", texto: "¿Nube?",
      ayuda: "AWS, Azure, Google Cloud, contenedores, lo que sea.",
      opciones: [
        { t: "Nada", temas: {} },
        { t: "Usé algún servicio suelto", temas: { cloud: 1 } },
        { t: "Despliego cosas ahí", temas: { cloud: 2 } },
        { t: "Administro la infraestructura", temas: { cloud: 3, prog: 1 } }
      ] }
  ];'''

NUEVAS = u'''  /* Las cinco preguntas.

     Eran cuatro y eran de datos -programas, SQL, datos en un trabajo,
     nube- porque se escribieron cuando el sitio eran tres rutas de
     datos. Hoy hay diecisiete rutas y ocho puestos, y a la mitad no
     le toca una base de datos: a alguien que eligio frontend se le
     preguntaba si armo pipelines, que es preguntarle por el trabajo
     de otro.

     Estas cubren el ancho del sitio: programar, la pantalla, el
     servidor, los datos y la infraestructura. Nadie contesta las
     cinco sobre lo mismo, y cada una suma temas que existen en
     temas.js desde que entraron las rutas de desarrollo. */
  var PREGUNTAS = [
    { id: "prog", texto: "¿Programas?",
      ayuda: "En cualquier lenguaje, aunque sea para automatizar algo tuyo.",
      opciones: [
        { t: "Nunca escribí código", temas: {} },
        { t: "Algo, scripts sueltos", temas: { prog: 1 } },
        { t: "Sí, es parte de mi trabajo", temas: { prog: 2 } },
        { t: "Vengo del desarrollo", temas: { prog: 3 } }
      ] },
    { id: "pantalla", texto: "¿Construiste algo que se vea en pantalla?",
      ayuda: "Una página, una app, aunque haya sido para vos.",
      opciones: [
        { t: "No, nunca", temas: {} },
        { t: "HTML y CSS, algo suelto", temas: { web: 1 } },
        { t: "Interfaces con un framework", temas: { web: 2, prog: 1 } },
        { t: "Es lo que hago", temas: { web: 3, prog: 2 } }
      ] },
    { id: "servidor", texto: "¿Y del otro lado: APIs, servidores, bases?",
      ayuda: "Lo que hay detrás de la pantalla, o detrás de un dashboard.",
      opciones: [
        { t: "No me tocó", temas: {} },
        { t: "Consumí APIs de otros", temas: { backend: 1 } },
        { t: "Escribí endpoints y consultas", temas: { backend: 2, sql: 2 } },
        { t: "Diseño el backend y su base", temas: { backend: 3, sql: 3, modelado: 2 } }
      ] },
    { id: "datos", texto: "¿Trabajaste con datos para que otro decida?",
      ayuda: "Cuenta cualquier cosa que alguien más haya usado para decidir.",
      opciones: [
        { t: "Todavía no", temas: {} },
        { t: "Reportes y planillas", temas: { viz: 1, sql: 1 } },
        { t: "Dashboards o análisis para otros", temas: { viz: 2, sql: 2 } },
        { t: "Pipelines o modelos en producción", temas: { pipelines: 2, modelado: 2, python: 2 } }
      ] },
    { id: "nube", texto: "¿Nube e infraestructura?",
      ayuda: "AWS, Azure, Google Cloud, Docker, lo que sea.",
      opciones: [
        { t: "Nada", temas: {} },
        { t: "Usé algún servicio suelto", temas: { cloud: 1 } },
        { t: "Despliego lo que hago", temas: { cloud: 2, prog: 1 } },
        { t: "Administro la infraestructura", temas: { cloud: 3, prog: 1, mlops: 1 } }
      ] }
  ];'''

parchar("onboarding.js", [(VIEJAS, NUEVAS, 1)])

# --- el texto que decia cuatro
parchar("cv.html", [
 (u'''<h2>Cuatro preguntas, de a una</h2>''',
  u'''<h2 id="pregTitulo">Cinco preguntas, de a una</h2>''', 1),
 (u'''o salta directo al paso 3 y ponlas a mano.''',
  u'''o salta directo al paso 3 y ponlas a mano.''', 1),
])

# El numero, del array y no a mano: es el mismo error de "quince
# rutas" y "treinta y tres niveles", y ya se arreglo dos veces.
parchar("cv.html", [
 (u'''  pregEn = pregPrimeraSinContestar();
  pintarPreguntas();''',
  u'''  /* El titulo dice cuantas son, contando el array. Escribirlo a
     mano es lo que dejo "quince rutas" y "treinta y tres niveles"
     colgados meses. */
  var pt = document.getElementById("pregTitulo");
  if(pt) pt.textContent = NUMERO[Onb.PREGUNTAS.length] || Onb.PREGUNTAS.length;
  if(pt) pt.textContent += " preguntas, de a una";
  pregEn = pregPrimeraSinContestar();
  pintarPreguntas();''', 1),

 (u'''/* En cuál de las preguntas estás.''',
  u'''/* Los numeros hasta diez, en palabra: el titulo los usa. */
var NUMERO = ["cero", "Una", "Dos", "Tres", "Cuatro", "Cinco", "Seis",
              "Siete", "Ocho", "Nueve", "Diez"];

/* En cuál de las preguntas estás.''', 1),
])
