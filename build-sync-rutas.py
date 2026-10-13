# -*- coding: utf-8 -*-
u"""Que el avance de las rutas suba y baje de la nube.

   La nube era de una sola direccion: las paginas escribian el perfil
   -el nombre, que app usaste- y nunca lo leian, y las veintidos rutas
   ni siquiera subian el avance. saveState() guardaba en localStorage
   y ahi terminaba.

   O sea que la cuenta no hacia lo unico que promete su propio cartel:
   "Entra con tu mail para llevarlo a otra computadora". Entrabas en
   otra maquina y no habia nada.

   Dos enganches por pagina:

     al cargar   sincronizarRuta baja lo que haya, lo une con lo
                 local, y si trajo algo nuevo se guarda y se repinta.
     al marcar   subirRuta manda lo local, que ahi es lo mas nuevo.

   La union es la regla, y es la que el archivo ya usaba para los
   hitos: lo marcado en cualquier lado queda. El precio es que
   desmarcar en una maquina no se propaga; perder avance es mas caro
   que eso.

   Los dos son best-effort: sin sesion o sin red no hacen nada y el
   avance local sigue igual.

   Uso: python build-sync-rutas.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

BAJAR = u'''
/* Traer de la nube lo que se marco en otra computadora.

   Es lo unico que la cuenta promete -"entra con tu mail para llevarlo
   a otra computadora"- y hasta ahora no pasaba: las rutas guardaban
   en este navegador y nada mas.

   La union es la regla: lo marcado en cualquier lado queda. Desmarcar
   no se propaga, y es barato al lado de perder avance. */
function bajarDeLaNube(){
  if(!window.PathSync || !PathSync.sincronizarRuta || !MI_CLAVE) return;
  PathSync.sincronizarRuta(MI_CLAVE, done).then(function(mezcla){
    if(!mezcla) return;
    cs.done = mezcla;
    done = cs.done;
    saveState();
    renderMap();
    if(typeof pintarMia === "function") pintarMia();
  });
}
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if u"var MI_CLAVE" not in t or u"function saveState()" not in t:
        continue
    if u"bajarDeLaNube" in t:
        print(u"  %s: ya estaba" % a); continue
    if u"function renderMap()" not in t:
        print(u"  %s: sin renderMap, lo salteo" % a); continue

    # 1. la funcion
    t = t.replace(u"function loadState(){", BAJAR + u"\nfunction loadState(){", 1)

    # 2. bajar despues de pintar el mapa por primera vez
    if t.count(u"  renderMap();\n") < 1:
        print(u"  ABORTA en %s: no encuentro renderMap()" % a); sys.exit(1)
    t = t.replace(u"  renderMap();\n", u"  renderMap();\n  bajarDeLaNube();\n", 1)

    # 3. subir al guardar
    m = re.search(r"function saveState\(\)\{\n(.*?)\n\}", t, re.S)
    if not m:
        print(u"  ABORTA en %s: no encuentro saveState" % a); sys.exit(1)
    cuerpo = m.group(1)
    nuevo = (u"function saveState(){\n"
             u"  /* Y arriba, si hay sesion. Va antes del return porque el\n"
             u"     cuerpo de abajo tiene varios: poniendolo despues se\n"
             u"     ejecutaba en un solo camino y el avance subia a veces. */\n"
             u"  if(window.PathSync && PathSync.subirRuta && MI_CLAVE){\n"
             u"    PathSync.subirRuta(MI_CLAVE, done);\n"
             u"  }\n" + cuerpo + u"\n}")
    t = t[:m.start()] + nuevo + t[m.end():]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d rutas sincronizan en los dos sentidos" % n)
