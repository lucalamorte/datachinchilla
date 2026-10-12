# -*- coding: utf-8 -*-
u"""Cada ruta, su propio cajon. Nueve compartian uno.

   ai-fundamentos, airflow, claude, fullstack, funcional, mlops, nube,
   testing y visualizacion guardaban el avance en la MISMA clave, en
   los dos lados:

     perfil      p.aifund
     anonimo     "aifund-path/v1/anon"

   Las ocho ultimas son copias de ai-fundamentos a las que se les
   cambio todo menos esto. Es la quinta vez que una pagina copiada se
   trae algo de la original -MI_RUTA, MI_CLAVE, la insignia de
   Anthropic, "las quince partes"- y la primera que corrompe datos en
   vez de mentir en un texto.

   QUE PASABA. Marcabas un curso en Testing y aparecia marcado en
   MLOps, en Nube y en las otras seis. Peor: al abrir otra de las
   nueve, su saveState pisaba el cajon con lo suyo. El avance de ocho
   rutas se venia perdiendo entre si.

   LA MIGRACION. El avance que ya existe se reparte por los ids de
   cada ruta: los de Airflow empiezan con g, los de MLOps con m, los
   de Nube con n. Seis de las nueve se separan sin ninguna duda.

   Tres comparten prefijo -ai-fundamentos, fullstack y funcional usan
   f01, f02...- y ahi no hay forma de saber de cual vino cada marca.
   Esas tres se quedan cada una con todas las f*, que es exactamente
   lo que las tres muestran HOY: el dia de la migracion nadie ve
   cambiar nada, y a partir de ahi van por separado. Es la unica
   opcion que no inventa ni pierde.

   Corre una sola vez por ruta y deja su marca.

   Uso: python build-claves-propias.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

# Las ocho que estaban de prestado. ai-fundamentos se queda con la
# clave: es la suya, y asi no tiene nada que migrar.
PRESTADAS = ["airflow", "claude", "fullstack", "funcional",
             "mlops", "nube", "testing", "visualizacion"]

MIGRACION = u'''
/* El avance que estaba en el cajon compartido.

   Esta pagina guardaba en p.aifund y en "aifund-path/v1/anon", igual
   que otras ocho: es una copia de ai-fundamentos a la que se le
   cambio todo menos eso. Marcabas un curso aca y aparecia marcado en
   las otras, y la que abrias despues pisaba el cajon con lo suyo.

   Se rescata lo que es de esta ruta mirando los ids de sus propios
   nodos, y se deja donde corresponde. Corre una sola vez.

   Lo viejo no se borra: ai-fundamentos sigue siendo el dueno de esa
   clave y lo necesita. */
function migrarDelCajonCompartido(p){
  var MARCA = "%(clave)s-path/v1/migrado";
  if(safeGet(MARCA)) return;
  safeSet(MARCA, "1");

  var mios = {}, i;
  for(i=0;i<NODES.length;i++) mios[NODES[i].id] = true;
  function soloMios(d){
    var o = {}, k;
    for(k in (d || {})){ if(mios[k] && d[k]) o[k] = true; }
    return o;
  }

  var dePerfil = (p && p.aifund && p.aifund.done) || null;
  var deAnon = null;
  try{
    var raw = safeGet("aifund-path/v1/anon");
    deAnon = raw ? (JSON.parse(raw) || {}).done : null;
  }catch(e){ deAnon = null; }

  var mezcla = PathSync.union(soloMios(dePerfil), soloMios(deAnon));
  var cuantas = 0, z;
  for(z in mezcla) cuantas++;
  if(!cuantas) return;

  if(p){ p.%(clave)s = { done: mezcla }; PathSync.store.save(); }
  else safeSet(STORAGE.anon, JSON.stringify({ done: mezcla }));
}
'''

n = 0
for clave in PRESTADAS:
    archivo = {"visualizacion": "visualizacion.html"}.get(clave, clave + ".html")
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        print(u"  ABORTA: no encuentro %s" % archivo); sys.exit(1)
    t = io.open(p, encoding="utf-8").read()
    if u"migrarDelCajonCompartido" in t:
        print(u"  %s: ya estaba" % archivo); continue

    # 1. la clave del perfil
    antes = t
    t = t.replace(u"p.aifund = cs;", u"p.%s = cs;" % clave)
    t = t.replace(u"p.aifund && typeof p.aifund", u"p.%s && typeof p.%s" % (clave, clave))
    t = t.replace(u"cs = { done: p.aifund.done || {} };",
                  u"cs = { done: p.%s.done || {} };" % clave)
    if t == antes:
        print(u"  ABORTA en %s: no encontre la clave del perfil" % archivo); sys.exit(1)

    # 2. la clave anonima
    if u'"aifund-path/v1/anon"' not in t:
        print(u"  ABORTA en %s: no encontre la clave anonima" % archivo); sys.exit(1)
    t = t.replace(u'"aifund-path/v1/anon"', u'"%s-path/v1/anon"' % clave, 1)

    # 3. la migracion, y su llamada
    t = t.replace(u"function loadState(){",
                  (MIGRACION % {"clave": clave}) + u"\nfunction loadState(){", 1)
    if t.count(u"  var p = activeProfile();\n") < 1:
        print(u"  ABORTA en %s: no encontre donde llamarla" % archivo); sys.exit(1)
    t = t.replace(u"  var p = activeProfile();\n",
                  u"  var p = activeProfile();\n  migrarDelCajonCompartido(p);\n", 1)

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d rutas con su propio cajon, y su migracion" % n)
