# -*- coding: utf-8 -*-
"""El globo de la chinchilla, en las paginas donde habla.

   Va anclado abajo a la derecha, encima de todo pero sin tapar el
   contenido: la idea es que uses el sitio de verdad mientras te
   explica, no que leas cuatro pantallas antes de ver nada.

   La chinchilla es el mismo dibujo del logo, mas grande y asomando
   por el borde del globo, como si escarbara desde abajo.

   Uso: python build-guia.py
"""
import io, os, re, sys, hashlib

D = os.path.dirname(os.path.abspath(__file__))

# Donde habla: la portada, y las rutas (para el paso de la semana).
PAGINAS = [
    "cv.html", "semana.html", "practica.html",
    "index.html", "snowpro.html", "data-engineer.html", "dbt.html",
    "subir-nivel.html", "bigdata.html", "arquitectura.html", "cs50.html",
    "data-science.html", "sql-python.html", "ai-fundamentos.html",
    "deep-learning.html", "llm-agentes.html", "ml-aplicado.html",
    "claude.html",
    "web3.html", "mi-ruta.html",
]

# El dibujo, sacado del logo. Sin fondo: asoma sobre el globo.
CHINCHILLA = (
    '<svg class="chin-svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path fill="color-mix(in srgb, var(--accent) 70%, var(--surface))" '
    'd="M 6.47 17.58 Q 6.26 19.36 5.23 17.77 Q 4.28 19.19 4.10 17.39 Q 2.68 18.16 3.32 16.56 '
    'Q 1.79 16.60 3.03 15.53 Q 1.74 14.90 3.24 14.54 Q 2.44 13.45 3.85 13.80 '
    'C 4.4 10.6 7.6 10.0 9.4 11.8 C 10.6 14.2 10.4 17.2 9.6 19.4 Z"/>'
    '<ellipse fill="var(--accent)" cx="10.4" cy="5.3" rx="2.8" ry="3.4" transform="rotate(-21 10.4 5.3)"/>'
    '<ellipse fill="var(--accent)" cx="18.0" cy="5.3" rx="2.8" ry="3.4" transform="rotate(21 18.0 5.3)"/>'
    '<ellipse fill="var(--accent-soft)" cx="10.6" cy="5.7" rx="1.4" ry="1.8" transform="rotate(-21 10.6 5.7)"/>'
    '<ellipse fill="var(--accent-soft)" cx="17.8" cy="5.7" rx="1.4" ry="1.8" transform="rotate(21 17.8 5.7)"/>'
    '<ellipse fill="var(--accent)" cx="14.2" cy="17.2" rx="5.8" ry="5.2"/>'
    '<circle fill="var(--accent)" cx="14.2" cy="11.3" r="5.4"/>'
    '<ellipse fill="var(--surface)" cx="12.3" cy="10.8" rx=".85" ry="1.05"/>'
    '<ellipse fill="var(--surface)" cx="16.3" cy="10.8" rx=".85" ry="1.05"/>'
    '<circle fill="var(--accent)" cx="12.6" cy="10.4" r=".3"/>'
    '<circle fill="var(--accent)" cx="16.6" cy="10.4" r=".3"/>'
    '<path fill="var(--surface)" d="M13.6 12.5h1.4c.26 0 .41.29.25.5l-.7.92a.31.31 0 0 1-.5 0'
    'l-.7-.92a.31.31 0 0 1 .25-.5Z"/></svg>'
)

HTML = u"""
<div class="chin" id="chin" hidden>
  <div class="chin-globo">
    <button class="chin-x" type="button" id="chinX" title="No mostrar más" aria-label="Cerrar la guía">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <div class="chin-fig">%s</div>
    <b class="chin-t" id="chinT"></b>
    <p class="chin-p" id="chinP"></p>
    <div class="chin-acc">
      <span class="chin-n" id="chinN"></span>
      <button class="btn-primary chin-b" type="button" id="chinB">
        <span class="stack"><span class="verb">Seguir</span><span class="dest" id="chinBT"></span></span>
      </button>
    </div>
  </div>
</div>
""" % CHINCHILLA

