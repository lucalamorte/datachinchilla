# -*- coding: utf-8 -*-
"""Sumar o sacar la ruta de tu semana, desde la ruta misma.

   Hasta ahora una ruta se activaba en un solo lado -el catalogo- y
   solo despues de cargar el CV. Estando adentro de la ruta, leyendo
   sus cursos, decidiendo si la vas a hacer, no habia forma de
   decirlo: habia que volver a la portada a buscarla en la grilla.

   Es el momento en que alguien decide, asi que el boton va ahi.

   El estado vive en Onb.estado.rutas, que es un array y siempre
   soporto varias: lo que faltaba era poder tocarlo desde aca.

   Uso: python build-activar.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

# archivo -> clave de la ruta en PASOS
RUTAS = {
    "sql-python.html":     "sqlpy",
    "data-engineer.html":  "de",
    "snowpro.html":        "__suelto__",
    "cs50.html":           "cs50",
    "dbt.html":            "dbt",
    "bigdata.html":        "bigdata",
    "data-science.html":   "data_science",
    "arquitectura.html":   "arquitectura",
    "subir-nivel.html":    "subirnivel",
    "ai-fundamentos.html": "aifund",
    "claude.html":         "claude",
    "deep-learning.html":  "deeplearning",
    "llm-agentes.html":    "llmagentes",
    "ml-aplicado.html":    "mlaplicado",
    "web3.html":           "web3",
    "fullstack.html":      "fullstack",
}

BOTON = u'''      <button class="btn-quiet btn-mia" id="miaBtn" type="button" hidden>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
        <span class="stack"><span class="verb" id="miaVerb">Sumar a</span><span class="dest" id="miaDest">mi semana</span></span>
      </button>
'''

CSS = u'''
/* --- Sumar o sacar esta ruta de tu semana ------------------------
   El boton vive en el hero porque es donde se decide: estas leyendo
   la ruta y resolves si la vas a hacer. Antes habia que volver a la
   portada y buscarla en la grilla. */
.btn-mia[hidden]{ display:none; }
.btn-mia.on{
  background:var(--accent-soft);
  border-color:var(--accent);
  color:var(--accent-strong);
}
.btn-mia.on .verb{ color:var(--accent-strong); opacity:.85; }
'''

JS = u'''
/* ============================================================
   ESTA RUTA, EN TU SEMANA
   ============================================================ */
/* La decision de hacer una ruta se toma aca adentro, leyendola, no
   en la grilla de la portada. El estado es el mismo que usa el
   catalogo y la semana: Onb.estado.rutas. */
function pintarMia(){
  var b = document.getElementById("miaBtn");
  if(!b || typeof Onb === "undefined") return;
  Onb.cargar();
  var esMia = Onb.activa(MI_RUTA);
  b.hidden = false;
  b.classList.toggle("on", esMia);
  b.setAttribute("aria-pressed", esMia ? "true" : "false");
  b.setAttribute("title", esMia
    ? "Sacarla: deja de ocupar tiempo en tu semana"
    : "Sumarla: entra en el reparto de tu semana");
  document.getElementById("miaVerb").textContent = esMia ? "Est\\u00e1 en" : "Sumar a";
  document.getElementById("miaDest").textContent = "tu semana";
}

function engancharMia(){
  var b = document.getElementById("miaBtn");
  if(!b || typeof Onb === "undefined") return;
  b.addEventListener("click", function(){
    Onb.alternarRuta(MI_RUTA);
    pintarMia();
    if(typeof Chin !== "undefined"){
      Chin.festejar(Onb.activa(MI_RUTA) ? "festeja" : "busca",
        Onb.activa(MI_RUTA) ? "Sumada a tu semana" : "Fuera de tu semana",
        Onb.activa(MI_RUTA)
          ? "El tiempo que tengas se reparte con las otras que elegiste."
          : "Sigue ac\\u00e1 y tu avance no se toca. Solo deja de ocupar tiempo.");
    }
  });
}
'''


def hacer(archivo, clave):
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        return "no existe"
    t = io.open(p, encoding="utf-8").read()
    if 'id="miaBtn"' in t:
        return "ya lo tenia"

    # --- el boton, al final de los del hero
    m = re.search(r'<div class="hero-cta">.*?\n(\s*)</div>', t, re.S)
    if not m:
        return "sin hero-cta"
    t = t[:m.start(1)] + BOTON + t[m.start(1):]

    # --- el estilo
    if "\n</style>" not in t:
        return "sin style"
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    # --- el js, con la clave de esta ruta
    m2 = re.search(r"\nfunction init\(\)\{", t)
    if not m2:
        return "sin init"
    js = u'\nvar MI_RUTA = "%s";\n' % clave + JS
    t = t[:m2.start()] + js + t[m2.start():]

    # --- y las llamadas, adentro de init Y NO DE OTRA COSA
    #
    # Buscar el primer paintAccount() del archivo es lo que hice la
    # primera vez, y cayo dentro de ensureLocal(), que corre solo
    # cuando marcas un curso sin perfil: el boton nunca aparecia. Ya
    # habia pasado igual con las llamadas de la guia.
    #
    # Asi que se busca DESDE init() en adelante.
    mi = re.search(r"\nfunction init\(\)\{", t)
    if not mi:
        return "sin init donde llamar"
    m3 = re.search(r"(\n\s*)paintAccount\(\);", t[mi.end():])
    if not m3:
        return "init no llama a paintAccount"
    corte = mi.end() + m3.end()
    t = t[:corte] + m3.group(1) + "pintarMia();" + \
        m3.group(1) + "engancharMia();" + t[corte:]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo"


for a in sorted(RUTAS):
    print(u"%-22s %s" % (a, hacer(a, RUTAS[a])))
