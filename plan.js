/* ============================================================
   plan.js

   El plan semanal: cuántas horas, qué días, qué ruta, y cómo se
   reparte todo eso en bloques.

   Vive acá y no dentro de semana.html porque la portada necesita
   la misma cuenta para decir "hoy toca esto". Dos copias de esta
   lógica serían dos semanas distintas para el mismo usuario.

   Depende de path-sync.js (el perfil) y de pasos.js (las rutas).
   ============================================================ */
var Plan = (function(){
  "use strict";

  var K = "datachinchilla/v1/plan";

  var DIAS       = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
  var DIAS_CORTO = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];

  /* Práctica corta y diaria, bloque largo para lo nuevo, y un repaso
     al final. Los números salen de lo que aguanta la atención, no de
     una cuenta redonda. */
  var MIN_PRACTICA = 25;
  var MIN_REPASO   = 45;
  var MAX_BLOQUE   = 90;
  /* Cuántos bloques de estudio entran en un día. Dos es lo que
     aguanta la cabeza; con más, el día deja de ser un día. */
  var MAX_POR_DIA  = 2;

  /* `movidos` es lo unico que guarda algo sobre la distribucion:
     por clave de bloque, a que dia lo mandaste a mano. El resto lo
     decide el repartidor cada vez. */
  var estado = { ruta: "sqlpy", horas: 6, dias: [0,1,2,3,4], movidos: {} };

  function perfil(){
    try{ return (window.PathSync && PathSync.store) ? PathSync.store.active() : null; }
    catch(e){ return null; }
  }
  function get(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function set(k, v){ try{ localStorage.setItem(k, v); return true; }catch(e){ return false; } }

  function cargar(){
    var pf = perfil(), crudo = null;
    if(pf && pf.plan) crudo = pf.plan;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }
    if(crudo && typeof crudo === "object"){
      if(crudo.ruta)  estado.ruta  = String(crudo.ruta);
      if(crudo.horas) estado.horas = parseInt(crudo.horas, 10) || 6;
      if(Object.prototype.toString.call(crudo.dias) === "[object Array]") estado.dias = crudo.dias;
      if(crudo.movidos && typeof crudo.movidos === "object") estado.movidos = crudo.movidos;
    }
    return estado;
  }

  function guardar(){
    var pf = perfil();
    if(pf){ pf.plan = estado; return PathSync.store.save(); }
    return set(K, JSON.stringify(estado));
  }

  function rutas(){ return (typeof PASOS !== "undefined") ? PASOS : []; }

  /* Las rutas que entran en la semana. Salen del onboarding; si
     todavía no lo hizo, la que tenga elegida a mano. Una sola fuente:
     antes el plan miraba su propia ruta y el onboarding otra cosa, y
     terminar el onboarding no cambiaba la semana. */
  function activas(){
    var out = [], i, r;
    if(typeof Onb !== "undefined"){
      Onb.cargar();
      for(i=0;i<Onb.estado.rutas.length;i++){
        r = rutaDe(Onb.estado.rutas[i]);
        if(r) out.push(r);
      }
    }
    /* Y si no elegiste ninguna, ninguna.

       Aca se devolvia rutaDe(estado.ruta), que arranca en "sqlpy" por
       defecto: alguien que nunca conto nada abria la portada y
       encontraba una semana entera de SQL y Python. Si esa persona
       quiere ser full stack, lo primero que ve el sitio es una semana
       de cosas que no le sirven.

       Estaba puesto para que la agenda no saliera vacia. Pero una
       agenda llena de algo que no elegiste es peor que una vacia: la
       vacia dice la verdad. */
    if(!out.length && estado.ruta && rutaElegidaAMano()){
      r = rutaDe(estado.ruta);
      if(r) out.push(r);
    }
    return out;
  }

  /* Qué conviene practicar a diario, según lo que te falta. Antes
     decía siempre "SQL y algoritmos" aunque ya supieras SQL. */
  /* Que la ruta del plan la hayas elegido vos y no sea el valor con
     el que nace el estado. Se sabe porque quedo guardada: cargar()
     solo la pisa si venia en lo guardado. */
  function rutaElegidaAMano(){
    var pf = perfil(), crudo = null;
    if(pf && pf.plan) crudo = pf.plan;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }
    return !!(crudo && crudo.ruta);
  }

  /* Que practicar sale del PUESTO, no de la nada.

     Antes miraba solo cuanto sabias de SQL y de Python, asi que a
     cualquiera que no supiera ninguno de los dos -o sea a cualquiera
     que recien llega- le ponia "SQL y Python, mezclados" cinco dias
     por semana. A alguien que apunta a full stack eso no le sirve, y
     nadie le pregunto.

     Los dos bancos que hay son consultas SQL y algoritmos. Si el
     puesto no pide ninguna de las dos cosas, no hay practica: es
     mejor una semana con menos que una semana con relleno.

     Y el nombre: el banco de algoritmos esta escrito en Python, pero
     lo que entrena son algoritmos. Decirle "Python" a un full stack
     que programa en JavaScript era describir la herramienta en vez de
     lo que se practica. */
  function quePracticar(){
    var pide = {};
    if(typeof Onb !== "undefined" && typeof CV !== "undefined" && Onb.estado.puesto){
      var pu = CV.puestoDe(Onb.estado.puesto);
      if(pu && pu.temas) pide = pu.temas;
    }
    /* Sin puesto elegido no se adivina: se practica lo que sirve para
       casi cualquier entrevista tecnica, que son los algoritmos. */
    var sinPuesto = !Object.keys(pide).length;

    var quiereSql  = sinPuesto ? false : (pide.sql || 0) >= 2;
    var quiereProg = sinPuesto ? true  : ((pide.python || 0) >= 2 ||
                                          (pide.prog || 0) >= 2 ||
                                          (pide.backend || 0) >= 2 ||
                                          (pide.web || 0) >= 2);
    if(!quiereSql && !quiereProg) return null;

    var sabe = (typeof Onb !== "undefined" && Onb.estado.temas) ? Onb.estado.temas : {};
    var sql = sabe.sql ? sabe.sql.nivel : 0;
    var py  = sabe.python ? sabe.python.nivel : 0;

    if(quiereSql && quiereProg){
      if(sql < 2 && py < 2) return { qué: "SQL y algoritmos, mezclados", b: "ambos" };
      if(sql < 2)           return { qué: "SQL, una o dos consultas", b: "sql" };
      if(py < 2)            return { qué: "Algoritmos, un ejercicio", b: "py" };
      return { qué: "SQL y algoritmos, para no perder la mano", b: "ambos" };
    }
    if(quiereSql) return { qué: "SQL, una o dos consultas", b: "sql" };
    return { qué: "Algoritmos, un ejercicio", b: "py" };
  }

  function rutaDe(clave){
    var rs = rutas(), i;
    for(i=0;i<rs.length;i++){ if(rs[i].clave === clave) return rs[i]; }
    return rs[0] || null;
  }

  /* Lo hecho de una ruta. snowpro guarda suelto en el perfil porque
     fue la primera que existió; el resto usa su propia clave. */
  function hechosDe(ruta){
    var pf = perfil();
    if(!pf || !ruta) return {};
    if(ruta.clave === "__suelto__") return pf.done || {};
    var r = pf[ruta.clave];
    return (r && r.done) ? r.done : {};
  }

  function pendientesDe(ruta){
    if(!ruta) return [];
    var hechos = hechosDe(ruta), out = [], i;
    for(i=0;i<ruta.pasos.length;i++){
      if(!hechos[ruta.pasos[i].id]) out.push(ruta.pasos[i]);
    }
    return out;
  }

  /* Reparte los minutos de estudio sin pasar de MAX_BLOQUE por bloque
     y respetando el orden de los pasos. Un paso largo se parte en
     varias sesiones y lo dice, así nadie abre un curso de seis horas
     pensando que entra en una tarde. */
  /* Cuánto dura algo, en palabras cortas. Para decir el tamaño de un
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
        : (partesDe[paso.id] === 0 ? " · " + tamano(paso.min) + " en total" : "");
      bloques.push({
        tipo: "estudio", min: dura, id: paso.id,
        /* La parte, como dato y no solo adentro del texto: es la
           mitad de la clave con la que se recuerda a donde lo
           moviste. */
        parte: parte,
        qué: paso.t + cola,
        url: ruta.archivo
      });
      resto -= dura;
      usadoDelPaso += dura;
      parte++;
      if(usadoDelPaso >= paso.min){ idx++; paso = pend[idx]; usadoDelPaso = 0; parte = 1; }
    }
    return bloques;
  }

  function armar(){
    var lista = activas();

    /* Sin ruta elegida no se arma nada. Devuelve la semana vacia -los
       siete dias siguen ahi, que es el marco- y avisa por que, para
       que quien la pinte diga la verdad en vez de mostrar bloques de
       algo que nadie pidio. */
    if(!lista.length){
      var vacia = [], v;
      for(v=0;v<7;v++) vacia.push({ dia: v, bloques: [] });
      return { semana: vacia, ruta: null, rutas: [], practica: 0,
               estudio: 0, repaso: 0, practicar: null, sobran: 0,
               sinRuta: true };
    }

    var ruta = lista[0];
    var dias = estado.dias.slice(0).sort(function(a,b){ return a - b; });
    if(!dias.length) dias = [0,1,2,3,4];

    var total    = estado.horas * 60;
    var practicarAntes = quePracticar();
    var practica = practicarAntes ? MIN_PRACTICA * dias.length : 0;
    var repaso   = dias.length >= 3 ? MIN_REPASO : 0;
    var estudio  = Math.max(0, total - practica - repaso);
    var practicar = practicarAntes;

    /* El estudio se reparte entre todas las activas, no en una sola:
       tener tres rutas activas y estudiar siempre la primera era lo
       mismo que tener una. Cada una se lleva su parte y va en orden. */
    var bloquesEstudio = [], cuanto = lista.length ? Math.floor(estudio / lista.length) : estudio;
    for(var z=0;z<lista.length;z++){
      bloquesEstudio = bloquesEstudio.concat(repartirEstudio(cuanto, lista[z]));
    }
    if(!lista.length) bloquesEstudio = repartirEstudio(estudio, ruta);

    /* Y no más de los que entran en la semana. Sin este tope, subir
       las horas apilaba veinte tarjetas en un mismo día. */
    var tope = dias.length * MAX_POR_DIA;
    var sobran = Math.max(0, bloquesEstudio.length - tope);
    if(sobran) bloquesEstudio = bloquesEstudio.slice(0, tope);

    var semana = [], d, b;
    for(d=0;d<7;d++) semana.push({ dia: d, bloques: [] });

    /* Solo si hay algo que practicar para este puesto. Un analista
       funcional no necesita resolver algoritmos cinco dias por
       semana, y ponerselo igual es relleno. */
    if(practicar){
      for(b=0;b<dias.length;b++){
        semana[dias[b]].bloques.push({
          tipo: "practica", min: MIN_PRACTICA,
          qué: practicar.qué,
          url: "index.html#rutina"
        });
      }
    }

    /* Cronológico, para que la parte 1 caiga antes que la 2; y
       espaciado, para que dos bloques en cinco días vayan al primero
       y al cuarto en vez de a dos días seguidos. El tema descansa
       entre sesiones, que es cuando termina de acomodarse. */
    var salto = bloquesEstudio.length
      ? Math.max(1, Math.floor(dias.length / bloquesEstudio.length)) : 1;
    for(b=0;b<bloquesEstudio.length;b++){
      semana[dias[(b * salto) % dias.length]].bloques.push(bloquesEstudio[b]);
    }

    if(repaso){
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

    return { semana: semana, ruta: ruta, rutas: lista, practica: practica,
             estudio: estudio, repaso: repaso, practicar: practicar,
             /* Cuántos bloques no entraron: sirve para decir que te
                sobra tiempo en vez de inventar días imposibles. */
             sobran: sobran };
  }

  /* Mover un bloque a otro dia, y volver a como estaba.

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

  /* Lunes = 0, que es como está armada la semana. */
  function hoy(){ return (new Date().getDay() + 6) % 7; }

  /* Lo del día, que es lo único que la portada necesita mostrar. */
  function deHoy(){
    var r = armar(), d = hoy();
    return { bloques: r.semana[d].bloques, dia: d, ruta: r.ruta };
  }

  return {
    DIAS: DIAS, DIAS_CORTO: DIAS_CORTO,
    MIN_PRACTICA: MIN_PRACTICA, MIN_REPASO: MIN_REPASO, MAX_BLOQUE: MAX_BLOQUE,
    estado: estado,
    cargar: cargar, guardar: guardar,
    rutas: rutas, rutaDe: rutaDe, activas: activas, quePracticar: quePracticar,
    hechosDe: hechosDe, pendientesDe: pendientesDe,
    armar: armar, hoy: hoy, deHoy: deHoy,
    mover: mover, sinMover: sinMover, hayMovidos: hayMovidos
  };
})();
