# -*- coding: utf-8 -*-
"""cv.html: el path que sale de tu CV.

   Se compone desde semana.html, que ya trae la cabecera, el pie, el
   panel de cuenta y el tema. Lo unico propio son las tres secciones
   del medio y el bloque de JS que las maneja.

   El CV no se sube a ningun lado: se lee en el navegador y se cruza
   contra temas.js. Eso no es un detalle tecnico, es la promesa de la
   pagina, asi que se dice en pantalla y no en un pie de pagina.
"""
import io, re, sys, hashlib

D = u"C:/Users/Luca/Desktop/snowflake path/"


def uno(t, a, b, q):
    if t.count(a) != 1:
        print("  ABORTA [%s]: %d veces" % (q, t.count(a)))
        sys.exit(1)
    return t.replace(a, b)


t = io.open(D + u"semana.html", encoding="utf-8").read()

# --------------------------------------------------------------- colores
t = uno(t, u"""  --accent:        #0D7A5F;
  --accent-strong: #0A6650;
  --accent-soft:   #E9F7F2;
  --accent-line:   #B0E0D0;""",
           u"""  --accent:        #B45309;
  --accent-strong: #92400E;
  --accent-soft:   #FEF3E2;
  --accent-line:   #F0D5AE;""", "claro")
t = uno(t, u"""  --accent:        #34D399;
  --accent-strong: #6EE7B7;
  --accent-soft:   #06291F;
  --accent-line:   #12483A;""",
           u"""  --accent:        #FBBF24;
  --accent-strong: #FCD34D;
  --accent-soft:   #2C1D05;
  --accent-line:   #4A3410;""", "oscuro")

# ------------------------------------------------------------------- css
CSS = u"""
/* --- El CV: elegir puesto, pegar el texto, ver qué falta --------- */
.cv-paso{ margin-bottom:28px; }
.cv-num{
  display:inline-grid; place-items:center; width:22px; height:22px;
  border-radius:var(--r-pill); background:var(--accent-soft);
  color:var(--accent-strong); font-size:12px; font-weight:800;
  margin-right:9px;
}
.puestos{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:11px; }
.puesto{
  text-align:left; padding:14px 15px; border-radius:var(--r-lg);
  background:var(--surface); border:1.5px solid var(--divider);
  cursor:pointer; font:inherit; color:inherit;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.puesto:hover{ border-color:var(--accent-line); }
.puesto[aria-pressed="true"]{ border-color:var(--accent); background:var(--accent-soft); }
.puesto b{ display:block; font-size:14.5px; margin-bottom:4px; }
.puesto span{ font-size:12px; color:var(--text-2); line-height:1.5; }
.puesto .cob{
  display:inline-block; margin-top:9px; padding:2px 8px;
  border-radius:var(--r-pill); background:var(--surface-sunk);
  font-size:10.5px; font-weight:700; color:var(--text-3);
}
.puesto .cob.baja{ color:var(--warn); }

.cv-zona{
  border:1.5px dashed var(--divider); border-radius:var(--r-lg);
  background:var(--surface); padding:22px; text-align:center;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.cv-zona.encima{ border-color:var(--accent); background:var(--accent-soft); }
.cv-zona p{ font-size:13.5px; color:var(--text-2); margin:10px 0 0; }
.cv-o{ margin:14px 0 8px; font-size:12px; color:var(--text-3); }
#cvTexto{
  width:100%; min-height:130px; resize:vertical;
  padding:12px 13px; border-radius:var(--r-md);
  background:var(--surface-sunk); border:1px solid var(--divider);
  font:inherit; font-size:13px; color:var(--text); line-height:1.6;
}
#cvTexto:focus{ outline:2px solid var(--accent); outline-offset:1px; }
.cv-privado{
  display:flex; align-items:flex-start; gap:9px; margin-top:12px;
  padding:11px 13px; border-radius:var(--r-md);
  background:var(--surface-sunk); border:1px solid var(--divider-soft);
  font-size:12.5px; color:var(--text-2); line-height:1.55;
}
.cv-privado svg{ flex:none; color:var(--accent); margin-top:1px; }

.cv-res{ display:none; }
.cv-res.on{ display:block; }
.sabe{ display:flex; flex-wrap:wrap; gap:7px; margin-bottom:6px; }
.sabe span{
  padding:5px 11px; border-radius:var(--r-pill);
  background:var(--accent-soft); border:1px solid var(--accent-line);
  font-size:12px; font-weight:650; color:var(--accent-strong);
}
.sabe span.deduc{
  background:var(--surface-sunk); border-color:var(--divider);
  color:var(--text-3); font-weight:500;
}
.cv-lista{ list-style:none; margin:0; padding:0; }
.cv-lista li{
  display:flex; align-items:baseline; gap:13px; padding:12px 2px;
  border-top:1px solid var(--divider-soft);
}
.cv-lista li:first-child{ border-top:0; }
.cv-lista .tema{
  flex:0 0 auto; min-width:132px; font-size:11px; font-weight:800;
  letter-spacing:.05em; text-transform:uppercase; color:var(--text-3);
}
.cv-lista .qué{ flex:1 1 auto; font-size:14.5px; font-weight:600; }
.cv-lista .qué a{ color:inherit; text-decoration:none; }
.cv-lista .qué a:hover{ color:var(--accent); }
.cv-lista .rato{ flex:0 0 auto; font-size:12.5px; color:var(--text-3);
  font-variant-numeric:tabular-nums; }
.cv-hueco{
  margin-top:16px; padding:13px 15px; border-radius:var(--r-md);
  background:var(--warn-soft); border:1px solid var(--warn);
  font-size:13px; color:var(--text); line-height:1.6;
}
.cv-acc{ display:flex; gap:11px; flex-wrap:wrap; margin-top:22px; }
@media (max-width:560px){
  .cv-lista li{ flex-wrap:wrap; gap:4px 12px; }
  .cv-lista .qué{ flex:1 1 100%; order:3; }
}
"""
t = uno(t, u"\n</style>", CSS + u"\n</style>", "cierre style")

