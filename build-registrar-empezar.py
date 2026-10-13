# -*- coding: utf-8 -*-
u"""Dar de alta empezar.html donde tiene que estar.

   Una ruta no existe por tener pagina. Son cinco registros separados
   -los pasos, la cabecera, el catalogo, el boton de sumarla a tu
   semana y los temas que ensena- y olvidarse de uno la deja a medias
   de una forma distinta cada vez.

   Y entra un puesto que no es un puesto: "Todavia no se". Es el que
   le faltaba al sitio y se nota en como esta armado todo lo demas: el
   flujo del CV arranca preguntando a que puesto apuntas, y para mucha
   gente -la que mas ayuda necesita- esa es justamente la pregunta.
   Sin una opcion que diga "no se", esa persona elige cualquiera y el
   sitio le contesta cualquier cosa.

   Los temas que pide son los fundamentos que sirven para todos los
   caminos: programar y Python en 3, SQL, web y nube mas abajo. No
   pide nada especializado a proposito: pedir ml o pipelines seria
   empujarlo hacia un lado antes de que elija.

   Nivel del catalogo: desde cero. Es la unica ruta del sitio que
   empieza sin saber nada y termina sin un puesto: termina en poder
   elegirlo.

   Uso: python build-registrar-empezar.py
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
                  % (archivo, viejo[:50], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-24s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------- 1. los pasos
parchar("build-pasos.py", [
 (u'    ("airflow.html",        "airflow",      u"Airflow"),\n',
  u'    ("airflow.html",        "airflow",      u"Airflow"),\n'
  u'    ("empezar.html",        "empezar",      u"No s\\u00e9 qu\\u00e9 seguir"),\n', 1),

 (u'    "airflow.html": u"Con Python sabido",\n',
  u'    "airflow.html": u"Con Python sabido",\n'
  u'    "empezar.html": u"Desde cero",\n', 1),
])

# ------------------------------------------------- 2. la cabecera
parchar("build-brand.py", [
 (u'    "airflow.html": {',
  u'    "empezar.html": {\n'
  u'        "titulo": u"No s\\u00e9 qu\\u00e9 seguir: el camino de cero \\u00b7 " + MARCA,\n'
  u'        "desc": u"Si no sab\\u00e9s qu\\u00e9 camino seguir en tech, \\u00e9ste es el camino: '
  u'CS50x, Python, SQL y Full Stack Open en orden, m\\u00e1s nube, y despu\\u00e9s cuatro proyectos '
  u'chicos para elegir con informaci\\u00f3n propia.",\n'
  u'        "color": u"#0B1020",\n'
  u'        "ogtitulo": u"No s\\u00e9 qu\\u00e9 seguir: el camino de cero",\n'
  u'    },\n'
  u'    "airflow.html": {', 1),
])

# ------------------------------------------------- 3. sumarla a la semana
parchar("build-activar.py", [
 (u'    "airflow.html":        "airflow",\n',
  u'    "airflow.html":        "airflow",\n'
  u'    "empezar.html":        "empezar",\n', 1),
])

# ------------------------------------------------- 4. los temas y el puesto
parchar("build-temas.py", [
 (u' ("fullstack", 1):    ["web", "prog"],',
  u' # El camino de cero. Cada tramo ensena lo que ensena, sin inflar:\n'
  u' # el primero son fundamentos, el segundo construir algo entero y\n'
  u' # publicarlo, y el tercero no ensena un tema nuevo -es probar y\n'
  u' # elegir- asi que suma programacion y nada mas.\n'
  u' ("empezar", 1):      ["prog", "python", "sql"],\n'
  u' ("empezar", 2):      ["web", "backend", "cloud"],\n'
  u' ("empezar", 3):      ["prog"],\n\n'
  u' ("fullstack", 1):    ["web", "prog"],', 1),

 (u' {"id": "data_engineer", "nombre": u"Data Engineer",',
  u' # El puesto que no es un puesto, y el que le faltaba al sitio.\n'
  u' #\n'
  u' # El flujo del CV arranca preguntando a que apuntas, y para mucha\n'
  u' # gente esa es justamente la pregunta. Sin una opcion que diga "no\n'
  u' # se", esa persona elige cualquiera y el sitio le contesta\n'
  u' # cualquier cosa.\n'
  u' #\n'
  u' # Pide los fundamentos que sirven para todos los caminos y nada\n'
  u' # especializado: pedir ml o pipelines seria empujarlo hacia un lado\n'
  u' # antes de que elija.\n'
  u' {"id": "no_se", "nombre": u"Todav\\u00eda no s\\u00e9",\n'
  u'  "resumen": u"Quer\\u00e9s entrar a tech y todav\\u00eda no sab\\u00e9s a qu\\u00e9. Primero los '
  u'fundamentos, y el camino se elige despu\\u00e9s con informaci\\u00f3n tuya.",\n'
  u'  "distingue": u"Es el \\u00fanico que no termina en un puesto: termina en poder elegirlo.",\n'
  u'  "temas": {"prog": 3, "python": 3, "sql": 2, "web": 2, "cloud": 2,\n'
  u'            "backend": 1}},\n\n'
  u' {"id": "data_engineer", "nombre": u"Data Engineer",', 1),
])

# ------------------------------------------------- 5. el catalogo
parchar("index.html", [
 (u'''  {
    t: "Airflow", nivel: "Con Python sabido", i: "flow", u: "airflow.html", listo: true,''',
  u'''  {
    t: "No sé qué seguir", nivel: "Desde cero", i: "boss", u: "empezar.html", listo: true,
    d: "Si no sabés qué camino seguir, éste es el camino. Un año de fundamentos en orden -CS50x, Python, SQL, Full Stack Open y nube- y después cuatro proyectos chicos para elegir con información tuya. Es la única que no termina en un puesto: termina en poder elegirlo.",
    s: "abrir la ruta"
  },
  {
    t: "Airflow", nivel: "Con Python sabido", i: "flow", u: "airflow.html", listo: true,''', 1),
])

print()
print(u"Falta correr, en este orden:")
print(u"  python build-pasos.py")
print(u"  python build-temas.py")
print(u"  python build-brand.py")
print(u"  python build-activar.py")
print(u"  python build-catalog.py")
print(u"  python build-etiquetas.py")
print(u"  python build-respaldos.py")
print(u"  python sellar.py")
