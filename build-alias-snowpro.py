# -*- coding: utf-8 -*-
u"""La ruta de SnowPro cambio de id y se llevaba puestas las guardadas.

   Al derivar la lista de rutas de pasos.js, cada ruta paso a llamarse
   como su clave ahi. Diecisis quedaron igual, pero snowpro.html tiene
   la clave "__suelto__" -es la ruta vieja, la que guarda el avance
   suelto en el perfil-, asi que sus piezas pasaron de "snowpro:xxx" a
   "__suelto__:xxx".

   Una ruta armada a mano guarda los ids con los que se guardo, y
   normalizar() descarta en silencio la pieza que ya no esta en el
   catalogo. O sea: a quien tenia una ruta armada con niveles de
   SnowPro, esos niveles le desaparecian sin aviso.

   Entra un mapa de ids viejos. Lo emite build-catalog.py, que es
   quien construye los ids, y lo aplican los dos que leen rutas
   guardadas: el armador -que ademas las vuelve a guardar ya
   traducidas- y la portada, para contar bien las horas.

   La portada no carga catalog.js -78 kB por un mapa de una entrada-,
   asi que ahi el mapa va escrito. cuentas.py comprueba que los dos
   digan lo mismo.

   Uso: python build-alias-snowpro.py
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


# ------------------------------------------------- 1. lo emite el generador
parchar("build-catalog.py", [
 (u'''# los campos que necesita el armador, nada más''',
  u'''# Ids de ruta que cambiaron de nombre, viejo -> nuevo. Una ruta
# armada a mano guarda los ids con los que se guardo, asi que sin esto
# sus piezas se descartan en silencio al abrirla.
#
# snowpro estaba escrito a mano cuando la lista era a mano. Al pasar a
# salir de pasos.js quedo con la clave que usa esa pagina, que es
# "__suelto__" porque es la ruta vieja, la que guarda el avance suelto
# en el perfil. Es un hecho historico: no se deduce de ningun lado y
# no se puede borrar mientras exista una ruta guardada de antes.
ALIAS_VIEJOS = {"snowpro": "__suelto__"}


# los campos que necesita el armador, nada más''', 1),

 (u'''          u"var CATALOGO_RUTAS = " + json.dumps(''',
  u'''          u"/* Ids de ruta que cambiaron. Ver ALIAS_VIEJOS en\\n"
          u"   build-catalog.py: una ruta guardada trae los ids viejos. */\\n"
          u"var CATALOGO_ALIAS = " + json.dumps(ALIAS_VIEJOS, ensure_ascii=False) + u";\\n\\n"
          u"var CATALOGO_RUTAS = " + json.dumps(''', 1),
])

# ------------------------------------------------- 2. el armador lo aplica
parchar("armar.html", [
 (u'''var PORID = {}, PORRUTA = {};''',
  u'''/* Ids de ruta que cambiaron. Lo emite build-catalog.py; acá sólo se
   aplica al leer una ruta guardada, que trae los ids con los que se
   guardó. Sin esto los niveles de SnowPro de una ruta vieja
   desaparecían sin aviso. */
var ALIAS = (typeof CATALOGO_ALIAS !== "undefined") ? CATALOGO_ALIAS : {};
function alDia(id){
  var c = String(id).indexOf(":");
  if(c < 0) return id;
  var r = String(id).slice(0, c);
  return ALIAS[r] ? ALIAS[r] + String(id).slice(c) : id;
}

var PORID = {}, PORRUTA = {};''', 1),

 (u'''      if(PORID[raw.items[i]] && out.items.indexOf(raw.items[i]) < 0) out.items.push(raw.items[i]);''',
  u'''      var pid = alDia(raw.items[i]);
      if(PORID[pid] && out.items.indexOf(pid) < 0) out.items.push(pid);''', 1),

 # el avance guardado viaja con la misma clave vieja
 (u'''  if(raw.done && typeof raw.done === "object") out.done = raw.done;''',
  u'''  if(raw.done && typeof raw.done === "object"){
    /* El avance está guardado con la misma clave vieja que los items:
       traducirlos y dejar el avance atrás sería mostrar la ruta con
       todo sin hacer. */
    for(var d in raw.done){ if(raw.done[d]) out.done[alDia(d)] = true; }
  }''', 1),

 # el link compartido también trae ids de antes
 (u'''    if(PORID[crudos[i]] && out.indexOf(crudos[i]) < 0) out.push(crudos[i]);''',
  u'''    var cid = alDia(crudos[i]);
    if(PORID[cid] && out.indexOf(cid) < 0) out.push(cid);''', 1),
])

# ------------------------------------------------- 3. la portada, para las horas
parchar("index.html", [
 (u'''var PIEZAS_IX = null;
function piezaDe(id){''',
  u'''/* Los ids de ruta que cambiaron. El mapa lo emite build-catalog.py
   en catalog.js, pero la portada no carga catalog.js -78 kB por una
   entrada-, así que acá va escrito. cuentas.py comprueba que digan lo
   mismo. */
var ALIAS_RUTA = { "snowpro": "__suelto__" };

var PIEZAS_IX = null;
function piezaDe(id){''', 1),

 (u'''  return PIEZAS_IX[id] || null;
}''',
  u'''  if(PIEZAS_IX[id]) return PIEZAS_IX[id];
  /* Una ruta guardada trae los ids con los que se guardó. */
  var c = String(id).indexOf(":"), r = c < 0 ? "" : String(id).slice(0, c);
  if(r && ALIAS_RUTA[r]) return PIEZAS_IX[ALIAS_RUTA[r] + String(id).slice(c)] || null;
  return null;
}''', 1),
])

print(u"listo · falta correr build-catalog.py para regenerar catalog.js")