# ------------------------------------------------------------------ hero
t = uno(t, u'<p class="lema">Decidir cansa más que estudiar</p>',
           u'<p class="lema">Lo que ya sabes no hace falta estudiarlo</p>', "lema")
t = uno(t, u'<h1>Tu <span class="grad">semana</span></h1>',
           u'<h1>Tu ruta, desde tu <span class="grad">CV</span></h1>', "h1")
t = uno(t, u"Con quince rutas cargadas, el problema deja de ser el material y pasa a ser saber qué hacer un martes a las siete. Dime cuánto tiempo tienes y a qué apuntas, y te queda la semana escrita: qué día, cuánto rato y qué exactamente.",
           u"Quince rutas es mucho catálogo para alguien que solo quiere saber qué le falta. Pega tu CV, elige el puesto al que apuntas, y en vez del catálogo entero te queda la lista corta: lo que todavía no aparece en tu experiencia y dónde estudiarlo.",
        "hero lead")

# -------------------------------------------------------- las secciones
CUERPO = u"""<section class="section" id="config">
  <div class="wrap">

    <div class="cv-paso">
      <div class="section-head">
        <p class="eyebrow"><span class="cv-num">1</span>El puesto</p>
        <h2>A qué apuntas</h2>
        <p>El mismo CV necesita cosas distintas según a dónde vayas. Elige uno y después cámbialo las veces que quieras.</p>
      </div>
      <div class="puestos" id="puestos"></div>
    </div>

    <div class="cv-paso">
      <div class="section-head">
        <p class="eyebrow"><span class="cv-num">2</span>Tu experiencia</p>
        <h2>Cuenta qué hiciste</h2>
        <p>Con el CV alcanza. Si no lo tienes a mano, escribe en un renglón las herramientas que usaste y sirve igual.</p>
      </div>

      <div class="cv-zona" id="cvZona">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="color:var(--text-3)"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>
        <p><b>Suelta tu CV acá</b> o <button class="link-btn" type="button" id="cvElegir">elige el archivo</button></p>
        <p style="font-size:12px;color:var(--text-3);margin-top:6px">PDF o texto</p>
        <input type="file" id="cvFile" accept=".pdf,.txt,.md" hidden>
      </div>

      <p class="cv-o">o pega el texto directamente</p>
      <textarea id="cvTexto" placeholder="Data Analyst con 2 años de experiencia. SQL sobre Postgres, dashboards en Power BI, algo de Python con pandas..."></textarea>

      <div class="cv-privado">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <span><b>Tu CV no se sube a ningún lado.</b> Se lee en tu navegador y ahí se queda: no viaja a ningún servidor, no lo guardamos y no lo ve nadie. Puedes comprobarlo cortando internet antes de pegarlo.</span>
      </div>
    </div>

  </div>
</section>

<section class="section cv-res" id="resultado">
  <div class="wrap">

    <div class="cv-paso">
      <div class="section-head">
        <p class="eyebrow"><span class="cv-num">3</span>Lo que ya tienes</p>
        <h2 id="sabeTitulo">Esto no hace falta que lo estudies</h2>
        <p id="sabeSub"></p>
      </div>
      <div class="sabe" id="sabe"></div>
    </div>

    <div class="cv-paso">
      <div class="section-head">
        <p class="eyebrow"><span class="cv-num">4</span>Tu ruta</p>
        <h2 id="rutaTitulo">Lo que te falta</h2>
        <p id="rutaSub"></p>
      </div>
      <ul class="cv-lista" id="rutaLista"></ul>
      <div id="hueco"></div>
      <div class="cv-acc">
        <button class="btn-primary" type="button" id="guardarRuta">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/></svg>
          <span class="stack"><span class="verb">Guardar</span><span class="dest">como ruta mía</span></span>
        </button>
        <a class="btn-quiet" href="semana.html">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>
          <span class="stack"><span class="verb">Repartirla en</span><span class="dest">tu semana</span></span>
        </a>
      </div>
    </div>

  </div>
</section>
"""
ini = t.index(u'<section class="section" id="config">')
fin = t.index(u'<footer class="foot">')
t = t[:ini] + CUERPO + u"\n" + t[fin:]

