# -*- coding: utf-8 -*-
u"""La pagina del CV, en pasos que se entienden.

   Tres cosas del mismo pedido.

   1. "Carga tu CV" era la unica entrada. Ahora dice lo que de verdad
      hace: sacar tus skills del CV, o que las pongas vos. El motor ya
      dejaba sacar con una cruz lo que no correspondia; faltaba lo
      simetrico, que es lo que hace falta cuando el CV esta viejo,
      cuando aprendiste algo por tu cuenta o cuando lo escribiste con
      otras palabras.

   2. Las cuatro preguntas salian las cuatro juntas, una abajo de la
      otra, con cuatro botones cada una: dieciseis botones en un
      bloque. Ahora va una por vez, con su flecha, y al contestar pasa
      sola a la siguiente.

      Y dejan de ser de datos. El sitio tiene diecisiete rutas y
      ocho puestos, la mitad de los cuales no toca una base de datos:
      preguntarle a alguien que quiere ser frontend si trabajo con
      pipelines es preguntarle por el trabajo de otro.

   3. El orden. Las preguntas estaban metidas adentro del paso del
      CV, como su letra chica. Pasan a ser su propio paso, y despues
      del de las skills: primero lo que sale de tu CV, despues lo que
      corregis vos, y recien ahi las preguntas para lo que quedo sin
      cubrir. Cinco pasos numerados en vez de cuatro.

   Uso: python build-cv-pasos.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cv.html")

t = io.open(P, encoding="utf-8").read()
if "agregarCaja" in t:
    print(u"  ya estaba"); sys.exit(1)


def cambiar(viejo, nuevo, veces=1):
    global t
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r x%d, esperaba %d" % (viejo[:56], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)


# ============================================================
# 1. El paso del CV: lo que hace, dicho
# ============================================================
cambiar(u'''        <p class="eyebrow"><span class="cv-num">2</span>Tu experiencia</p>
        <h2>Cuenta qué hiciste</h2>
        <p>Con el CV alcanza. Si no lo tienes a mano, escribe en un renglón las herramientas que usaste y sirve igual.</p>''',
        u'''        <p class="eyebrow"><span class="cv-num">2</span>Tu experiencia</p>
        <h2>Carga tu CV y saco tus skills</h2>
        <p>Con el CV alcanza: leo las herramientas que nombras y las dejo listas en el paso siguiente, donde sacas lo que no corresponda y agregas lo que falte. Si no lo tienes a mano, escribe en un renglón lo que usaste, o salta directo al paso 3 y ponlas a mano.</p>''')

# las preguntas se van de este paso: son su propio paso, y despues
cambiar(u'''      <p class="cv-otra">¿No lo tienes a mano?
        <button class="btn-quiet btn-preg" type="button" id="verPreg">Contesta cuatro preguntas</button>
      </p>
      <div id="pregCaja" hidden></div>

''', u"")


# ============================================================
# 2. El paso 3 pasa a ser el de las skills, con el agregar
# ============================================================
cambiar(u'''        <p class="eyebrow"><span class="cv-num">3</span>Lo que ya tienes</p>
        <h2 id="sabeTitulo">Esto ya lo tienes</h2>
        <p id="sabeSub"></p>
      </div>
      <div class="sabe" id="sabe"></div>
      <div class="sacados" id="sacados" hidden></div>
    </div>''',
        u'''        <p class="eyebrow"><span class="cv-num">3</span>Tus skills</p>
        <h2 id="sabeTitulo">Esto ya lo tienes</h2>
        <p id="sabeSub"></p>
      </div>
      <div class="sabe" id="sabe"></div>
      <div class="sacados" id="sacados" hidden></div>

      <!-- Lo simetrico de la cruz. Se podia restar y no sumar, que es
           lo que hace falta cuando el CV esta viejo, cuando
           aprendiste algo por tu cuenta o cuando lo escribiste con
           otras palabras. -->
      <div class="agregar">
        <button class="btn-quiet" type="button" id="agregarBtn">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          Agregar una que sepas
        </button>
        <div class="agregar-caja" id="agregarCaja" hidden></div>
      </div>
    </div>

    <div class="cv-paso" id="pasoPreg">
      <div class="section-head">
        <p class="eyebrow"><span class="cv-num">4</span>Para afinar</p>
        <h2>Cuatro preguntas, de a una</h2>
        <p id="pregSub">Lo que el CV no dice: hasta dónde llegas en cada cosa. Puedes saltarlas todas, la ruta sale igual.</p>
      </div>
      <div id="pregCaja"></div>
    </div>''')

cambiar(u'''        <p class="eyebrow"><span class="cv-num">4</span>Tu ruta</p>''',
        u'''        <p class="eyebrow"><span class="cv-num">5</span>Tu ruta</p>''')


# ============================================================
# 3. Las preguntas, de a una
# ============================================================
cambiar(u'''function pintarPreguntas(){
  var c = document.getElementById("pregCaja");
  var h = "", i, j;
  for(i=0;i<Onb.PREGUNTAS.length;i++){
    var p = Onb.PREGUNTAS[i], sel = Onb.estado.respuestas[p.id];
    h += '<div class="preg"><b class="preg-t">' + esc(p.texto) + '</b>' +
         '<i class="preg-a">' + esc(p.ayuda) + '</i><div class="preg-ops">';
    for(j=0;j<p.opciones.length;j++){
      h += '<button class="preg-op" type="button" data-p="' + p.id + '" data-o="' + j + '" ' +
           'aria-pressed="' + (sel === j) + '">' + esc(p.opciones[j].t) + '</button>';
    }
    h += "</div></div>";
  }
  c.innerHTML = h;
  var b = c.querySelectorAll("[data-p]"), k;
  for(k=0;k<b.length;k++){
    b[k].addEventListener("click", function(){
      Onb.estado.respuestas[this.getAttribute("data-p")] = parseInt(this.getAttribute("data-o"), 10);
      Onb.recalcularTemas();
      Onb.guardar();
      pintarPreguntas();
      analizar(document.getElementById("cvTexto").value);
    });
  }
}''',
        u'''/* En cuál de las preguntas estás. No se guarda: es de esta visita, y
   al volver conviene empezar por la primera sin contestar. */
var pregEn = 0;

function pintarPreguntas(){
  var c = document.getElementById("pregCaja");
  if(!c) return;
  var lista = Onb.PREGUNTAS, n = lista.length;

  /* Al abrir, en la primera sin contestar: seguir donde quedaste es
     mejor que volver a leer las que ya contestaste. */
  if(pregEn < 0) pregEn = 0;
  if(pregEn >= n) pregEn = n - 1;

  var p = lista[pregEn], sel = Onb.estado.respuestas[p.id], j;
  var listas = 0;
  for(j=0;j<n;j++){ if(Onb.estado.respuestas[lista[j].id] !== undefined) listas++; }

  var puntos = "";
  for(j=0;j<n;j++){
    puntos += '<button class="preg-pto' + (j === pregEn ? " aca" : "") +
      (Onb.estado.respuestas[lista[j].id] !== undefined ? " ok" : "") +
      '" type="button" data-ir="' + j + '" aria-label="Pregunta ' + (j + 1) +
      ' de ' + n + '" title="Pregunta ' + (j + 1) + '"></button>';
  }

  var ops = "";
  for(j=0;j<p.opciones.length;j++){
    ops += '<button class="preg-op" type="button" data-p="' + p.id + '" data-o="' + j + '" ' +
           'aria-pressed="' + (sel === j) + '">' + esc(p.opciones[j].t) + '</button>';
  }

  c.innerHTML =
    '<div class="preg una">' +
      '<div class="preg-cab">' +
        '<span class="preg-n">' + (pregEn + 1) + ' de ' + n + '</span>' +
        '<span class="preg-ptos">' + puntos + '</span>' +
      '</div>' +
      '<b class="preg-t">' + esc(p.texto) + '</b>' +
      '<i class="preg-a">' + esc(p.ayuda) + '</i>' +
      '<div class="preg-ops">' + ops + '</div>' +
      '<div class="preg-pie">' +
        '<button class="preg-fl" type="button" data-mueve="-1"' +
          (pregEn <= 0 ? " disabled" : "") + ' aria-label="La anterior">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>' +
          'Anterior</button>' +
        '<span class="preg-cuenta">' + listas + ' de ' + n + ' contestadas</span>' +
        '<button class="preg-fl" type="button" data-mueve="1"' +
          (pregEn >= n - 1 ? " disabled" : "") + ' aria-label="La siguiente">' +
          'Siguiente' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>' +
          '</button>' +
      '</div>' +
    '</div>';

  var b = c.querySelectorAll("[data-p]"), k;
  for(k=0;k<b.length;k++){
    b[k].addEventListener("click", function(){
      Onb.estado.respuestas[this.getAttribute("data-p")] = parseInt(this.getAttribute("data-o"), 10);
      Onb.recalcularTemas();
      Onb.guardar();
      /* Contestar pasa a la siguiente: quedarse mirando la que acabas
         de contestar no es lo que uno quiere hacer despues. */
      if(pregEn < Onb.PREGUNTAS.length - 1) pregEn++;
      pintarPreguntas();
      analizar(document.getElementById("cvTexto").value);
    });
  }
  var fl = c.querySelectorAll("[data-mueve]");
  for(k=0;k<fl.length;k++){
    fl[k].addEventListener("click", function(){
      pregEn += parseInt(this.getAttribute("data-mueve"), 10);
      pintarPreguntas();
    });
  }
  var pt = c.querySelectorAll("[data-ir]");
  for(k=0;k<pt.length;k++){
    pt[k].addEventListener("click", function(){
      pregEn = parseInt(this.getAttribute("data-ir"), 10);
      pintarPreguntas();
    });
  }
}

/* La primera sin contestar. Se usa al abrir la pagina: volver a la
   uno cuando ya contestaste tres es hacerte pasar por lo mismo. */
function pregPrimeraSinContestar(){
  var l = Onb.PREGUNTAS, i;
  for(i=0;i<l.length;i++){
    if(Onb.estado.respuestas[l[i].id] === undefined) return i;
  }
  return 0;
}


/* ============================================================
   AGREGAR UNA SKILL A MANO
   ============================================================ */
/* El motor dejaba sacar con una cruz lo que no correspondia y no
   dejaba sumar nada. Un CV viejo, algo que aprendiste por tu cuenta o
   una herramienta escrita con otras palabras no tenian forma de
   entrar. */
function pintarAgregar(){
  var caja = document.getElementById("agregarCaja");
  if(!caja || typeof CV === "undefined" || !CV.temas) return;

  var det = Onb.estado.temas || {};
  var todos = CV.temas(), h = "", i, tm;
  for(i=0;i<todos.length;i++){
    tm = todos[i];
    if(det[tm.id]) continue;          /* ya lo tienes: no hay nada que sumar */
    h += '<button class="chip-mas" type="button" data-suma="' + esc(tm.id) + '">' +
         esc(tm.nombre) + '</button>';
  }
  caja.innerHTML = h ||
    '<p class="agregar-nada">Ya tienes todos los temas que conozco.</p>';

  var b = caja.querySelectorAll("[data-suma]"), k;
  for(k=0;k<b.length;k++){
    b[k].addEventListener("click", function(){
      Onb.agregarTema(this.getAttribute("data-suma"), true);
      analizar(document.getElementById("cvTexto").value);
      pintarAgregar();
    });
  }
}''')


# ============================================================
# 4. Enganches: el boton de agregar, y las preguntas ya abiertas
# ============================================================
cambiar(u'''  document.getElementById("verPreg").addEventListener("click", function(){
    var c = document.getElementById("pregCaja");
    c.hidden = !c.hidden;
    this.textContent = c.hidden ? "Contesta cuatro preguntas" : "Listo, cerrar";
    if(!c.hidden) pintarPreguntas();
  });

  /* Si ya contesto antes, se muestran abiertas. */
  if(Object.keys(Onb.estado.respuestas || {}).length){
    document.getElementById("pregCaja").hidden = false;
    document.getElementById("verPreg").textContent = "Listo, cerrar";
    pintarPreguntas();
  }''',
        u'''  /* Las preguntas son un paso propio y estan siempre a la vista:
     antes vivian adentro del paso del CV, detras de un boton, como
     si fueran su letra chica. */
  pregEn = pregPrimeraSinContestar();
  pintarPreguntas();

  /* Agregar a mano lo que el CV no dijo. */
  var ab = document.getElementById("agregarBtn");
  if(ab) ab.addEventListener("click", function(){
    var c = document.getElementById("agregarCaja");
    c.hidden = !c.hidden;
    if(!c.hidden) pintarAgregar();
  });''')


# ============================================================
# 5. Como se ve
# ============================================================
CSS = u'''
/* --- Agregar una skill a mano ------------------------------------ */
.agregar{ margin-top:16px; }
.agregar-caja{
  display:flex; flex-wrap:wrap; gap:7px; margin-top:12px;
  padding:14px; border-radius:var(--r-lg);
  background:var(--surface-sunk); border:1px solid var(--divider);
}
.agregar-caja[hidden]{ display:none; }
.chip-mas{
  padding:6px 12px; border-radius:var(--r-pill); cursor:pointer;
  background:var(--surface); border:1px solid var(--divider);
  font:inherit; font-size:12.5px; font-weight:650; color:var(--text-2);
}
.chip-mas:hover{ border-color:var(--accent); color:var(--accent-strong); }
.agregar-nada{ font-size:12.5px; color:var(--text-3); margin:0; }
/* El que pusiste vos se distingue del que salio del CV: son dos cosas
   distintas y una es tu palabra. */
.chip-sabe.mano{ border-style:dashed; }

/* --- Las preguntas, de a una ------------------------------------- */
.preg.una{
  padding:20px; border-radius:var(--r-lg);
  background:var(--surface); border:1px solid var(--divider);
}
.preg-cab{ display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.preg-n{
  font-size:11px; font-weight:800; letter-spacing:.08em;
  text-transform:uppercase; color:var(--text-3);
}
.preg-ptos{ display:inline-flex; gap:6px; margin-left:auto; }
.preg-pto{
  width:8px; height:8px; padding:0; border-radius:50%; cursor:pointer;
  border:1px solid var(--divider); background:var(--surface-sunk);
}
.preg-pto.ok{ background:var(--accent-line); border-color:var(--accent-line); }
.preg-pto.aca{ background:var(--accent); border-color:var(--accent); }
.preg-pie{
  display:flex; align-items:center; gap:12px; margin-top:16px;
  padding-top:14px; border-top:1px solid var(--divider-soft);
}
.preg-fl{
  display:inline-flex; align-items:center; gap:6px;
  padding:6px 12px; border-radius:var(--r-pill); cursor:pointer;
  background:none; border:1px solid var(--divider);
  font:inherit; font-size:12.5px; font-weight:700; color:var(--text-2);
}
.preg-fl:hover:not(:disabled){ border-color:var(--accent); color:var(--accent); }
.preg-fl:disabled{ opacity:.4; cursor:default; }
.preg-fl:last-child{ margin-left:auto; }
.preg-cuenta{
  font-size:11.5px; color:var(--text-3); font-variant-numeric:tabular-nums;
}
@media (max-width:560px){
  .preg-cuenta{ display:none; }
}
'''
cambiar(u"\n</style>", CSS + u"\n</style>")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cv.html: cinco pasos, skills a mano y preguntas de a una")
