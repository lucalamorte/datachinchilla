# -*- coding: utf-8 -*-
"""Encadena CV -> ruta -> semana.

   Las tres paginas existian sueltas: terminabas el CV y quedabas en
   la portada, entrabas a una ruta y no habia forma de seguir, y la
   semana habia que ir a buscarla.

   Ahora:
     - el CV, al terminar, te lleva a tu ruta;
     - la ruta, si es la tuya, ofrece armar la semana con ella;
     - la semana usa esa ruta, que ya lo hacia.

   Solo la ruta que sale del CV alimenta la semana: las que mires
   sueltas del catalogo no entran, porque mirarlas no es elegirlas.

   Uso: python build-cadena.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

# Las paginas de ruta, que son las que reciben el pie.
RUTAS = [
    "snowpro.html", "data-engineer.html", "dbt.html", "subir-nivel.html",
    "bigdata.html", "arquitectura.html", "cs50.html", "data-science.html",
    "sql-python.html", "ai-fundamentos.html", "deep-learning.html",
    "llm-agentes.html", "ml-aplicado.html", "web3.html", "mi-ruta.html",
]

HTML = u"""
<section class="section sigue" id="sigue" hidden>
  <div class="wrap">
    <a class="sigue-caja" href="semana.html">
      <span class="ico">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>
      </span>
      <span class="txt">
        <b>Ahora, cuándo</b>
        <span id="sigueSub">Esta es tu ruta. Falta repartirla en la semana: qué días, a qué hora y cuánto rato.</span>
      </span>
      <span class="fl">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </span>
    </a>
  </div>
</section>
"""

CSS = u"""
/* El paso siguiente: de la ruta a la semana. Sin esto, terminabas de
   mirar tu ruta y no habia a donde ir. */
.sigue[hidden]{ display:none; }
.sigue-caja{
  display:flex; align-items:center; gap:16px;
  padding:20px 22px; border-radius:var(--r-xl);
  background:linear-gradient(160deg, var(--accent-soft), var(--surface) 68%);
  border:1px solid var(--accent-line); text-decoration:none; color:inherit;
  transition:border-color 160ms ease, transform 160ms ease;
}
.sigue-caja:hover{ border-color:var(--accent); transform:translateY(-2px); }
.sigue-caja .ico{
  display:grid; place-items:center; width:46px; height:46px; flex:none;
  border-radius:var(--r-lg); background:var(--surface); color:var(--accent);
}
.sigue-caja .txt{ display:flex; flex-direction:column; gap:3px; }
.sigue-caja .txt b{ font-size:17px; letter-spacing:-.01em; }
.sigue-caja .txt span{ font-size:13px; color:var(--text-2); line-height:1.55; }
.sigue-caja .fl{ margin-left:auto; color:var(--accent); flex:none; display:flex;
  transition:transform 160ms ease; }
.sigue-caja:hover .fl{ transform:translateX(3px); }
@media (max-width:560px){ .sigue-caja{ flex-wrap:wrap; } .sigue-caja .fl{ margin-left:0; } }
"""

JS = u"""
/* El pie sale solo si esta es tu ruta, la que salio del CV. Mirar una
   ruta del catalogo no es elegirla, asi que ahi no aparece. */
function pintarSigue(){
  var caja = document.getElementById("sigue");
  if(!caja || typeof Onb === "undefined") return;
  Onb.cargar();
  var mia = (Onb.estado.rutas || []).indexOf(MI_CLAVE) >= 0;
  caja.hidden = !mia;
}
"""


def clave_de(archivo):
    """La clave con la que el plan conoce a esta ruta."""
    import json
    p = os.path.join(D, "pasos.js")
    t = io.open(p, encoding="utf-8").read()
    d = json.loads(t[t.index("["):t.rindex(";")])
    for r in d:
        if r["archivo"] == archivo:
            return r["clave"]
    return ""


def hacer(archivo):
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        return "no existe"
    t = io.open(p, encoding="utf-8").read()
    if 'id="sigue"' in t:
        return "ya lo tenia"

    clave = clave_de(archivo)
    if not clave and archivo != "mi-ruta.html":
        return "sin clave en pasos.js"

    # el bloque, antes del pie
    m = re.search(r'\n<footer class="foot">', t)
    if not m:
        return "sin footer"
    t = t[:m.start()] + "\n" + HTML + t[m.start():]

    # el estilo
    if "\n</style>" not in t:
        return "sin style"
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    # el script: la clave y la funcion
    m2 = re.search(r"function init\(\)\{", t)
    if not m2:
        return "sin init"
    t = (t[:m2.start()] + u'var MI_CLAVE = "%s";\n' % clave + JS + u"\n" + t[m2.start():])

    # la llamada
    m3 = re.search(r"(\n\s*)paintAccount\(\);", t)
    if m3:
        t = t[:m3.end()] + m3.group(1) + "pintarSigue();" + t[m3.end():]
    else:
        t = t.replace("function init(){", "function init(){\n  setTimeout(pintarSigue, 0);", 1)

    # onboarding.js, que es de donde sale el estado
    if 'src="onboarding.js' not in t:
        m4 = re.search(r'<script src="path-sync\.js[^"]*"></script>', t)
        if not m4:
            return "sin path-sync"
        extra = ""
        for n in ("pasos.js", "temas.js", "cv.js", "onboarding.js"):
            if 'src="%s' % n not in t:
                extra += '<script src="%s"></script>\n' % n
        t = t[:m4.start()] + extra + t[m4.start():]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo (%s)" % clave


for a in RUTAS:
    print(u"%-22s %s" % (a, hacer(a)))
