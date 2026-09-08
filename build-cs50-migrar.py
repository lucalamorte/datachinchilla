# -*- coding: utf-8 -*-
u"""Que partir CS50 no le borre el avance a nadie.

   La ruta pasa de once cursos enteros a treinta y siete pasos, y tres
   de esos cursos se partieron en semanas. Eso cambia los ids: el que
   tenia CS50x marcado como hecho lo tenia guardado como "c02", y c02
   ya no existe.

   Sin esto, a quien termino CS50x -sesenta horas- se le vacia la
   ruta al entrar. Es exactamente lo que paso con SnowPro cuando la
   ruta cambio de clave, y ahi lo encontre de casualidad.

   La traduccion es directa y no pierde nada: si terminaste el curso,
   terminaste sus doce semanas. Se expande una vez, se borra la marca
   vieja y queda guardado.

   Al reves no se puede y no se intenta: alguien que hoy hace la
   semana 3 no tiene "medio c02". Por eso la migracion va en un solo
   sentido y corre una sola vez.

   Uso: python build-cs50-migrar.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cs50.html")

VIEJO = u'''  done = cs.done;
  absorberCompartidos();
}'''

NUEVO = u'''  done = cs.done;
  migrarCursosPartidos();
  absorberCompartidos();
}

/* Los tres cursos que se partieron en semanas.

   La ruta tenia once pasos y cada uno era un curso entero: CS50x son
   sesenta horas. El planificador reparte en bloques de noventa
   minutos, asi que ese paso se partia en cuarenta bloques y no habia
   forma de marcar nada hasta terminarlo todo.

   Harvard publica la estructura -once semanas con nombre propio mas
   el proyecto-, asi que se usa esa. Pero eso cambia los ids, y el que
   ya lo termino lo tenia guardado como "c02".

   Si terminaste el curso, terminaste sus semanas: se expande. Al
   reves no se puede -quien va por la semana 3 no tiene "medio c02"-
   asi que esto va en un solo sentido y corre una sola vez. */
var PARTIDOS = {
  c02: ["x00","x01","x02","x03","x04","x05","x06","x07","x08","x09","x10","x11"],
  c03: ["p00","p01","p02","p03","p04","p05","p06","p07","p08","p09"],
  c04: ["q00","q01","q02","q03","q04","q05","q06"]
};

function migrarCursosPartidos(){
  var toco = false, viejo, i, partes;
  for(viejo in PARTIDOS){
    if(!done[viejo]) continue;
    partes = PARTIDOS[viejo];
    for(i=0;i<partes.length;i++) done[partes[i]] = true;
    delete done[viejo];
    toco = true;
  }
  if(toco) saveState();
}'''

t = io.open(P, encoding="utf-8").read()
if "migrarCursosPartidos" in t:
    print(u"  ya estaba"); sys.exit(1)
if t.count(VIEJO) != 1:
    print(u"  ABORTA: el cargador aparece %d veces" % t.count(VIEJO)); sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
print(u"cs50.html: el avance viejo se expande a las semanas")
