/* ============================================================
   cv.js

   El path que sale de tu CV, calculado acá en el navegador.

   El CV no se sube a ningún lado. Entra como texto, se cruza contra
   el vocabulario de temas.js y sale una lista de pasos. Nada viaja,
   nada se guarda salvo que vos guardes la ruta.

   Cómo estima el nivel: contando señales distintas del mismo tema.
   Un CV que dice "SQL" dice menos que uno que dice "SQL, Postgres,
   BigQuery y window functions", aunque los dos digan SQL. No es una
   medida de cuánto sabes, es una medida de cuánto contás, que es
   con lo único que se puede trabajar leyendo un papel.

   Depende de temas.js.
   ============================================================ */
var CV = (function(){
  "use strict";

  /* pdf.js descarga el texto en un worker aparte y hay que decirle de
     dónde sacarlo. Sin esto no falla: se queda esperando, que es peor,
     porque parece que no hiciste nada. */
  if(typeof pdfjsLib !== "undefined"){
    pdfjsLib.GlobalWorkerOptions.workerSrc =
      "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
  }

  /* Sin acentos y en minúscula, igual que build-temas.py, porque las
     señales están escritas así. */
  function limpiar(s){
    s = (s || "").normalize ? (s || "").normalize("NFD") : (s || "");
    return s.replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  /* Una señal cuenta sólo si aparece como palabra suelta o frase, no
     dentro de otra. Sin esto "r" o "java" pescarían medio CV. */
  function apareceEn(texto, senal){
    var esc = senal.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp("(^|[^a-z0-9])" + esc + "([^a-z0-9]|$)").test(texto);
  }

  /* Qué temas asoma el CV, y con cuánta insistencia. */
  function leer(texto){
    var t = limpiar(texto), out = {}, i, j;
    for(i=0;i<TEMAS.temas.length;i++){
      var tema = TEMAS.temas[i], vistas = [];
      for(j=0;j<tema.senales.length;j++){
        if(apareceEn(t, tema.senales[j])) vistas.push(tema.senales[j]);
      }
      if(vistas.length){
        out[tema.id] = {
          nivel: Math.min(3, vistas.length),   /* 1 mención es 1; 3 o más, 3 */
          senales: vistas
        };
      }
    }
    return inferir(out);
  }

  /* Saber una cosa implica saber la de abajo. Nadie orquesta con
     Airflow sin programar, ni entrena redes sin haber visto un
     modelo antes. Sin esto, el CV de alguien con oficio da cero en
     temas básicos sólo porque ya no los menciona, y el path le
     ofrece el curso para principiantes.

     tema: [nivel desde el que aplica, {tema implicado: piso}] */
  var IMPLICA = {
    python:    [2, { prog: 1 }],
    pipelines: [2, { prog: 1 }],
    bigdata:   [2, { prog: 1, cloud: 1 }],
    modelado:  [2, { sql: 1 }],
    ml:        [2, { stats: 1, python: 1 }],
    deep:      [1, { ml: 1, python: 1 }],
    llm:       [2, { python: 1 }],
    mlops:     [1, { cloud: 1, ml: 1 }],
    cloud:     [3, { prog: 1 }]
  };

  function inferir(det){
    var k, reg, piso, t;
    for(k in IMPLICA){
      if(!det[k]) continue;
      reg = IMPLICA[k];
      if(det[k].nivel < reg[0]) continue;
      piso = reg[1];
      for(t in piso){
        if(!det[t]) det[t] = { nivel: piso[t], deducido: k, senales: [] };
        else if(det[t].nivel < piso[t]) det[t].nivel = piso[t];
      }
    }
    return det;
  }

  function puestoDe(id){
    var p = TEMAS.puestos, i;
    for(i=0;i<p.length;i++){ if(p[i].id === id) return p[i]; }
    return p[0];
  }

  function nombreTema(id){
    var t = TEMAS.temas, i;
    for(i=0;i<t.length;i++){ if(t[i].id === id) return t[i].nombre; }
    return id;
  }

  /* Lo que ya está hecho en el sitio cuenta como sabido: si cerraste
     el curso, no tiene sentido que el path te lo vuelva a poner. */
  function hechos(){
    var out = {}, i, r, pf;
    if(typeof Plan === "undefined") return out;
    var rs = Plan.rutas();
    for(i=0;i<rs.length;i++){
      r = rs[i];
      var d = Plan.hechosDe(r);
      for(var k in d){ if(d[k]) out[r.clave + ":" + k] = true; }
    }
    return out;
  }

  /* El path: lo que el puesto pide menos lo que el CV ya muestra.

     Prioridad de un tema = cuánto lo pide el puesto por cuánto te
     falta. Un tema central que no aparece en el CV va primero; uno
     secundario que ya mencionaste, último o afuera. */
  function armar(puestoId, detectados, tope){
    var puesto = puestoDe(puestoId), ya = hechos();
    var faltantes = [], sinMaterial = [], k;

    for(k in puesto.temas){
      var pide = puesto.temas[k];
      var tiene = detectados[k] ? detectados[k].nivel : 0;
      var falta = pide - tiene;
      if(falta <= 0) continue;
      var pasos = TEMAS.pasosPorTema[k] || [];
      if(!pasos.length){ sinMaterial.push({ id: k, nombre: nombreTema(k), pide: pide }); continue; }
      faltantes.push({
        id: k, nombre: nombreTema(k), pide: pide, tiene: tiene,
        falta: falta, prioridad: pide * falta, pasos: pasos
      });
    }
    faltantes.sort(function(a,b){ return b.prioridad - a.prioridad; });

    /* Cuántos pasos por tema: el que más falta se lleva más. Se
       reparte por prioridad, no en partes iguales, porque un path
       plano no es un plan, es un índice. */
    var total = tope || 12, suma = 0, i;
    for(i=0;i<faltantes.length;i++) suma += faltantes[i].prioridad;

    var elegidos = [], usados = {};
    for(i=0;i<faltantes.length;i++){
      var f = faltantes[i];
      var cuota = suma ? Math.max(1, Math.round(total * f.prioridad / suma)) : 1;
      /* Nunca más de lo que te falta más uno, ni más de cuatro: un
         tema con diez pasos seguidos deja de ser un plan. */
      cuota = Math.min(cuota, f.falta + 1, 4);
      /* Empezar donde estás: si ya tienes nivel 2 del tema, los
         primeros pasos de la lista te los sabes. */
      var puestos = 0, j, desde = Math.min(f.tiene, Math.max(0, f.pasos.length - cuota));
      for(j=desde;j<f.pasos.length && puestos<cuota;j++){
        var p = f.pasos[j], clave = p.ruta + ":" + p.id;
        if(usados[clave] || ya[clave]) continue;   /* ni repetido ni ya hecho */
        usados[clave] = true; puestos++;
        elegidos.push({
          ruta: p.ruta, archivo: p.archivo, id: p.id, t: p.t, min: p.min,
          tema: f.id, temaNombre: f.nombre
        });
      }
    }

    /* Cuánto del puesto podemos enseñar, para poder decirlo. */
    var peso = 0, cubierto = 0;
    for(k in puesto.temas){
      peso += puesto.temas[k];
      if((TEMAS.pasosPorTema[k] || []).length) cubierto += puesto.temas[k];
    }

    var minutos = 0;
    for(i=0;i<elegidos.length;i++) minutos += elegidos[i].min;

    return {
      puesto: puesto,
      pasos: elegidos,
      faltantes: faltantes,
      sinMaterial: sinMaterial,
      minutos: minutos,
      cobertura: peso ? Math.round(100 * cubierto / peso) : 0
    };
  }

  /* Lo que el CV ya muestra, ordenado para poder mostrarlo. */
  function fuertes(detectados){
    var out = [], k;
    for(k in detectados){
      out.push({ id: k, nombre: nombreTema(k),
                 nivel: detectados[k].nivel, senales: detectados[k].senales });
    }
    out.sort(function(a,b){ return b.nivel - a.nivel; });
    return out;
  }

  /* Los PDF se leen con pdf.js. Si no carga (sin internet, o el CDN
     caído), el textarea sigue estando y la página no se rompe. */
  /* pdf.js descarga el texto en un worker aparte y hay que decirle
     de dónde sacarlo. Sin esto no falla: se queda esperando, que es
     peor, porque parece que no hiciste nada. */
  if(typeof pdfjsLib !== "undefined"){
    pdfjsLib.GlobalWorkerOptions.workerSrc =
      "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
  }


  function leerPDF(file, listo, falla){
    if(typeof pdfjsLib === "undefined"){ falla("No pude cargar el lector de PDF. Pega el texto en el recuadro de abajo."); return; }
    var fr = new FileReader();
    fr.onload = function(){
      pdfjsLib.getDocument({ data: new Uint8Array(fr.result) }).promise.then(function(doc){
        var partes = [], n;
        var seq = Promise.resolve();
        for(n=1;n<=doc.numPages;n++){
          (function(pag){
            seq = seq.then(function(){
              return doc.getPage(pag).then(function(p){
                return p.getTextContent().then(function(c){
                  var s = "", k;
                  for(k=0;k<c.items.length;k++) s += c.items[k].str + " ";
                  partes.push(s);
                });
              });
            });
          })(n);
        }
        seq.then(function(){ listo(partes.join("\n")); });
      })["catch"](function(){ falla("No pude leer ese PDF. Pega el texto a mano."); });
    };
    fr.onerror = function(){ falla("No pude abrir el archivo."); };
    fr.readAsArrayBuffer(file);
  }

  return { leer: leer, armar: armar, fuertes: fuertes, leerPDF: leerPDF,
           puestoDe: puestoDe, nombreTema: nombreTema };
})();
