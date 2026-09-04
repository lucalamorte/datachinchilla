# -*- coding: utf-8 -*-
"""mi-ruta.html: la ruta que sale de tu CV, como ruta de verdad.

   Se compone desde subir-nivel.html, que ya es una ruta: mismo mapa,
   mismos tramos, mismas tarjetas de curso con duracion, "Gratis" y
   credencial. Lo unico distinto es de donde salen los datos.

   En las otras rutas, ACTS y NODES estan escritos en la pagina. Aca
   se calculan al cargar, desde el onboarding: los tramos son los
   temas que te faltan y los cursos, los que los cubren.

   Por eso no es una lista: una lista no dice en que tramo estas ni
   por que un curso va antes que otro.
"""
import io, re, sys, hashlib

D = u"C:/Users/Luca/Desktop/snowflake path/"


def uno(t, a, b, q):
    if t.count(a) != 1:
        print("  ABORTA [%s]: %d veces" % (q, t.count(a)))
        sys.exit(1)
    return t.replace(a, b)


t = io.open(D + u"subir-nivel.html", encoding="utf-8").read()

# --------------------------------------------------------------- colores
m = re.search(r"  /\* [^\n]*\*/\n  --accent:\s*#[0-9A-Fa-f]{6};\n"
              r"  --accent-strong:\s*#[0-9A-Fa-f]{6};\n"
              r"  --accent-soft:\s*#[0-9A-Fa-f]{6};\n"
              r"  --accent-line:\s*#[0-9A-Fa-f]{6};", t)
if m:
    t = t[:m.start()] + u"""  /* Mi ruta */
  --accent:        #6D28D9;
  --accent-strong: #5B21B6;
  --accent-soft:   #F1ECFD;
  --accent-line:   #D6C7F5;""" + t[m.end():]

m = re.search(r'(:root\[data-theme="dark"\]\{\n)  --accent:\s*#[0-9A-Fa-f]{6};\n'
              r'  --accent-strong:\s*#[0-9A-Fa-f]{6};\n'
              r'  --accent-soft:\s*#[0-9A-Fa-f]{6};\n'
              r'  --accent-line:\s*#[0-9A-Fa-f]{6};', t)
if m:
    t = t[:m.start()] + m.group(1) + u"""  --accent:        #A78BFA;
  --accent-strong: #C4B5FD;
  --accent-soft:   #241640;
  --accent-line:   #3E2A6B;""" + t[m.end():]

# ------------------------------------------------------------------ hero
t = re.sub(r'<p class="lema">[^<]*</p>',
           u'<p class="lema">Sale de lo que contaste</p>', t, count=1)
t = re.sub(r"<h1>.*?</h1>",
           u'<h1>Tu <span class="grad">ruta</span></h1>', t, count=1, flags=re.S)
m = re.search(r'<p class="hero-lead">(.*?)</p>', t, re.S)
if m:
    t = (t[:m.start(1)] +
         u"Los tramos son lo que te falta para el puesto que elegiste, y los cursos "
         u"son los que lo cubren. Salen del catálogo entero, ordenados: no hay material "
         u"nuevo acá, hay una selección hecha con lo que ya contaste." +
         t[m.end(1):])

# ------------------------------------------------------------ la migaja
t = re.sub(r'<span class="brand-sub">/ [^<]*</span>',
           u'<span class="brand-sub">/ Tu ruta</span>', t, count=1)
t = re.sub(r'<a class="backlink" href="index\.html#rutas"',
           u'<a class="backlink" href="index.html"', t, count=1)
t = t.replace(u'<span class="back-txt">Todas las rutas</span>',
              u'<span class="back-txt">Inicio</span>')

# --------------------------------------- ACTS y NODES, calculados al vuelo
vieja = re.search(r"var ACTS = \[.*?\n\];\n\nvar NODES = \[.*?\n\];", t, re.S)
if not vieja:
    print("  ABORTA: no encontre ACTS/NODES")
    sys.exit(1)

