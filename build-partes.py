# -*- coding: utf-8 -*-
u""""Parte 1 de 40" era mentira, no solo feo.

   El planificador parte cada paso en bloques de noventa minutos y los
   numera. Con un paso de cincuenta horas eso da cuarenta bloques, y
   la agenda decia "CS50 Scratch - parte 1 de 34".

   Pero el problema de fondo no es el numero grande. Es que el numero
   no avanza: armar() recalcula la semana desde cero cada vez, a
   partir de los pasos que faltan, y adentro de un paso no hay nada
   guardado. Asi que el lunes siguiente vuelve a decir "parte 1", y el
   otro tambien, hasta que marques el paso entero -cincuenta horas-
   como hecho. Once semanas diciendo "parte 1 de 34".

   Numerar solo se puede cuando el paso entra en la semana: ahi las
   partes son de verdad la 1, la 2 y la 3, y la semana que viene el
   paso ya no esta. Cuando no entra, el numero se cae y en su lugar va
   el tamano del paso, que es el dato que a esa persona le falta:
   estas adentro de un curso de cincuenta horas, no de una leccion.

   Lo que esto NO arregla: que CS50 tenga pasos de cincuenta horas.
   Eso se arregla partiendolos por su estructura real -CS50x tiene
   diez semanas publicadas- y es trabajo de contenido, no de codigo.
   Queda anotado.

   Uso: python build-partes.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "plan.js")

VIEJO = u'''  function repartirEstudio(minutos, ruta){
    var pend = pendientesDe(ruta), bloques = [], i;
    var paso = pend[0], usadoDelPaso = 0, parte = 1, partesDe = {}, resto = minutos, idx = 0;

    for(i=0;i<pend.length;i++){ partesDe[pend[i].id] = Math.ceil(pend[i].min / MAX_BLOQUE); }

    while(resto >= 30 && paso){
      var libreEnPaso = paso.min - usadoDelPaso;
      var dura = Math.min(MAX_BLOQUE, libreEnPaso, resto);
      if(dura < 20) dura = Math.min(20, resto);
      bloques.push({
        tipo: "estudio", min: dura, id: paso.id,
        qué: paso.t + (partesDe[paso.id] > 1 ? " · parte " + parte + " de " + partesDe[paso.id] : ""),
        url: ruta.archivo
      });
      resto -= dura;
      usadoDelPaso += dura;
      parte++;
      if(usadoDelPaso >= paso.min){ idx++; paso = pend[idx]; usadoDelPaso = 0; parte = 1; }
    }
    return bloques;
  }'''

NUEVO = u'''  /* Cuánto dura algo, en palabras cortas. Para decir el tamaño de un
     paso que no entra en la semana. */
  function tamano(min){
    var h = Math.round(min / 60);
    if(h < 1) return min + " min";
    return h + (h === 1 ? " hora" : " horas");
  }

  function repartirEstudio(minutos, ruta){
    var pend = pendientesDe(ruta), bloques = [], i;
    var paso = pend[0], usadoDelPaso = 0, parte = 1, partesDe = {}, resto = minutos, idx = 0;

    /* Numerar las partes sólo cuando el paso entra en la semana.

       Antes se numeraba siempre, contra el total del paso, y con un
       paso de cincuenta horas eso daba "parte 1 de 34". El número
       grande era lo de menos: el problema es que no avanzaba. armar()
       rehace la semana desde cero cada vez -a partir de los pasos que
       faltan- y adentro de un paso no hay nada guardado, así que el
       lunes siguiente volvía a decir "parte 1", y el otro también,
       hasta marcar el paso entero como hecho. Once semanas diciendo
       lo mismo, y diciéndolo mal.

       Si el paso entra en la semana, las partes son de verdad la 1,
       la 2 y la 3, y la semana que viene el paso ya no está. */
    for(i=0;i<pend.length;i++){
      partesDe[pend[i].id] = (pend[i].min <= minutos)
        ? Math.ceil(pend[i].min / MAX_BLOQUE) : 0;
    }

    while(resto >= 30 && paso){
      var libreEnPaso = paso.min - usadoDelPaso;
      var dura = Math.min(MAX_BLOQUE, libreEnPaso, resto);
      if(dura < 20) dura = Math.min(20, resto);
      /* Y cuando no entra, en vez del número va el tamaño del paso,
         que es el dato que falta: estás adentro de un curso de
         cincuenta horas, no de una lección que se termina hoy. */
      var cola = partesDe[paso.id] > 1
        ? " · parte " + parte + " de " + partesDe[paso.id]
        : (partesDe[paso.id] === 0 ? " · de " + tamano(paso.min) : "");
      bloques.push({
        tipo: "estudio", min: dura, id: paso.id,
        qué: paso.t + cola,
        url: ruta.archivo
      });
      resto -= dura;
      usadoDelPaso += dura;
      parte++;
      if(usadoDelPaso >= paso.min){ idx++; paso = pend[idx]; usadoDelPaso = 0; parte = 1; }
    }
    return bloques;
  }'''

t = io.open(P, encoding="utf-8").read()
if "function tamano" in t:
    print(u"  ya estaba"); sys.exit(1)
if t.count(VIEJO) != 1:
    print(u"  ABORTA: repartirEstudio aparece %d veces" % t.count(VIEJO)); sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
print(u"plan.js: las partes se numeran solo cuando son ciertas")
