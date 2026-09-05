# -*- coding: utf-8 -*-
"""Los temas y los puestos del desarrollo web.

   El vocabulario del sitio era el de datos: SQL, modelado, pipelines,
   estadistica. Un CV que dice React, Node y TypeScript no encontraba
   una sola senal que lo reconociera, asi que el motor lo leia como si
   no supiera nada y le ofrecia dbt.

   Entran dos temas -el frontend y el backend- y tres puestos que los
   piden. Las pruebas, los contenedores y el CI/CD no necesitan tema
   nuevo: ya existen como "calidad" y "cloud", y partirlos en dos
   habria sido tener el mismo concepto en dos lugares.

   Ademas se toca miNivel() en onboarding.js. La escalera que decidia
   si una ruta te queda grande miraba pipelines, modelado, SQL y
   Python: alguien con diez anos de React daba nivel cero y quedaba
   fuera de su propia ruta.

   Uso: python build-perfiles-web.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r aparece %d veces, esperaba %d"
                  % (archivo, viejo[:50], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


TEMAS_NUEVOS = u''' ("web", u"Desarrollo web",
  ["javascript", "typescript", "react", "angular", "vue", "svelte", "html",
   "css", "frontend", "front-end", "front end", "next.js", "nextjs", "tailwind",
   "jquery", "redux", "sass", "webpack", "vite", "spa", "responsive",
   "react native", "flutter", "bootstrap"],
  ["react", "javascript", "typescript", "frontend", "componente", "hook",
   "next.js", "interfaz", "pantalla", "app web", "react native", "estado que"]),

 ("backend", u"Backend y APIs",
  ["api", "rest", "restful", "graphql", "node", "nodejs", "node.js", "express",
   "backend", "back-end", "back end", "endpoint", "spring", "spring boot",
   ".net", "laravel", "rails", "nestjs", "jwt", "oauth", "autenticacion",
   "microservicios", "http"],
  ["servidor", "express", "node", "api", "graphql", "backend", "endpoint",
   "autenticacion", "usuarios", "rest"]),

'''

PUESTOS_NUEVOS = u'''
 # --- fuera de datos -------------------------------------------------
 # El sitio dice "para trabajar en tech" y hasta aca solo sabia leer
 # curriculums de datos. Estos tres son los primeros que no lo son.
 {"id": "fullstack", "nombre": u"Desarrollador Full Stack",
  "resumen": u"Construir la aplicación entera: la pantalla, el servidor que la alimenta y lo que hace falta para publicarla.",
  "temas": {"web": 3, "backend": 3, "prog": 2, "calidad": 2, "sql": 2,
            "cloud": 2}},

 {"id": "frontend", "nombre": u"Desarrollador Frontend",
  "resumen": u"La parte que la gente toca: que se entienda, que responda y que funcione en cualquier pantalla.",
  "temas": {"web": 3, "prog": 2, "calidad": 2, "backend": 1}},

 {"id": "backend_dev", "nombre": u"Desarrollador Backend",
  "resumen": u"Lo que hay detrás de la pantalla: las APIs, los datos y que aguante cuando entra gente de verdad.",
  "temas": {"backend": 3, "prog": 2, "sql": 2, "calidad": 2, "cloud": 2}},
'''

# ------------------------------------------------------ 1. build-temas.py
parchar("build-temas.py", [
 # los temas nuevos, antes del de web3 que cierra la lista
 (u' ("web3", u"Blockchain y Web3",', TEMAS_NUEVOS + u' ("web3", u"Blockchain y Web3",', 1),

 # que tema ensena cada tramo de la ruta nueva
 (u''' ("claude", 5):       ["llm", "cloud", "mlops"],
}''',
  u''' ("claude", 5):       ["llm", "cloud", "mlops"],
 # Full Stack Open: cada tramo ensena algo distinto y los titulos
 # estan en espanol pero no usan el vocabulario de datos, asi que
 # sin esto los quince pasos caerian en el mismo saco.
 ("fullstack", 1):    ["web", "prog"],
 ("fullstack", 2):    ["backend", "calidad"],
 ("fullstack", 3):    ["web"],
 ("fullstack", 4):    ["web", "backend"],
 ("fullstack", 5):    ["cloud", "backend", "sql"],
}''', 1),

 (u' "web3":         ["web3"],\n}',
  u' "web3":         ["web3"],\n "fullstack":    ["web", "backend"],\n}', 1),

 # los puestos nuevos, al final de la lista
 (u'PUESTOS = [', u'PUESTOS = [' + PUESTOS_NUEVOS, 1),
])

# ---------------------------------------------------- 2. onboarding.js
parchar("onboarding.js", [
 (u'''  function miNivel(){
    var s = estado.temas || {};
    function n(k){ return s[k] ? s[k].nivel : 0; }
    /* Experiencia es haber hecho algo con esto, no haberlo leído:
       pipelines o modelado en serio, o nube que se administra. */
    if(n("pipelines") >= 2 || n("modelado") >= 2 || n("cloud") >= 3) return 3;
    if(n("python") >= 2) return 2;
    if(n("sql") >= 2) return 1;
    return 0;
  }''',
  u'''  function miNivel(){
    var s = estado.temas || {};
    function n(k){ return s[k] ? s[k].nivel : 0; }
    /* Experiencia es haber hecho algo con esto, no haberlo leído:
       pipelines o modelado en serio, o nube que se administra. */
    if(n("pipelines") >= 2 || n("modelado") >= 2 || n("cloud") >= 3) return 3;
    /* Saber programar es saber programar, en el lenguaje que sea.
       Esta escalera era solo de datos, así que alguien con diez años
       de React daba cero y quedaba afuera de su propia ruta: las
       rutas que piden saber programar se le escondían por
       "arranca más arriba de donde estás". */
    if(n("python") >= 2 || n("web") >= 2 || n("backend") >= 2 ||
       n("prog") >= 2) return 2;
    if(n("sql") >= 2) return 1;
    return 0;
  }''', 1),
])

print()
print(u"Ahora: python build-pasos.py && python build-temas.py")
