# -*- coding: utf-8 -*-
"""Los botones de la guia, segun lo que el paso pida.

   Un paso que pide una accion tenia igual un boton para avanzar, en
   gris y con un aviso. Pero si la accion es la unica forma de seguir,
   un boton que no avanza no es un boton: es una cosa que se aprieta y
   no pasa nada. Se saca.

   Queda el texto diciendo que falta, que es la informacion que ese
   boton intentaba dar.

   Y "Saltear" pasa a ser lo que su nombre dice: salir del recorrido
   entero. Antes era lo mismo que la cruz, sin decirlo. Ahora
   pregunta antes -para no salirse de un clic al pasar- y avisa que
   arriba a la derecha se vuelve a activar, que es la parte que nadie
   podia adivinar.

   Uso: python build-guia-botones.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

# --- el boton principal: no existe si el paso pide algo
V_BOTON = u"""  var pendiente = Guia.falta ? Guia.falta(p) : null;
  var bot = document.getElementById("chinB");
  bot.classList.toggle("chin-b-flojo", !!pendiente);
  bot.title = pendiente || "";
  bot.onclick = function(){
    var f = Guia.falta ? Guia.falta(p) : null;
    if(f){ toast(f); return; }"""

N_BOTON = u"""  /* Si el paso pide una accion, no hay boton: la unica forma de
     seguir es hacerla. Un boton que no avanza no es un boton, es una
     cosa que se aprieta y no pasa nada. En su lugar queda dicho que
     falta, que es lo que ese boton intentaba explicar. */
  var pendiente = Guia.falta ? Guia.falta(p) : null;
  var bot = document.getElementById("chinB");
  var pide = document.getElementById("chinPide");
  bot.hidden = !!pendiente;
  if(pide){
    pide.hidden = !pendiente;
    pide.textContent = pendiente || "";
  }
  bot.onclick = function(){
    var f = Guia.falta ? Guia.falta(p) : null;
    if(f){ return; }"""

# --- saltear: salir del recorrido, preguntando
V_SALTO = u"""  document.getElementById("chinX").onclick = cerrarGuia;
  var salto = document.getElementById("chinSalto");
  if(salto) salto.onclick = cerrarGuia;"""

N_SALTO = u"""  document.getElementById("chinX").onclick = cerrarGuia;
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
  };"""

# --- el renglon que dice que falta
V_HTML = u"""      <span class="chin-n" id="chinN"></span>"""
N_HTML = u"""      <span class="chin-n" id="chinN"></span>
      <span class="chin-pide" id="chinPide" hidden></span>"""

CSS = u'''
/* Lo que falta para poder seguir. Ocupa el lugar del boton, que en
   esos pasos no existe: la unica forma de avanzar es hacer la accion. */
.chin-pide{
  display:block; margin-left:auto; text-align:right;
  font-size:12px; font-weight:700; color:var(--text-3); max-width:19ch;
  line-height:1.4;
}
.chin-pide[hidden]{ display:none; }
'''

n_js, n_html = 0, 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "chinB" not in t or 'id="chinPide"' in t:
        continue

    if V_BOTON in t:
        t = t.replace(V_BOTON, N_BOTON, 1)
        n_js += 1
    if V_SALTO in t:
        t = t.replace(V_SALTO, N_SALTO, 1)
    if t.count(V_HTML) == 1:
        t = t.replace(V_HTML, N_HTML, 1)
        n_html += 1
    if ".chin-pide{" not in t and "\n</style>" in t:
        t = t.replace("\n</style>", CSS + "\n</style>", 1)

    io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"%d paginas con el boton condicionado, %d con el renglon" % (n_js, n_html))
