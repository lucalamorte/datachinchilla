# -*- coding: utf-8 -*-
u"""Que los dos mapas de ids viejos no se separen.

   El mapa de ids de ruta que cambiaron lo emite build-catalog.py en
   catalog.js, y lo usa el armador. La portada no carga catalog.js -78
   kB por una entrada- asi que ahi va escrito, y dos copias de una
   regla se separan solas. Que duela aca.

   Uso: python build-cuentas-alias.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cuentas.py")

ANCLA = u'''print()
print(u"los numeros coinciden" if not mal else'''

NUEVO = u'''# --- y que los dos mapas de ids viejos digan lo mismo
#
# Cuando una ruta cambia de id, una ruta armada a mano guarda los ids
# viejos: sin traducirlos, sus piezas se descartan en silencio. El
# mapa lo emite build-catalog.py en catalog.js, pero la portada no
# carga catalog.js, asi que ahi hay una copia escrita. Dos copias de
# una regla se separan solas.
def _alias(texto, marca):
    i = texto.find(marca)
    if i < 0:
        return None
    j = texto.index("{", i)
    k = texto.index("}", j)
    out = {}
    for par in texto[j + 1:k].split(","):
        if ":" not in par:
            continue
        a, b = par.split(":", 1)
        out[a.strip().strip('"\\'')] = b.strip().strip('"\\'')
    return out

try:
    _a = _alias(io.open("catalog.js", encoding="utf-8").read(), "var CATALOGO_ALIAS")
    _b = _alias(io.open("index.html", encoding="utf-8").read(), "var ALIAS_RUTA")
except IOError:
    _a = _b = None

if _a is None or _b is None:
    mal += 1
    print(u"  %-20s %-16s no encuentro uno de los dos mapas de ids viejos" %
          ("catalog.js", u"los alias"))
elif _a != _b:
    mal += 1
    print(u"  %-20s %-16s catalog.js dice %s, index.html dice %s" %
          ("index.html", u"los alias", _a, _b))

print()
print(u"los numeros coinciden" if not mal else'''

t = io.open(P, encoding="utf-8").read()
if "CATALOGO_ALIAS" in t:
    print(u"  ya estaba"); sys.exit(1)
if t.count(ANCLA) != 1:
    print(u"  ABORTA: el ancla aparece %d veces" % t.count(ANCLA)); sys.exit(1)
t = t.replace(ANCLA, NUEVO, 1)
io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cuentas.py: comprueba los dos mapas de ids viejos")
