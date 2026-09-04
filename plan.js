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

  var estado = { ruta: "sqlpy", horas: 6, dias: [0,1,2,3,4] };

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
    if(!out.length){
      r = rutaDe(estado.ruta);
      if(r) out.push(r);
    }
    return out;
  }

  /* Qué conviene practicar a diario, según lo que te falta. Antes
     decía siempre "SQL y algoritmos" aunque ya supieras SQL. */
  function quePracticar(){
    var sabe = (typeof Onb !== "undefined" && Onb.estado.temas) ? Onb.estado.temas : {};
    var sql = sabe.sql ? sabe.sql.nivel : 0;
    var py  = sabe.python ? sabe.python.nivel : 0;
    if(sql < 2 && py < 2) return { qué: "SQL y Python, mezclados", b: "ambos" };
    if(sql < 2)           return { qué: "SQL, una o dos consultas", b: "sql" };
    if(py < 2)            return { qué: "Python, un ejercicio", b: "py" };
    return { qué: "SQL y algoritmos, para no perder la mano", b: "ambos" };
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
  function repartirEstudio(minutos, ruta){
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
  }

  function armar(){
    var lista = activas();
    var ruta = lista[0] || rutaDe(estado.ruta);
    var dias = estado.dias.slice(0).sort(function(a,b){ return a - b; });
    if(!dias.length) dias = [0,1,2,3,4];

    var total    = estado.horas * 60;
    var practica = MIN_PRACTICA * dias.length;
    var repaso   = dias.length >= 3 ? MIN_REPASO : 0;
    var estudio  = Math.max(0, total - practica - repaso);
    var practicar = quePracticar();

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

    for(b=0;b<dias.length;b++){
      semana[dias[b]].bloques.push({
        tipo: "practica", min: MIN_PRACTICA,
        qué: practicar.qué,
        url: "index.html#rutina"
      });
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
    return { semana: semana, ruta: ruta, rutas: lista, practica: practica,
             estudio: estudio, repaso: repaso, practicar: practicar,
             /* Cuántos bloques no entraron: sirve para decir que te
                sobra tiempo en vez de inventar días imposibles. */
             sobran: sobran };
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
    armar: armar, hoy: hoy, deHoy: deHoy
  };
})();
