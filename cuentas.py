# -*- coding: utf-8 -*-
"""Cada ruta anuncia cuantos cursos tiene. Que sea verdad.

   El numero esta escrito con letras en siete lugares -tres metadatos,
   el hero, el titulo del mapa, dos lineas de la constancia y el texto
   del boton- mientras el contador de arriba cuenta NODES. Agregar un
   curso mueve el contador y no mueve el texto, y nadie se entera
   hasta que alguien lee "veintisiete pasos" arriba de veintiocho
   tarjetas.

   Paso cuatro veces: subir-nivel decia catorce con diecisiete,
   llm-agentes veintisiete con veintiocho, arquitectura seis en el
   titulo y nueve en los metadatos con diez, y el boton de
   data-science decia tres con doce.

   Este script mira SOLO los lugares donde la ruta habla de si misma.
   Fuera quedan, a proposito:

     - "Diecis\u00e9is hitos hasta la certificacion": es la descripcion de
       SnowPro en el listado de otras rutas, y SnowPro tiene dieciseis
     - "Marca los tres pasos para cerrar el hito": son los pasos de UN
       hito, no de la ruta
     - "seis pasos para crear, cambiar y destruir": son los pasos del
       tutorial de Terraform

   Mirar todo el archivo daba mas ruido que senal: diecinueve avisos,
   de los cuales trece eran correctos.

   Uso: python cuentas.py
"""
import io, json, re, sys

LETRAS = [
 (3,u"tres"),(4,u"cuatro"),(5,u"cinco"),(6,u"seis"),(7,u"siete"),(8,u"ocho"),
 (9,u"nueve"),(10,u"diez"),(11,u"once"),(12,u"doce"),(13,u"trece"),
 (14,u"catorce"),(15,u"quince"),(16,u"diecis\u00e9is"),(17,u"diecisiete"),
 (18,u"dieciocho"),(19,u"diecinueve"),(20,u"veinte"),(21,u"veintiuno"),
 (22,u"veintid\u00f3s"),(23,u"veintitr\u00e9s"),(24,u"veinticuatro"),
 (25,u"veinticinco"),(26,u"veintis\u00e9is"),(27,u"veintisiete"),
 (28,u"veintiocho"),(29,u"veintinueve"),(30,u"treinta"),(31,u"treinta y uno"),
]
PALABRA = dict(LETRAS)
NUMERO  = dict((p, n) for n, p in LETRAS)
TODAS   = "|".join(re.escape(p) for _, p in LETRAS)
SUST    = r"(?:cursos|pasos|hitos|niveles)"

# Los lugares donde la ruta habla de si misma, y solo esos.
DONDE = [
  (u"el t\u00edtulo del mapa",  r"<h2>[^<]*?\b(%s)\s+(%s)\b" % (TODAS, SUST)),
  (u"los metadatos",       r'content="[^"]*?\b(%s)\s+(%s)\b' % (TODAS, SUST)),
  (u"la constancia",       r'class="cert-(?:linea|nota)"[^>]*>(?:[^<]|<br>)*?\b(%s)\s+(%s)\b' % (TODAS, SUST)),
  (u"el pie del hero",     r'class="hero-(?:foot|lead)"[^>]*>[^<]*?\b(%s)\s+(%s)\b' % (TODAS, SUST)),
  (u"el bot\u00f3n",           r'startDest[^;]*?"[^"]*?\b(%s)\s+(%s)\b' % (TODAS, SUST)),
]

t = io.open("pasos.js", encoding="utf-8").read()
rutas = json.loads(t[t.index("["):t.rindex("]")+1])

mal = 0
for r in rutas:
    n = len(r["pasos"])
    try: h = io.open(r["archivo"], encoding="utf-8").read()
    except IOError: continue
    for nombre, pat in DONDE:
        for m in re.finditer(pat, h, re.I):
            dice = NUMERO.get(m.group(1).lower())
            if dice is None or dice == n: continue
            mal += 1
            print(u"  %-20s %-16s dice %s, tiene %d (%s)" %
                  (r["archivo"], nombre, m.group(1), n, PALABRA.get(n, n)))

# --- y el catalogo de la portada, que anuncia el tamano de cada ruta
#
# La descripcion de cada tarjeta suele abrir con la cantidad
# ("Veintitres pasos gratuitos en orden..."). Se compara contra la
# misma cuenta de pasos.js. Las que no abren con un numero se saltean:
# hay varias que describen sin contar, y esta bien.
idx = io.open("index.html", encoding="utf-8").read()
b = idx[idx.index("var PATHS"):]
b = b[:b.index("\n];")]
por_archivo = dict((r["archivo"], len(r["pasos"])) for r in rutas)

for ent in b.split("\n  {")[1:]:
    mu = re.search(r'u:\s*"([^"]+)"', ent)
    md = re.search(r'd:\s*"([^"]+)"', ent)
    if not mu or not md:
        continue
    n = por_archivo.get(mu.group(1))
    if n is None:
        continue
    mn = re.match(r"(%s)\s+(%s)\b" % (TODAS, SUST), md.group(1), re.I)
    if not mn:
        continue
    dice = NUMERO.get(mn.group(1).lower())
    if dice is None or dice == n:
        continue
    mal += 1
    print(u"  %-20s %-16s dice %s, tiene %d (%s)" %
          ("index.html", u"el catálogo", mn.group(1), n, PALABRA.get(n, n)))

# --- y que cada ruta active la suya
#
# El boton "sumar a tu semana" decide con var MI_RUTA. Las paginas se
# arman copiando otra, asi que esa variable se hereda: el boton de
# Full Stack Open activaba la ruta de Claude, y eso no se ve mirando
# la pagina. Dos rutas con la misma clave, o una clave que no existe,
# tienen que doler aca.
vistas = {}
for r in rutas:
    try:
        h = io.open(r["archivo"], encoding="utf-8").read()
    except IOError:
        continue
    m = re.search(r'var MI_RUTA = "([^"]*)"', h)
    if not m:
        continue
    k = m.group(1)
    if k != r["clave"]:
        mal += 1
        print(u"  %-20s %-16s activa %s, tendria que activar %s" %
              (r["archivo"], u"la clave", k, r["clave"]))
    if k in vistas:
        mal += 1
        print(u"  %-20s %-16s comparte la clave %s con %s" %
              (r["archivo"], u"la clave", k, vistas[k]))
    vistas[k] = r["archivo"]

# --- y que los dos mapas de ids viejos digan lo mismo
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
        out[a.strip().strip('"\'')] = b.strip().strip('"\'')
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
print(u"los numeros coinciden" if not mal else
      u"%d desajustes: el texto dice una cantidad y el mapa tiene otra" % mal)
sys.exit(1 if mal else 0)
