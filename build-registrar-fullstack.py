# -*- coding: utf-8 -*-
"""Dar de alta fullstack.html en todos los lados que la tienen que
   conocer.

   Una ruta no existe por tener pagina: hay cinco registros separados
   -los pasos, la cabecera, el catalogo, el boton de sumarla a tu
   semana y el nivel que pide- y olvidarse de uno la deja a medias de
   una forma distinta cada vez.

   Ademas entra un nivel nuevo. Los cuatro que habia -desde cero, con
   SQL, con Python, con experiencia- son la escalera de datos, y
   pedirle SQL a alguien que va a hacer React no tiene sentido.

   Uso: python build-registrar-fullstack.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r aparece %d veces, esperaba %d"
                  % (archivo, viejo[:50], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-24s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------- 1. los pasos
parchar("build-pasos.py", [
 (u'    ("web3.html",           "web3",         u"Web3"),\n]',
  u'    ("web3.html",           "web3",         u"Web3"),\n'
  u'    ("fullstack.html",      "fullstack",    u"Full Stack Open"),\n]', 1),

 (u'    "web3.html": u"Desde cero",\n}',
  u'    "web3.html": u"Desde cero",\n'
  u'    "fullstack.html": u"Con programación sabida",\n}', 1),

 # El nivel nuevo va al mismo escalon que Python: los dos piden saber
 # programar, cada uno en su mundo. No se renumeran los otros porque
 # onboarding.js compara contra estos numeros.
 (u'    u"Con Python sabido": 2,\n',
  u'    u"Con Python sabido": 2,\n'
  u'    u"Con programación sabida": 2,\n', 1),
])

# ------------------------------------------------- 2. la cabecera
parchar("build-brand.py", [
 (u'    "web3.html": {',
  u'    "fullstack.html": {\n'
  u'        "titulo": u"Full Stack Open, gratis y en orden · " + MARCA,\n'
  u'        "desc": u"Las quince partes del curso gratuito de la Universidad de Helsinki: '
  u'React, Node, pruebas, TypeScript, contenedores y CI/CD, con certificado y sin examen.",\n'
  u'        "color": u"#08121C",\n'
  u'        "ogtitulo": u"Full Stack Open, en orden",\n'
  u'    },\n'
  u'    "web3.html": {', 1),
])

# ------------------------------------------------- 3. sumarla a la semana
parchar("build-activar.py", [
 (u'    "web3.html":           "web3",\n}',
  u'    "web3.html":           "web3",\n'
  u'    "fullstack.html":      "fullstack",\n}', 1),
])

# ------------------------------------------------- 4. el catalogo
parchar("index.html", [
 (u'  var ORDEN = ["Desde cero", "Con SQL sabido", "Con Python sabido", "Con experiencia"];',
  u'  var ORDEN = ["Desde cero", "Con SQL sabido", "Con Python sabido",\n'
  u'               "Con programación sabida", "Con experiencia"];', 1),

 (u'''  {
    t: "Airflow", nivel: "Con Python sabido", i: "flow", listo: false,''',
  u'''  {
    t: "Full Stack Open", nivel: "Con programación sabida", i: "web", u: "fullstack.html", listo: true,
    d: "Quince partes del curso gratuito de la Universidad de Helsinki: React, Node, pruebas, TypeScript, contenedores y CI/CD. Da certificado y no hay examen.",
    s: "abrir la ruta"
  },
  {
    t: "Airflow", nivel: "Con Python sabido", i: "flow", listo: false,''', 1),
])

print()
print(u"Falta correr, en este orden:")
print(u"  python build-pasos.py")
print(u"  python build-temas.py")
print(u"  python build-brand.py")
print(u"  python sellar.py")
