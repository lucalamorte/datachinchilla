# -*- coding: utf-8 -*-
"""El menu de navegacion.

   Hasta ahora, para ir de una pagina a otra habia que volver a la
   portada. Las rutas tienen un "volver" y nada mas, y desde /practica
   no se llegaba a /semana sin pasar por el medio. En el telefono era
   peor, porque ahi no hay ni pie a la vista.

   Lo que va adentro lo definio el pedido: el CV, el armador, las
   rutas, la practica diaria y la semana. Se suman recursos y
   preguntas, que son las dos paginas que quedaron sueltas al sacarlas
   de la portada, y que hoy solo se alcanzan por el pie.

   Cuando entre el idioma, va aca: por eso es un panel y no una fila
   de links.

   Detalles que importan:

   - Marca donde estas. Un menu que no lo dice obliga a mirar la
     direccion para saber en que pagina estas parado.
   - Cierra con la tecla de escape y con un clic afuera. Un panel que
     solo cierra con su propio boton es una trampa, y ya nos paso con
     el de la cuenta.
   - Es un <nav> con aria-expanded, para que un lector de pantalla lo
     anuncie como lo que es.

   Uso: python build-menu.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

# (archivo, etiqueta, que es)
DESTINOS = [
 ("index.html",     u"Inicio",           u"Por dónde empezar"),
 ("cv.html",        u"Tu CV",            u"Tu ruta salida de tu experiencia"),
 ("armar.html",     u"Ármala a mano",    u"Elegís los niveles y los ordenás"),
 ("index.html#rutas", u"Todas las rutas", u"El catálogo entero"),
 ("practica.html",  u"Práctica diaria",  u"Blind 75 y consultas de entrevistas"),
 ("semana.html",    u"Tu semana",        u"Qué día, cuánto rato y con qué"),
 ("recursos.html",  u"Recursos",         u"Gratis y no son cursos"),
 ("preguntas.html", u"Preguntas",        u"Si cuesta algo, qué pasa con tu CV"),
]

BOTON = u'''    <button class="icon-btn" id="menuBtn" type="button" title="Ir a otra parte del sitio" aria-label="Menú" aria-expanded="false" aria-controls="menuPanel">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true">
        <path d="M4 7h16M4 12h16M4 17h16"/>
      </svg>
    </button>
'''

ANCLA = u'''    <button class="icon-btn" id="themeBtn" type="button"'''


def panel(archivo):
    filas = []
    for destino, etiqueta, que in DESTINOS:
        aqui = (destino == archivo) or (archivo == "index.html" and destino.startswith("index.html"))
        filas.append(
            u'      <a class="menu-i%s" href="%s"%s>'
            u'<b>%s</b><span>%s</span></a>'
            % (u" aqui" if aqui else u"", destino,
               u' aria-current="page"' if aqui else u"", etiqueta, que))
    return (u'<nav class="menu" id="menuPanel" hidden aria-label="Secciones del sitio">\n' +
            u"\n".join(filas) + u'\n</nav>\n')


JS = u'''
/* ============================================================
   EL MENU
   ============================================================ */
/* Cierra con escape y con un clic afuera, no solo con su boton: un
   panel que solo cierra desde adentro es una trampa, y con el de la
   cuenta ya nos paso. */
(function(){
  var b = document.getElementById("menuBtn");
  var p = document.getElementById("menuPanel");
  if(!b || !p) return;

  function abrir(si){
    p.hidden = !si;
    b.setAttribute("aria-expanded", si ? "true" : "false");
  }
  b.addEventListener("click", function(ev){
    ev.stopPropagation();
    abrir(p.hidden);
  });
  document.addEventListener("click", function(ev){
    if(p.hidden) return;
    if(p.contains(ev.target) || ev.target === b) return;
    abrir(false);
  });
  document.addEventListener("keydown", function(ev){
    if(ev.key === "Escape" && !p.hidden){ abrir(false); b.focus(); }
  });
})();
'''

CSS = u'''
/* --- El menu -------------------------------------------------------
   Para ir de una pagina a otra sin volver a la portada. En el
   telefono es la unica forma: ahi no hay pie a la vista. */
.menu{
  position:fixed; z-index:60; top:58px; right:14px;
  width:min(280px, calc(100vw - 28px));
  display:flex; flex-direction:column; gap:2px; padding:7px;
  background:var(--surface); border:1px solid var(--divider);
  border-radius:var(--r-lg); box-shadow:var(--shadow-lg);
}
.menu[hidden]{ display:none; }
.menu-i{
  display:flex; flex-direction:column; gap:1px;
  padding:9px 11px; border-radius:var(--r-md);
  text-decoration:none; color:var(--text);
}
.menu-i b{ font-size:13.5px; font-weight:750; }
.menu-i span{ font-size:11.5px; color:var(--text-3); line-height:1.35; }
.menu-i:hover{ background:var(--surface-2); }
/* Donde estas parado. Sin esto hay que mirar la direccion para
   saberlo. */
.menu-i.aqui{ background:var(--accent-soft); }
.menu-i.aqui b{ color:var(--accent-strong); }
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_") or a == "og.html":
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if 'id="menuBtn"' in t or ANCLA not in t:
        continue
    if t.count(ANCLA) != 1:
        print(u"  ABORTA en %s: el ancla aparece %d veces" % (a, t.count(ANCLA)))
        sys.exit(1)

    t = t.replace(ANCLA, BOTON + ANCLA, 1)

    # el panel, justo despues del encabezado
    i = t.index("</header>") + len("</header>")
    t = t[:i] + u"\n\n" + panel(a) + t[i:]

    # el script, al final del ultimo <script> de la pagina
    j = t.rindex("</script>")
    t = t[:j] + JS + t[j:]

    if ".menu-i{" not in t:
        t = t.replace("\n</style>", CSS + "\n</style>", 1)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d paginas con el menu" % n)
