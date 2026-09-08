# -*- coding: utf-8 -*-
u"""Los textos de CS50, ahora que son semanas y no once cursos.

   cuentas.py encontro las siete: el titulo, dos metadatos, el hero,
   el titulo del mapa, la constancia y el boton. Todos decian "los
   once cursos".

   La redaccion no es "treinta y siete cursos", que seria cambiar una
   mentira por otra: son ocho cursos enteros mas veintinueve semanas
   de los tres que se recorren completos. Eso es lo que dice ahora.

   Y se extiende la tabla de numeros de cuentas.py, que llegaba hasta
   treinta y uno. Sin eso, un texto que diga "treinta y siete pasos"
   no lo comprueba nadie: la palabra no esta en la tabla, la
   comprobacion no la reconoce y pasa de largo. Una ruta que crece mas
   alla de su comprobacion se queda sin comprobacion, y en silencio.

   Uso: python build-cs50-textos.py
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
                  % (archivo, viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------- 1. la tabla de numeros
parchar("cuentas.py", [
 (u''' (28,u"veintiocho"),(29,u"veintinueve"),(30,u"treinta"),(31,u"treinta y uno"),
]''',
  u''' (28,u"veintiocho"),(29,u"veintinueve"),(30,u"treinta"),(31,u"treinta y uno"),
 # Hasta cuarenta y cinco. Llegaba a treinta y uno, y CS50 paso a
 # treinta y siete al partirse en semanas: un texto que dijera
 # "treinta y siete pasos" no lo reconocia la tabla, no lo comprobaba
 # nadie y pasaba de largo. Una ruta que crece mas alla de su
 # comprobacion se queda sin comprobacion, y en silencio.
 (32,u"treinta y dos"),(33,u"treinta y tres"),(34,u"treinta y cuatro"),
 (35,u"treinta y cinco"),(36,u"treinta y seis"),(37,u"treinta y siete"),
 (38,u"treinta y ocho"),(39,u"treinta y nueve"),(40,u"cuarenta"),
 (41,u"cuarenta y uno"),(42,u"cuarenta y dos"),(43,u"cuarenta y tres"),
 (44,u"cuarenta y cuatro"),(45,u"cuarenta y cinco"),
]''', 1),
])

# ------------------------------------------------- 2. los siete textos
parchar("cs50.html", [
 (u"<title>Los once cursos de CS50, ordenados · DataChinchilla</title>",
  u"<title>CS50 de Harvard, semana por semana · DataChinchilla</title>", 1),

 (u'<meta property="og:title" content="Los once cursos abiertos de CS50, en orden">',
  u'<meta property="og:title" content="CS50 de Harvard, semana por semana">', 1),

 (u'<meta name="twitter:title" content="Los once cursos abiertos de CS50, en orden">',
  u'<meta name="twitter:title" content="CS50 de Harvard, semana por semana">', 1),

 (u'<h1>Los once cursos abiertos de <span class="grad">CS50</span></h1>',
  u'<h1>CS50 de Harvard, <span class="grad">semana por semana</span></h1>', 1),

 (u". Este mapa los pone en orden y dice qué esperar de cada uno, porque once cursos sin criterio abruman más de lo que ayudan.</p>",
  u". Los tres que se hacen enteros -CS50x, Python y bases de datos- van semana por semana, con la estructura que publica Harvard: así cada semana se marca sola y entra en un bloque de tu agenda, en vez de ser un curso de sesenta horas que no se puede repartir. Los otros ocho van completos, porque se eligen y no se recorren.</p>", 1),

 (u"<h2>Cuatro tramos, once cursos</h2>",
  u"<h2>Cuatro tramos, treinta y siete pasos</h2>", 1),

 (u"<p class=\"cert-nota\">Se desbloquea cuando cierres los once cursos del mapa.</p>",
  u"<p class=\"cert-nota\">Se desbloquea cuando cierres los treinta y siete pasos del mapa: "
  u"las veintinueve semanas de CS50x, Python y bases de datos, más los otros ocho, que van enteros.</p>", 1),

 (u'document.getElementById("startDest").textContent = "Los once cursos";',
  u'/* Contado, no escrito: aca decia "once" y la ruta paso a treinta\n'
  u'       y siete al partirse en semanas. */\n'
  u'    document.getElementById("startDest").textContent =\n'
  u'      "Los " + NODES.length + " pasos";', 1),
])
