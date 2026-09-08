# -*- coding: utf-8 -*-
u"""Tres rutas prometian una insignia de Anthropic que no dan.

   "Casi todos dejan insignia de Anthropic al terminarlos" es cierto
   en la ruta de Claude, que es de donde salio. Airflow, Full Stack
   Open y testing lo dicen tambien, heredado de copiar la pagina, y
   ahi es falso: Astronomer no da insignias de Anthropic, Helsinki
   menos, y la documentacion de Playwright no da nada.

   Dos de esas tres estan publicadas. Prometer una credencial que no
   existe es lo peor que puede decir un sitio que se sostiene en que
   lo que dice es verdad.

   Es la tercera vez que una pagina copiada se trae texto de la
   original: primero MI_RUTA, despues MI_CLAVE, ahora esto. Asi que
   entra tambien la comprobacion: "Anthropic" solo puede aparecer en
   la ruta de Claude.

   Uso: python build-insignia.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

VIEJO = (u"Toca cualquiera para ver qué te llevas y por qué está acá. "
         u"Casi todos dejan insignia de Anthropic al terminarlos.")

# archivo -> lo que de verdad deja esa ruta
NUEVO = {
    "airflow.html": u"Toca cualquiera para ver qué te llevas y por qué está acá. "
                    u"Los de Astronomer dejan constancia en su academia; los de Apache "
                    u"son documentación y no dejan nada más que saberlo.",
    "fullstack.html": u"Toca cualquiera para ver qué te llevas y por qué está acá. "
                      u"La Universidad de Helsinki da certificado al cerrar las partes, "
                      u"y no hay examen.",
    "testing.html": u"Toca cualquiera para ver qué te llevas y por qué está acá. "
                    u"Ninguno deja credencial: son documentación oficial. La que existe "
                    u"en este mundo es ISTQB, y su examen se paga aparte.",
}

n = 0
for a, texto in NUEVO.items():
    p = os.path.join(D, a)
    if not os.path.exists(p):
        continue
    t = io.open(p, encoding="utf-8").read()
    if t.count(VIEJO) != 1:
        print(u"  %s: no esta el texto heredado" % a)
        continue
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, texto, 1))
    print(u"%-24s al dia" % a)
    n += 1

# ------------------------------------------------- que no vuelva
P = os.path.join(D, "cuentas.py")
t = io.open(P, encoding="utf-8").read()

ANCLA = u'''print()
print(u"los numeros coinciden" if not mal else'''

NUEVO_CHK = u'''# --- y que ninguna ruta prometa la credencial de otra
#
# Es la tercera vez que una pagina copiada se trae texto de la
# original: MI_RUTA, MI_CLAVE, y "dejan insignia de Anthropic" en tres
# rutas que no dejan nada de eso. Dos estaban publicadas. Prometer una
# credencial que no existe es lo peor que puede decir un sitio que se
# sostiene en que lo que dice es verdad.
for _r in rutas:
    if _r["archivo"] == "claude.html":
        continue
    try:
        _h = io.open(_r["archivo"], encoding="utf-8").read()
    except IOError:
        continue
    if "Anthropic" in _h:
        mal += 1
        print(u"  %-20s %-16s promete algo de Anthropic, y no es la ruta de Claude" %
              (_r["archivo"], u"la credencial"))

print()
print(u"los numeros coinciden" if not mal else'''

if "promete algo de Anthropic" in t:
    print(u"  cuentas.py ya lo comprueba")
elif t.count(ANCLA) != 1:
    print(u"  ABORTA: no encuentro el cierre de cuentas.py"); sys.exit(1)
else:
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace(ANCLA, NUEVO_CHK, 1))
    print(u"cuentas.py: ninguna ruta puede prometer la credencial de otra")
