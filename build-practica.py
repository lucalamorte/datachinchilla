# -*- coding: utf-8 -*-
"""practica.html: la lista de problemas con tu avance.

   Se compone desde semana.html, que ya trae cabecera, pie, panel de
   cuenta y tema.

   La idea: el enunciado se lee en LeetCode o StrataScratch, y el
   casillero vive aca. Es lo unico que falta hoy para que practicar
   deje de ser una sucesion de links sueltos.
"""
import io, sys, hashlib

D = u"C:/Users/Luca/Desktop/snowflake path/"


def uno(t, a, b, q):
    if t.count(a) != 1:
        print("  ABORTA [%s]: %d veces" % (q, t.count(a)))
        sys.exit(1)
    return t.replace(a, b)


t = io.open(D + u"semana.html", encoding="utf-8").read()

# --------------------------------------------------------------- colores
t = uno(t, u"""  --accent:        #0D7A5F;
  --accent-strong: #0A6650;
  --accent-soft:   #E9F7F2;
  --accent-line:   #B0E0D0;""",
           u"""  --accent:        #B91C4A;
  --accent-strong: #9F1239;
  --accent-soft:   #FDF0F4;
  --accent-line:   #F4CBD8;""", "claro")
t = uno(t, u"""  --accent:        #34D399;
  --accent-strong: #6EE7B7;
  --accent-soft:   #06291F;
  --accent-line:   #12483A;""",
           u"""  --accent:        #FB7185;
  --accent-strong: #FDA4AF;
  --accent-soft:   #2C0A14;
  --accent-line:   #4C1526;""", "oscuro")

# ------------------------------------------------------------------- css
CSS = u"""
/* --- La practica: los problemas y tu avance --------------------- */
.bancos{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
  gap:12px; margin-bottom:26px; }
.banco{
  display:flex; flex-direction:column; gap:9px; text-align:left;
  padding:16px 18px; border-radius:var(--r-lg); cursor:pointer;
  background:var(--surface); border:1.5px solid var(--divider);
  font:inherit; color:inherit;
  transition:border-color 160ms ease, background 160ms ease;
}
.banco:hover{ border-color:var(--accent); }
.banco[aria-pressed="true"]{ border-color:var(--accent); background:var(--accent-soft); }
.banco .cab{ display:flex; align-items:baseline; gap:10px; }
.banco b{ font-size:16px; letter-spacing:-.01em; }
.banco .n{ margin-left:auto; font-size:12.5px; color:var(--text-3);
  font-variant-numeric:tabular-nums; white-space:nowrap; }
.banco .d{ font-size:12.5px; color:var(--text-2); line-height:1.5; }
.barra{ height:5px; border-radius:3px; background:var(--surface-sunk); overflow:hidden; }
.barra i{ display:block; height:100%; background:var(--accent);
  transition:width 260ms ease; }

.filtros{ display:flex; gap:8px; flex-wrap:wrap; align-items:center;
  margin-bottom:16px; }
.filtro{
  padding:6px 13px; border-radius:var(--r-pill); cursor:pointer;
  background:var(--surface); border:1px solid var(--divider);
  font:inherit; font-size:12.5px; font-weight:650; color:var(--text-2);
}
.filtro:hover{ border-color:var(--accent); }
.filtro[aria-pressed="true"]{
  background:var(--accent-soft); border-color:var(--accent); color:var(--accent-strong);
}
.filtro .c{ opacity:.6; margin-left:5px; font-variant-numeric:tabular-nums; }
#qProb{
  flex:1 1 180px; min-width:150px; padding:8px 13px;
  border-radius:var(--r-pill); background:var(--surface-sunk);
  border:1px solid var(--divider); font:inherit; font-size:13px; color:var(--text);
}
#qProb:focus{ outline:2px solid var(--accent); outline-offset:1px; }

.probs{ list-style:none; margin:0; padding:0;
  border:1px solid var(--divider); border-radius:var(--r-lg);
  background:var(--surface); overflow:hidden; }
.probs li{ display:flex; align-items:center; gap:0;
  border-top:1px solid var(--divider-soft); }
.probs li:first-child{ border-top:0; }
.probs li.ok{ background:var(--accent-soft); }
.tilde{
  flex:none; display:grid; place-items:center; width:46px; height:46px;
  background:none; border:0; cursor:pointer; color:var(--text-3);
}
.tilde .caja{
  width:19px; height:19px; border-radius:5px; display:grid; place-items:center;
  border:1.5px solid var(--divider); color:transparent;
}
.tilde:hover .caja{ border-color:var(--accent); }
li.ok .tilde .caja{ background:var(--accent); border-color:var(--accent); color:#fff; }
.prob{
  flex:1; display:flex; align-items:center; gap:12px; min-width:0;
  padding:11px 14px 11px 0; text-decoration:none; color:inherit;
}
.prob .t{ flex:1; min-width:0; font-size:14px; font-weight:600;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
li.ok .prob .t{ color:var(--text-3); }
.prob .pat{ flex:none; font-size:11px; color:var(--text-3); }
.prob .dif{
  flex:none; padding:2px 8px; border-radius:var(--r-pill);
  font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:.04em;
}
.dif.facil{ background:var(--good-soft); color:var(--good); }
.dif.medio{ background:var(--warn-soft); color:var(--warn); }
.dif.dificil{ background:var(--bad-soft); color:var(--bad); }
.prob .ir{ flex:none; color:var(--text-3); display:flex; }
.prob:hover .ir{ color:var(--accent); }
.prob:hover .t{ color:var(--accent); }
.vacio{ padding:26px; text-align:center; color:var(--text-3); font-size:13.5px; }
.prox{
  display:flex; align-items:center; gap:14px; flex-wrap:wrap;
  padding:15px 18px; border-radius:var(--r-lg); margin-bottom:22px;
  background:var(--accent-soft); border:1px solid var(--accent-line);
}
.prox .et{ font-size:11px; font-weight:800; letter-spacing:.08em;
  text-transform:uppercase; color:var(--accent-strong); }
.prox .t{ flex:1; font-size:15px; font-weight:700; min-width:150px; }
.prox .hoy{ font-size:12.5px; color:var(--text-2); }
@media (max-width:560px){
  .prob .pat{ display:none; }
}
"""
t = uno(t, u"\n</style>", CSS + u"\n</style>", "css")

