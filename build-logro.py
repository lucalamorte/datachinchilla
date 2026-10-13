# -*- coding: utf-8 -*-
u"""Que la tarjeta se desbloquee de verdad.

   Decia "Se desbloquea cuando cierres los veintitres pasos del mapa"
   y no habia nada que la desbloqueara: la marca de agua que dice
   EJEMPLO estaba puesta para siempre. Una promesa que el sitio no
   cumple, en el sitio que se sostiene en que lo que dice es verdad.

   Ahora pasa. Cuando cierras el ultimo paso:

     - se va la marca de agua
     - aparecen los botones de compartir
     - el cartel de abajo deja de decir cuanto falta

   Y mientras falta, los botones no estan. Compartir "termine la
   ruta" sin haberla terminado no es un boton que sobra: es uno que
   miente, y lo primero que haria cualquiera es apretarlo para ver.
   En su lugar dice cuantos pasos quedan, que es el dato que uno
   quiere en ese momento.

   Uso: python build-logro.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

CSS = u'''
/* La tarjeta, cuando de verdad la terminaste. Antes decia "se
   desbloquea" y no habia nada que la desbloqueara: la marca de agua
   que dice EJEMPLO estaba puesta para siempre. */
.cert-card .cert-compartir{ display:none; }
.cert-card.lograda .cert-compartir{ display:flex; }
.cert-card.lograda .cert-agua{ display:none; }
.cert-card.lograda .cert-hoja{ border-color:var(--accent); }
'''

JS = u'''
/* Desbloquear la tarjeta al cerrar el ultimo paso.

   Se mira contra NODES y no contra un numero escrito: una ruta que
   crece -CS50 paso de once pasos a treinta y siete- dejaria el numero
   viejo diciendo que terminaste cuando no.

   Corre al pintar el mapa y cada vez que marcas, que son los dos
   momentos en que esto puede cambiar. */
function pintarLogro(){
  var card = document.querySelector(".cert-card");
  if(!card || typeof NODES === "undefined") return;
  var faltan = 0, i;
  for(i=0;i<NODES.length;i++){ if(!done[NODES[i].id]) faltan++; }
  card.classList.toggle("lograda", faltan === 0);
  var nota = card.querySelector(".cert-nota");
  if(nota){
    nota.textContent = faltan === 0
      ? "Lo terminaste. La tarjeta es tuya y el texto dice lo que hiciste."
      : (faltan === 1 ? "Falta un paso del mapa."
                      : "Faltan " + faltan + " pasos del mapa.");
  }
}
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if u"cert-compartir" not in t or u"pintarLogro" in t:
        continue

    # el estilo
    k = t.index(u"</style>")
    t = t[:k] + CSS + t[k:]

    # la funcion, al lado de renderMap
    if u"function renderMap(){" not in t:
        print(u"  %s: sin renderMap, lo salteo" % a); continue
    t = t.replace(u"function renderMap(){", JS + u"\nfunction renderMap(){", 1)

    # y que corra: al pintar el mapa y al marcar
    if t.count(u"  renderMap();\n") < 1:
        print(u"  ABORTA en %s: no encuentro renderMap()" % a); sys.exit(1)
    t = t.replace(u"  renderMap();\n", u"  renderMap();\n  pintarLogro();\n", 1)

    # toggleDone termina llamando a renderMap en algun lado; se engancha
    # en saveState, que es por donde pasa todo cambio.
    v = u"function saveState(){\n"
    if v not in t:
        print(u"  ABORTA en %s: no encuentro saveState" % a); sys.exit(1)
    t = t.replace(v, u"function saveState(){\n"
                     u"  /* La tarjeta mira el avance, y aca es por donde pasa todo\n"
                     u"     cambio de avance: marcar, desmarcar y lo que baja de la\n"
                     u"     nube. Engancharlo en toggleDone dejaba afuera los otros\n"
                     u"     dos. */\n"
                     u"  if(typeof pintarLogro === \"function\") pintarLogro();\n", 1)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d rutas con la tarjeta que se desbloquea" % n)