# --------------------------------------------------------------- scripts
for nombre in (u"temas.js", u"cv.js"):
    h = hashlib.md5(io.open(D + nombre, "rb").read()).hexdigest()[:8]
    t = uno(t, u'<script src="plan.js',
            u'<script src="%s?v=%s"></script>\n<script src="plan.js' % (nombre, h),
            u"script " + nombre)

# --------------------------------- el bloque del planificador, por el del CV
ini = t.index(u"/* ============================================================\n   EL PLAN")
fin = t.index(u"/* ============================================================\n   ARRANQUE")
JS = u"""/* ============================================================
   EL CV \xb7 elegir puesto, leer el texto, mostrar lo que falta
   ============================================================ */
var puestoElegido = "data_engineer";
var ultimoTexto = "";
var ultimo = null;

function ratoLargo(min){
  var h = Math.floor(min / 60);
  if(h >= 10) return h + " horas";
  var m = min % 60;
  if(!h) return m + " min";
  return h + " h" + (m ? " " + m + " min" : "");
}

/* Cu\xe1nto de un puesto podemos ense\xf1ar. Se muestra siempre, tambi\xe9n
   cuando es poco: prometer una ruta completa para algo que no tenemos
   cubierto ser\xeda vender humo. */
function coberturaDe(p){
  var peso = 0, cub = 0, k;
  for(k in p.temas){
    peso += p.temas[k];
    if((TEMAS.pasosPorTema[k] || []).length) cub += p.temas[k];
  }
  return peso ? Math.round(100 * cub / peso) : 0;
}

function pintarPuestos(){
  var html = "", i;
  for(i=0;i<TEMAS.puestos.length;i++){
    var p = TEMAS.puestos[i], cob = coberturaDe(p);
    html += '<button class="puesto" type="button" data-puesto="' + p.id + '" ' +
      'aria-pressed="' + (p.id === puestoElegido ? "true" : "false") + '">' +
      '<b>' + esc(p.nombre) + '</b><span>' + esc(p.resumen) + '</span>' +
      '<span class="cob' + (cob < 90 ? " baja" : "") + '">' +
        (cob >= 100 ? "Material completo" : "Tenemos el " + cob + "% del temario") +
      '</span></button>';
  }
  var cont = document.getElementById("puestos");
  cont.innerHTML = html;
  var b = cont.querySelectorAll("[data-puesto]"), j;
  for(j=0;j<b.length;j++){
    b[j].addEventListener("click", function(){
      puestoElegido = this.getAttribute("data-puesto");
      pintarPuestos();
      if(ultimoTexto) analizar(ultimoTexto);
    });
  }
}

function analizar(texto){
  ultimoTexto = texto;
  var caja = document.getElementById("resultado");
  if(!texto || texto.replace(/\\s/g, "").length < 30){
    caja.classList.remove("on");
    return;
  }

  var det = CV.leer(texto);
  var r = CV.armar(puestoElegido, det, 12);
  ultimo = r;

  /* --- lo que ya tiene */
  var f = CV.fuertes(det), html = "", i;
  for(i=0;i<f.length;i++){
    var deduc = !f[i].senales.length;
    html += '<span class="' + (deduc ? "deduc" : "") + '" title="' +
      (deduc ? "No lo dice el CV, se deduce de lo dem\\u00e1s"
             : "En tu CV: " + esc(f[i].senales.join(", "))) + '">' +
      esc(f[i].nombre) + '</span>';
  }
  document.getElementById("sabe").innerHTML = html ||
    '<span class="deduc">No reconoc\\u00ed nada todav\\u00eda</span>';
  document.getElementById("sabeSub").textContent = f.length
    ? "Reconoc\\u00ed " + f.length + (f.length === 1 ? " tema" : " temas") +
      " en lo que escribiste. Pas\\u00e1 el mouse por cada uno para ver de d\\u00f3nde sale."
    : "Todav\\u00eda no reconoc\\u00ed ning\\u00fan tema. Prob\\u00e1 nombrando las herramientas que usaste.";

  /* --- lo que falta */
  var l = "", p;
  for(i=0;i<r.pasos.length;i++){
    p = r.pasos[i];
    l += '<li><span class="tema">' + esc(p.temaNombre) + '</span>' +
         '<span class="qu\\u00e9"><a href="' + esc(p.archivo) + '">' + esc(p.t) + '</a></span>' +
         '<span class="rato">' + ratoLargo(p.min) + '</span></li>';
  }
  document.getElementById("rutaLista").innerHTML = l ||
    '<li><span class="qu\\u00e9">Nada. Para este puesto tu CV ya cubre todo lo que tenemos.</span></li>';

  document.getElementById("rutaTitulo").textContent = r.pasos.length
    ? "Te faltan " + r.pasos.length + " pasos"
    : "No te falta nada de lo que tenemos";
  document.getElementById("rutaSub").textContent = r.pasos.length
    ? "Son " + ratoLargo(r.minutos) + " para " + r.puesto.nombre +
      ", contra las " + Math.round(totalDeTodo() / 60) + " horas del cat\\u00e1logo entero."
    : "Lo que sigue es practicar y presentarse.";

  /* --- lo que no podemos ense\\u00f1ar, dicho y no escondido */
  var h = "";
  if(r.sinMaterial.length){
    var nombres = [];
    for(i=0;i<r.sinMaterial.length;i++) nombres.push(r.sinMaterial[i].nombre);
    h = '<p class="cv-hueco"><b>Esto te falta y todav\\u00eda no lo cubrimos:</b> ' +
        esc(nombres.join(", ")) + '. No hay ninguna ruta con ese material, as\\u00ed que ' +
        'para eso vas a tener que buscar afuera. Prefiero dec\\u00edrtelo a que lo descubras a mitad de camino.</p>';
  }
  document.getElementById("hueco").innerHTML = h;

  caja.classList.add("on");
}

/* Las horas de todo el cat\\u00e1logo, para poder comparar contra la ruta
   corta. El n\\u00famero solo no dice nada; al lado del total, s\\u00ed. */
function totalDeTodo(){
  var rs = (typeof PASOS !== "undefined") ? PASOS : [], m = 0, i, j;
  for(i=0;i<rs.length;i++){
    for(j=0;j<rs[i].pasos.length;j++) m += rs[i].pasos[j].min;
  }
  return m;
}

/* Los PDF se leen con pdf.js. Si no carga (sin internet, o el CDN
   caído), el textarea sigue estando y la p\\u00e1gina no se rompe. */
/* pdf.js descarga el texto en un worker aparte y hay que decirle
   de dónde sacarlo. Sin esto no falla: se queda esperando, que es
   peor, porque parece que no hiciste nada. */
if(typeof pdfjsLib !== "undefined"){
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
}

function leerPDF(file, listo, falla){
  if(typeof pdfjsLib === "undefined"){ falla("No pude cargar el lector de PDF. Peg\\u00e1 el texto en el recuadro de abajo."); return; }
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
      seq.then(function(){ listo(partes.join("\\n")); });
    })["catch"](function(){ falla("No pude leer ese PDF. Peg\\u00e1 el texto a mano."); });
  };
  fr.onerror = function(){ falla("No pude abrir el archivo."); };
  fr.readAsArrayBuffer(file);
}

function tomarArchivo(file){
  if(!file) return;
  var caja = document.getElementById("cvTexto");
  if(/\\.pdf$/i.test(file.name)){
    toast("Leyendo el PDF...");
    leerPDF(file, function(txt){
      caja.value = txt.replace(/[ \\t]+/g, " ").trim();
      analizar(caja.value);
      toast("Listo, sali\\u00f3 de tu m\\u00e1quina y no fue a ning\\u00fan lado.");
    }, function(m){ toast(m); });
  }else{
    var fr = new FileReader();
    fr.onload = function(){ caja.value = fr.result; analizar(fr.result); };
    fr.readAsText(file);
  }
}

function guardarComoRuta(){
  if(!ultimo || !ultimo.pasos.length){ toast("Todav\\u00eda no hay ruta que guardar."); return; }
  var pf = activeProfile();
  if(!pf){ toast("Entr\\u00e1 con tu mail para guardarla y que te siga."); openAccount(); return; }
  pf.mias = pf.mias || [];
  var items = [], i;
  for(i=0;i<ultimo.pasos.length;i++){
    var p = ultimo.pasos[i];
    items.push({ ruta: p.ruta, id: p.id, t: p.t, min: p.min, tema: p.temaNombre });
  }
  pf.mias.push({
    id: "cv-" + Date.now(),
    nombre: "Mi ruta a " + ultimo.puesto.nombre,
    origen: "cv",
    items: items
  });
  if(PathSync.store.save()) toast("Guardada. La ves en Armar la m\\u00eda.");
  else toast("No pude guardarla en este navegador.");
}

"""
t = t[:ini] + JS + t[fin:]

