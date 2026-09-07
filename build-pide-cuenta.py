# -*- coding: utf-8 -*-
"""Marcar avance pide cuenta.

   Se podian marcar problemas y cursos sin estar logueado: el avance
   se guardaba en un perfil local que nace solo, y quedaba atado a ese
   navegador. Cambiabas de maquina y no estaba.

   El candado va en los dos lugares donde de verdad se escribe, no en
   cada boton: Practica.marcar() para los problemas y ensureLocal()
   para los cursos. Poniendolo en los botones habria que acordarse en
   cada uno nuevo, y ya paso con los botones que se agregaron despues.

   Leer sigue abierto: las rutas, los problemas y el catalogo se ven
   sin cuenta. Lo que pide cuenta es guardar.

   Uso: python build-pide-cuenta.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios, silencio=False):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r aparece %d veces, esperaba %d"
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    if not silencio:
        print(u"%-22s %d cambios" % (archivo, len(cambios)))


# ---------------------------------------------- 1. path-sync: quien puede guardar
parchar("path-sync.js", [
 (u"    isOn: function(){ return !!(cfg.url && cfg.key); },\n"
  u"    session: function(){ return ses; },",

  u"    isOn: function(){ return !!(cfg.url && cfg.key); },\n"
  u"    session: function(){ return ses; },\n\n"
  u"    /* Guardar avance pide cuenta. Un unico lugar que lo diga, para\n"
  u"       que no haya dos ideas distintas de que significa estar\n"
  u"       logueado repartidas por las paginas. */\n"
  u"    puedeGuardar: function(){ return !!ses; },", 1),
])

# ---------------------------------------------- 2. practica: el candado
parchar("practica.js", [
 (u"""  function marcar(banco, item, valor){
    var mapa = leer(), k = clave(banco, item);""",

  u"""  function marcar(banco, item, valor){
    /* Sin cuenta no se marca. Va aca y no en los botones porque hay
       dos lugares que marcan -la lista de practica y la tarjeta de la
       portada- y el que se agregue manana tambien tiene que quedar
       tapado sin que nadie se acuerde. */
    if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()){
      return { hecho: false, cerroElDia: false, sinCuenta: true };
    }
    var mapa = leer(), k = clave(banco, item);""", 1),
])

# ---------------------------------------------- 3. los dos botones que marcan
parchar("practica.html", [
 (u"""          var r = Practica.marcar(bancoActual, lista2[z]);
          if(r.cerroElDia && typeof Chin !== "undefined"){""",

  u"""          var r = Practica.marcar(bancoActual, lista2[z]);
          if(r.sinCuenta){ pedirCuenta(); break; }
          if(r.cerroElDia && typeof Chin !== "undefined"){""", 1),
])

parchar("index.html", [
 (u"""      var r = Practica.marcar(id, s, true);
      if(r.cerroElDia && typeof Chin !== "undefined"){""",

  u"""      var r = Practica.marcar(id, s, true);
      if(r.sinCuenta){ pedirCuenta(); return; }
      if(r.cerroElDia && typeof Chin !== "undefined"){""", 1),
])

# ---------------------------------------------- 4. los cursos, en cada ruta
VIEJO_TOGGLE = u"""function toggleDone(id){
  if(!activeProfile()) ensureLocal();"""
NUEVO_TOGGLE = u"""function toggleDone(id){
  /* Sin cuenta no se marca. Antes ensureLocal() creaba un perfil
     local sin que nadie lo pidiera y el avance quedaba atado a este
     navegador: cambiabas de maquina y no estaba. */
  if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()){
    pedirCuenta();
    return;
  }
  if(!activeProfile()) ensureLocal();"""

# la funcion que abre el cartel, una por pagina
PEDIR = u"""
/* Un solo lugar donde se pide la cuenta, con el porque adelante. */
function pedirCuenta(){
  toast("Para guardar tu avance hace falta una cuenta.");
  try{ openAccount(); }catch(e){}
}
"""

n_toggle, n_pedir = 0, 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "function pedirCuenta" in t:
        continue
    if "function openAccount" not in t:
        continue

    if VIEJO_TOGGLE in t:
        t = t.replace(VIEJO_TOGGLE, NUEVO_TOGGLE, 1)
        n_toggle += 1
    if "pedirCuenta(" not in t:
        continue          # esta pagina no marca nada, no hace falta

    # la funcion, justo antes de openAccount
    m = t.index("function openAccount")
    ini = t.rfind("\n", 0, m)
    t = t[:ini] + PEDIR + t[ini:]
    n_pedir += 1
    io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"%-22s %d rutas con el candado, %d paginas con el cartel"
      % ("las paginas", n_toggle, n_pedir))
