# -*- coding: utf-8 -*-
u"""Dar de alta testing.html donde tiene que estar.

   Una ruta no existe por tener pagina. Hay cinco registros separados
   -los pasos, la cabecera, el catalogo, el boton de sumarla a tu
   semana y los temas que ensena- y olvidarse de uno la deja a medias
   de una forma distinta cada vez.

   Ademas entra un puesto: QA / Tester. Una ruta sin puesto que la
   pida no la puede recomendar el CV, y el sitio se apoya en eso.

   El puesto pide calidad en 3 -es lo suyo- y programacion, web,
   backend y nube mas abajo, porque un tester que no sabe leer el
   codigo que prueba se queda en apretar botones. No pide SQL alto: se
   consulta una base para verificar datos, no se modela.

   Nivel del catalogo: desde cero. El primer tramo -el silabo y el
   articulo de la piramide- no pide escribir una linea, y los que si
   piden codigo arrancan desde su propia documentacion de entrada. Es
   la ruta de cambio de carrera mas realista que tiene el sitio.

   Uso: python build-registrar-testing.py
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
 (u'    ("airflow.html",        "airflow",      u"Airflow"),\n]',
  u'    ("airflow.html",        "airflow",      u"Airflow"),\n'
  u'    ("testing.html",        "testing",      u"Testing y QA"),\n]', 1),

 (u'    "airflow.html": u"Con Python sabido",\n}',
  u'    "airflow.html": u"Con Python sabido",\n'
  u'    "testing.html": u"Desde cero",\n}', 1),
])

# ------------------------------------------------- 2. la cabecera
parchar("build-brand.py", [
 (u'    "airflow.html": {',
  u'    "testing.html": {\n'
  u'        "titulo": u"Testing y QA gratis, en orden \\u00b7 " + MARCA,\n'
  u'        "desc": u"Probar software sin pagar nada: el s\\u00edlabo de ISTQB y la '
  u'documentaci\\u00f3n oficial de Playwright, Cypress, pytest y k6, en el orden que conviene.",\n'
  u'        "color": u"#08121C",\n'
  u'        "ogtitulo": u"Testing y QA, en orden",\n'
  u'    },\n'
  u'    "airflow.html": {', 1),
])

# ------------------------------------------------- 3. sumarla a la semana
parchar("build-activar.py", [
 (u'    "airflow.html":        "airflow",\n}',
  u'    "airflow.html":        "airflow",\n'
  u'    "testing.html":        "testing",\n}', 1),
])

# ------------------------------------------------- 4. los temas que ensena
parchar("build-temas.py", [
 (u' ("fullstack", 1):    ["web", "prog"],',
  u' # Testing: cada tramo suma calidad, que es lo suyo, y ademas el\n'
  u' # mundo sobre el que se prueba en ese tramo.\n'
  u' ("testing", 1):      ["calidad"],\n'
  u' ("testing", 2):      ["calidad", "prog"],\n'
  u' ("testing", 3):      ["calidad", "web", "backend"],\n'
  u' ("testing", 4):      ["calidad", "cloud"],\n\n'
  u' ("fullstack", 1):    ["web", "prog"],', 1),

 (u' {"id": "data_engineer", "nombre": u"Data Engineer",',
  u' # Un puesto sin ruta no se puede recomendar, y una ruta sin puesto\n'
  u' # no la encuentra nadie desde el CV.\n'
  u' {"id": "tester", "nombre": u"QA / Tester",\n'
  u'  "resumen": u"Encontrar lo que se rompe antes que el usuario, y dejarlo comprobado solo.",\n'
  u'  "temas": {"calidad": 3, "prog": 2, "web": 2, "backend": 2, "cloud": 1,\n'
  u'            "sql": 1}},\n\n'
  u' {"id": "data_engineer", "nombre": u"Data Engineer",', 1),
])

# ------------------------------------------------- 5. el catalogo
parchar("index.html", [
 (u'''  {
    t: "Airflow", nivel: "Con Python sabido", i: "flow", u: "airflow.html", listo: true,''',
  u'''  {
    t: "Testing y QA", nivel: "Desde cero", i: "check", u: "testing.html", listo: true,
    d: "Trece pasos para probar software: el sílabo de ISTQB, la pirámide de pruebas, pytest, Playwright, Cypress, APIs, carga y accesibilidad. Todo documentación oficial y abierta.",
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
print(u"  python sellar.py")
