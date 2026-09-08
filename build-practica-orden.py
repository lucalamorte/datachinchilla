# -*- coding: utf-8 -*-
u"""Los ejercicios, de facil a dificil, tambien en la portada.

   practica.js ordena por dificultad desde el principio y lo dice en
   su propio comentario: "empezar por un dificil de programacion
   dinamica es abandonar el primer dia". Esa funcion se llama
   ordenados(), esta exportada, y practica.html la usa.

   La portada no. Recorre b.items, que es el orden en que lo dejo
   build-problemas.py: Blind 75 arranca 128 medio, 1 facil, 3 medio,
   5 medio, 133 medio. O sea que el primer ejercicio que le ofrece el
   sitio a alguien que recien llega es uno medio, y despues sale un
   dificil de la nada. No es al azar, pero se ve igual que al azar, y
   es peor: parece que hay un criterio y no lo hay.

   El arreglo no es reordenar en la portada -eso serian dos ideas
   distintas del orden, y ya se sabe como termina eso-. La lista de
   pendientes se calcula una sola vez, en practica.js, al lado del
   sort del que sale. La portada la pide.

   Se arreglan los dos lugares que la armaban a mano. El segundo es
   el que importa mas de lo que parece: es el que decide cual marcas
   al tocar "Lo resolvi". Con las dos listas en ordenes distintos,
   marcabas uno y se tildaba otro.

   Uso: python build-practica-orden.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo in cambios:
        n = t.count(viejo)
        if n != 1:
            print(u"  ABORTA en %s: %r x%d, esperaba 1"
                  % (archivo, viejo[:50], n))
            sys.exit(1)
        t = t.replace(viejo, nuevo, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-14s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------- 1. una sola lista de pendientes
parchar("practica.js", [
 (u'''  function siguiente(id){
    var lista = ordenados(id), mapa = leer(), i;''',
  u'''  /* Los que te faltan, en el orden en que conviene hacerlos.

     Vivia suelta en la portada, escrita sobre b.items -el orden del
     archivo- mientras aca al lado ordenados() ordenaba por
     dificultad. Dos ideas del orden en el mismo sitio: la portada
     ofrecia un medio primero y un dificil cuarto.

     Y habia una tercera copia, la del boton "Lo resolvi", tambien
     sobre b.items: marcabas el que veias y se tildaba otro. */
  function pendientes(id){
    var lista = ordenados(id), mapa = leer(), out = [], i;
    for(i=0;i<lista.length;i++){
      if(!mapa[clave(id, lista[i])]) out.push(lista[i]);
    }
    return out;
  }

  function siguiente(id){
    var lista = ordenados(id), mapa = leer(), i;'''),

 (u'''    avance: avance, ordenados: ordenados, siguiente: siguiente,''',
  u'''    avance: avance, ordenados: ordenados, siguiente: siguiente,
    pendientes: pendientes,'''),
])

# --------------------------------------------------- 2. la portada la pide
parchar("index.html", [
 (u'''    /* Los que quedan, en orden. Se calcula aca y no en practica.js
       porque es lo unico que hace falta: la lista de pendientes. */
    var pend = [], k;
    for(k=0;k<b.items.length;k++){
      if(!Practica.hecho(b.id, b.items[k])) pend.push(b.items[k]);
    }''',
  u'''    /* Los que quedan, de facil a dificil. Esto se calculaba aca
       sobre b.items, que es el orden del archivo: Blind 75 empieza
       con uno medio y el cuarto es dificil. El orden bueno ya
       existia en practica.js; lo que faltaba era pedirlo. */
    var pend = Practica.pendientes(b.id);'''),

 (u'''      var bb = Practica.bancoDe(id), pp = [], w;
      for(w=0;w<bb.items.length;w++){
        if(!Practica.hecho(id, bb.items[w])) pp.push(bb.items[w]);
      }
      var s = pp[retoEn[id] || 0] || null;''',
  u'''      /* La misma lista que se pinto, no otra armada igual: con una
         en orden de archivo y otra en orden de dificultad, marcabas
         el que veias y se tildaba el que no. */
      var s = Practica.pendientes(id)[retoEn[id] || 0] || null;'''),
])
