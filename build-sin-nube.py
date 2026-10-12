# -*- coding: utf-8 -*-
u"""Que el sitio funcione sin nube, que es como esta hoy.

   El proyecto de Supabase ya no existe: el dominio ni siquiera
   resuelve. Y como guardar avance pedia sesion -puedeGuardar() es
   `!!ses`- y no puede haber sesion sin servidor, HOY NADIE PUEDE
   MARCAR NADA. Marcas un curso, se abre el cartel de la cuenta, y
   ahi muere.

   path-sync.js lo tenia previsto en su propia cabecera: "Sin claves
   cargadas, PathSync.isOn() devuelve false y ninguna pagina intenta
   nada: siguen funcionando con perfiles locales". Faltaba una sola
   cosa para que eso fuera cierto: puedeGuardar() no miraba si habia
   nube, solo si habia sesion.

   Entonces:

   - Las claves se vacian. Apuntaban a un proyecto borrado, asi que
     cada intento de entrar era una espera y un error. De paso sale
     del codigo la clave que habia que rotar.
   - puedeGuardar() devuelve true cuando no hay nube. Tu avance vive
     en este navegador, que es lo que el cartel de la cuenta viene
     diciendo desde siempre.

   Esto NO es la migracion: es dejar el sitio usable mientras tanto.
   Cuando haya proyecto nuevo, se vuelven a cargar dos valores y la
   nube vuelve a estar, porque el store local sigue siendo la fuente
   y la nube siempre fue una capa encima.

   Uso: python build-sin-nube.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

VIEJO = u'''var CONFIG = {
  supabaseUrl: "https://sscfykrodjnfnnbmkopp.supabase.co",
  supabaseKey: "sb_publishable_t8bH_XUtTPUi9XnEPxJrgQ_9qTsK-m6"
};'''

NUEVO = u'''/* Sin nube, por ahora.

   El proyecto de Supabase que habia aca se borro: el dominio ni
   resuelve. Dejar la direccion puesta no es neutro -cada intento de
   entrar es una espera y un error- asi que se vacia, y con eso
   PathSync.isOn() da false y ninguna pagina intenta nada.

   Tu avance vive en este navegador, que es lo que el cartel de la
   cuenta viene diciendo desde siempre.

   Cuando haya backend nuevo, se cargan estos dos valores y vuelve a
   haber nube: el store local siempre fue la fuente y la nube una capa
   encima, asi que no hay nada que migrar de este lado. */
var CONFIG = {
  supabaseUrl: "",
  supabaseKey: ""
};'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if VIEJO not in t:
        continue
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
    n += 1
print(u"%d paginas sin las claves del proyecto borrado" % n)


# ---------------------------------------------------------- el candado
P = os.path.join(D, "path-sync.js")
t = io.open(P, encoding="utf-8").read()
v = u'''    /* Guardar avance pide cuenta. Un unico lugar que lo diga, para
       que no haya dos ideas distintas de que significa estar
       logueado repartidas por las paginas. */
    puedeGuardar: function(){ return !!ses; },'''
n2 = u'''    /* Guardar avance pide cuenta SI HAY NUBE. Un unico lugar que lo
       diga, para que no haya dos ideas distintas de que significa
       estar logueado repartidas por las paginas.

       Sin nube devuelve true, y no es un parche: la cuenta existe
       para que tu avance te siga a otra computadora. Si no hay a
       donde sincronizar, pedirla no protege nada, solo impide
       guardar. Con el proyecto borrado esto dejaba el sitio sin
       poder marcar un solo curso: marcabas, se abria el cartel de la
       cuenta, y ahi moria. */
    puedeGuardar: function(){ return !cfg.url || !cfg.key || !!ses; },'''
if t.count(v) != 1:
    print(u"  ABORTA: el candado aparece %d veces" % t.count(v)); sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(t.replace(v, n2, 1))
print(u"path-sync.js: sin nube, se guarda igual")
