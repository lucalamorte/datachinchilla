# -*- coding: utf-8 -*-
u"""La ruta que armaste a mano, anclada junto a la del CV.

   El pedido: "La ruta que armaste vos mismo deberia estar anclada
   junto con la que te arma automatico con el cv. Deberia tener cada
   una su propio color, filtros, etc."

   Hasta ahora la portada solo conocia la del CV. Las armadas a mano
   vivian en /armar y no habia forma de llegar a ellas sin acordarse
   de que esa pagina existe: se guardaban, y desaparecian.

   Tres cosas:

   1. La portada las lee y las ancla al lado de la del CV, con su
      avance. Los datos salen del perfil -o de la clave suelta, si es
      de antes de que hubiera cuenta-, igual que los lee /armar, que
      es donde se escriben.

      Las horas se resuelven con pasos.js, que la portada ya carga.
      Traer catalog.js -78 kB- para sumar minutos seria pagar el
      catalogo entero por una cuenta.

   2. Cada una con su color. El de una ruta armada sale de su propio
      id, asi que es estable y dos rutas distintas no se confunden.
      Se aplica pisando --accent en la tarjeta: las reglas de .card.own
      ya estaban escritas contra ese token, asi que no hay CSS
      duplicado, solo un tono distinto.

   3. Los filtros. Antes las ancladas se escondian con cualquier
      filtro o busqueda, que es justo lo contrario de lo que uno
      espera de lo suyo. Ahora responden a la busqueda por nombre y
      entra un filtro "Tuyas": la del CV, las armadas a mano y las del
      sitio que tengas en tu semana. Los filtros por nivel siguen sin
      mostrarlas, porque una ruta armada a mano no tiene nivel.

   De paso, el icono de la tarjeta del CV: pedia "map", que no existe
   en el juego de la portada, asi que caia en el de por defecto y
   mostraba un tilde.

   Uso: python build-ancla-armadas.py
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
                  % (archivo, viejo[:50], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-18s %d cambios" % (archivo, len(cambios)))


# ============================================================
# 1. index.html
# ============================================================

# --- el icono que faltaba -----------------------------------------
V_ICO = u'''    lock:   '<rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>\''''
N_ICO = u'''    lock:   '<rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    /* La tarjeta de tu ruta lo pedia desde siempre y no estaba: caia
       en el de por defecto y mostraba un tilde. */
    map:    '<path d="M9 4L3 6.5v14L9 18l6 2.5 6-2.5v-14L15 6.5z"/><path d="M9 4v14M15 6.5v14"/>\''''

# --- leer las rutas armadas a mano --------------------------------
V_LEER = u'''function pasaFiltro(p){'''
N_LEER = u'''/* ---------------------------------------------------------------
   LAS RUTAS ARMADAS A MANO

   Se guardan en /armar y hasta ahora se quedaban ahi: la portada no
   las conocia, asi que quien armaba una tenia que acordarse de que
   esa pagina existe para volver a verla.

   Se leen igual que las lee /armar -perfil primero, clave suelta
   despues- porque es el mismo dato y no puede tener dos verdades.
   La clave suelta es lo de antes de que guardar pidiera cuenta.
   --------------------------------------------------------------- */
function armadas(){
  var pf = null, crudo = null, out = [], i, r;
  try{ pf = activeProfile(); }catch(e){ pf = null; }
  if(pf && pf.customs){
    crudo = pf.customs;
  }else{
    try{ crudo = JSON.parse(localStorage.getItem("custom-path/v1/guardadas") || "[]"); }
    catch(e){ crudo = null; }
  }
  if(Object.prototype.toString.call(crudo) !== "[object Array]") return out;
  for(i=0;i<crudo.length;i++){
    r = crudo[i];
    if(!r || !r.id) continue;
    if(Object.prototype.toString.call(r.items) !== "[object Array]" || !r.items.length) continue;
    out.push(r);
  }
  return out;
}

/* "sqlpy:q01" -> el paso, sacado de pasos.js, que la portada ya
   carga. Es lo unico que hace falta para contar niveles y horas de
   una ruta armada: traer catalog.js entero -78 kB- para eso seria
   pagar el catalogo por una cuenta. Se arma una vez. */
var PIEZAS_IX = null;
function piezaDe(id){
  if(!PIEZAS_IX){
    PIEZAS_IX = {};
    var rs = (typeof PASOS !== "undefined") ? PASOS : [], a, b;
    for(a=0;a<rs.length;a++){
      for(b=0;b<rs[a].pasos.length;b++){
        PIEZAS_IX[rs[a].clave + ":" + rs[a].pasos[b].id] = rs[a].pasos[b];
      }
    }
  }
  return PIEZAS_IX[id] || null;
}

/* El color de cada ruta armada. Sale de su id, asi que es el mismo
   siempre y dos rutas distintas no se confunden. Se pisa --accent en
   la tarjeta y listo: las reglas de .card.own ya estan escritas
   contra ese token. */
var TONOS = ["#0F766E", "#B45309", "#9D174D", "#1D4ED8", "#4D7C0F", "#A21CAF"];
function tonoDe(id){
  var n = 0, i;
  for(i=0;i<id.length;i++) n = (n * 31 + id.charCodeAt(i)) % 100003;
  return TONOS[n % TONOS.length];
}

function tarjetaArmada(r){
  var min = 0, hechos = 0, i, pz;
  for(i=0;i<r.items.length;i++){
    pz = piezaDe(r.items[i]);
    if(pz) min += pz.min || 0;
    if(r.done && r.done[r.items[i]]) hechos++;
  }
  var n = r.items.length, hs = Math.round(min / 60);
  var av = hechos > 0
    ? '<span class="card-av"><span class="b"><i style="width:' +
        Math.round(100 * hechos / n) + '%"></i></span>' +
      '<span class="n">' + hechos + " de " + n + '</span></span>'
    : "";
  return '<div class="card-wrap tuya armada" style="--tono:' + tonoDe(r.id) + '">' +
    '<a class="card own" href="armar.html#abrir=' + encodeURIComponent(r.id) + '">' +
      '<span class="own-ribbon">' + icon("build", 11) + 'La armaste tú</span>' +
      '<span class="ico">' + icon("build", 19) + '</span>' +
      '<h3>' + esc(r.name || "Tu ruta a mano") + '</h3>' +
      '<div class="card-tags"><span class="chip">' + n +
        (n === 1 ? ' nivel' : ' niveles') + '</span>' +
        (hs ? '<span class="chip official">' + hs + ' horas</span>' : '') +
      '</div>' + av +
      '<p>La elegiste nivel por nivel. Se edita cuando quieras y el avance queda guardado.</p>' +
      '<span class="go">Abrirla ' + icon("arrow", 12) + '</span></a></div>';
}

/* Las rutas del sitio que tenés en tu semana también son tuyas: el
   filtro "Tuyas" junta las tres cosas, o diría una cosa y mostraría
   otra. */
function enTuSemana(p){
  var clave = claveDe(p);
  return !!(clave && typeof Onb !== "undefined" && Onb.activa(clave));
}

function pasaFiltro(p){
  if(filtroRuta === "tuyas") return enTuSemana(p) && cabeEnBusqueda(p);'''

V_FIN_FILTRO = u'''  if(filtroRuta === "favoritas" && !esFavorita(idRuta(p))) return false;
  if(filtroRuta !== "todo" && filtroRuta !== "favoritas" && p.nivel !== filtroRuta) return false;
  if(!buscaRuta) return true;
  var texto = (p.t + " " + p.d + " " + p.nivel).toLowerCase();
  return texto.indexOf(buscaRuta) >= 0;
}'''
N_FIN_FILTRO = u'''  if(filtroRuta === "favoritas" && !esFavorita(idRuta(p))) return false;
  if(filtroRuta !== "todo" && filtroRuta !== "favoritas" && p.nivel !== filtroRuta) return false;
  return cabeEnBusqueda(p);
}

function cabeEnBusqueda(p){
  if(!buscaRuta) return true;
  var texto = (p.t + " " + p.d + " " + p.nivel).toLowerCase();
  return texto.indexOf(buscaRuta) >= 0;
}'''

# --- el filtro "Tuyas" --------------------------------------------
V_PILL = u'''  if(favs){
    html += '<button class="lib-filter' + (filtroRuta === "favoritas" ? " on" : "") + '" type="button" data-fr="favoritas">' +
            'Favoritas <span class="n">' + favs + '</span></button>';
  }'''
N_PILL = u'''  /* Lo tuyo, junto: la del CV, las que armaste a mano y las del
     sitio que metiste en tu semana. Antes lo tuyo se escondia con
     cualquier filtro, que es lo contrario de lo que uno espera. */
  var tuyas = cuantasTuyas();
  if(tuyas){
    html += '<button class="lib-filter' + (filtroRuta === "tuyas" ? " on" : "") + '" type="button" data-fr="tuyas">' +
            'Tuyas <span class="n">' + tuyas + '</span></button>';
  }
  if(favs){
    html += '<button class="lib-filter' + (filtroRuta === "favoritas" ? " on" : "") + '" type="button" data-fr="favoritas">' +
            'Favoritas <span class="n">' + favs + '</span></button>';
  }'''

V_TOPE = u'''/* Cuántas rutas se ven antes de "ver más". Seis entra en dos filas
   en pantalla ancha y en una tarjeta y media en el teléfono. */'''
N_TOPE = u'''/* Cuántas son tuyas: para el número del filtro. */
function cuantasTuyas(){
  var n = armadas().length, i;
  if(hayRutaDelCV()) n++;
  for(i=0;i<PATHS.length;i++){ if(enTuSemana(PATHS[i])) n++; }
  return n;
}

function hayRutaDelCV(){
  return (typeof Onb !== "undefined") && Onb.hecho() && (typeof CV !== "undefined");
}

/* Cuántas rutas se ven antes de "ver más". Seis entra en dos filas
   en pantalla ancha y en una tarjeta y media en el teléfono. */'''

# --- que las ancladas respondan a filtro y busqueda ----------------
V_TUYA = u'''  /* Tu ruta, primera y aparte: es la única armada para vos. */
  var tuya = "";
  if(hayOnb && !buscaRuta && filtroRuta === "todo" && typeof CV !== "undefined"){'''
N_TUYA = u'''  /* Lo tuyo, primero y aparte. Va en "Todo" y en "Tuyas", y responde
     a la búsqueda por nombre: esconderlo con cualquier filtro era
     justo lo contrario de lo que uno espera de lo suyo. */
  var anclado = (filtroRuta === "todo" || filtroRuta === "tuyas");
  var nAnclas = 0;
  function buscada(nombre){
    return !buscaRuta || String(nombre).toLowerCase().indexOf(buscaRuta) >= 0;
  }

  var tuya = "";
  if(hayOnb && anclado && typeof CV !== "undefined"){'''

V_CIERRA = u'''    tuya = '<div class="card-wrap tuya">' +
      '<a class="card own" href="mi-ruta.html">' +
        '<span class="own-ribbon">' + icon("arrow", 11) + 'Armada para ti</span>' +
        '<span class="ico">' + icon("map", 19) + '</span>' +
        '<h3>' + esc(titulo) + '</h3>' +
        '<div class="card-tags"><span class="chip">' + nCursos + ' cursos</span>' +
          '<span class="chip official">' + Math.round(hs / 60) + ' horas</span></div>' +
        '<p>' + esc(sub) + '</p>' +
        '<span class="go">Abrirla ' + icon("arrow", 12) + '</span></a></div>';
  }'''
N_CIERRA = u'''    if(buscada(titulo)){
      tuya = '<div class="card-wrap tuya">' +
        '<a class="card own" href="mi-ruta.html">' +
          '<span class="own-ribbon">' + icon("arrow", 11) + 'Armada para ti</span>' +
          '<span class="ico">' + icon("map", 19) + '</span>' +
          '<h3>' + esc(titulo) + '</h3>' +
          '<div class="card-tags"><span class="chip">' + nCursos + ' cursos</span>' +
            '<span class="chip official">' + Math.round(hs / 60) + ' horas</span></div>' +
          '<p>' + esc(sub) + '</p>' +
          '<span class="go">Abrirla ' + icon("arrow", 12) + '</span></a></div>';
      nAnclas++;
    }
  }

  /* Las que armaste a mano, al lado de la del CV. */
  if(anclado){
    var ar = armadas(), w;
    for(w=0;w<ar.length;w++){
      if(!buscada(ar[w].name || "")) continue;
      tuya += tarjetaArmada(ar[w]);
      nAnclas++;
    }
  }'''

V_CUPO = u'''  /* La tuya ocupa un lugar de la grilla, así que cuenta para el tope:
     si no, quedaban siete tarjetas y una sola en la última fila. */
  var propia = hayOnb && !buscaRuta && filtroRuta === "todo";
  var cupo = TOPE_RUTAS - (propia ? 1 : 0);'''
N_CUPO = u'''  /* Las tuyas ocupan lugares de la grilla, así que cuentan para el
     tope: si no, quedaban siete tarjetas y una sola en la última
     fila. */
  var cupo = TOPE_RUTAS - nAnclas;
  if(cupo < 2) cupo = 2;'''

V_VACIO = u'''  vacio.hidden = lista.length > 0;
  if(!lista.length && typeof Chin !== "undefined"){'''
N_VACIO = u'''  vacio.hidden = (lista.length + nAnclas) > 0;
  if(!lista.length && !nAnclas && typeof Chin !== "undefined"){'''

CSS = u'''
/* Cada ruta armada a mano con su color. El tono sale de su id y se
   aplica pisando --accent acá: las reglas de .card.own ya están
   escritas contra ese token, así que no hay una segunda tarjeta que
   mantener, sólo un tono distinto.

   Los cuatro se derivan de uno para que el degradado y el borde no
   queden peleados: mezclar contra --surface los deja bien en los dos
   temas. */
.card-wrap.armada{
  --accent:        var(--tono);
  --accent-strong: color-mix(in srgb, var(--tono) 82%, #000000);
  --accent-soft:   color-mix(in srgb, var(--tono) 13%, var(--surface));
  --accent-line:   color-mix(in srgb, var(--tono) 32%, var(--surface));
}
/* En oscuro el tono entero queda ilegible sobre el fondo: se aclara,
   igual que hace el tema con su propio acento. */
:root[data-theme="dark"] .card-wrap.armada{
  --accent:        color-mix(in srgb, var(--tono) 52%, #FFFFFF);
  --accent-strong: color-mix(in srgb, var(--tono) 30%, #FFFFFF);
  --accent-soft:   color-mix(in srgb, var(--tono) 32%, var(--surface));
  --accent-line:   color-mix(in srgb, var(--tono) 48%, var(--surface));
}
'''

parchar("index.html", [
    (V_ICO, N_ICO, 1),
    (V_LEER, N_LEER, 1),
    (V_FIN_FILTRO, N_FIN_FILTRO, 1),
    (V_PILL, N_PILL, 1),
    (V_TOPE, N_TOPE, 1),
    (V_TUYA, N_TUYA, 1),
    (V_CIERRA, N_CIERRA, 1),
    (V_CUPO, N_CUPO, 1),
    (V_VACIO, N_VACIO, 1),
    (u"\n</style>", CSS + u"\n</style>", 1),
])

# ============================================================
# 2. armar.html · abrir una guardada desde la portada
# ============================================================
parchar("armar.html", [
    (u'''  if(compartida) ofrecerCompartida(compartida);''',
     u'''  if(compartida) ofrecerCompartida(compartida);

  /* La portada ancla las rutas armadas a mano y linkea con #abrir=.
     Sin esto el link caía en el armador vacío y había que buscarla
     otra vez en la lista de abajo. Reusa abrirGuardada, que ya
     pregunta antes de pisar lo que tenías a medio armar. */
  var pedida = (location.hash || "").indexOf("#abrir=") === 0
             ? decodeURIComponent(location.hash.slice(7)) : "";
  if(pedida) abrirGuardada(pedida);''', 1),
])

# ============================================================
# 3. path-sync.js · que un perfil nuevo se lleve lo armado a mano
# ============================================================
parchar("path-sync.js", [
    (u'''        ["datachinchilla/v1/cursos",     "cursos"]
      ];''',
     u'''        ["datachinchilla/v1/cursos",     "cursos"],
        /* Lo armado a mano antes de tener cuenta. Sin esto, quien
           armó una ruta y después se hizo el perfil la veía
           desaparecer de la portada y del armador: el perfil vacío
           gana sobre la clave suelta. */
        ["custom-path/v1/anon",          "custom"],
        ["custom-path/v1/guardadas",     "customs"]
      ];''', 1),
])

print(u"listo")
