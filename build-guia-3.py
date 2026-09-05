# -*- coding: utf-8 -*-
"""Tres cosas de la guia, que son la misma cosa vista de tres lados.

   1. Volvia a aparecer despues de cerrarla. El estado se guardaba en
      el perfil cuando habia perfil y en la clave suelta cuando no, y
      si el perfil no estaba activo todavia al cargar la pagina no se
      encontraba ninguno de los dos: la guia arrancaba de cero otra
      vez. Un recorrido guiado es de este navegador, como el saludo
      del dia, asi que se guarda siempre en la clave suelta. El
      perfil se sigue leyendo, para el que ya lo tenga ahi.

   2. Habia que confirmar lo que ya habias hecho. Subias el CV y
      ademas tenias que apretar "Seguir" para decir que lo subiste.
      Ahora cada accion adelanta su paso sola: elegir el puesto,
      pegar el CV, guardar la ruta, repartir la semana. El boton
      queda para los pasos que solo explican algo.

      Para que se note sin recargar, onboarding.js avisa cuando su
      estado cambia y la guia se vuelve a pintar.

   3. Si la cerrabas o la salteabas no habia forma de volver. El
      mensaje decia "la puedes volver a ver desde tu perfil" y en el
      perfil no habia nada. Entra un boton al lado del de tema.

   Uso: python build-guia-3.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios, callar=False):
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
    if not callar:
        print(u"%-22s %d cambios" % (archivo, len(cambios)))


# ============================================================ 1 y 2
parchar("guia.js", [
 # --- el estado vive en este navegador
 (u'''  function cargar(){
    var pf = perfil(), crudo = null;
    if(pf && pf.guia) crudo = pf.guia;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }''',
  u'''  function cargar(){
    /* Primero la clave suelta y despues el perfil, al reves que el
       resto del sitio y a proposito: un recorrido guiado es de este
       navegador, no de quien lo usa. Guardandolo en el perfil, si el
       perfil no estaba activo todavia al cargar la pagina no se
       encontraba nada y la guia volvia a aparecer entera despues de
       haberla cerrado. El perfil se sigue leyendo para el que ya
       tenga su estado ahi. */
    var pf = perfil(), crudo = null;
    try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; }
    if(!crudo && pf && pf.guia) crudo = pf.guia;''', 1),

 (u'''  function guardar(){
    var pf = perfil();
    if(pf){ pf.guia = estado; return PathSync.store.save(); }
    return set(K, JSON.stringify(estado));
  }''',
  u'''  function guardar(){
    /* Siempre en la clave suelta, por lo mismo que cargar(). */
    return set(K, JSON.stringify(estado));
  }''', 1),

 # --- cada accion adelanta su paso
 (u'''    var hayCV = !!(Onb.estado.cv && Onb.estado.cv.replace(/\\s/g, "").length >= 30) ||
                Object.keys(Onb.estado.respuestas || {}).length >= 2;''',
  u'''    var hayPuesto = !!Onb.estado.puesto;
    var hayCV = !!(Onb.estado.cv && Onb.estado.cv.replace(/\\s/g, "").length >= 30) ||
                Object.keys(Onb.estado.respuestas || {}).length >= 2;''', 1),

 (u'''    else if(hayCV && estado.paso < i("leido")) estado.paso = i("leido");
  }''',
  u'''    else if(hayCV && estado.paso < i("leido")) estado.paso = i("leido");
    /* Elegir el puesto ya es haber hecho el paso del puesto: pedir
       ademas que confirme que lo eligio es preguntarle algo que
       acaba de contestar. */
    else if(hayPuesto && estado.paso < i("cargar")) estado.paso = i("cargar");
  }''', 1),
])

# onboarding.js avisa cuando cambia, para que la guia se entere sin recargar
parchar("onboarding.js", [
 (u'''  function guardar(){
    var pf = perfil();
    if(pf){ pf.onb = estado; return PathSync.store.save(); }
    return set(K, JSON.stringify(estado));
  }''',
  u'''  function guardar(){
    var pf = perfil(), ok;
    if(pf){ pf.onb = estado; ok = PathSync.store.save(); }
    else ok = set(K, JSON.stringify(estado));
    /* La guia mira este estado para saber por que paso vas. Sin este
       aviso solo se enteraba al recargar, y por eso habia que
       confirmarle a mano lo que acababas de hacer. */
    try{
      if(typeof document !== "undefined" && document.dispatchEvent){
        document.dispatchEvent(new CustomEvent("onb:cambio"));
      }
    }catch(e){}
    return ok;
  }''', 1),
])

# ============================================================ 3
BOTON = u'''    <button class="icon-btn" id="guiaBtn" type="button" title="Volver a ver la guia paso a paso" aria-label="Ver la guia">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="9"/><path d="M9.6 9.2a2.5 2.5 0 1 1 3.3 2.4c-.6.2-.9.7-.9 1.3v.4"/><path d="M12 17h.01"/>
      </svg>
    </button>
'''

ANCLA_BOTON = u'''    <button class="icon-btn" id="themeBtn" type="button"'''

JS_BOTON = u'''
  /* Volver a ver la guia. El mensaje al cerrarla decia "la puedes
     volver a ver desde tu perfil" y en el perfil no habia nada. */
  var gb = document.getElementById("guiaBtn");
  if(gb && typeof Guia !== "undefined"){
    gb.addEventListener("click", function(){
      Guia.reabrir();
      pintarGuia();
      var c = document.getElementById("chin");
      if(c && !c.hidden && c.scrollIntoView) c.scrollIntoView({ block: "nearest" });
    });
  }
  /* Y que se actualice sola cuando cambia el onboarding, para que las
     acciones adelanten el paso sin apretar nada mas. */
  document.addEventListener("onb:cambio", function(){ pintarGuia(); });
'''

paginas = [a for a in sorted(os.listdir(D))
           if a.endswith(".html") and not a.startswith("_")]

n_boton, n_js, saltadas = 0, 0, []
for a in paginas:
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "pintarGuia" not in t or "themeBtn" not in t:
        saltadas.append(a)
        continue
    if 'id="guiaBtn"' in t:
        continue

    if t.count(ANCLA_BOTON) != 1:
        print(u"  ABORTA en %s: el ancla del boton aparece %d veces"
              % (a, t.count(ANCLA_BOTON)))
        sys.exit(1)
    t = t.replace(ANCLA_BOTON, BOTON + ANCLA_BOTON, 1)
    n_boton += 1

    # el enganche, DESPUES de la ultima llamada a pintarGuia() del init,
    # que es la que corre de verdad. Buscar la primera caia dentro de
    # otra funcion, que es el error que ya cometi dos veces.
    m = None
    for m2 in re.finditer(r"\n(\s*)pintarGuia\(\);", t):
        m = m2
    if not m:
        print(u"  ABORTA en %s: no encuentro donde enganchar" % a)
        sys.exit(1)
    corte = m.end()
    t = t[:corte] + JS_BOTON + t[corte:]
    n_js += 1

    io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"%-22s %d botones, %d enganches" % ("las paginas", n_boton, n_js))
if saltadas:
    print(u"   sin guia, no se tocan: %s" % ", ".join(saltadas))
