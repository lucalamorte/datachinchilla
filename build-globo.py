# -*- coding: utf-8 -*-
"""El globo de la guia quedaba fuera de pantalla si ya habias
   scrolleado.

   ubicarGuia() manda a la pagina al ancla con scroll suave y despues
   espera 320 ms fijos para medir donde quedo. Alcanzaba mientras el
   ancla estuviera cerca. Si ya habias bajado, el viaje es largo, la
   medicion cae a mitad de camino y el globo se fija en una posicion
   que ya no existe: termina con top negativo, cortado contra el
   borde de arriba.

   Tres cambios:

   1. Se espera a que el scroll TERMINE, no un tiempo fijo. Se mira
      cuando deja de moverse, con una red a los 1200 ms por si el
      navegador no hace scroll suave.

   2. La posicion se mete dentro de la pantalla si o si. Antes solo se
      corregia el caso de "no entra abajo"; el de "no entra arriba"
      quedaba sin corregir y ese era justo el que se veia mal.

   3. Mientras esta anclado, el globo sigue al ancla al scrollear. Con
      position:fixed y un top calculado una sola vez, cualquier scroll
      posterior lo dejaba apuntando al aire.

   Uso: python build-globo.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

VIEJO = u"""  e.classList.add("chin-foco");
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
}"""

NUEVO = u"""  e.classList.add("chin-foco");
  chinAncla = e;
  e.scrollIntoView({ block: "center", behavior: "smooth" });

  /* Se espera a que el scroll TERMINE, no un tiempo fijo. Con 320 ms
     alcanzaba mientras el ancla estuviera cerca; si ya habias bajado,
     el viaje es largo, la medicion caia a mitad de camino y el globo
     quedaba fijado en una posicion que ya no existia. */
  if(chinReloj){ clearInterval(chinReloj); chinReloj = 0; }
  var ultimo = -1, quietos = 0;
  chinReloj = setInterval(function(){
    var y = Math.round(window.pageYOffset);
    if(y === ultimo) quietos++;
    else { quietos = 0; ultimo = y; }
    if(quietos >= 2){
      clearInterval(chinReloj); chinReloj = 0;
      colocarGlobo(caja, e);
    }
  }, 60);
  /* Red, por si el navegador no hace scroll suave o lo interrumpen. */
  setTimeout(function(){
    if(chinReloj){ clearInterval(chinReloj); chinReloj = 0; }
    colocarGlobo(caja, e);
  }, 1200);
}

/* Donde va el globo respecto de lo que senala. Sale aparte de
   ubicarGuia porque tambien corre en cada scroll: con position:fixed
   y un top calculado una sola vez, bajar dos lineas dejaba al globo
   apuntando al aire. */
function colocarGlobo(caja, e){
  if(!caja || !e) return;
  var r = e.getBoundingClientRect();
  var ancho = Math.min(340, window.innerWidth - 32);
  var alto = caja.offsetHeight || 220;

  caja.className = "chin chin-anclada";
  var top = r.bottom + 16;
  if(top + alto > window.innerHeight - 12) top = r.top - alto - 16;
  /* Y si tampoco entra arriba, se lo mete adentro a la fuerza. Antes
     solo se corregia el caso de "no entra abajo": el de "no entra
     arriba" quedaba con top negativo, que es como se veia roto. */
  if(top < 12) top = 12;
  if(top + alto > window.innerHeight - 12){
    top = Math.max(12, window.innerHeight - alto - 12);
  }

  var left = r.left;
  if(left + ancho > window.innerWidth - 12) left = window.innerWidth - ancho - 12;
  if(left < 12) left = 12;

  caja.style.top = Math.round(top) + "px";
  caja.style.left = Math.round(left) + "px";
}"""

# la variable de estado y el listener de scroll, antes de ubicarGuia
CABECERA_VIEJA = u"function ubicarGuia(caja, sel){"
CABECERA_NUEVA = u"""/* El ancla que el globo esta senalando, para poder recolocarlo
   mientras se scrollea. */
var chinAncla = null, chinReloj = 0;

if(typeof window !== "undefined"){
  window.addEventListener("scroll", function(){
    var caja = document.getElementById("chin");
    if(!caja || caja.hidden || !chinAncla) return;
    if(caja.className.indexOf("chin-anclada") < 0) return;
    if(chinReloj) return;          /* todavia esta viajando */
    colocarGlobo(caja, chinAncla);
  }, { passive: true });
  window.addEventListener("resize", function(){
    var caja = document.getElementById("chin");
    if(caja && !caja.hidden && chinAncla &&
       caja.className.indexOf("chin-anclada") >= 0) colocarGlobo(caja, chinAncla);
  }, { passive: true });
}

function ubicarGuia(caja, sel){"""

# y las dos salidas por la esquina tienen que soltar el ancla
SALIDA_VIEJA = u"""    caja.className = "chin chin-esquina";
    caja.style.top = ""; caja.style.left = "";
    return;"""
SALIDA_NUEVA = u"""    caja.className = "chin chin-esquina";
    caja.style.top = ""; caja.style.left = "";
    chinAncla = null;
    return;"""

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "function ubicarGuia" not in t:
        continue
    if "colocarGlobo" in t:
        continue

    for viejo, nuevo, veces in [(VIEJO, NUEVO, 1),
                                (CABECERA_VIEJA, CABECERA_NUEVA, 1),
                                (SALIDA_VIEJA, SALIDA_NUEVA, 2)]:
        c = t.count(viejo)
        if c != veces:
            print(u"  ABORTA en %s: %r aparece %d veces, esperaba %d"
                  % (a, viejo[:44], c, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d paginas: el globo espera a que el scroll termine y no se sale de pantalla" % n)