# ------------------------------------------------------------------ hero
t = uno(t, u'<p class="lema">Decidir cansa más que estudiar</p>',
           u'<p class="lema">Dos por día alcanzan</p>', "lema")
t = uno(t, u'<h1>Tu <span class="grad">semana</span></h1>',
           u'<h1>La <span class="grad">práctica</span></h1>', "h1")
t = uno(t, u"Con todas las rutas cargadas, el problema deja de ser el material y pasa a ser saber qué hacer un martes a las siete. Dime cuánto tiempo tienes y a qué apuntas, y te queda la semana escrita: qué día, cuánto rato y qué exactamente.",
           u"Los enunciados son de LeetCode y de StrataScratch, y ahí se leen. Lo que falta allá es saber por dónde vas: cuáles hiciste, cuáles te faltan y cuál conviene ahora. Eso vive acá.",
        "lead")

# -------------------------------------------------------------- secciones
CUERPO = u"""<section class="section" id="config">
  <div class="wrap">
    <div class="bancos" id="bancos"></div>
    <div class="prox" id="prox" hidden></div>

    <div class="filtros" id="filtros"></div>
    <div class="filtros" id="patrones"></div>

    <ul class="probs" id="probs"></ul>
    <p class="hero-foot" style="margin-top:18px" id="pieBanco"></p>
  </div>
</section>
"""
ini = t.index(u'<section class="section" id="config">')
fin = t.index(u'<footer class="foot">')
t = t[:ini] + CUERPO + u"\n" + t[fin:]

# --------------------------------------------------------------- scripts
for nombre in (u"problemas.js", u"practica.js"):
    h = hashlib.md5(io.open(D + nombre, "rb").read()).hexdigest()[:8]
    t = uno(t, u'<script src="plan.js',
            u'<script src="%s?v=%s"></script>\n<script src="plan.js' % (nombre, h),
            u"script " + nombre)

