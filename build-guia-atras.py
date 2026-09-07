# -*- coding: utf-8 -*-
"""Que el recorrido diga donde estas, y poder volver un paso.

   Dos cosas del mismo pedido:

   1. Al llegar a una pagina nueva, el paso hablaba del siguiente sin
      decir en que pagina te acababa de dejar. El caso peor es el paso
      de la ruta: te lleva al mapa de tu ruta -que es la pantalla mas
      importante del sitio- y el globo arranca hablando de la semana.
      Quien llega ahi por primera vez no sabe que esta mirando.

      Los tres pasos que cambian de pagina ahora abren diciendo donde
      estas y para que sirve, y despues ofrecen lo que sigue.

   2. Volver al paso anterior. Antes solo se podia avanzar o cerrar,
      asi que un clic de mas te dejaba sin forma de releer lo que
      acababas de saltear. El boton vuelve a la pagina del paso
      anterior si es otra: volver sin moverte de pagina mostraria un
      globo hablando de algo que no esta a la vista.

   Uso: python build-guia-atras.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r x%d, esperaba %d" % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------- 1. los textos y retroceder
parchar("guia.js", [
 # el paso de la ruta: decir que es esta pantalla antes de hablar de otra
 (u'''      titulo: "Ahora, cuándo",
      texto: "Ya tienes tu ruta. Ahora te la reparto en la semana: qué día, a qué " +
             "hora y cuánto rato, para que sepas qué hacer un martes a las siete.",''',
  u'''      titulo: "Ésta es tu ruta",
      texto: "Cada tarjeta es un curso, en el orden que conviene, con cuánto lleva " +
             "y qué te deja. Se marcan a medida que los haces y el mapa lleva la " +
             "cuenta. Lo que falta es cuándo: te la reparto en tu semana.",''', 1),

 # el de la semana: idem
 (u'''      titulo: "Tus días y tu rato",
      texto: "Marca los días que vas a tener de verdad y cuánto rato. Con eso te " +
             "reparto la ruta y queda escrito qué hacer cada día.",''',
  u'''      titulo: "Acá se arma tu semana",
      texto: "Marca los días que vas a tener de verdad y cuánto rato. Con eso reparto " +
             "los cursos de tu ruta en bloques concretos, y queda escrito qué hacer " +
             "un martes a las siete.",''', 1),

 # el ultimo: decir que es la portada de vuelta
 (u'''      titulo: "Listo. Elige por dónde",''',
  u'''      titulo: "Listo, ésta es tu portada",''', 1),

 # poder volver
 (u'''  function avanzar(){
    estado.paso++;
    guardar();
  }''',
  u'''  function avanzar(){
    estado.paso++;
    guardar();
  }

  /* Volver un paso. Antes solo se podia avanzar o cerrar, asi que un
     clic de mas te dejaba sin forma de releer lo que salteaste.
     Devuelve el paso al que se llego, para que quien llama sepa a que
     pagina tiene que ir: volver sin moverse mostraria un globo
     hablando de algo que no esta a la vista. */
  function retroceder(){
    if(estado.paso <= 0) return null;
    estado.paso--;
    guardar();
    return PASOS[estado.paso];
  }''', 1),

 (u'    avanzar: avanzar, cerrar: cerrar, reabrir: reabrir, retomar: retomar',
  u'    avanzar: avanzar, retroceder: retroceder,\n'
  u'    cerrar: cerrar, reabrir: reabrir, retomar: retomar', 1),
])

# ------------------------------------------------- 2. el boton, en cada pagina
V_HTML = u'''      <button class="chin-salto" type="button" id="chinSalto">Saltear</button>'''
N_HTML = u'''      <button class="chin-atras" type="button" id="chinAtras" hidden>Atrás</button>
      <button class="chin-salto" type="button" id="chinSalto">Saltear</button>'''

V_JS = u'''  document.getElementById("chinX").onclick = cerrarGuia;'''
N_JS = u'''  /* Volver al paso anterior, y a su pagina si es otra. */
  var atras = document.getElementById("chinAtras");
  if(atras){
    atras.hidden = Guia.estado.paso <= 0;
    atras.onclick = function(){
      var previo = Guia.retroceder();
      if(!previo) return;
      var aca = Guia.donde();
      /* Cada paso vive en una pagina. Si el anterior no es de esta,
         hay que ir: un globo que habla de algo que no esta en
         pantalla no explica nada. */
      if(previo.donde !== aca){
        var dest = previo.donde === "index" ? "index.html"
                 : previo.donde === "cv" ? "cv.html"
                 : previo.donde === "semana" ? "semana.html" : "";
        if(dest){ location.href = dest; return; }
      }
      pintarGuia();
    };
  }
  document.getElementById("chinX").onclick = cerrarGuia;'''

CSS = u'''
/* Volver un paso. Va tenue: es una salida, no el camino. */
.chin-atras{
  border:0; background:none; cursor:pointer; font:inherit;
  font-size:12px; font-weight:700; color:var(--text-3);
  padding:4px 2px; text-decoration:underline;
}
.chin-atras:hover{ color:var(--text-2); }
.chin-atras[hidden]{ display:none; }
'''

n_h, n_j = 0, 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if 'id="chinAtras"' in t or "chinSalto" not in t:
        continue
    if t.count(V_HTML) == 1:
        t = t.replace(V_HTML, N_HTML, 1); n_h += 1
    if t.count(V_JS) == 1:
        t = t.replace(V_JS, N_JS, 1); n_j += 1
    if ".chin-atras{" not in t and "\n</style>" in t:
        t = t.replace("\n</style>", CSS + "\n</style>", 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"%-22s %d botones, %d enganches" % ("las paginas", n_h, n_j))
