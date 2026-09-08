/* ============================================================
   practica.js

   Qué problemas hiciste y cuál sigue.

   El enunciado se lee en LeetCode o en StrataScratch, que es de
   quien es. Acá vive la lista, el orden y tu avance, que es
   justamente lo que allá no queda: puedes hacer treinta de los
   setenta y cinco y no tener forma de saber cuáles.

   También es lo que le da sentido a la racha. Antes el botón
   "Practiqué" era un botón de confianza: no sabía qué hiciste ni
   cuántos. Ahora marcar dos problemas es el día practicado, y el
   número quiere decir algo.

   Depende de problemas.js y de path-sync.js.
   ============================================================ */
var Practica = (function(){
  "use strict";

  var K    = "datachinchilla/v1/practica";
  var KDIA = "datachinchilla/v1/dias";

  /* Cuántos problemas cuentan como un día practicado. Dos es poco
     para sentirse productivo y suficiente para no perder la mano,
     que es exactamente lo que se busca de la práctica diaria. */
  var POR_DIA = 2;

  function perfil(){
    try{ return (window.PathSync && PathSync.store) ? PathSync.store.active() : null; }
    catch(e){ return null; }
  }
  function get(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function set(k, v){ try{ localStorage.setItem(k, v); return true; }catch(e){ return false; } }

  /* { "blind75:1": "2026-09-03", ... } — se guarda el día y no un
     true, para poder contar cuántos hiciste hoy sin llevar otra
     lista aparte. */
  function leer(){
    var pf = perfil();
    if(pf) return pf.practica || (pf.practica = {});
    try{ return JSON.parse(get(K) || "{}") || {}; }catch(e){ return {}; }
  }

  function guardar(mapa){
    var pf = perfil();
    if(pf){ pf.practica = mapa; return PathSync.store.save(); }
    return set(K, JSON.stringify(mapa));
  }

  function clave(banco, item){
    return banco + ":" + (item.n !== undefined ? item.n : item.t);
  }

  function hecho(banco, item){ return !!leer()[clave(banco, item)]; }

  function hoyKey(d){
    d = d || new Date();
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m +
           "-" + (day < 10 ? "0" : "") + day;
  }

  function marcar(banco, item, valor){
    /* Sin cuenta no se marca. Va aca y no en los botones porque hay
       dos lugares que marcan -la lista de practica y la tarjeta de la
       portada- y el que se agregue manana tambien tiene que quedar
       tapado sin que nadie se acuerde. */
    if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()){
      return { hecho: false, cerroElDia: false, sinCuenta: true };
    }
    var mapa = leer(), k = clave(banco, item);
    if(valor === undefined) valor = !mapa[k];
    if(valor) mapa[k] = hoyKey();
    else delete mapa[k];
    guardar(mapa);
    /* Los dos datos que acá se saben: si quedó marcado, y si con este
       se cerró el día. El segundo se perdía y las páginas lo tenían
       que deducir contando de nuevo, que además no distingue el salto
       de "ya estaba cerrado". */
    return { hecho: valor, cerroElDia: sincronizarRacha(banco) };
  }

  /* Cuántos hiciste hoy de un banco. */
  function hoyCuantos(banco){
    var mapa = leer(), hoy = hoyKey(), n = 0, k;
    for(k in mapa){
      if(mapa[k] === hoy && k.indexOf(banco + ":") === 0) n++;
    }
    return n;
  }

  /* Los bancos se corresponden con los bloques de la racha: los de
     SQL van al bloque de SQL y los de algoritmos al de Python. */
  var BLOQUE = { strata: "sql", blind75: "py" };

  /* El día se marca solo cuando hiciste los suficientes, y se
     desmarca si los deshacés. La racha deja de depender de que uno
     se acuerde de apretar un botón. */
  /* Devuelve true sólo en el salto: el día que no estaba marcado y
     queda marcado. Es el momento del festejo, y acá es el único lugar
     donde se sabe. Quién avisa es la página; este módulo no dibuja. */
  function sincronizarRacha(banco){
    var b = BLOQUE[banco];
    if(!b) return false;
    var dias = leerDias();
    var hoy = hoyKey();
    var basta = hoyCuantos(banco) >= POR_DIA;
    if(!dias[b] || typeof dias[b] !== "object") dias[b] = {};
    var antes = !!dias[b][hoy];
    if(basta) dias[b][hoy] = true;
    else if(dias[b][hoy]) delete dias[b][hoy];
    guardarDias(dias);
    return basta && !antes;
  }

  /* Cuántos días seguidos, contando desde hoy hacia atrás. Es el
     número que hace que la racha valga algo. */
  function racha(banco){
    var b = BLOQUE[banco];
    if(!b) return 0;
    var dias = leerDias()[b] || {};
    var d = new Date(), n = 0;
    /* Si hoy todavía no está, la racha es la de ayer: el día no
       terminó y contarlo como cortado sería castigar la mañana. */
    if(!dias[hoyKey(d)]) d.setDate(d.getDate() - 1);
    while(dias[hoyKey(d)]){ n++; d.setDate(d.getDate() - 1); }
    return n;
  }

  function leerDias(){
    var pf = perfil();
    if(pf) return pf.dias || (pf.dias = {});
    try{ return JSON.parse(get(KDIA) || "{}") || {}; }catch(e){ return {}; }
  }

  function guardarDias(d){
    var pf = perfil();
    if(pf){ pf.dias = d; return PathSync.store.save(); }
    return set(KDIA, JSON.stringify(d));
  }

  function bancoDe(id){
    var i;
    for(i=0;i<PROBLEMAS.length;i++){ if(PROBLEMAS[i].id === id) return PROBLEMAS[i]; }
    return PROBLEMAS[0];
  }

  function avance(id){
    var b = bancoDe(id), mapa = leer(), n = 0, i;
    for(i=0;i<b.items.length;i++){
      if(mapa[clave(id, b.items[i])]) n++;
    }
    return { hechos: n, total: b.items.length };
  }

  /* El próximo problema: el primero sin hacer, en el orden en que
     está la lista. Se ordena por dificultad porque empezar por un
     difícil de programación dinámica es abandonar el primer día. */
  var ORDEN_DIF = { facil: 0, medio: 1, dificil: 2 };

  function ordenados(id){
    var b = bancoDe(id);
    return b.items.slice(0).sort(function(a, c){
      var d = ORDEN_DIF[a.d] - ORDEN_DIF[c.d];
      if(d) return d;
      /* Dentro de la misma dificultad, el más resuelto primero: la
         tasa de aceptación es una medida decente de cuán directo es. */
      return (c.ac || 50) - (a.ac || 50);
    });
  }

  /* Los que te faltan, en el orden en que conviene hacerlos.

     Vivia suelta en la portada, escrita sobre b.items -el orden del
     archivo- mientras aca al lado ordenados() ordenaba por
     dificultad. Dos ideas del orden en el mismo sitio: la portada
     ofrecia un medio primero y un dificil cuarto.

     Habia una segunda copia identica, la del boton "Lo resolvi".
     Coincidian, porque las dos estaban igual de mal. Pero arreglar
     una sola las habria puesto en ordenes distintos y entonces si:
     marcabas el que veias y se tildaba otro. Por eso las dos piden
     la misma lista y no hay ninguna escrita a mano. */
  function pendientes(id){
    var lista = ordenados(id), mapa = leer(), out = [], i;
    for(i=0;i<lista.length;i++){
      if(!mapa[clave(id, lista[i])]) out.push(lista[i]);
    }
    return out;
  }

  function siguiente(id){
    var lista = ordenados(id), mapa = leer(), i;
    for(i=0;i<lista.length;i++){
      if(!mapa[clave(id, lista[i])]) return lista[i];
    }
    return null;
  }

  /* Qué banco toca practicar hoy, según lo que te falta para el
     puesto. Si ya sabes SQL, el tiempo rinde más en algoritmos. */
  function bancoDeHoy(){
    var sabe = (typeof Onb !== "undefined" && Onb.estado.temas) ? Onb.estado.temas : {};
    var sql = sabe.sql ? sabe.sql.nivel : 0;
    var py  = sabe.python ? sabe.python.nivel : 0;
    return (sql < py) ? "strata" : "blind75";
  }

  return {
    POR_DIA: POR_DIA,
    bancos: function(){ return (typeof PROBLEMAS !== "undefined") ? PROBLEMAS : []; },
    bancoDe: bancoDe, clave: clave, hecho: hecho, marcar: marcar,
    avance: avance, ordenados: ordenados, siguiente: siguiente,
    pendientes: pendientes,
    hoyCuantos: hoyCuantos, bancoDeHoy: bancoDeHoy, racha: racha
  };
})();
