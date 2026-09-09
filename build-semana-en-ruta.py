# -*- coding: utf-8 -*-
u"""El camino a la semana, al lado del boton que la cambia.

   TRES COSAS, la misma idea: no decir dos veces lo mismo.

   1. En el catalogo, una ruta que ya sumaste llevaba dos carteles
      identicos: una cinta arriba que dice "En tu semana" y un boton
      abajo que dice "En tu semana". El boton ademas hace algo -la
      saca- y la cinta no hace nada. Se va la cinta.

   2. En las paginas de ruta habia una franja entera, "Ahora, cuando",
      que solo llevaba a la semana. Ocupaba el ancho completo para
      decir una cosa que cabe en un boton, y estaba a media pagina de
      distancia del boton de sumar, que es donde uno esta mirando
      cuando piensa en su semana.

   3. En su lugar, al lado de "Sumar a tu semana" / "Esta en tu
      semana", un boton para ir a la semana. Aparece solo cuando la
      ruta ya esta sumada: antes de eso no hay nada que ver alla.

   El paso del recorrido que apuntaba a la franja pasa a apuntar al
   boton, que es donde quedo la accion.

   Uso: python build-semana-en-ruta.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# ======================================================== 1. el catalogo
P = os.path.join(D, "index.html")
t = io.open(P, encoding="utf-8").read()
if u"mia-ribbon" in t:
    t = cambiar(t,
u'''    /* Cinta solo cuando dice algo. "Lista para hacer" estaba en las
       dieciséis: una etiqueta que llevan todas no distingue nada, y
       ocupaba el mismo lugar que ésta, que sí. */
    var cinta = mia
      ? '<span class="own-ribbon mia-ribbon">' + icon("check", 11) + 'En tu semana</span>'
      : '';''',
u'''    /* Sin cinta. Decia "En tu semana", igual que el boton de abajo, y
       encima el boton hace algo -la saca- y la cinta no hacia nada.
       Dos carteles identicos en la misma tarjeta no son enfasis, son
       uno de mas. El borde de la tarjeta ya dice que es tuya. */
    var cinta = '';''',
u"la cinta", "index.html")
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print(u"index.html: sin la cinta que repetia el boton")


# =================================================== 2 y 3. las rutas
BOTON = u'''      <a class="btn-quiet btn-semana" id="verSemana" href="semana.html" hidden>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>
        <span class="stack"><span class="verb">Ir a</span><span class="dest">mi semana</span></span>
      </a>
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if u'id="miaBtn"' not in t or u'id="verSemana"' in t:
        continue

    # el boton, justo despues del de sumar
    m = re.search(r'      <button class="btn-quiet btn-mia" id="miaBtn".*?</button>\n', t, re.S)
    if not m:
        print(u"  ABORTA en %s: no encuentro el boton de sumar" % a); sys.exit(1)
    t = t[:m.end()] + BOTON + t[m.end():]

    # fuera la franja
    m2 = re.search(r'<section class="section sigue" id="sigue" hidden>.*?</section>\n', t, re.S)
    if not m2:
        print(u"  ABORTA en %s: no encuentro la franja" % a); sys.exit(1)
    t = t[:m2.start()] + (
        u'<!-- Aca estaba la franja "Ahora, cuando", que ocupaba el ancho\n'
        u'     entero para llevar a la semana. Lo hace el boton "Ir a mi\n'
        u'     semana" del hero, que ademas esta al lado del de sumar: es\n'
        u'     donde uno esta mirando cuando piensa en su semana. -->\n'
    ) + t[m2.end():]

    # y pintarSigue pasa a encender los dos botones
    t = cambiar(t,
u'''function pintarSigue(){
  var caja = document.getElementById("sigue");
  if(!caja || typeof Onb === "undefined") return;
  Onb.cargar();
  var mia = (Onb.estado.rutas || []).indexOf(MI_CLAVE) >= 0;
  caja.hidden = !mia;
}''',
u'''function pintarSigue(){
  /* El boton para ir a la semana sale solo si esta ruta ya esta
     sumada: antes de eso no hay nada que ver alla. Mirar una ruta del
     catalogo no es elegirla. */
  var b = document.getElementById("verSemana");
  if(!b || typeof Onb === "undefined") return;
  Onb.cargar();
  b.hidden = (Onb.estado.rutas || []).indexOf(MI_CLAVE) < 0;
}''',
u"pintarSigue", a)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d paginas de ruta con el boton al lado y sin la franja" % n)


# ============================================ el recorrido, re-anclado
G = os.path.join(D, "guia.js")
g = io.open(G, encoding="utf-8").read()
g = cambiar(g,
u'''      ancla: "#sigue"''',
u'''      /* Al boton, que es donde quedo la accion: la franja "Ahora,
         cuando" que estaba aca se fue por decir lo mismo. */
      ancla: "#miaBtn"''',
u"el ancla", "guia.js")
io.open(G, "w", encoding="utf-8", newline="").write(g)
print(u"guia.js: el paso de la semana apunta al boton")
