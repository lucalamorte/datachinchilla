/* ============================================================
   guia.js

   La chinchilla te lleva por el sitio la primera vez.

   El onboarding era una pantalla aparte: un formulario de cuatro
   pasos antes de dejarte ver nada. Esto es al revés. Ves el sitio
   de verdad, y la chinchilla te va diciendo qué hacer desde una
   esquina, sin taparte nada.

   El recorrido, y cada paso se completa cuando de verdad hiciste la
   cosa, no cuando cerraste el globo:

     portada   se cuenta qué es esto, y se invita a cargar el CV
     cv        el puesto, la experiencia, lo que ya sabes, y guardar
     ruta      la ruta guardada, y de ahí a la semana
     semana    los días y el rato
     portada   la agenda armada y la práctica del día

   Los pasos del CV se saltean si ya lo cargaste, y el de la semana si
   ya la configuraste. Se pregunta por eso mismo y no por algo
   parecido: mirar si había rutas activas daba por hecho el CV, y
   desde que una ruta se puede activar de a un botón, eso dejó de ser
   cierto y la guía desaparecía en cv.html.

   Se puede cerrar en cualquier momento y no vuelve a aparecer.

   Depende de path-sync.js y de onboarding.js (el estado).
   ============================================================ */
var Guia = (function(){
  "use strict";

  var K = "datachinchilla/v1/guia";

  var PASOS = [
    {
      id: "hola",
      donde: "index",
      titulo: "Hola, soy la chinchilla",
      texto: "Escarbo en internet y encuentro lo mejor que anda dando vueltas: " +
             "cursos de universidades y de las empresas que hacen las herramientas, " +
             "puestos en el orden que conviene.",
      accion: "Muéstrame cómo",
      lleva: "",
      /* El primero no apunta a nada: es la presentación. */
      ancla: ""
    },
    {
      id: "cv",
      donde: "index",
      titulo: "Primero, cuéntame de ti",
      texto: "Con tu CV encuentro exactamente lo que te falta para el puesto que " +
             "quieres, y te lo dejo en orden. Se lee acá en tu navegador.",
      accion: "Cargar mi CV",
      lleva: "cv.html",
      /* La tarjeta del CV, que es la unica puerta que queda: el
         banner que pedia lo mismo abajo se fue. */
      ancla: ".puerta.destacada"
    },
    {
      id: "rol",
      donde: "cv",
      titulo: "¿A dónde vas?",
      texto: "Elige el puesto primero: lo mismo que sabes te falta distinto según " +
             "a dónde apuntes. Se puede cambiar cuando quieras.",
      accion: "Ya elegí",
      lleva: "",
      ancla: "#puestos"
    },
    {
      id: "cargar",
      donde: "cv",
      titulo: "Ahora sí, tu experiencia",
      texto: "Arrastra el CV o pega el texto. En cuanto lo lea te muestro qué " +
             "reconocí y cuál de las rutas te sirve para ese puesto.",
      accion: "Ya está, seguir",
      lleva: "",
      ancla: "#cvZona"
    },
    {
      id: "leido",
      donde: "cv",
      titulo: "Esto ya lo sabes",
      texto: "Lo que reconocí en lo que contaste, y que por eso no te voy a " +
             "ofrecer. Si alguno no corresponde, sácalo con su cruz y rehago la " +
             "ruta sin él.",
      accion: "Está bien así",
      lleva: "",
      ancla: "#sabe"
    },
    {
      id: "guardar",
      donde: "cv",
      titulo: "Y esto es lo que falta",
      texto: "Los cursos que te faltan para ese puesto, en el orden que conviene " +
             "hacerlos. Guárdala y queda como tu ruta.",
      /* No promete guardar: el botón del globo avanza la guía, el que
         guarda es el de la página. Prometerlo dejaba a alguien
         creyendo que ya lo había hecho. */
      accion: "Listo, la guardé",
      lleva: "",
      ancla: "#guardarRuta"
    },
    {
      id: "semana",
      donde: "ruta",
      titulo: "Ahora, cuándo",
      texto: "Ya tienes tu ruta. Ahora te la reparto en la semana: qué día, a qué " +
             "hora y cuánto rato, para que sepas qué hacer un martes a las siete.",
      accion: "Armar mi semana",
      lleva: "semana.html",
      ancla: "#sigue"
    },
    {
      id: "repartir",
      donde: "semana",
      titulo: "Tus días y tu rato",
      texto: "Marca los días que vas a tener de verdad y cuánto rato. Con eso te " +
             "reparto la ruta y queda escrito qué hacer cada día.",
      accion: "Listo, ver mi agenda",
      lleva: "index.html",
      ancla: ".plan-form"
    },
    {
      id: "listo",
      donde: "index",
      titulo: "Listo. Elige por dónde",
      texto: "Arriba tienes tu agenda y abajo la práctica del día. Elige por dónde " +
             "arrancas y del resto me encargo yo.",
      /* Dos acciones y ninguna es "entendido": terminar la guía
         mirando la misma página que ya viste no lleva a nada. */
      dobles: true,
      accion: "El curso que sigue",
      lleva: "",
      accion2: "Un problema, 10 min",
      lleva2: "practica.html",
      ancla: "#retos"
    }
  ];

  var estado = { paso: 0, cerrada: false };

  function perfil(){
    try{ return (window.PathSync && PathSync.store) ? PathSync.store.active() : null; }
    catch(e){ return null; }
  }
  function get(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function set(k, v){ try{ localStorage.setItem(k, v); return true; }catch(e){ return false; } }

  function cargar(){
    var pf = perfil(), crudo = null;
    if(pf && pf.guia) crudo = pf.guia;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }
    if(crudo && typeof crudo === "object"){
      if(typeof crudo.paso === "number") estado.paso = crudo.paso;
      estado.cerrada = !!crudo.cerrada;
    }
    return estado;
  }

  function guardar(){
    var pf = perfil();
    if(pf){ pf.guia = estado; return PathSync.store.save(); }
    return set(K, JSON.stringify(estado));
  }

  /* Si ya hiciste algo por tu cuenta, la guía no te lo vuelve a
     pedir: se adelanta hasta donde de verdad estás. */
  function alDia(){
    if(typeof Onb === "undefined") return;
    Onb.cargar();

    /* Cada paso pregunta por lo que el paso hace, y no por un
       parecido.

       Antes esto miraba si había rutas activas para dar por hecho el
       CV. Dejó de valer cuando el catálogo y las páginas de ruta
       pudieron activarlas solas: con tocar un botón, la guía saltaba
       al paso de la semana, que sólo se pinta en una página de ruta,
       y en cv.html el globo desaparecía para siempre. */
    var hayCV = !!(Onb.estado.cv && Onb.estado.cv.replace(/\s/g, "").length >= 30) ||
                Object.keys(Onb.estado.respuestas || {}).length >= 2;

    /* La marca explícita: los días y los minutos vienen con valor
       por defecto y siempre daban que sí. */
    var haySemana = !!Onb.estado.semanaLista;

    /* La ruta guardada: la marca terminar(), que corre el botón de
       guardar del CV. Es la señal exacta de "ya cerré ese paso", a
       diferencia de tener rutas activas, que se llenan de mil formas
       y no dicen nada sobre el CV. */
    var hayRutaPropia = !!Onb.estado.hecho;

    /* Cada señal adelanta hasta el paso que ESA cosa completa, ni uno
       más. Antes el CV saltaba directo a la semana y se comía los dos
       pasos que explican el resultado. */
    var i = indiceDe;
    if(haySemana && estado.paso < i("listo")) estado.paso = i("listo");
    else if(hayRutaPropia && estado.paso < i("semana")) estado.paso = i("semana");
    else if(hayCV && estado.paso < i("leido")) estado.paso = i("leido");
  }

  function indiceDe(id){
    var i;
    for(i=0;i<PASOS.length;i++){ if(PASOS[i].id === id) return i; }
    return 0;
  }

  function actual(){
    cargar();
    alDia();
    if(estado.cerrada) return null;
    if(estado.paso >= PASOS.length) return null;
    return PASOS[estado.paso];
  }

  /* En qué página estamos, en los términos de la guía. */
  function donde(){
    var f = (location.pathname.split("/").pop() || "index").toLowerCase();
    /* En produccion las URLs son limpias: /cv, no /cv.html. Comparar
       contra el nombre de archivo hacia que ningun paso de cv ni de
       semana encontrara su pagina, y el recorrido se cortaba en el
       paso 2. Local andaba, porque ahi si se abre cv.html. */
    f = f.replace(/\.html$/, "");
    if(f === "" || f === "index") return "index";
    if(f === "cv") return "cv";
    if(f === "semana") return "semana";
    return "ruta";
  }

  /* El paso se muestra sólo en su página: la de la semana aparece
     cuando estás mirando tu ruta, no antes. */
  function tocaAca(){
    var p = actual();
    if(!p) return null;
    return (p.donde === donde()) ? p : null;
  }

  /* A dónde lleva "el curso que sigue": el primer paso sin hacer de
     tu ruta. Se calcula al abrir el globo, no antes, porque para
     entonces ya marcaste cosas. */
  function proximoCurso(){
    if(typeof Plan === "undefined") return "";
    var act = Plan.activas(), i;
    for(i=0;i<act.length;i++){
      var pend = Plan.pendientesDe(act[i]);
      if(pend.length) return act[i].archivo + "#" + pend[0].id;
    }
    return act.length ? act[0].archivo : "";
  }

  function avanzar(){
    estado.paso++;
    guardar();
  }

  function cerrar(){
    estado.cerrada = true;
    guardar();
  }

  function reabrir(){
    estado.cerrada = false;
    estado.paso = 0;
    guardar();
  }

  return {
    PASOS: PASOS, estado: estado,
    cargar: cargar, guardar: guardar,
    actual: actual, tocaAca: tocaAca, donde: donde, proximoCurso: proximoCurso,
    avanzar: avanzar, cerrar: cerrar, reabrir: reabrir
  };
})();
