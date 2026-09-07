# -*- coding: utf-8 -*-
"""No se puede pasar de un paso sin haber hecho lo que pide.

   Los pasos que piden una accion tenian un boton que decia "Ya elegi"
   o "Ya lo cargue" y avanzaba te lo hubieras hecho o no. Apretandolo
   sin haber cargado el CV, la guia seguia adelante y los pasos
   siguientes hablaban de algo que no existia: el recorrido se cortaba
   solo.

   Ahora cada paso que pide algo declara como se sabe si esta hecho.
   Si no lo esta, el boton no avanza: dice que falta. Y como desde el
   arreglo anterior las acciones adelantan el paso solas, el boton en
   esos pasos ya casi no hace falta; queda para decir que falta.

   Uso: python build-guia-pide.py
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


# ------------------------------------------------ 1. guia.js: que pide cada paso
parchar("guia.js", [
 (u'''      accion: "Ya elegí",
      lleva: "",
      ancla: "#puestos"''',
  u'''      accion: "Ya elegí",
      lleva: "",
      ancla: "#puestos",
      pide: "puesto"''', 1),

 (u'''  function retomar(id){''',
  u'''  /* Lo que falta para poder pasar de este paso, o null si no falta
     nada. Los pasos que solo explican algo no piden nada.

     Sin esto el boton avanzaba igual: apretabas "Ya lo cargue" sin
     haber cargado nada y los pasos siguientes hablaban de algo que no
     existia. */
  function falta(p){
    if(!p || !p.pide) return null;
    if(typeof Onb === "undefined") return null;
    Onb.cargar();
    if(p.pide === "puesto"){
      return Onb.estado.puesto ? null : "Elige un puesto para seguir.";
    }
    if(p.pide === "cv"){
      var hay = !!(Onb.estado.cv && Onb.estado.cv.replace(/\\s/g, "").length >= 30) ||
                Object.keys(Onb.estado.respuestas || {}).length >= 2;
      return hay ? null : "Pega tu CV o contesta las preguntas para seguir.";
    }
    if(p.pide === "ruta"){
      return Onb.estado.hecho ? null : "Guarda la ruta para seguir.";
    }
    if(p.pide === "semana"){
      return Onb.estado.semanaLista ? null : "Reparte tu semana para seguir.";
    }
    return null;
  }

  function retomar(id){''', 1),

 (u'    actual: actual, tocaAca: tocaAca, donde: donde, proximoCurso: proximoCurso,',
  u'    actual: actual, tocaAca: tocaAca, donde: donde, proximoCurso: proximoCurso,\n'
  u'    falta: falta,', 1),
])

# los otros tres pasos que piden algo
import re
p = os.path.join(D, "guia.js")
t = io.open(p, encoding="utf-8").read()
for ancla, pide in [(u'ancla: "#cvZona"', "cv"),
                    (u'ancla: "#guardarRuta"', "ruta"),
                    (u'ancla: ".plan-form"', "semana")]:
    if t.count(ancla) != 1:
        print(u"  ABORTA: %s aparece %d veces" % (ancla, t.count(ancla)))
        sys.exit(1)
    t = t.replace(ancla, ancla + u',\n      pide: "%s"' % pide, 1)
io.open(p, "w", encoding="utf-8", newline="").write(t)
print(u"%-22s 3 pasos mas con condicion" % "guia.js")

# ------------------------------------------------ 2. las paginas: el boton mira
VIEJO_BOTON = u"""  document.getElementById("chinB").onclick = function(){
    Guia.avanzar();
    var dest = p.lleva || (p.dobles ? Guia.proximoCurso() : "");
    if(dest){ location.href = dest; return; }
    pintarGuia();
  };"""

NUEVO_BOTON = u"""  /* Si el paso pide una accion y no esta hecha, el boton no avanza:
     dice que falta. Antes avanzaba igual y el recorrido se cortaba
     solo unos pasos despues, hablando de algo que no existia. */
  var pendiente = Guia.falta ? Guia.falta(p) : null;
  var bot = document.getElementById("chinB");
  bot.classList.toggle("chin-b-flojo", !!pendiente);
  bot.title = pendiente || "";
  bot.onclick = function(){
    var f = Guia.falta ? Guia.falta(p) : null;
    if(f){ toast(f); return; }
    Guia.avanzar();
    var dest = p.lleva || (p.dobles ? Guia.proximoCurso() : "");
    if(dest){ location.href = dest; return; }
    pintarGuia();
  };"""

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    ruta = os.path.join(D, a)
    t = io.open(ruta, encoding="utf-8").read()
    if "chin-b-flojo" in t or VIEJO_BOTON not in t:
        continue
    if t.count(VIEJO_BOTON) != 1:
        print(u"  ABORTA en %s: el ancla del boton aparece %d veces" % (a, t.count(VIEJO_BOTON)))
        sys.exit(1)
    io.open(ruta, "w", encoding="utf-8", newline="").write(t.replace(VIEJO_BOTON, NUEVO_BOTON, 1))
    n += 1
print(u"%-22s %d paginas" % ("el boton", n))

# ------------------------------------------------ 3. el estilo del boton flojo
parchar("chinchilla.css", [
 (u".chin-x{", u""".chin-b-flojo{
  opacity:.55;
  /* Se deja clickeable a proposito: apretarlo dice que falta, que es
     mas util que un boton muerto que no explica nada. */
}
.chin-x{""", 1),
])
