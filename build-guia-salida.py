# -*- coding: utf-8 -*-
u"""Una sola salida del recorrido, y que la interrogacion funcione.

   Dos cosas del mismo pedido.

   1. Sacar "Saltear". Habia dos botones para lo mismo: la cruz de
      arriba cerraba el recorrido de una, y "Saltear", abajo al lado
      de "Seguir", cerraba el recorrido preguntando antes. Dos salidas
      para una sola accion, y la que preguntaba era la que estaba
      pegada al boton de avanzar.

      Queda la cruz, que es donde uno busca cerrar algo, y la pregunta
      se muda ahi: era lo unico bueno que tenia "Saltear".

   2. El boton de la interrogacion fuera de la portada. Llamaba a
      reabrir(), que deja el recorrido en el paso 0 -que vive en la
      portada-, y el globo no se pinta donde el paso no es de esa
      pagina: o sea que en /practica, en /semana y en las diecisiete
      rutas el boton no hacia absolutamente nada.

      Ahora lleva a la portada. Y saltea el saludo: quien abre el
      recorrido desde adentro del sitio ya sabe quien es la
      chinchilla, y hacerle leer la presentacion otra vez es
      empezar por lo unico que ya no le hace falta.

      La decision de a donde ir vive en guia.js, no repetida en las
      veintidos paginas.

   Uso: python build-guia-salida.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r x%d, esperaba %d"
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


# ---------------------------------------------------- 1. guia.js: a donde ir
parchar("guia.js", [
 (u'''  function reabrir(){
    estado.cerrada = false;
    estado.paso = 0;
    guardar();
  }''',
  u'''  function reabrir(){
    estado.cerrada = false;
    estado.paso = 0;
    guardar();
  }

  /* El boton de la interrogacion, desde cualquier pagina.

     Antes llamaba a reabrir() y listo, o sea que dejaba el recorrido
     en el paso 0 -que vive en la portada- y el globo no se pinta
     donde el paso no es de esa pagina: fuera de la portada el boton
     no hacia nada.

     Devuelve a donde hay que ir, o "" si ya estamos donde toca. La
     decision vive aca y no repetida en veintidos paginas.

     Desde otra pagina saltea el saludo: quien abre el recorrido
     estando adentro del sitio ya sabe quien soy, y empezar por la
     presentacion es empezar por lo unico que ya no le hace falta. */
  function abrir(){
    estado.cerrada = false;
    if(donde() === "index"){
      estado.paso = 0;
      guardar();
      return "";
    }
    estado.paso = 1;
    guardar();
    return "index.html";
  }''', 1),

 (u"    cerrar: cerrar, reabrir: reabrir, retomar: retomar",
  u"    cerrar: cerrar, reabrir: reabrir, abrir: abrir, retomar: retomar", 1),
])

# ---------------------------------------------------- 2. el boton, en todas
V_BOTON = u'''    gb.addEventListener("click", function(){
      Guia.reabrir();
      pintarGuia();
      var c = document.getElementById("chin");
      if(c && !c.hidden && c.scrollIntoView) c.scrollIntoView({ block: "nearest" });'''

N_BOTON = u'''    gb.addEventListener("click", function(){
      /* Fuera de la portada hay que ir: el primer paso vive alla y
         el globo no se pinta donde el paso no es de esta pagina. */
      var ir = Guia.abrir ? Guia.abrir() : (Guia.reabrir(), "");
      if(ir){ location.href = ir; return; }
      pintarGuia();
      var c = document.getElementById("chin");
      if(c && !c.hidden && c.scrollIntoView) c.scrollIntoView({ block: "nearest" });'''

# ---------------------------------------------------- 3. una sola salida
V_SALTO_HTML = u'''
      <button class="chin-salto" type="button" id="chinSalto">Saltear</button>'''

V_X = u'''  document.getElementById("chinX").onclick = cerrarGuia;
  var salto = document.getElementById("chinSalto");
  if(salto) salto.onclick = function(){
    /* Pregunta antes: saltear cierra el recorrido entero, y estaba
       al lado del boton de seguir, asi que se iba de un clic al
       pasar. Y avisa donde vuelve a activarse, que es lo que nadie
       podia adivinar. */
    if(!window.confirm("Se cierra el recorrido completo. Lo vuelves a abrir " +
                       "cuando quieras con el bot\\u00f3n de la interrogaci\\u00f3n, " +
                       "arriba a la derecha. \\u00bfSalir?")) return;
    cerrarGuia();
  };'''

N_X = u'''  /* La unica salida. Antes habia dos: esta cruz, que cerraba de una,
     y un "Saltear" abajo que preguntaba. Dos botones para lo mismo, y
     el que preguntaba estaba pegado al de avanzar. Queda la cruz, que
     es donde uno busca cerrar algo, con la pregunta que era lo unico
     bueno que tenia el otro. */
  document.getElementById("chinX").onclick = function(){
    if(!window.confirm("Se cierra el recorrido completo. Lo vuelves a abrir " +
                       "cuando quieras con el bot\\u00f3n de la interrogaci\\u00f3n, " +
                       "arriba a la derecha. \\u00bfSalir?")) return;
    cerrarGuia();
  };'''

n_b, n_s, n_x = 0, 0, 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a == "og.html":
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    antes = t
    if t.count(V_BOTON) == 1:
        t = t.replace(V_BOTON, N_BOTON, 1); n_b += 1
    if t.count(V_SALTO_HTML) == 1:
        t = t.replace(V_SALTO_HTML, u"", 1); n_s += 1
    if t.count(V_X) == 1:
        t = t.replace(V_X, N_X, 1); n_x += 1
    if t != antes:
        io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"%-22s %d botones de ayuda, %d 'Saltear' fuera, %d cruces que preguntan"
      % ("las paginas", n_b, n_s, n_x))

# El CSS de .chin-salto queda sin usar. Se saca el bloque entero por
# texto, no por linea: borrar solo las lineas que dicen ".chin-salto"
# dejaria el cuerpo de la regla suelto y rompe la hoja.
CSS_SALTO = u"""
.chin-salto{
  background:none; border:0; padding:4px 2px; cursor:pointer;
  font:inherit; font-size:12px; color:var(--text-3); text-decoration:underline;
}
.chin-salto:hover{ color:var(--text); }
"""

n_css = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "chinSalto" in t or t.count(CSS_SALTO) != 1:
        continue
    io.open(p, "w", encoding="utf-8", newline="").write(
        t.replace(CSS_SALTO, u"\n", 1))
    n_css += 1
print(u"%-22s %d hojas sin la regla que sobraba" % ("el css", n_css))
