# -*- coding: utf-8 -*-
u"""No preguntar lo que el CV ya contesto.

   Las cinco preguntas salen siempre, aunque el CV las haya contestado
   todas. A alguien que escribio "senior developer" le preguntabamos
   si programa; a quien puso "dashboards en Power BI", si trabajo con
   datos para que otro decida.

   Preguntar algo que la persona acaba de escribir dos renglones mas
   arriba dice que no lo leimos. Y son cinco pasos mas en un flujo que
   ya tiene cinco.

   Cada pregunta declara sobre que tema es. Si el CV -no las
   respuestas, el CV- ya deja ese tema en nivel 2 o mas, la pregunta
   no se hace. Nivel 2 es el piso de "esto lo usaste", que es
   justamente lo que la pregunta viene a averiguar.

   Las que quedan se numeran sobre las que quedan: "1 de 3", no "1 de
   5" con dos saltadas en el medio.

   Si el CV las contesta todas no queda ninguna, y esta bien: la
   seccion se esconde y el paso del recorrido se saltea solo.

   Uso: python build-preguntas-que-faltan.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# =========================================================== onboarding.js
P = os.path.join(D, "onboarding.js")
t = io.open(P, encoding="utf-8").read()
if u"preguntasQueFaltan" in t:
    print(u"  ya estaba"); sys.exit(1)

# --- 1. cada pregunta dice sobre que es
for viejo, nuevo in [
 (u'''    { id: "prog", texto: "¿Programas?",''',
  u'''    /* `sobre` es el tema que la pregunta averigua. Si el CV ya lo deja
       en nivel 2 -que es el piso de "esto lo usaste"- la pregunta no
       se hace: preguntarle a alguien que escribio "senior developer"
       si programa dice que no lo leimos. */
    { id: "prog", sobre: "prog", texto: "¿Programas?",'''),
 (u'''    { id: "pantalla", texto:''', u'''    { id: "pantalla", sobre: "web", texto:'''),
 (u'''    { id: "servidor", texto:''', u'''    { id: "servidor", sobre: "backend", texto:'''),
 (u'''    { id: "datos", texto:''',    u'''    { id: "datos", sobre: "viz", texto:'''),
 (u'''    { id: "nube", texto:''',     u'''    { id: "nube", sobre: "cloud", texto:'''),
]:
    t = cambiar(t, viejo, nuevo, u"el tema de una pregunta", "onboarding.js")

# --- 2. la funcion que las filtra
t = cambiar(t,
u'''  function temasDeRespuestas(resp){''',
u'''  /* Las que el CV no contesto.

     Mira el CV y no estado.temas, que ya trae mezcladas las
     respuestas: filtrando por ahi, contestar una pregunta hacia
     desaparecer la siguiente. */
  function preguntasQueFaltan(){
    var delCv = {};
    try{
      if(typeof CV !== "undefined" && estado.cv) delCv = CV.leer(estado.cv) || {};
    }catch(e){ delCv = {}; }
    var out = [], i, p;
    for(i=0;i<PREGUNTAS.length;i++){
      p = PREGUNTAS[i];
      if(p.sobre && delCv[p.sobre] && delCv[p.sobre].nivel >= 2) continue;
      out.push(p);
    }
    return out;
  }

  function temasDeRespuestas(){''',
u"la funcion", "onboarding.js")

t = cambiar(t,
u'''    PREGUNTAS: PREGUNTAS,''',
u'''    PREGUNTAS: PREGUNTAS, preguntasQueFaltan: preguntasQueFaltan,''',
u"la exportacion", "onboarding.js")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"onboarding.js: cada pregunta dice sobre que tema es")


# =============================================================== cv.html
C = os.path.join(D, "cv.html")
c = io.open(C, encoding="utf-8").read()

c = cambiar(c,
u'''  var lista = Onb.PREGUNTAS, n = lista.length;''',
u'''  /* Solo las que el CV no contesto, y numeradas sobre esas: "1 de 3",
     no "1 de 5" con dos saltadas en el medio. */
  var lista = Onb.preguntasQueFaltan(), n = lista.length;

  /* Si el CV las contesto todas no queda ninguna, y esta bien: la
     seccion entera se esconde en vez de mostrar una caja vacia. */
  var paso = document.getElementById("pasoPreg");
  if(paso) paso.hidden = !n;
  if(!n){ c.innerHTML = ""; return; }''',
u"la lista filtrada", "cv.html")

c = cambiar(c,
u'''function pregPrimeraSinContestar(){
  var l = Onb.PREGUNTAS, i;''',
u'''function pregPrimeraSinContestar(){
  var l = Onb.preguntasQueFaltan(), i;''',
u"la primera sin contestar", "cv.html")

io.open(C, "w", encoding="utf-8", newline="").write(c)
print(u"cv.html: se pintan solo las que faltan")
