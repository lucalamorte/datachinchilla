/* ============================================================
   onboarding.js

   Dónde estás, a dónde vas y cuánto tiempo tienes.

   Es la única entrada del sitio. Antes había cuatro puertas (el
   catálogo, la semana, el CV, el armador) y ninguna decía por cuál
   empezar; ahora hay una sola y de ella sale todo lo demás: las
   rutas activas, la semana y qué toca hoy.

   Guarda en el perfil si hay cuenta, y en este navegador si no.

   Depende de temas.js (los temas y los puestos) y de cv.js (leer un
   CV). No depende de la página: la misma información la usan la
   portada, la semana y el detalle de cada ruta.
   ============================================================ */
var Onb = (function(){
  "use strict";

  var K = "datachinchilla/v1/onboarding";

  /* Para el que no tiene el CV a mano. Cuatro preguntas dan un mapa
     de temas parecido al que sale de leer un CV, y se responden en
     menos de lo que tarda en encontrar el archivo. */
  /* Las cinco preguntas.

     Eran cuatro y eran de datos -programas, SQL, datos en un trabajo,
     nube- porque se escribieron cuando el sitio eran tres rutas de
     datos. Hoy hay diecisiete rutas y ocho puestos, y a la mitad no
     le toca una base de datos: a alguien que eligio frontend se le
     preguntaba si armo pipelines, que es preguntarle por el trabajo
     de otro.

     Estas cubren el ancho del sitio: programar, la pantalla, el
     servidor, los datos y la infraestructura. Nadie contesta las
     cinco sobre lo mismo, y cada una suma temas que existen en
     temas.js desde que entraron las rutas de desarrollo. */
  var PREGUNTAS = [
    { id: "prog", texto: "¿Programas?",
      ayuda: "En cualquier lenguaje, aunque sea para automatizar algo tuyo.",
      opciones: [
        { t: "Nunca escribí código", temas: {} },
        { t: "Algo, scripts sueltos", temas: { prog: 1 } },
        { t: "Sí, es parte de mi trabajo", temas: { prog: 2 } },
        { t: "Vengo del desarrollo", temas: { prog: 3 } }
      ] },
    { id: "pantalla", texto: "¿Construiste algo que se vea en pantalla?",
      ayuda: "Una página, una app, aunque haya sido para vos.",
      opciones: [
        { t: "No, nunca", temas: {} },
        { t: "HTML y CSS, algo suelto", temas: { web: 1 } },
        { t: "Interfaces con un framework", temas: { web: 2, prog: 1 } },
        { t: "Es lo que hago", temas: { web: 3, prog: 2 } }
      ] },
    { id: "servidor", texto: "¿Y del otro lado: APIs, servidores, bases?",
      ayuda: "Lo que hay detrás de la pantalla, o detrás de un dashboard.",
      opciones: [
        { t: "No me tocó", temas: {} },
        { t: "Consumí APIs de otros", temas: { backend: 1 } },
        { t: "Escribí endpoints y consultas", temas: { backend: 2, sql: 2 } },
        { t: "Diseño el backend y su base", temas: { backend: 3, sql: 3, modelado: 2 } }
      ] },
    { id: "datos", texto: "¿Trabajaste con datos para que otro decida?",
      ayuda: "Cuenta cualquier cosa que alguien más haya usado para decidir.",
      opciones: [
        { t: "Todavía no", temas: {} },
        { t: "Reportes y planillas", temas: { viz: 1, sql: 1 } },
        { t: "Dashboards o análisis para otros", temas: { viz: 2, sql: 2 } },
        { t: "Pipelines o modelos en producción", temas: { pipelines: 2, modelado: 2, python: 2 } }
      ] },
    { id: "nube", texto: "¿Nube e infraestructura?",
      ayuda: "AWS, Azure, Google Cloud, Docker, lo que sea.",
      opciones: [
        { t: "Nada", temas: {} },
        { t: "Usé algún servicio suelto", temas: { cloud: 1 } },
        { t: "Despliego lo que hago", temas: { cloud: 2, prog: 1 } },
        { t: "Administro la infraestructura", temas: { cloud: 3, prog: 1, mlops: 1 } }
      ] }
  ];

  /* Las franjas existen porque "seis horas por semana" no dice cuándo,
     y el cuándo es la mitad de que un plan se cumpla. */
  var FRANJAS = [
    { id: "manana", t: "A la mañana", d: "Antes de que empiece el día" },
    { id: "tarde",  t: "A la tarde",  d: "En algún hueco" },
    { id: "noche",  t: "A la noche",  d: "Cuando ya está todo cerrado" },
    { id: "finde",  t: "Los fines",   d: "Sábado o domingo, en bloques largos" }
  ];

  var estado = {
    hecho: false,
    paso: 0,
    desde: "",            /* "cv" o "preguntas" */
    cv: "",               /* el texto, sólo en este navegador */
    respuestas: {},
    temas: {},            /* lo que ya sabes, venga de donde venga */
    /* Los temas que dijiste que no sabes, aunque yo los haya leido
       en el CV. Van aparte de `temas` porque no son un dato menos:
       recalcularTemas los saca cada vez que se rehace la lista. */
    sacados: [],
    /* Y los que dijiste que si sabes aunque el CV no los nombre. Es
       el espejo de sacados, y por eso vive al lado. */
    agregados: [],
    puesto: "",
    rutas: [],            /* las activas; salen del puesto y se editan */
    /* Si tu ruta es una del sitio y no una mezcla, acá queda cuál. */
    deRuta: "",
    dias: [0, 1, 2, 3, 4],
    franja: "noche",
    /* Que la semana se configuro a proposito: los dias y los
       minutos vienen con valor por defecto, asi que no sirven
       para saber si alguien paso por ahi. */
    semanaLista: false,
    minutos: 360          /* por semana; en minutos para no redondear feo */
  };

  function perfil(){
    try{ return (window.PathSync && PathSync.store) ? PathSync.store.active() : null; }
    catch(e){ return null; }
  }
  function get(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function set(k, v){ try{ localStorage.setItem(k, v); return true; }catch(e){ return false; } }

  function cargar(){
    var pf = perfil(), crudo = null;
    if(pf && pf.onb) crudo = pf.onb;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }
    if(crudo && typeof crudo === "object"){
      for(var k in estado){
        if(crudo[k] !== undefined) estado[k] = crudo[k];
      }
    }
    return estado;
  }

  function guardar(){
    var pf = perfil(), ok;
    if(pf){ pf.onb = estado; ok = PathSync.store.save(); }
    else ok = set(K, JSON.stringify(estado));
    /* La guia mira este estado para saber por que paso vas. Sin este
       aviso solo se enteraba al recargar, y por eso habia que
       confirmarle a mano lo que acababas de hacer. */
    try{
      if(typeof document !== "undefined" && document.dispatchEvent){
        document.dispatchEvent(new CustomEvent("onb:cambio"));
      }
    }catch(e){}
    return ok;
  }

  function hecho(){ return !!estado.hecho; }

  /* Los temas que salen de las respuestas, en el mismo formato que
     devuelve cv.js, para que de acá en adelante dé igual de dónde
     vinieron. */
  function temasDeRespuestas(resp){
    var out = {}, i, p, o, k;
    for(i=0;i<PREGUNTAS.length;i++){
      p = PREGUNTAS[i];
      if(resp[p.id] === undefined) continue;
      o = p.opciones[resp[p.id]];
      if(!o) continue;
      for(k in o.temas){
        if(!out[k]) out[k] = { nivel: o.temas[k], senales: [] };
        else out[k].nivel = Math.max(out[k].nivel, o.temas[k]);
      }
    }
    return out;
  }

  /* Un CV dice más que cuatro preguntas, así que si hay CV manda el
     CV; las respuestas quedan como piso. */
  function recalcularTemas(){
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
    if(suma.length && typeof CV !== "undefined" && CV.inferir) out = CV.inferir(out);
    /* Lo que dices que no sabes gana contra lo que yo lei. El CV
       cuenta lo que hiciste, no lo que te quedo, y esa diferencia
       solo la sabes vos. */
    var fuera = estado.sacados || [];
    for(var j=0;j<fuera.length;j++) delete out[fuera[j]];

    estado.temas = out;
    return out;
  }

  /* Marca un tema como no sabido, o lo devuelve.

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
  }

  /* Las rutas que cubren lo que te falta para el puesto, ordenadas
     por cuánto aportan. Son las que se proponen como activas: nadie
     necesita las quince, y elegir entre quince cada vez que armas la
     semana es el problema que esto viene a sacar. */
  function rutasSugeridas(){
    if(!estado.puesto || typeof CV === "undefined") return [];
    var r = CV.armar(estado.puesto, estado.temas, 40);
    var peso = {}, i, p;
    for(i=0;i<r.pasos.length;i++){
      p = r.pasos[i];
      peso[p.ruta] = (peso[p.ruta] || 0) + 1;
    }
    var out = [];
    for(var k in peso) out.push({ clave: k, pasos: peso[k] });
    out.sort(function(a, b){ return b.pasos - a.pasos; });
    return out;
  }

  /* Desde dónde puedes empezar, en la misma escala que las rutas:
     0 desde cero, 1 con SQL, 2 con Python, 3 con experiencia. */
  function miNivel(){
    var s = estado.temas || {};
    function n(k){ return s[k] ? s[k].nivel : 0; }
    /* Experiencia es haber hecho algo con esto, no haberlo leído:
       pipelines o modelado en serio, o nube que se administra. */
    if(n("pipelines") >= 2 || n("modelado") >= 2 || n("cloud") >= 3) return 3;
    /* Saber programar es saber programar, en el lenguaje que sea.
       Esta escalera era solo de datos, así que alguien con diez años
       de React daba cero y quedaba afuera de su propia ruta: las
       rutas que piden saber programar se le escondían por
       "arranca más arriba de donde estás". */
    if(n("python") >= 2 || n("web") >= 2 || n("backend") >= 2 ||
       n("prog") >= 2) return 2;
    if(n("sql") >= 2) return 1;
    return 0;
  }

  /* Los temas que cubre una ruta, con cuantos pasos le dedica. */
  function temasDeRuta(clave){
    var out = {}, k, i, lista;
    if(typeof TEMAS === "undefined") return out;
    for(k in TEMAS.pasosPorTema){
      lista = TEMAS.pasosPorTema[k];
      for(i=0;i<lista.length;i++){
        if(lista[i].ruta === clave) out[k] = (out[k] || 0) + 1;
      }
    }
    return out;
  }

  /* Qué tan bien te queda cada ruta que ya existe.

     Se mira contra lo que te falta para el puesto, no contra el
     puesto entero: a alguien que ya sabe SQL no le sirve que una
     ruta cubra SQL, le sirve que cubra lo que no tiene. */
  function rutasQueCalzan(){
    if(!estado.puesto || typeof CV === "undefined") return [];
    var puesto = CV.puestoDe(estado.puesto);
    var r = CV.armar(estado.puesto, estado.temas, 60);

    /* Cuánto pesa cada tema que falta. */
    var falta = {}, pesoTotal = 0, i;
    for(i=0;i<r.faltantes.length;i++){
      falta[r.faltantes[i].id] = r.faltantes[i].prioridad;
      pesoTotal += r.faltantes[i].prioridad;
    }
    if(!pesoTotal) return [];

    /* Los temas que son el oficio: los que el puesto pide en 3 y
       todavía te faltan. Una ruta que no toca ninguno puede servirte
       después, pero no es TU ruta.

       Sin esta regla, a un desarrollador de React apuntando a Full
       Stack le salía SnowPro Core: dieciséis pasos de nube y SQL, que
       también le hacen falta un poco, sumaban más que las quince
       partes que cubren justo lo que el puesto es. Todos los temas
       pesaban igual en la cuenta. */
    var puesto = (typeof CV !== "undefined") ? CV.puestoDe(estado.puesto) : null;
    var pide = (puesto && puesto.temas) ? puesto.temas : {};
    var centrales = [], kk;
    /* Sobre lo que el puesto pide, no sobre lo que te falta: un CV
       que ya trae React y Node deja "web" y "backend" fuera de los
       faltantes, la lista quedaba vacía y no filtraba nada. Central
       es lo que el puesto es, lo sepas o no. */
    for(kk in pide){ if(pide[kk] >= 3) centrales.push(kk); }

    var rs = (typeof PASOS !== "undefined") ? PASOS : [], out = [], j, k;
    var nivel = miNivel();
    for(j=0;j<rs.length;j++){
      var clave = rs[j].clave;
      if(clave === "de") continue;          /* es un mapa, no una ruta */
      /* Una ruta que arranca más arriba de donde estás no es tu
         ruta, por mucho que cubra los temas que te faltan. */
      if((rs[j].nivelN || 0) > nivel) continue;
      var temas = temasDeRuta(clave);
      var cubre = 0, pasosUtiles = 0, pasosTotal = 0;
      for(k in temas){
        pasosTotal += temas[k];
        if(falta[k]){ cubre += falta[k]; pasosUtiles += temas[k]; }
      }
      if(!pasosTotal) continue;

      var tocaCentral = 0, c;
      for(c=0;c<centrales.length;c++){ if(temas[centrales[c]]) tocaCentral++; }
      /* Si el puesto tiene oficio declarado y esta ruta no toca nada
         de él, queda afuera de la recomendación. */
      if(centrales.length && !tocaCentral) continue;

      out.push({
        clave: clave,
        nombre: rs[j].nombre,
        archivo: rs[j].archivo,
        /* Cuánto de lo que te falta resuelve esta ruta. */
        cubre: cubre / pesoTotal,
        /* Cuánto de la ruta te sirve: si la mitad ya la sabes, no
           es tu ruta aunque cubra los temas. */
        aprovecha: pasosUtiles / pasosTotal,
        /* Cuántos de los temas centrales del puesto toca. Desempata:
           entre dos rutas parecidas, la que va más al centro. */
        central: centrales.length ? tocaCentral / centrales.length : 0,
        pasos: rs[j].pasos.length
      });
    }
    out.sort(function(a, b){
      var pa = a.cubre * a.aprovecha * (1 + a.central);
      var pb = b.cubre * b.aprovecha * (1 + b.central);
      return pb - pa;
    });
    return out;
  }

  /* La que se recomienda, si alguna vale la pena. Los umbrales:
     tiene que resolver al menos la mitad de lo que te falta y que al
     menos la mitad de la ruta te sirva. Por debajo de eso conviene
     una selección hecha a medida. */
  function laQueCalza(){
    var c = rutasQueCalzan();
    if(!c.length) return null;
    return (c[0].cubre >= 0.5 && c[0].aprovecha >= 0.5) ? c[0] : null;
  }

  /* Los dos caminos. La regla contra la redundancia: un tema lo
     cubre una sola ruta, la que mas pasos le aporta. Si dos rutas
     ensenan modelado, entra una; hacer las dos es repetir. */
  function caminos(){
    if(!estado.puesto || typeof CV === "undefined") return { corto: [], largo: [] };

    var puesto = CV.puestoDe(estado.puesto);
    var r = CV.armar(estado.puesto, estado.temas, 60);

    /* Cuanto aporta cada ruta a cada tema que falta. */
    var porTema = {}, i, p;
    for(i=0;i<r.pasos.length;i++){
      p = r.pasos[i];
      if(!porTema[p.tema]) porTema[p.tema] = {};
      porTema[p.tema][p.ruta] = (porTema[p.tema][p.ruta] || 0) + 1;
    }

    /* Para cada tema, la ruta que mas lo cubre. Los temas centrales
       (los que el puesto pide 3) arman el camino corto; el resto se
       suma al largo. */
    var corto = [], largo = [], k, mejor, mejorN, ruta;

    function sumar(lista, clave, tema){
      var j;
      for(j=0;j<lista.length;j++){
        if(lista[j].clave === clave){ lista[j].temas.push(tema); return; }
      }
      lista.push({ clave: clave, temas: [tema] });
    }

    var temas = [];
    for(k in porTema) temas.push(k);
    temas.sort(function(a, b){
      return (puesto.temas[b] || 0) - (puesto.temas[a] || 0);
    });

    for(i=0;i<temas.length;i++){
      k = temas[i];
      mejor = ""; mejorN = 0;
      for(ruta in porTema[k]){
        if(porTema[k][ruta] > mejorN){ mejorN = porTema[k][ruta]; mejor = ruta; }
      }
      if(!mejor) continue;
      var central = (puesto.temas[k] || 0) >= 3;
      /* El motivo se acumula: una ruta puede entrar por dos temas. */
      if(central) sumar(corto, mejor, k);
      sumar(largo, mejor, k);
    }
    /* Si el corto quedo vacio porque no falta nada central, se toma
       lo primero del largo para no ofrecer un camino sin pasos. */
    if(!corto.length && largo.length) corto = largo.slice(0, 1);

    return { corto: corto, largo: largo };
  }

  /* Cuanto lleva un camino, para poder compararlos. */
  function horasDe(items){
    var min = 0, i, j, r, pend, clave;
    if(typeof Plan === "undefined") return 0;
    for(i=0;i<items.length;i++){
      clave = items[i].clave || items[i];
      r = Plan.rutaDe(clave);
      if(!r) continue;
      pend = Plan.pendientesDe(r);
      for(j=0;j<pend.length;j++) min += pend[j].min;
    }
    return Math.round(min / 60);
  }

  /* El motivo en palabras, para poner debajo del nombre de la ruta. */
  function porQue(item){
    if(typeof CV === "undefined") return "";
    var n = item.temas.map(function(k){ return CV.nombreTema(k); });
    /* Coma y no "y": varios temas ya tienen una "y" adentro
       ("Estadística y experimentos") y quedaba "por a y b y c". */
    return "Por " + n.join(", ").toLowerCase();
  }

  function nombreRuta(clave){
    var rs = (typeof PASOS !== "undefined") ? PASOS : [], i;
    for(i=0;i<rs.length;i++){ if(rs[i].clave === clave) return rs[i].nombre; }
    return clave;
  }

  function activa(clave){
    return estado.rutas.indexOf(clave) >= 0;
  }

  function alternarRuta(clave){
    var i = estado.rutas.indexOf(clave);
    if(i >= 0) estado.rutas.splice(i, 1);
    else estado.rutas.push(clave);
    return guardar();
  }

  /* Cierra el onboarding y deja el plan listo, que es el punto: que
     al terminar no haya que configurar nada más. */
  function terminar(){
    recalcularTemas();
    if(!estado.rutas.length){
      var s = rutasSugeridas(), i;
      for(i=0;i<s.length && i<3;i++) estado.rutas.push(s[i].clave);
    }
    estado.hecho = true;
    /* La semana que hubiera era para la ruta anterior: al cambiar de
       ruta queda sin acomodar. Dejar el true puesto hacia que la guia
       se saltara ese paso y desapareciera de todas las paginas menos
       la portada. */
    estado.semanaLista = false;
    /* La semana la marca la semana: darla por configurada acá hacía
       que la guía se salteara ese paso sin que nadie lo hiciera. */
    if(typeof Plan !== "undefined"){
      Plan.cargar();
      if(estado.rutas.length) Plan.estado.ruta = estado.rutas[0];
      Plan.estado.dias = estado.dias.slice(0);
      Plan.estado.horas = Math.round(estado.minutos / 60);
      Plan.guardar();
    }
    return guardar();
  }

  function reabrir(){
    estado.hecho = false;
    estado.paso = 0;
    return guardar();
  }

  return {
    PREGUNTAS: PREGUNTAS, FRANJAS: FRANJAS,
    estado: estado,
    cargar: cargar, guardar: guardar, hecho: hecho,
    temasDeRespuestas: temasDeRespuestas, recalcularTemas: recalcularTemas,
    sacarTema: sacarTema, agregarTema: agregarTema,
    rutasSugeridas: rutasSugeridas, caminos: caminos, horasDe: horasDe,
    rutasQueCalzan: rutasQueCalzan, laQueCalza: laQueCalza, miNivel: miNivel,
    porQue: porQue,
    nombreRuta: nombreRuta,
    activa: activa, alternarRuta: alternarRuta,
    terminar: terminar, reabrir: reabrir
  };
})();
