# -*- coding: utf-8 -*-
u"""El menu se abre pegado a su boton, y marca un solo destino.

   1. SE ABRIA AL COSTADO. El panel era `position:fixed; top:58px;
      right:14px`, o sea clavado a la esquina de la ventana. El boton
      vive adentro del encabezado, que esta centrado y tiene ancho
      maximo: en una ventana de 1440 el boton termina en 1203 y el
      panel en 1416. Doscientos trece pixeles de distancia entre el
      boton y lo que abre. Cuanto mas ancha la pantalla, peor.

      Ahora se coloca al abrir, alineado por su derecha con la derecha
      del boton y justo debajo del encabezado, medido y no supuesto.
      Se recoloca al cambiar el tamano de la ventana, porque un panel
      abierto que se queda donde estaba es el mismo problema.

   2. MARCABA DOS. La regla decia: estas aca si el destino es esta
      pagina, O si estamos en la portada y el destino empieza con
      "index.html". En la portada eso da verdadero dos veces -"Inicio"
      y "Todas las rutas", que es un ancla de la misma pagina- y se
      encendian los dos. "Donde estas" tiene que ser un solo lugar.

   Se arregla el generador -que es de donde salen las paginas nuevas- y
   ademas las 30 que ya estaban, porque build-menu.py saltea la pagina
   que ya tiene menu y por si solo no las tocaria.

   Uso: python build-menu-anclado.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

CSS_VIEJO = u'''.menu{
  position:fixed; z-index:60; top:58px; right:14px;
  width:min(280px, calc(100vw - 28px));'''

CSS_NUEVO = u'''/* Sin top ni right acá: los pone el script, medidos contra el botón.
   Clavado a la esquina de la ventana, el panel abria a 213 pixeles
   del boton que lo abre, porque el encabezado esta centrado. */
.menu{
  position:fixed; z-index:60; top:58px; right:14px;
  width:min(280px, calc(100vw - 28px));'''

JS_VIEJO = u'''  function abrir(si){
    p.hidden = !si;
    b.setAttribute("aria-expanded", si ? "true" : "false");
  }
  b.addEventListener("click", function(ev){
    ev.stopPropagation();
    abrir(p.hidden);
  });'''

JS_NUEVO = u'''  /* Pegado al boton, no a la esquina de la ventana.

     El panel era top:58px right:14px, o sea clavado al borde. El
     boton vive en el encabezado, que esta centrado y con ancho
     maximo: en una ventana de 1440 el boton termina en 1203 y el
     panel en 1416. Se abria a 213 pixeles de lo que lo abre, y
     cuanto mas ancha la pantalla peor.

     Se mide al abrir. La derecha del panel se alinea con la del
     boton, y arriba queda justo debajo del encabezado. Si no entra
     por la izquierda se lo mete a la fuerza, que es mejor que
     mostrarlo cortado. */
  function colocar(){
    var r = b.getBoundingClientRect();
    var barra = document.querySelector(".topbar");
    var abajo = barra ? barra.getBoundingClientRect().bottom : r.bottom;
    var ancho = p.offsetWidth || 280;
    var x = r.right - ancho;
    if(x < 8) x = 8;
    if(x + ancho > window.innerWidth - 8) x = window.innerWidth - 8 - ancho;
    p.style.left = Math.round(x) + "px";
    p.style.right = "auto";
    p.style.top = Math.round(abajo + 6) + "px";
  }

  function abrir(si){
    p.hidden = !si;
    b.setAttribute("aria-expanded", si ? "true" : "false");
    if(si) colocar();
  }
  b.addEventListener("click", function(ev){
    ev.stopPropagation();
    abrir(p.hidden);
  });
  /* Un panel abierto que se queda donde estaba al cambiar el tamano
     es el mismo problema que arreglamos. */
  window.addEventListener("resize", function(){
    if(!p.hidden) colocar();
  }, { passive: true });'''

AQUI_VIEJO = u'''        aqui = (destino == archivo) or (archivo == "index.html" and destino.startswith("index.html"))'''
AQUI_NUEVO = u'''        # Exacto, y nada mas. Decia ademas "o si estamos en la
        # portada y el destino empieza con index.html", y eso da
        # verdadero dos veces en la portada -"Inicio" y "Todas las
        # rutas", que es un ancla de la misma pagina-: se encendian
        # los dos. Donde estas es un solo lugar.
        aqui = (destino == archivo)'''

# En la portada, la fila que sobra.
FILA_VIEJA = u'''<a class="menu-i aqui" href="index.html#rutas" aria-current="page"><b>Todas las rutas</b>'''
FILA_NUEVA = u'''<a class="menu-i" href="index.html#rutas"><b>Todas las rutas</b>'''


def parchar(archivo, cambios, obligatorio=True):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    tocado = 0
    for viejo, nuevo in cambios:
        n = t.count(viejo)
        if n == 0:
            continue
        if n != 1:
            print(u"  ABORTA en %s: %r x%d" % (archivo, viejo[:40], n)); sys.exit(1)
        t = t.replace(viejo, nuevo, 1); tocado += 1
    if obligatorio and not tocado:
        return 0
    if tocado:
        io.open(p, "w", encoding="utf-8", newline="").write(t)
    return tocado


# ---------------------------------------------- 1. el generador, primero
n = parchar("build-menu.py", [(CSS_VIEJO, CSS_NUEVO),
                              (JS_VIEJO, JS_NUEVO),
                              (AQUI_VIEJO, AQUI_NUEVO)])
if n != 3:
    print(u"  ABORTA: el generador solo acepto %d de 3 cambios" % n); sys.exit(1)
print(u"build-menu.py   3 cambios")

# ---------------------------------------------- 2. y las que ya existen
tocadas = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_") or a == "og.html":
        continue
    if parchar(a, [(CSS_VIEJO, CSS_NUEVO), (JS_VIEJO, JS_NUEVO),
                   (FILA_VIEJA, FILA_NUEVA)], obligatorio=False):
        tocadas += 1

print(u"%d paginas con el menu pegado a su boton" % tocadas)