# ----------------------------------------------- el arranque de la pagina
t = uno(t, u"""  cargarPlan();
  pintarObjetivo();
  pintarDias();
  pintarSemana();""",
        u"""  pintarPuestos();

  var zona = document.getElementById("cvZona");
  var input = document.getElementById("cvFile");
  document.getElementById("cvElegir").addEventListener("click", function(){ input.click(); });
  input.addEventListener("change", function(){ tomarArchivo(this.files[0]); });

  ["dragenter", "dragover"].forEach(function(e){
    zona.addEventListener(e, function(ev){ ev.preventDefault(); zona.classList.add("encima"); });
  });
  ["dragleave", "drop"].forEach(function(e){
    zona.addEventListener(e, function(ev){ ev.preventDefault(); zona.classList.remove("encima"); });
  });
  zona.addEventListener("drop", function(ev){
    if(ev.dataTransfer && ev.dataTransfer.files) tomarArchivo(ev.dataTransfer.files[0]);
  });

  /* Se analiza mientras escribe, pero no en cada tecla. */
  var reloj = null;
  document.getElementById("cvTexto").addEventListener("input", function(){
    var v = this.value;
    clearTimeout(reloj);
    reloj = setTimeout(function(){ analizar(v); }, 400);
  });

  document.getElementById("guardarRuta").addEventListener("click", guardarComoRuta);""",
        "arranque")

# los oyentes del planificador que ya no existen
t = re.sub(r"\n *document\.getElementById\(\"(objetivo|horas)\"\)\.addEventListener\("
           r"[\s\S]*?\n *\}\);", "", t)

io.open(D + u"cv.html", "w", encoding="utf-8", newline="").write(t)
print(u"cv.html escrito (%.1f KB)" % (len(t) / 1024.0))