CSS = u"""
/* --- La chinchilla que te guia ---------------------------------- */
.chin{
  position:fixed; right:20px; bottom:20px; z-index:70;
  width:min(340px, calc(100vw - 40px));
  animation:chin-entra 320ms cubic-bezier(.2,.9,.3,1.2);
}
.chin[hidden]{ display:none; }
@keyframes chin-entra{
  from{ opacity:0; transform:translateY(14px) scale(.96); }
  to{ opacity:1; transform:none; }
}
.chin-globo{
  position:relative; padding:26px 20px 18px;
  border-radius:var(--r-xl);
  background:var(--surface); border:1px solid var(--accent-line);
  box-shadow:var(--shadow-lg);
}
/* La chinchilla asoma por arriba del globo, como escarbando. */
.chin-fig{
  position:absolute; top:-30px; left:18px;
  width:56px; height:56px; border-radius:50%;
  background:var(--accent-soft); border:1px solid var(--accent-line);
  display:grid; place-items:center; overflow:hidden;
}
.chin-svg{ width:42px; height:42px; margin-top:7px; }
.chin-x{
  position:absolute; top:9px; right:9px;
  display:grid; place-items:center; width:26px; height:26px;
  border-radius:var(--r-pill); cursor:pointer;
  background:none; border:0; color:var(--text-3);
}
.chin-x:hover{ background:var(--surface-2); color:var(--text); }
.chin-t{ display:block; margin-top:14px; font-size:16px; letter-spacing:-.01em; }
.chin-p{ margin:6px 0 0; font-size:13.5px; color:var(--text-2); line-height:1.6; }
.chin-acc{ display:flex; align-items:center; gap:12px; margin-top:16px; }
.chin-n{ font-size:11px; font-weight:800; letter-spacing:.06em;
  text-transform:uppercase; color:var(--text-3); }
.chin-b{ margin-left:auto; padding:10px 16px; }
.chin-b .dest{ font-size:14px; }
@media (max-width:560px){
  .chin{ right:12px; left:12px; bottom:12px; width:auto; }
}
"""

JS = u"""
/* ============================================================
   LA GUIA · la chinchilla te dice que sigue
   ============================================================ */
function pintarGuia(){
  var caja = document.getElementById("chin");
  if(!caja || typeof Guia === "undefined") return;

  var p = Guia.tocaAca();
  if(!p){ caja.hidden = true; return; }

  document.getElementById("chinT").textContent = p.titulo;
  document.getElementById("chinP").textContent = p.texto;
  document.getElementById("chinBT").textContent = p.accion;
  document.getElementById("chinN").textContent =
    "Paso " + (Guia.estado.paso + 1) + " de " + Guia.PASOS.length;
  caja.hidden = false;

  document.getElementById("chinB").onclick = function(){
    Guia.avanzar();
    if(p.lleva){ location.href = p.lleva; return; }
    pintarGuia();
  };
  document.getElementById("chinX").onclick = function(){
    Guia.cerrar();
    caja.hidden = true;
  };
}
"""


def hacer(archivo):
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        return "no existe"
    t = io.open(p, encoding="utf-8").read()
    if 'id="chin"' in t:
        return "ya lo tenia"

    if "</body>" in t:
        t = t.replace("</body>", HTML + "</body>", 1)
    else:
        t = t.rstrip() + "\n" + HTML

    if "\n</style>" not in t:
        return "sin style"
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    m = re.search(r"function init\(\)\{", t)
    if not m:
        return "sin init"
    t = t[:m.start()] + JS + u"\n" + t[m.start():]

    m2 = re.search(r"(\n\s*)paintAccount\(\);", t)
    if m2:
        t = t[:m2.end()] + m2.group(1) + "pintarGuia();" + t[m2.end():]
    else:
        return "sin donde llamar"

    if 'src="guia.js' not in t:
        m3 = re.search(r'<script src="onboarding\.js[^"]*"></script>', t)
        if not m3:
            return "sin onboarding.js"
        t = t[:m3.end()] + '\n<script src="guia.js"></script>' + t[m3.end():]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo"


for a in PAGINAS:
    print(u"%-22s %s" % (a, hacer(a)))
