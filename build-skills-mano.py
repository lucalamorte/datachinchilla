# -*- coding: utf-8 -*-
u"""Agregar a mano lo que el CV no dijo.

   El motor saca los temas del CV y deja sacar con una cruz los que no
   corresponden. Lo simetrico no estaba: si sabes algo que el CV no
   nombra -porque lo aprendiste por tu cuenta, porque el CV esta
   viejo, porque lo escribiste con otras palabras- no habia forma de
   decirlo. Solo se podia restar.

   Entra "agregados", que es el espejo de "sacados":

   - Sacar algo es decir "esto no lo se": el tema se cae entero.
   - Agregarlo es decir "esto si lo se": entra en nivel 3, que es el
     mismo peso que le da un CV que lo nombra tres veces.

   Los dos son la misma clase de dato -lo que la persona corrige sobre
   lo que leyo la maquina- asi que uno deshace al otro: agregar algo
   lo saca de la lista de sacados y al reves. Si no, quedaba un estado
   en el que un tema estaba en las dos listas y ganaba el que
   corriera ultimo.

   Lo agregado tambien pasa por la inferencia. Decir que manejas la
   nube y que igual te ofrezcan los fundamentos de programacion es
   justo lo que la inferencia esta para evitar, y no vale menos
   porque lo dijiste vos en vez de tu CV.

   Uso: python build-skills-mano.py
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
    print(u"%-18s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------- 1. cv.js expone inferir
parchar("cv.js", [
 (u"  return { leer: leer, armar: armar, fuertes: fuertes, leerPDF: leerPDF,",
  u"  return { leer: leer, armar: armar, fuertes: fuertes, leerPDF: leerPDF,\n"
  u"           inferir: inferir, temas: function(){ return TEMAS.temas; },", 1),
])

# ------------------------------------------------- 2. el modelo
parchar("onboarding.js", [
 (u'''  function recalcularTemas(){
    var deResp = temasDeRespuestas(estado.respuestas), k;
    var deCV = (estado.cv && typeof CV !== "undefined") ? CV.leer(estado.cv) : {};
    var out = {};
    for(k in deResp) out[k] = { nivel: deResp[k].nivel, senales: [] };
    for(k in deCV){
      if(!out[k] || deCV[k].nivel > out[k].nivel) out[k] = deCV[k];
    }''',
  u'''  function recalcularTemas(){
    var deResp = temasDeRespuestas(estado.respuestas), k;
    var deCV = (estado.cv && typeof CV !== "undefined") ? CV.leer(estado.cv) : {};
    var out = {};
    for(k in deResp) out[k] = { nivel: deResp[k].nivel, senales: [] };
    for(k in deCV){
      if(!out[k] || deCV[k].nivel > out[k].nivel) out[k] = deCV[k];
    }
    /* Lo que agregaste a mano. Es el espejo de sacar: sacar algo es
       decir "esto no lo sé" y el tema se cae entero, agregarlo es
       decir "esto sí lo sé" y entra en nivel 3, el mismo peso que le
       da un CV que lo nombra tres veces.

       Existe porque el CV no dice todo: lo que aprendiste por tu
       cuenta, lo que hiciste después de la última versión, o lo que
       escribiste con otras palabras. Antes sólo se podía restar. */
    var suma = estado.agregados || [];
    for(var a=0;a<suma.length;a++){
      out[suma[a]] = { nivel: 3, senales: [], aMano: true };
    }
    /* Y pasa por la inferencia, como lo que sale del CV: decir que
       manejas la nube y que igual te ofrezcan los fundamentos de
       programación es justo lo que la inferencia evita, y no vale
       menos porque lo dijiste vos. */
    if(suma.length && typeof CV !== "undefined" && CV.inferir) out = CV.inferir(out);''', 1),

 (u'''  /* Marca un tema como no sabido, o lo devuelve. */
  function sacarTema(clave, sacar){
    if(!estado.sacados) estado.sacados = [];
    var i = estado.sacados.indexOf(clave);
    if(sacar && i < 0) estado.sacados.push(clave);
    if(!sacar && i >= 0) estado.sacados.splice(i, 1);
    recalcularTemas();
    guardar();
  }''',
  u'''  /* Marca un tema como no sabido, o lo devuelve.

     Saca de "agregados" lo que se saca: los dos son la misma clase de
     dato -lo que la persona corrige sobre lo que leyó la máquina- y
     un tema en las dos listas dejaba ganar al que corriera último. */
  function sacarTema(clave, sacar){
    if(!estado.sacados) estado.sacados = [];
    if(!estado.agregados) estado.agregados = [];
    var i = estado.sacados.indexOf(clave);
    if(sacar && i < 0) estado.sacados.push(clave);
    if(!sacar && i >= 0) estado.sacados.splice(i, 1);
    if(sacar){
      var j = estado.agregados.indexOf(clave);
      if(j >= 0) estado.agregados.splice(j, 1);
    }
    recalcularTemas();
    guardar();
  }

  /* Y el espejo: marcarlo como sabido aunque el CV no lo diga. */
  function agregarTema(clave, agregar){
    if(!estado.agregados) estado.agregados = [];
    if(!estado.sacados) estado.sacados = [];
    var i = estado.agregados.indexOf(clave);
    if(agregar && i < 0) estado.agregados.push(clave);
    if(!agregar && i >= 0) estado.agregados.splice(i, 1);
    if(agregar){
      var j = estado.sacados.indexOf(clave);
      if(j >= 0) estado.sacados.splice(j, 1);
    }
    recalcularTemas();
    guardar();
  }''', 1),

 (u"    sacarTema: sacarTema,", u"    sacarTema: sacarTema, agregarTema: agregarTema,", 1),

 # el estado nuevo, declarado donde estan los otros
 (u"""    sacados: [],
    puesto: \"\",""",
  u"""    sacados: [],
    /* Y los que dijiste que si sabes aunque el CV no los nombre. Es
       el espejo de sacados, y por eso vive al lado. */
    agregados: [],
    puesto: \"\",""", 1),
])
