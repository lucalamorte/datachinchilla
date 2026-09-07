# -*- coding: utf-8 -*-
u"""Que el recorrido te lleve a donde esta, no a donde arranca.

   El arreglo anterior mandaba a la portada y ponia el paso en 1. No
   alcanza, y se ve enseguida con una cuenta que ya tiene avance:

   alDia() empuja el paso hasta donde llegaste de verdad. Si ya
   cargaste el CV, el paso pasa a ser uno de los de /cv. Entonces el
   boton te dejaba en la portada con el recorrido parado en un paso
   que vive en otra pagina, y el globo no se pinta donde el paso no es
   de esa pagina: mismo sintoma que antes, por otro camino.

   Lo correcto es al reves: primero se deja que alDia() diga en que
   paso estas, y despues se va a la pagina de ESE paso. Quien abre el
   recorrido quiere seguirlo, no reiniciarlo.

   Sin nada hecho sigue arrancando en el segundo paso, que es lo que
   se pidio: quien lo abre desde adentro del sitio ya sabe quien es la
   chinchilla.

   De paso, la tabla de "que pagina es cada paso" pasa a vivir en
   guia.js. Estaba escrita en el boton de volver de las veintidos
   paginas, y ademas le faltaba el caso "ruta": el paso del mapa de tu
   ruta no tenia a donde ir, asi que volver desde la semana no hacia
   nada.

   Uso: python build-guia-lleva.py
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
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


V_ABRIR = u'''  function abrir(){
    estado.cerrada = false;
    if(donde() === "index"){
      estado.paso = 0;
      guardar();
      return "";
    }
    estado.paso = 1;
    guardar();
    return "index.html";
  }'''

N_ABRIR = u'''  /* Que pagina le toca a un paso. Estaba escrita en el boton de
     volver de las veintidos paginas, con lo cual eran veintidos
     copias, y a todas les faltaba el caso "ruta": el paso del mapa de
     tu ruta no tenia a donde ir, asi que volver desde la semana no
     hacia nada. */
  function paginaDe(p){
    if(!p) return "";
    if(p.donde === "index")  return "index.html";
    if(p.donde === "cv")     return "cv.html";
    if(p.donde === "semana") return "semana.html";
    if(p.donde === "ruta")   return "mi-ruta.html";
    return "";
  }

  /* A donde ir para ver un paso, o "" si ya estamos donde toca. */
  function llevaA(p){
    if(!p || p.donde === donde()) return "";
    return paginaDe(p);
  }

  function abrir(){
    estado.cerrada = false;
    /* Sin nada hecho arranca en el segundo paso: quien abre el
       recorrido estando adentro del sitio ya sabe quien soy, y
       empezar por la presentacion es empezar por lo unico que ya no
       le hace falta. */
    if(estado.paso < 1) estado.paso = 1;
    /* Y con algo hecho manda alDia(), que sabe hasta donde llegaste.
       Va antes de decidir la pagina y no despues: si no, te dejaba en
       la portada con el paso parado en uno de /cv, y el globo no se
       pinta donde el paso no es de esa pagina. Que es el sintoma que
       esto viene a sacar, otra vez. */
    alDia();
    guardar();
    return llevaA(PASOS[estado.paso]);
  }'''

parchar("guia.js", [
 (V_ABRIR, N_ABRIR, 1),
 (u"    cerrar: cerrar, reabrir: reabrir, abrir: abrir, retomar: retomar",
  u"    cerrar: cerrar, reabrir: reabrir, abrir: abrir, retomar: retomar,\n"
  u"    paginaDe: paginaDe, llevaA: llevaA", 1),
])

# ---- el boton de volver, que tenia su propia copia de la tabla
V_ATRAS = u'''      var aca = Guia.donde();
      /* Cada paso vive en una pagina. Si el anterior no es de esta,
         hay que ir: un globo que habla de algo que no esta en
         pantalla no explica nada. */
      if(previo.donde !== aca){
        var dest = previo.donde === "index" ? "index.html"
                 : previo.donde === "cv" ? "cv.html"
                 : previo.donde === "semana" ? "semana.html" : "";
        if(dest){ location.href = dest; return; }
      }'''

N_ATRAS = u'''      /* Cada paso vive en una pagina. Si el anterior no es de esta,
         hay que ir: un globo que habla de algo que no esta en
         pantalla no explica nada. La tabla vive en guia.js: aca eran
         veintidos copias, y a todas les faltaba el caso "ruta". */
      var dest = Guia.llevaA ? Guia.llevaA(previo) : "";
      if(dest){ location.href = dest; return; }'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if t.count(V_ATRAS) != 1:
        continue
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(V_ATRAS, N_ATRAS, 1))
    n += 1
print(u"%-22s %d con la tabla en un solo lado" % ("el boton de volver", n))