# ------------------------------------- el bloque del planificador, por el nuevo
ini = t.index(u"/* ============================================================\n   EL PLAN")
fin = t.index(u"/* ============================================================\n   ARRANQUE")
JS = u'''/* ============================================================
   LA PRACTICA \\u00b7 la lista, los filtros y tu avance
   ============================================================ */
var bancoActual = "blind75";
var fDif = "todo";
var fPat = "todo";
var fEstado = "pendientes";
var busca = "";

function pintarBancos(){
  var h = "", i;
  var bs = Practica.bancos();
  for(i=0;i<bs.length;i++){
    var b = bs[i], a = Practica.avance(b.id);
    var pc = a.total ? Math.round(100 * a.hechos / a.total) : 0;
    h += '<button class="banco" type="button" data-banco="' + b.id + '" ' +
      'aria-pressed="' + (b.id === bancoActual) + '">' +
      '<span class="cab"><b>' + esc(b.nombre) + '</b>' +
        '<span class="n">' + a.hechos + " de " + a.total + '</span></span>' +
      '<span class="barra"><i style="width:' + pc + '%"></i></span>' +
      '<span class="d">' + esc(b.d) + '</span></button>';
  }
  var c = document.getElementById("bancos");
  c.innerHTML = h;
  var bt = c.querySelectorAll("[data-banco]"), j;
  for(j=0;j<bt.length;j++){
    bt[j].addEventListener("click", function(){
      bancoActual = this.getAttribute("data-banco");
      fPat = "todo";
      pintarTodo();
    });
  }
}

/* El que sigue, arriba de todo: la pregunta que uno se hace al
   entrar es "cual hago ahora", no "cuales hay". */
function pintarProximo(){
  var caja = document.getElementById("prox");
  var s = Practica.siguiente(bancoActual);
  if(!s){ caja.hidden = true; return; }
  caja.hidden = false;
  var hoy = Practica.hoyCuantos(bancoActual);
  var falta = Practica.POR_DIA - hoy;
  caja.innerHTML =
    '<span class="et">Empez\\u00e1 por</span>' +
    '<span class="t">' + (s.n ? s.n + ". " : "") + esc(s.t) + '</span>' +
    '<span class="hoy">' + (falta > 0
      ? "Hoy llevas " + hoy + " de " + Practica.POR_DIA
      : "Hoy ya cuenta como practicado") + '</span>' +
    '<a class="btn-primary" href="' + esc(s.u) + '" target="_blank" rel="noopener">' +
      '<span class="stack"><span class="verb">Abrir en</span>' +
      '<span class="dest">' + esc(Practica.bancoDe(bancoActual).fuente) + '</span></span></a>';
}

function pintarFiltros(){
  var b = Practica.bancoDe(bancoActual), i;
  var mapa = { todo: b.items.length, facil: 0, medio: 0, dificil: 0 };
  for(i=0;i<b.items.length;i++) mapa[b.items[i].d]++;

  var DIF = [["todo", "Todos"], ["facil", "F\\u00e1ciles"],
             ["medio", "Medios"], ["dificil", "Dif\\u00edciles"]];
  var h = "", k;
  for(k=0;k<DIF.length;k++){
    h += '<button class="filtro" type="button" data-dif="' + DIF[k][0] + '" ' +
      'aria-pressed="' + (fDif === DIF[k][0]) + '">' + DIF[k][1] +
      '<span class="c">' + mapa[DIF[k][0]] + '</span></button>';
  }
  h += '<button class="filtro" type="button" data-est="pendientes" ' +
       'aria-pressed="' + (fEstado === "pendientes") + '">Por hacer</button>';
  h += '<button class="filtro" type="button" data-est="todo" ' +
       'aria-pressed="' + (fEstado === "todo") + '">Todos</button>';
  h += '<input type="search" id="qProb" placeholder="Buscar" value="' + esc(busca) + '">';
  document.getElementById("filtros").innerHTML = h;

  /* Los patrones solo tienen sentido en el banco de algoritmos: el
     de SQL es todo el mismo patron. */
  var pats = {}, orden = [];
  for(i=0;i<b.items.length;i++){
    var p = b.items[i].p;
    if(!pats[p]){ pats[p] = 0; orden.push(p); }
    pats[p]++;
  }
  var ph = "";
  if(orden.length > 1){
    ph = '<button class="filtro" type="button" data-pat="todo" ' +
         'aria-pressed="' + (fPat === "todo") + '">Todo patr\\u00f3n</button>';
    for(i=0;i<orden.length;i++){
      ph += '<button class="filtro" type="button" data-pat="' + esc(orden[i]) + '" ' +
        'aria-pressed="' + (fPat === orden[i]) + '">' + esc(orden[i]) +
        '<span class="c">' + pats[orden[i]] + '</span></button>';
    }
  }
  document.getElementById("patrones").innerHTML = ph;

  engancharFiltros();
}

function engancharFiltros(){
  var i, b;
  b = document.querySelectorAll("[data-dif]");
  for(i=0;i<b.length;i++) b[i].addEventListener("click", function(){
    fDif = this.getAttribute("data-dif"); pintarTodo();
  });
  b = document.querySelectorAll("[data-est]");
  for(i=0;i<b.length;i++) b[i].addEventListener("click", function(){
    fEstado = this.getAttribute("data-est"); pintarTodo();
  });
  b = document.querySelectorAll("[data-pat]");
  for(i=0;i<b.length;i++) b[i].addEventListener("click", function(){
    fPat = this.getAttribute("data-pat"); pintarTodo();
  });
  var q = document.getElementById("qProb");
  if(q) q.addEventListener("input", function(){
    busca = this.value.toLowerCase(); pintarLista();
  });
}

function pasaProb(x){
  if(fDif !== "todo" && x.d !== fDif) return false;
  if(fPat !== "todo" && x.p !== fPat) return false;
  if(fEstado === "pendientes" && Practica.hecho(bancoActual, x)) return false;
  if(busca){
    var s = ((x.n ? x.n + " " : "") + x.t + " " + x.p + " " + (x.co || "")).toLowerCase();
    if(s.indexOf(busca) < 0) return false;
  }
  return true;
}

function pintarLista(){
  var lista = Practica.ordenados(bancoActual), h = "", i, n = 0;
  for(i=0;i<lista.length;i++){
    var x = lista[i];
    if(!pasaProb(x)) continue;
    n++;
    var ok = Practica.hecho(bancoActual, x);
    h += '<li' + (ok ? ' class="ok"' : '') + ' data-k="' + esc(Practica.clave(bancoActual, x)) + '">' +
      '<button class="tilde" type="button" aria-pressed="' + ok + '" ' +
        'title="' + (ok ? "Marcar como no hecho" : "Marcar como hecho") + '">' +
        '<span class="caja">' + icon("check", 12) + '</span></button>' +
      '<a class="prob" href="' + esc(x.u) + '" target="_blank" rel="noopener">' +
        '<span class="t">' + (x.n ? x.n + ". " : "") + esc(x.t) + '</span>' +
        '<span class="pat">' + esc(x.co || x.p) + '</span>' +
        '<span class="dif ' + x.d + '">' + x.d + '</span>' +
        '<span class="ir">' + icon("open", 12) + '</span>' +
      '</a></li>';
  }
  var c = document.getElementById("probs");
  c.innerHTML = h || '<li><p class="vacio">' +
    (fEstado === "pendientes" ? "Ninguno pendiente con esos filtros. Cambi\\u00e1 a Todos para ver los hechos."
                              : "Ninguno coincide.") + '</p></li>';

  var bt = c.querySelectorAll(".tilde"), j;
  for(j=0;j<bt.length;j++){
    bt[j].addEventListener("click", function(){
      var k = this.parentNode.getAttribute("data-k");
      var lista2 = Practica.bancoDe(bancoActual).items, z;
      for(z=0;z<lista2.length;z++){
        if(Practica.clave(bancoActual, lista2[z]) === k){
          var v = Practica.marcar(bancoActual, lista2[z]);
          toast(v ? "Marcado. " + Practica.hoyCuantos(bancoActual) + " hoy."
                  : "Desmarcado.");
          break;
        }
      }
      pintarTodo();
    });
  }
}

function pintarPie(){
  var b = Practica.bancoDe(bancoActual);
  document.getElementById("pieBanco").innerHTML =
    "Los enunciados son de " + esc(b.fuente) + " y se leen ah\\u00ed. " +
    "Ac\\u00e1 solo vive la lista y tu avance. " +
    '<a href="' + esc(b.url) + '" target="_blank" rel="noopener">Ver el set completo en ' +
    esc(b.fuente) + "</a>.";
}

function pintarTodo(){
  pintarBancos();
  pintarProximo();
  pintarFiltros();
  pintarLista();
  pintarPie();
}

'''
t = t[:ini] + JS + t[fin:]

# ------------------------------------------------- el arranque de la pagina
t = uno(t, u"""  cargarPlan();
  pintarObjetivo();
  pintarDias();
  pintarSemana();""", u"  pintarTodo();", "arranque")

import re
t = re.sub(r"\n *document\.getElementById\(\"(objetivo|horas)\"\)\.addEventListener\("
           r"[\s\S]*?\n *\}\);", "", t)

io.open(D + u"practica.html", "w", encoding="utf-8", newline="").write(t)
print(u"practica.html escrito (%.1f KB)" % (len(t) / 1024.0))
