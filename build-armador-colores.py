# -*- coding: utf-8 -*-
u"""Lo que quedo a mano en el armador cuando pasaron a ser diecisiete.

   Al derivar la lista de rutas de pasos.js, el armador paso de tres
   rutas a diecisiete y de 36 piezas a 263. Los datos quedaron bien,
   pero tres cosas de la pagina seguian escritas a mano contra el
   numero viejo:

   1. Los colores. Habia un --ruta-<id> por ruta, escrito a mano, y
      eran tres. Las otras catorce salian pidiendo una variable que no
      existe: sin color. Ahora salen de catalog.js, que ya trae el
      color de cada ruta -sacado del --accent de su propia pagina-, y
      se escriben al cargar. Los tres a mano se van: dos verdades para
      lo mismo es como se llego hasta aca.

      En oscuro se aclaran, que es lo que hacian los tres a mano y lo
      que necesita .tag, que pinta el icono con el color del fondo.

   2. "Las tres rutas del sitio" y "Treinta y tres niveles". Los dos
      numeros pasan a salir del catalogo: escribirlos de nuevo a mano
      seria dejarlos listos para volver a envejecer.

   3. La docstring del bloque, que tambien decia "las tres paginas".

   Uso: python build-armador-colores.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "armar.html")

CAMBIOS = [
 # --- 1. los colores, generados ------------------------------------
 (u'''
  /* un color por ruta de origen, el mismo que usa cada página */
  --ruta-snowpro:  #0E7FAE;
  --ruta-de:       #6D28D9;
  --ruta-cs50:     #A51C30;
}''',
  u'''
  /* Un color por ruta de origen. No están acá: los escribe la página
     al cargar, leyéndolos de catalog.js, que los saca del --accent de
     cada ruta. Escritos a mano eran tres, y las otras catorce salían
     pidiendo una variable que no existe. */
}''', 1),

 (u'''
  --ruta-snowpro:  #38BDF8;
  --ruta-de:       #A78BFA;
  --ruta-cs50:     #F2707F;
}''', u'''
}''', 1),

 (u'''/* ============================================================
   EL CATÁLOGO · lo genera build-catalog.py leyendo las tres
   páginas. Acá solo se indexa para buscarlo rápido.
   ============================================================ */''',
  u'''/* ============================================================
   EL CATÁLOGO · lo genera build-catalog.py leyendo cada página del
   sitio. Acá solo se indexa para buscarlo rápido.
   ============================================================ */''', 1),

 (u'''function colorRuta(id){ return "var(--ruta-" + (id || "de") + ")"; }''',
  u'''/* Un color por ruta, escrito al cargar y no a mano. A mano eran
   tres, y las otras catorce pedían una variable que no existe: sin
   color. El valor sale de catalog.js, que lo saca del --accent de la
   propia página de cada ruta.

   En oscuro se aclara, porque .tag pinta el icono con el color del
   fondo: un tono pensado para papel blanco deja el icono ilegible. */
(function tonosDeRuta(){
  var claro = [], oscuro = [], i, r;
  for(i=0;i<RUTAS.length;i++){
    r = RUTAS[i];
    if(!r.color) continue;
    claro.push("--ruta-" + r.id + ":" + r.color + ";");
    oscuro.push("--ruta-" + r.id + ":color-mix(in srgb," + r.color + " 55%,#FFFFFF);");
  }
  if(!claro.length) return;
  var s = document.createElement("style");
  s.textContent = ":root{" + claro.join("") + "}" +
                  ':root[data-theme="dark"]{' + oscuro.join("") + "}";
  document.head.appendChild(s);
})();

/* Si una ruta no trajera color, gris antes que una variable vacía. */
function colorRuta(id){
  return PORRUTA[id] && PORRUTA[id].color ? "var(--ruta-" + id + ")" : "#7C8AA0";
}''', 1),

 # --- 2. los dos numeros -------------------------------------------
 (u'''    <p class="hero-lead">Las tres rutas del sitio se abren en niveles sueltos.''',
  u'''    <p class="hero-lead">Las <b id="cuantasRutas">17</b> rutas del sitio se abren en niveles sueltos.''', 1),

 (u'''      <p>Treinta y tres niveles de todas tus rutas. Filtra, busca y suma los que quieras: el orden lo decides a la derecha.</p>''',
  u'''      <p><b id="cuantasPiezas">263</b> niveles de todas las rutas. Filtra, busca y suma los que quieras: el orden lo decides a la derecha.</p>''', 1),

 (u'''function colorRuta(id){
  return PORRUTA[id] && PORRUTA[id].color ? "var(--ruta-" + id + ")" : "#7C8AA0";
}''',
  u'''function colorRuta(id){
  return PORRUTA[id] && PORRUTA[id].color ? "var(--ruta-" + id + ")" : "#7C8AA0";
}

/* Los dos números del texto salen del catálogo. Escritos a mano
   decían tres rutas y treinta y tres niveles cuando ya eran
   diecisiete y doscientos sesenta y tres. */
(function cuantos(){
  var a = document.getElementById("cuantasRutas");
  var b = document.getElementById("cuantasPiezas");
  if(a && RUTAS.length)  a.textContent = RUTAS.length;
  if(b && PIEZAS.length) b.textContent = PIEZAS.length;
})();''', 1),
]

t = io.open(P, encoding="utf-8").read()
for viejo, nuevo, veces in CAMBIOS:
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r x%d, esperaba %d" % (viejo[:52], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)
io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"armar.html: colores y numeros salen del catalogo (%d cambios)" % len(CAMBIOS))
