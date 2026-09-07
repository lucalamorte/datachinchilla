# -*- coding: utf-8 -*-
u"""La agenda, donde se ve.

   "El widget de la agenda sigue sin estar en la landing", por tercera
   vez. Y estaba: se pinta bien, con plan y sin plan, con perfil y sin
   perfil. Lo comprobe en los dos caminos.

   El problema es donde. La agenda arrancaba a 2245 pixeles del borde
   de arriba, debajo de un hero de 1652 y de un bloque de estado de
   532. Dos pantallas y media de scroll antes de que aparezca. Algo
   que hay que buscar tanto, para quien lo usa no esta.

   Dos cambios:

   1. Una linea en el hero, arriba de todo, con lo de hoy: cuanto rato
      y con que. Es lo que se pidio tres veces cuando se dijo
      "widget", y es lo unico de la portada que uno mira todos los
      dias. Se ve sin scrollear y lleva a la agenda entera.

      Va debajo de las puertas y solo cuando hay plan: para quien
      llega por primera vez no hay nada que decir todavia.

   2. La agenda de los siete dias sube: pasa a ir antes del bloque de
      estado, no despues. "Que hago hoy" gana contra "como vengo".

   Uso: python build-agenda-arriba.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")

t = io.open(P, encoding="utf-8").read()

if "hoyMini" in t:
    print(u"  ya estaba"); sys.exit(1)


def cambiar(viejo, nuevo, veces=1):
    global t
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r x%d, esperaba %d" % (viejo[:52], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)


# ------------------------------------------------ 1. la agenda sube
SEC_INI = u'<section class="section hoy sigue cierra" id="hoy">'

i = t.index(SEC_INI)
j = t.index(u"</section>", i) + len(u"</section>\n")
seccion = t[i:j]
t = t[:i] + t[j:]

ANTES_DE = u'<section class="section estado sigue cierra" id="estado">'
cambiar(ANTES_DE, seccion + u"\n" + ANTES_DE)

# ------------------------------------------------ 2. la linea del hero
cambiar(u'''    <div class="puertas" id="puertas" hidden></div>''',
        u'''    <div class="puertas" id="puertas" hidden></div>
    <!-- Lo de hoy, sin scrollear. La agenda entera vive mas abajo;
         esto es el renglon que uno mira todos los dias. -->
    <a class="hoy-mini" id="hoyMini" href="#hoy" hidden></a>''')

# ------------------------------------------------ 3. pintarlo
cambiar(u'''function renderHoy(){
  var caja = document.getElementById("hoy");
  if(!caja || typeof Plan === "undefined" || !hayPlan()) return;''',
        u'''/* El renglon de hoy, arriba de todo.

   La agenta entera arrancaba a 2245 pixeles del borde: dos pantallas
   y media de scroll. Algo que hay que buscar tanto, para quien lo usa
   no esta, y por eso se pidio tres veces "el widget de la agenda".

   Esto es el widget: cuanto rato y con que, hoy. Lleva a la agenda
   completa, que sigue existiendo con los siete dias. */
function renderHoyMini(){
  var m = document.getElementById("hoyMini");
  if(!m || typeof Plan === "undefined" || !hayPlan()) return;

  Plan.cargar();
  var d = Plan.deHoy(), bl = d.bloques, i, total = 0, que = [];
  for(i=0;i<bl.length;i++){
    total += bl[i].min;
    if(que.length < 2) que.push(bl[i]["qué"]);
  }

  var cuerpo;
  if(!bl.length){
    /* Un dia libre es un dia que esta bien asi, no uno al que le
       falta algo. */
    cuerpo = '<b>Hoy no toca nada.</b>' +
             '<span>Tu semana lo dice, y esta bien. Mira los otros días.</span>';
  }else{
    cuerpo = '<b>Hoy: ' + ratoLargo(total) + '</b>' +
             '<span>' + esc(que.join(" y ")) +
             (bl.length > que.length ? ", y algo más" : "") + '</span>';
  }

  m.innerHTML =
    '<span class="hm-ico">' + icon("clock", 20) + '</span>' +
    '<span class="hm-txt">' + cuerpo + '</span>' +
    '<span class="hm-fl">Ver tu semana ' + icon("arrow", 12) + '</span>';
  m.hidden = false;
}

function renderHoy(){
  renderHoyMini();
  var caja = document.getElementById("hoy");
  if(!caja || typeof Plan === "undefined" || !hayPlan()) return;''')

# ------------------------------------------------ 4. como se ve
CSS = u'''
/* El renglon de hoy, en el hero. La agenda entera esta mas abajo:
   esto es lo que uno mira todos los dias, y tiene que verse sin
   scrollear. */
.hoy-mini{
  display:flex; align-items:center; gap:14px; margin-top:26px;
  padding:14px 18px; border-radius:var(--r-lg); text-decoration:none;
  background:var(--surface); border:1px solid var(--accent-line);
  box-shadow:var(--shadow-md);
}
.hoy-mini[hidden]{ display:none; }
.hoy-mini:hover{ border-color:var(--accent); }
.hm-ico{
  display:grid; place-items:center; flex-shrink:0;
  width:38px; height:38px; border-radius:var(--r-md);
  background:var(--accent-soft); color:var(--accent-strong);
}
.hm-ico svg{ width:22px; height:22px; }
.hm-txt{ display:flex; flex-direction:column; gap:2px; min-width:0; }
.hm-txt b{ font-size:15px; letter-spacing:-.01em; color:var(--text); }
.hm-txt span{
  font-size:12.5px; color:var(--text-2);
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.hm-fl{
  margin-left:auto; flex-shrink:0;
  display:inline-flex; align-items:center; gap:7px;
  font-size:12.5px; font-weight:750; color:var(--accent);
}
.hoy-mini:hover .hm-fl{ gap:10px; }
@media (max-width:560px){
  .hm-fl span, .hm-fl{ font-size:0; }
  .hm-fl svg{ width:14px; height:14px; }
}
'''
cambiar(u"\n</style>", CSS + u"\n</style>")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: la agenda sube, y lo de hoy va en el hero")
