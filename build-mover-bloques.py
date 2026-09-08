# -*- coding: utf-8 -*-
u"""Mover los bloques de la semana a mano.

   El repartidor decide en que dia va cada bloque: cronologico y
   espaciado, que es un buen criterio y esta explicado en la pagina.
   Pero es el unico, y hay cosas que el no sabe: que los martes tenes
   gimnasia, que el jueves llegas tarde, que preferis el bloque largo
   el sabado.

   El problema tecnico es que armar() rehace la semana entera cada vez
   -a partir de los pasos que faltan, los dias y las horas- y no
   guarda nada de la distribucion. Asi que no alcanza con mover un
   nodo en el DOM: al recargar vuelve a su lugar.

   Cada bloque recibe una CLAVE estable, que sobrevive a que la semana
   se rehaga:

     estudio    e:<id del paso>:<numero de parte>
     practica   p:<dia para el que se genero>
     repaso     r

   Y `estado.movidos` guarda, por clave, a que dia lo mandaste.
   armar() reparte como siempre y despues aplica esos movimientos. Lo
   que no tiene movimiento queda donde el repartidor lo puso.

   Las claves que ya no existen -porque terminaste ese paso- se
   limpian solas: aplicar un movimiento de algo que no esta no hace
   nada, y al guardar se podan.

   La portada no necesita ningun cambio: lee la misma armar().

   Uso: python build-mover-bloques.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# ================================================================ plan.js
P = os.path.join(D, "plan.js")
t = io.open(P, encoding="utf-8").read()
if u"movidos" in t:
    print(u"  ya estaba"); sys.exit(1)

t = cambiar(t,
u'''  var estado = { ruta: "sqlpy", horas: 6, dias: [0,1,2,3,4] };''',
u'''  /* `movidos` es lo unico que guarda algo sobre la distribucion:
     por clave de bloque, a que dia lo mandaste a mano. El resto lo
     decide el repartidor cada vez. */
  var estado = { ruta: "sqlpy", horas: 6, dias: [0,1,2,3,4], movidos: {} };''',
u"el estado", "plan.js")

t = cambiar(t,
u'''      if(Object.prototype.toString.call(crudo.dias) === "[object Array]") estado.dias = crudo.dias;''',
u'''      if(Object.prototype.toString.call(crudo.dias) === "[object Array]") estado.dias = crudo.dias;
      if(crudo.movidos && typeof crudo.movidos === "object") estado.movidos = crudo.movidos;''',
u"la carga", "plan.js")

# --- la parte, en el bloque y no solo en el texto
t = cambiar(t,
u'''      bloques.push({
        tipo: "estudio", min: dura, id: paso.id,
        qué: paso.t + cola,
        url: ruta.archivo
      });''',
u'''      bloques.push({
        tipo: "estudio", min: dura, id: paso.id,
        /* La parte, como dato y no solo adentro del texto: es la
           mitad de la clave con la que se recuerda a donde lo
           moviste. */
        parte: parte,
        qué: paso.t + cola,
        url: ruta.archivo
      });''',
u"el bloque de estudio", "plan.js")

# --- la clave y los movimientos
t = cambiar(t,
u'''    if(repaso){
      semana[dias[dias.length - 1]].bloques.push({
        tipo: "repaso", min: MIN_REPASO,
        qué: "Rehacer lo que fallaste",
        url: "index.html#rutina"
      });
    }
    return { semana: semana, ruta: ruta, rutas: lista, practica: practica,''',
u'''    if(repaso){
      semana[dias[dias.length - 1]].bloques.push({
        tipo: "repaso", min: MIN_REPASO,
        qué: "Rehacer lo que fallaste",
        url: "index.html#rutina"
      });
    }

    /* La clave de cada bloque, y despues los que moviste a mano.

       Tiene que ser estable entre semanas: armar() rehace todo desde
       cero, asi que una clave por posicion no sirve. La de estudio es
       el paso mas la parte; la de practica, el dia para el que se
       genero -son intercambiables entre si-; la de repaso, una sola.

       Los movimientos se aplican DESPUES de repartir, no en vez de:
       lo que no moviste sigue donde el repartidor lo puso, y si
       manana cambias los dias o las horas, eso se reacomoda solo. */
    for(d=0;d<7;d++){
      for(b=0;b<semana[d].bloques.length;b++){
        var bq = semana[d].bloques[b];
        bq.clave = bq.tipo === "estudio" ? ("e:" + bq.id + ":" + bq.parte)
                 : bq.tipo === "practica" ? ("p:" + d)
                 : "r";
      }
    }

    var sueltos = [], destino;
    for(d=0;d<7;d++){
      for(b=semana[d].bloques.length-1;b>=0;b--){
        destino = estado.movidos[semana[d].bloques[b].clave];
        if(destino === undefined || destino === d) continue;
        if(destino < 0 || destino > 6) continue;
        sueltos.push({ a: destino, bloque: semana[d].bloques.splice(b, 1)[0] });
      }
    }
    for(b=0;b<sueltos.length;b++){
      semana[sueltos[b].a].bloques.push(sueltos[b].bloque);
    }

    /* Y en cada dia, la practica primero: es corta y es la que se
       hace todos los dias. Sin esto, un bloque movido caia al final y
       el dia quedaba con el orden al reves de los demas. */
    for(d=0;d<7;d++){
      semana[d].bloques.sort(function(x, y){
        var o = { practica: 0, estudio: 1, repaso: 2 };
        return o[x.tipo] - o[y.tipo];
      });
    }

    return { semana: semana, ruta: ruta, rutas: lista, practica: practica,''',
u"las claves y los movimientos", "plan.js")

# --- mover y volver al orden sugerido
t = cambiar(t,
u'''  /* Lunes = 0, que es como está armada la semana. */''',
u'''  /* Mover un bloque a otro dia, y volver a como estaba.

     Se poda al guardar: una clave de un paso que ya terminaste no
     tiene a que aplicarse, y dejarla ahi solo hace crecer el estado
     para siempre. */
  function mover(clave, dia){
    if(!clave || dia < 0 || dia > 6) return false;
    estado.movidos[clave] = dia;
    podar();
    guardar();
    return true;
  }

  function sinMover(){
    estado.movidos = {};
    guardar();
    return true;
  }

  function hayMovidos(){
    var k;
    for(k in estado.movidos) return true;
    return false;
  }

  function podar(){
    var vivas = {}, r, d, b;
    /* Sin movidos, para no podar mirando el resultado de podar. */
    var guardados = estado.movidos;
    estado.movidos = {};
    r = armar();
    estado.movidos = guardados;
    for(d=0;d<7;d++){
      for(b=0;b<r.semana[d].bloques.length;b++) vivas[r.semana[d].bloques[b].clave] = true;
    }
    var k;
    for(k in estado.movidos){ if(!vivas[k]) delete estado.movidos[k]; }
  }

  /* Lunes = 0, que es como está armada la semana. */''',
u"mover", "plan.js")

t = cambiar(t,
u'''    armar: armar, hoy: hoy, deHoy: deHoy''',
u'''    armar: armar, hoy: hoy, deHoy: deHoy,
    mover: mover, sinMover: sinMover, hayMovidos: hayMovidos''',
u"la exportacion", "plan.js")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"plan.js: cada bloque tiene clave, y se puede mover de dia")
