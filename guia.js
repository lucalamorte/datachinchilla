/* ============================================================
   guia.js

   La chinchilla te lleva por el sitio la primera vez.

   El onboarding era una pantalla aparte: un formulario de cuatro
   pasos antes de dejarte ver nada. Esto es al revés. Ves el sitio
   de verdad, y la chinchilla te va diciendo qué hacer desde una
   esquina, sin taparte nada.

   Cuatro pasos, y cada uno se completa solo cuando de verdad hiciste
   la cosa, no cuando cerraste el globo:

     1. Estás en la portada. Se cuenta qué es esto.
     2. Cargar el CV.        Se completa cuando hay ruta.
     3. Armar la semana.     Se completa cuando hay días y horas.
     4. Listo.               Queda tu agenda y la práctica del día.

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
      titulo: "Primero, cuéntame de vos",
      texto: "Con tu CV encuentro exactamente lo que te falta para el puesto que " +
             "quieres, y te lo dejo en orden. Se lee acá en tu navegador.",
      accion: "Cargar mi CV",
      lleva: "cv.html",
      ancla: ".invita"
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
    var hayRuta = (Onb.estado.rutas || []).length > 0;
    /* La marca explícita: los días y los minutos vienen con valor
       por defecto y siempre daban que sí. */
    var haySemana = hayRuta && !!Onb.estado.semanaLista;
    /* Los pasos se saltean solos cuando ya hiciste la cosa: si venías
       con tu ruta armada, la guía no te la vuelve a pedir. */
    var i = indiceDe;
    if(haySemana && estado.paso < i("listo")) estado.paso = i("listo");
    else if(hayRuta && estado.paso < i("semana")) estado.paso = i("semana");
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
    var f = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    if(f === "" || f === "index.html") return "index";
    if(f === "cv.html") return "cv";
    if(f === "semana.html") return "semana";
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
