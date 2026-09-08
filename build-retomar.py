# -*- coding: utf-8 -*-
u"""Que "retomar" te lleve al curso, no a la pagina.

   El renglon de la portada linkeaba a <ruta>#<id del paso>, y en las
   paginas de ruta los nodos no tienen ese id: tienen "card-<id>". O
   sea que el ancla no existia y el navegador te dejaba arriba de
   todo, en el hero, a buscar entre veintitres tarjetas cual era la
   que seguias.

   Ahora el link apunta a #card-<id>, que si existe, y ademas las
   paginas de ruta miran el hash al cargar: abren la ficha de ese
   curso y la dejan marcada. Retomar es abrir lo que estabas
   haciendo, no aterrizar cerca.

   Se toca el generador de la portada y las veintitres paginas de
   ruta, que comparten openSheet y el init.

   Uso: python build-retomar.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# =============================================================== index.html
P = os.path.join(D, "index.html")
t = io.open(P, encoding="utf-8").read()

t = cambiar(t,
u'''    h += '<a class="puerta fila" href="' + esc(sigue.ruta.archivo) + '#' + esc(sigue.paso.id) + '">' +''',
u'''    /* Al curso, no a la pagina. El ancla era "#<id>" y en las paginas
       de ruta los nodos se llaman "card-<id>": no existia, y el
       navegador te dejaba arriba de todo a buscar entre veintitres
       tarjetas cual era la que seguias. */
    h += '<a class="puerta fila" href="' + esc(sigue.ruta.archivo) +
      '#card-' + esc(sigue.paso.id) + '">' +''',
u"el ancla", "index.html")

t = cambiar(t,
u'''      '<span class="p-txt"><b>Retoma tu ruta</b>' +
        '<span>' + esc(sigue.paso.t) + ' · ' + esc(sigue.ruta.nombre) + '</span></span></a>' +
      /* Y como llegar al CV. Estaba solo en el bloque "Tu ruta", que
         al subir la agenda quedo abajo del pliegue: existia y no se
         veia, que para quien lo busca es lo mismo que no estar. */
      '<a class="puerta-cv" href="cv.html">' + icon("user", 14) +
        'Cambiar mi CV</a>';''',
u'''      '<span class="p-txt"><b>Retoma donde lo dejaste</b>' +
        '<span>' + esc(sigue.paso.t) + ' · ' + esc(sigue.ruta.nombre) + '</span></span></a>';''',
u"el texto y el link del CV", "index.html")

# y el estilo del link que se fue
t = cambiar(t,
u'''.puerta-cv{
  display:inline-flex; align-items:center; gap:7px; width:fit-content;
  font-size:12.5px; font-weight:650; text-decoration:none;
  color:var(--text-3); padding:6px 2px;
}
.puerta-cv:hover{ color:var(--accent-strong); }''',
u'''/* El link "Cambiar mi CV" que estuvo aca se fue: el menu lo tiene, y
   el bloque "Tu ruta" tambien, con sus dos botones. Tres caminos al
   mismo lado en la misma pantalla es lo que veniamos sacando. */''',
u"el estilo del link del CV", "index.html")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: retomar lleva al curso, y sin el link del CV")


# ==================================================== las paginas de ruta
GANCHO = u'''
/* Volver al curso que estabas haciendo.

   La portada linkea a #card-<id>. El navegador ya salta ahi solo,
   pero saltar no es abrir: lo que uno viene a hacer es ver ese curso,
   asi que se abre su ficha. Y se lo marca un momento, para que al
   cerrar la ficha sepas cual era entre veintitres.

   Va con un respiro porque renderMap() acaba de escribir el mapa y el
   nodo puede no estar todavia cuando corre el init. */
function abrirDelHash(){
  var h = (location.hash || "").replace("#", "");
  if(h.indexOf("card-") !== 0) return;
  var id = h.slice(5);
  window.setTimeout(function(){
    var el = document.getElementById(h);
    if(!el) return;
    el.scrollIntoView({ block: "center" });
    el.classList.add("recien");
    window.setTimeout(function(){ el.classList.remove("recien"); }, 2400);
    try{ openSheet(id); }catch(e){}
  }, 120);
}
'''

CSS = u'''
/* El curso al que volviste, marcado un momento: al cerrar la ficha,
   saber cual era entre veintitres. */
.node.recien{
  outline:3px solid var(--accent);
  outline-offset:3px;
  animation:reciennodo 2.4s ease-out;
}
@keyframes reciennodo{
  0%, 60%{ outline-color:var(--accent); }
  100%{ outline-color:transparent; }
}
'''

n_rutas = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if u"function openSheet" not in t or u"abrirDelHash" in t:
        continue
    if u"function init(){" not in t:
        print(u"  OJO: %s tiene openSheet y no init()" % a); continue

    t = t.replace(u"function init(){", GANCHO + u"\nfunction init(){", 1)

    # llamarlo al final del init: despues de renderMap, que es quien
    # escribe los nodos.
    if t.count(u"  renderMap();\n") != 1:
        print(u"  ABORTA en %s: renderMap x%d" % (a, t.count(u"  renderMap();\n"))); sys.exit(1)
    t = t.replace(u"  renderMap();\n", u"  renderMap();\n  abrirDelHash();\n", 1)

    # y el estilo, al final del <style>
    i = t.index(u"</style>")
    t = t[:i] + CSS + t[i:]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n_rutas += 1

print(u"%d paginas de ruta abren la ficha del curso al que volves" % n_rutas)