NUEVO = u'''/* ============================================================
   ACTS y NODES, calculados desde tu onboarding

   En las otras rutas están escritos en la página. Acá se arman al
   cargar: los tramos son los temas que te faltan para el puesto que
   elegiste, y los cursos, los que los cubren. Con eso el resto de la
   página (el mapa, el avance, la constancia) funciona igual que en
   cualquier otra ruta, sin tocar una línea.
   ============================================================ */
var ACTS = [];
var NODES = [];

/* Cuántos cursos por tramo. Más de esto y el tramo deja de ser un
   tramo: es otra lista. */
var POR_TRAMO = 5;

function nombreDeRuta(clave){
  var i;
  for(i=0;i<PASOS.length;i++){ if(PASOS[i].clave === clave) return PASOS[i].nombre; }
  return clave;
}

/* El paso completo, que pasos.js guarda entero: sin el resumen y la
   duración escrita, la tarjeta del curso queda vacía. */
function pasoCompleto(ruta, id){
  var i, j, r;
  for(i=0;i<PASOS.length;i++){
    r = PASOS[i];
    if(r.clave !== ruta) continue;
    for(j=0;j<r.pasos.length;j++){ if(r.pasos[j].id === id) return r.pasos[j]; }
  }
  return null;
}

function armarRuta(){
  ACTS = []; NODES = [];
  if(typeof Onb === "undefined" || typeof CV === "undefined") return;

  Onb.cargar();
  if(!Onb.hecho() || !Onb.estado.puesto) return;

  var r = CV.armar(Onb.estado.puesto, Onb.estado.temas, 60);

  /* Los pasos, agrupados por tema y en el orden en que CV.armar los
     puso: primero lo que más falta. */
  var orden = [], porTema = {}, i, p;
  for(i=0;i<r.pasos.length;i++){
    p = r.pasos[i];
    if(!porTema[p.tema]){ porTema[p.tema] = []; orden.push(p.tema); }
    porTema[p.tema].push(p);
  }

  var acto = 0, n;
  for(i=0;i<orden.length;i++){
    var tema = orden[i], lista = porTema[tema];
    if(!lista.length) continue;
    acto++;

    /* De qué rutas sale este tramo, para poder decirlo. */
    var deDonde = [], k;
    for(k=0;k<lista.length;k++){
      var nm = nombreDeRuta(lista[k].ruta);
      if(deDonde.indexOf(nm) < 0) deDonde.push(nm);
    }

    ACTS.push({
      n: acto,
      title: lista[0].temaNombre,
      desc: "De " + deDonde.join(" y ")
    });

    for(k=0;k<lista.length && k<POR_TRAMO;k++){
      p = lista[k];
      var full = pasoCompleto(p.ruta, p.id) || {};
      NODES.push({
        id: p.ruta + "-" + p.id,
        act: acto,
        time: full.time || "",
        i: full.i || "check",
        boss: !!full.boss,
        cert: full.cert || "",
        title: p.t,
        summary: full.sum || "",
        goal: full.goal || "",
        wins: full.wins || [],
        u: full.u || "",
        /* La misma clave que en su ruta de origen: marcar el curso
           acá lo marca allá, y al revés. Si no, tendrías el mismo
           curso hecho en un lado y pendiente en el otro. */
        mismo: p.ruta + ":" + p.id,
        deRuta: p.ruta,
        deId: p.id
      });
    }
  }
}

armarRuta();'''
t = t[:vieja.start()] + NUEVO + t[vieja.end():]

# --------------------------------------------------------------- scripts
for nombre in (u"temas.js", u"cv.js", u"onboarding.js"):
    h = hashlib.md5(io.open(D + nombre, "rb").read()).hexdigest()[:8]
    if u'src="%s' % nombre in t:
        continue
    m2 = re.search(r'<script src="path-sync\.js[^"]*"></script>', t)
    if not m2:
        print("  ABORTA: no encuentro path-sync")
        sys.exit(1)
    t = (t[:m2.end()] + u'\n<script src="%s?v=%s"></script>' % (nombre, h) +
         t[m2.end():])

# ------------------------------------------ el vacio, si no hizo el onboarding
t = uno(t, u"function init(){",
u'''/* Sin onboarding no hay ruta que mostrar: en vez de una página vacía,
   se dice qué falta y se lleva a hacerlo. */
function sinRuta(){
  var w = document.querySelector("#mapa") || document.querySelector(".wrap");
  if(!w) return;
  w.innerHTML =
    '<div class="sin-ruta">' +
      '<h2>Todavía no armaste tu ruta</h2>' +
      '<p>Se arma con cuatro respuestas: dónde estás, a dónde vas y cuánto ' +
      'tiempo tienes. Después queda acá, con sus tramos y sus cursos.</p>' +
      '<a class="btn-primary" href="index.html">' +
        '<span class="stack"><span class="verb">Armarla</span>' +
        '<span class="dest">en un minuto</span></span></a>' +
    '</div>';
}

function init(){''', "sinRuta")

t = uno(t, u"  renderMap();",
u'''  if(!NODES.length){ sinRuta(); return; }
  renderMap();''', "guardia")

CSS = u"""
.sin-ruta{
  text-align:center; padding:56px 22px;
  background:var(--surface); border:1px solid var(--divider);
  border-radius:var(--r-xl);
}
.sin-ruta h2{ font-size:24px; margin:0 0 10px; }
.sin-ruta p{ max-width:44ch; margin:0 auto 22px; color:var(--text-2);
  font-size:14.5px; line-height:1.65; }
"""
t = uno(t, u"\n</style>", CSS + u"\n</style>", "css")

io.open(D + u"mi-ruta.html", "w", encoding="utf-8", newline="").write(t)
print(u"mi-ruta.html escrito (%.1f KB)" % (len(t) / 1024.0))
