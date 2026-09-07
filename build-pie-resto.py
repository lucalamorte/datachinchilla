# -*- coding: utf-8 -*-
u"""El pie, igual en las veinticinco paginas.

   Se pidio sacar del pie "Todas las rutas" y "Armar la mia": los dos
   estan ahora en el menu, en todas las paginas, asi que en el pie
   repetian. Se hizo en la portada y se quedo ahi: las otras
   veinticuatro seguian con los dos links viejos, y ademas sin los dos
   que la portada si tiene -recursos y preguntas-, que son las unicas
   dos paginas a las que el pie llevaba de verdad.

   El pie de la portada es el que vale. Este script lo copia al resto.

   Uso: python build-pie-resto.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

VIEJO = u'''    <nav class="foot-links">
      <a href="index.html#rutas">Todas las rutas</a>
      <a href="armar.html">Armar la mía</a>
      <a href="https://ko-fi.com/lucalamorte" target="_blank" rel="noopener">Invitame un café</a>
      <a href="https://www.linkedin.com/in/lclamorte/" target="_blank" rel="noopener">Luca Lamorte</a>
    </nav>'''

NUEVO = u'''    <nav class="foot-links">
      <a href="recursos.html">Recursos</a>
      <a href="preguntas.html">Preguntas frecuentes</a>
      <a href="https://ko-fi.com/lucalamorte" target="_blank" rel="noopener">Invitame un café</a>
      <a href="https://www.linkedin.com/in/lclamorte/" target="_blank" rel="noopener">Luca Lamorte</a>
    </nav>'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a == "og.html":
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    c = t.count(VIEJO)
    if c == 0:
        continue
    if c != 1:
        print(u"  ABORTA en %s: el pie aparece %d veces" % (a, c))
        sys.exit(1)
    # una pagina no se linkea a si misma en su propio pie
    reemplazo = NUEVO
    if a == "recursos.html":
        reemplazo = NUEVO.replace(
            u'      <a href="recursos.html">Recursos</a>\n', u"")
    if a == "preguntas.html":
        reemplazo = NUEVO.replace(
            u'      <a href="preguntas.html">Preguntas frecuentes</a>\n', u"")
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, reemplazo, 1))
    n += 1

print(u"%d pies al dia" % n)
