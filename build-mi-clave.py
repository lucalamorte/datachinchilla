# -*- coding: utf-8 -*-
u"""Tres rutas creian ser AI: fundamentos.

   MI_CLAVE decide si el pie de "segui por aca" se muestra: aparece
   cuando esa ruta es una de las tuyas. Airflow, Trabajar con Claude y
   Full Stack Open tenian MI_CLAVE = "aifund", heredado de copiar
   ai-fundamentos.html para armarlas.

   O sea que en esas tres paginas el pie salia cuando tu ruta activa
   era AI: fundamentos, y nunca cuando era la que estabas mirando.
   Justo al reves.

   Es el mismo error que ya nos paso con MI_RUTA -el boton de sumar a
   la semana de Full Stack Open activaba la ruta de Claude- y por eso
   hay una comprobacion en cuentas.py. La comprobacion miraba MI_RUTA
   y no MI_CLAVE, asi que la mitad del problema seguia pasando.

   Se arregla, y se amplia la comprobacion a las dos variables.

   Uso: python build-mi-clave.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    mc = re.search(r'var MI_CLAVE = "([^"]*)"', t)
    mr = re.search(r'var MI_RUTA = "([^"]*)"', t)
    if not mc or not mr or mc.group(1) == mr.group(1):
        continue
    t = t[:mc.start()] + u'var MI_CLAVE = "%s"' % mr.group(1) + t[mc.end():]
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-24s %s -> %s" % (a, mc.group(1), mr.group(1)))

# ------------------------------------------------- que no vuelva
P = os.path.join(D, "cuentas.py")
t = io.open(P, encoding="utf-8").read()

VIEJO = u'''    m = re.search(r'var MI_RUTA = "([^"]*)"', h)
    if not m:
        continue
    k = m.group(1)
    if k != r["clave"]:
        mal += 1
        print(u"  %-20s %-16s activa %s, tendria que activar %s" %
              (r["archivo"], u"la clave", k, r["clave"]))'''

NUEVO = u'''    m = re.search(r'var MI_RUTA = "([^"]*)"', h)
    if not m:
        continue
    k = m.group(1)
    if k != r["clave"]:
        mal += 1
        print(u"  %-20s %-16s activa %s, tendria que activar %s" %
              (r["archivo"], u"la clave", k, r["clave"]))
    # Y la otra, que decide si sale el pie de "segui por aca". Se
    # heredaba igual de mal al copiar una pagina, y esta comprobacion
    # miraba solo MI_RUTA: tres rutas quedaron creyendo ser AI:
    # fundamentos sin que doliera en ningun lado.
    m2 = re.search(r'var MI_CLAVE = "([^"]*)"', h)
    if m2 and m2.group(1) != r["clave"]:
        mal += 1
        print(u"  %-20s %-16s dice ser %s, y es %s" %
              (r["archivo"], u"MI_CLAVE", m2.group(1), r["clave"]))'''

if "MI_CLAVE" in t:
    print(u"  cuentas.py ya lo comprueba")
elif t.count(VIEJO) != 1:
    print(u"  ABORTA: no encuentro la comprobacion de MI_RUTA"); sys.exit(1)
else:
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
    print(u"cuentas.py: ahora mira las dos variables")
