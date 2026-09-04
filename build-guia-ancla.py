# -*- coding: utf-8 -*-
"""El globo aparece donde vas a tocar.

   Estaba clavado en la esquina y te decia "carga tu CV" sin decirte
   donde: habia que buscarlo. Ahora la pagina hace scroll hasta el
   elemento, lo resalta y el globo sale al lado.

   Uso: python build-guia-ancla.py
"""
import io, os, re, sys, glob

D = os.path.dirname(os.path.abspath(__file__))

VIEJO_JS = '''function pintarGuia(){
  var caja = document.getElementById("chin");
  if(!caja || typeof Guia === "undefined") return;

  var p = Guia.tocaAca();
  if(!p){ caja.hidden = true; return; }
'''

NUEVO_JS = '''/* Deja el globo al lado de lo que hay que tocar. Debajo si entra,
   arriba si no; y si el paso no apunta a nada, en la esquina. */
function ubicarGuia(caja, sel){
  var viejo = document.querySelector(".chin-foco");
  if(viejo) viejo.classList.remove("chin-foco");

  if(!sel){
    caja.className = "chin chin-esquina";
    caja.style.top = ""; caja.style.left = "";
    return;
  }
  var e = document.querySelector(sel);
  if(!e){
    caja.className = "chin chin-esquina";
    caja.style.top = ""; caja.style.left = "";
    return;
  }

  e.classList.add("chin-foco");
  e.scrollIntoView({ block: "center", behavior: "smooth" });

  /* Se espera a que el scroll termine: medir antes da la posición
     vieja y el globo aparece en cualquier lado. */
  setTimeout(function(){
    var r = e.getBoundingClientRect();
    var ancho = Math.min(340, window.innerWidth - 32);
    var alto = caja.offsetHeight || 220;

    caja.className = "chin chin-anclada";
    var top = r.bottom + 16;
    if(top + alto > window.innerHeight - 12) top = Math.max(12, r.top - alto - 16);

    var left = r.left;
    if(left + ancho > window.innerWidth - 12) left = window.innerWidth - ancho - 12;
    if(left < 12) left = 12;

    caja.style.top = Math.round(top) + "px";
    caja.style.left = Math.round(left) + "px";
  }, 320);
}

function pintarGuia(){
  var caja = document.getElementById("chin");
  if(!caja || typeof Guia === "undefined") return;

  var p = Guia.tocaAca();
  if(!p){
    caja.hidden = true;
    var f = document.querySelector(".chin-foco");
    if(f) f.classList.remove("chin-foco");
    return;
  }
'''

VIEJO_FIN = '''  caja.hidden = false;
'''
NUEVO_FIN = '''  caja.hidden = false;
  ubicarGuia(caja, p.ancla);
'''

VIEJO_CSS = '''.chin{
  position:fixed; right:20px; bottom:20px; z-index:70;
  width:min(340px, calc(100vw - 40px));
  animation:chin-entra 320ms cubic-bezier(.2,.9,.3,1.2);
}'''

NUEVO_CSS = '''.chin{
  position:fixed; z-index:70;
  width:min(340px, calc(100vw - 32px));
  animation:chin-entra 320ms cubic-bezier(.2,.9,.3,1.2);
  transition:top 220ms ease, left 220ms ease;
}
/* Anclada a lo que hay que tocar, o en la esquina si el paso no
   apunta a nada. */
.chin-esquina{ right:20px; bottom:20px; }
.chin-anclada{ right:auto; bottom:auto; }

/* Lo que hay que tocar, resaltado. El recorte se hace con sombra en
   vez de un fondo aparte: así el elemento sigue siendo clickeable. */
.chin-foco{
  position:relative; z-index:69;
  border-radius:var(--r-lg);
  box-shadow:0 0 0 3px var(--accent), 0 0 0 9px color-mix(in srgb, var(--accent) 22%, transparent);
  animation:chin-late 1.8s ease-in-out infinite;
}
@keyframes chin-late{
  0%, 100%{ box-shadow:0 0 0 3px var(--accent), 0 0 0 9px color-mix(in srgb, var(--accent) 22%, transparent); }
  50%{ box-shadow:0 0 0 3px var(--accent), 0 0 0 14px color-mix(in srgb, var(--accent) 8%, transparent); }
}'''


def hacer(archivo):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    if "ubicarGuia" in t:
        return "ya lo tenia"
    if VIEJO_JS not in t:
        return "sin el bloque viejo"

    t = t.replace(VIEJO_JS, NUEVO_JS, 1)

    # el "caja.hidden = false" que sigue al pintado
    i = t.index("function pintarGuia()")
    j = t.index(VIEJO_FIN, i)
    t = t[:j] + NUEVO_FIN + t[j + len(VIEJO_FIN):]

    if VIEJO_CSS not in t:
        return "sin el css viejo"
    t = t.replace(VIEJO_CSS, NUEVO_CSS, 1)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo"


n = 0
for f in sorted(glob.glob(os.path.join(D, "*.html"))):
    nombre = os.path.basename(f)
    r = hacer(nombre)
    if r == "listo":
        n += 1
    elif r != "sin el bloque viejo":
        print(u"  %-22s %s" % (nombre, r))
print(u"%d paginas con el globo anclado" % n)
