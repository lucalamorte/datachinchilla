# -*- coding: utf-8 -*-
"""Muestra los nodos de una ruta tal como estan escritos en el HTML.

   Existe porque los NODES son la fuente de verdad del contenido y
   conviene mirarlos enteros antes de tocarlos, con sus urls y sus
   campos, no solo el titulo que sale en pasos.js.

   Uso: python ver_nodos.py subir-nivel.html [id1 id2 ...]
"""
import io, re, sys

D = u"C:/Users/Luca/Desktop/snowflake path/"

f = sys.argv[1] if len(sys.argv) > 1 else u"subir-nivel.html"
quiero = set(sys.argv[2:])

t = io.open(D + f, encoding="utf-8").read()
m = re.search(r"var NODES = \[(.*?)\n\];", t, re.S)
if not m:
    print("  sin NODES en %s" % f)
    sys.exit(1)

for bloque in re.split(r"\n(?=  \{\n)", m.group(1)):
    i = re.search(r'id:\s*"([^"]+)"', bloque)
    if not i:
        continue
    if quiero and i.group(1) not in quiero:
        continue
    print(bloque.rstrip().rstrip(","))
    print("-" * 68)
