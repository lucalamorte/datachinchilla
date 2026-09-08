# -*- coding: utf-8 -*-
u"""Arrastrar los bloques de la semana de un dia a otro.

   El repartidor tiene un criterio y esta explicado abajo del
   calendario: bloque largo para lo que se aprende, corto y todos los
   dias para lo que se practica, espaciado para que el tema descanse.
   Es un buen criterio y se queda. Pero es el unico, y hay cosas que
   el no sabe: que los martes tenes gimnasia, que el jueves llegas
   tarde, que preferis el bloque largo el sabado.

   El motor ya sabe mover -plan.js le puso clave a cada bloque y
   guarda a que dia lo mandaste-; esto es la mano.

   Arrastrar y soltar, con teclado tambien: los bloques son
   focusables y con las flechas izquierda y derecha se mueven de dia.
   Hacerlo solo con el mouse dejaria afuera a quien no puede usarlo, y
   ademas en el telefono arrastrar entre siete columnas es peor que
   dos toques.

   El dia donde va a caer se marca mientras arrastras: sin eso uno
   suelta a ciegas.

   Y aparece un boton para volver al orden sugerido, que solo esta si
   moviste algo: deshacer tiene que existir antes de que haga falta.

   Uso: python build-arrastrar.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "semana.html")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()
if u"data-clave" in t:
    print(u"  ya estaba"); sys.exit(1)

# ---------------------------------------------- 1. los bloques, arrastrables
t = cambiar(t,
u'''        html += '<a class="bloque ' + bl.tipo + '" href="' + bl.url + '">' +
                  '<span class="tipo">' + (bl.tipo === "practica" ? "Práctica" : bl.tipo === "repaso" ? "Repaso" : "Estudio") + '</span>' +
                  '<span class="qué">' + esc(bl.qué) + '</span>' +
                  '<span class="dur num">' + bl.min + ' min</span>' +
                '</a>';''',
u'''        /* Arrastrable, y con teclado tambien: es un link, asi que ya
           recibe foco, y con las flechas se mueve de dia. Solo con el
           mouse dejaria afuera a quien no puede usarlo, y en el
           telefono arrastrar entre siete columnas es peor que dos
           toques. */
        html += '<a class="bloque ' + bl.tipo + '" href="' + bl.url + '"' +
                  ' draggable="true" data-clave="' + esc(bl.clave) + '"' +
                  ' data-dia="' + d + '"' +
                  ' title="Arrástralo a otro día, o muévelo con las flechas">' +
                  '<span class="tipo">' + (bl.tipo === "practica" ? "Práctica" : bl.tipo === "repaso" ? "Repaso" : "Estudio") + '</span>' +
                  '<span class="qué">' + esc(bl.qué) + '</span>' +
                  '<span class="dur num">' + bl.min + ' min</span>' +
                '</a>';''',
u"el bloque")

t = cambiar(t,
u'''    html += '<div class="dia' + (dia.bloques.length ? "" : " libre") + (d === hoy ? " hoy" : "") + '">' +''',
u'''    html += '<div class="dia' + (dia.bloques.length ? "" : " libre") + (d === hoy ? " hoy" : "") +
              '" data-dia="' + d + '">' +''',
u"el dia")

# ---------------------------------------------- 2. el cableado
t = cambiar(t,
u'''  document.getElementById("semana").innerHTML = html;''',
u'''  document.getElementById("semana").innerHTML = html;
  engancharArrastre();''',
u"la llamada")

t = cambiar(t,
u'''/* Qué estás estudiando sale del CV: elegirlo acá era preguntar dos''',
u'''/* Arrastrar un bloque a otro día, y moverlo con las flechas.

   Se engancha después de cada pintada porque el HTML se rehace
   entero: escuchar en el contenedor sería otra opción, pero
   dragstart y drop necesitan el elemento igual. */
function engancharArrastre(){
  var caja = document.getElementById("semana");
  if(!caja) return;
  var arrastrando = null;

  var bl = caja.querySelectorAll(".bloque"), i;
  for(i=0;i<bl.length;i++){
    bl[i].addEventListener("dragstart", function(ev){
      arrastrando = this.getAttribute("data-clave");
      this.classList.add("va");
      try{
        ev.dataTransfer.setData("text/plain", arrastrando);
        ev.dataTransfer.effectAllowed = "move";
      }catch(e){}
    });
    bl[i].addEventListener("dragend", function(){
      this.classList.remove("va");
      var m = caja.querySelectorAll(".dia.cae"), z;
      for(z=0;z<m.length;z++) m[z].classList.remove("cae");
    });

    /* Con el teclado. Es un link, así que ya tiene foco; las flechas
       no hacen nada más acá, y con el bloque enfocado son lo que uno
       intentaría. */
    bl[i].addEventListener("keydown", function(ev){
      var paso = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
      if(!paso) return;
      ev.preventDefault();
      var d = parseInt(this.getAttribute("data-dia"), 10);
      var destino = (d + paso + 7) % 7;
      moverA(this.getAttribute("data-clave"), destino);
    });
  }

  var ds = caja.querySelectorAll(".dia"), j;
  for(j=0;j<ds.length;j++){
    ds[j].addEventListener("dragover", function(ev){
      if(!arrastrando) return;
      /* Sin esto el navegador no deja soltar: el default de dragover
         es "acá no se puede". */
      ev.preventDefault();
      try{ ev.dataTransfer.dropEffect = "move"; }catch(e){}
      this.classList.add("cae");
    });
    ds[j].addEventListener("dragleave", function(){ this.classList.remove("cae"); });
    ds[j].addEventListener("drop", function(ev){
      ev.preventDefault();
      this.classList.remove("cae");
      var clave = arrastrando;
      try{ clave = ev.dataTransfer.getData("text/plain") || clave; }catch(e){}
      arrastrando = null;
      moverA(clave, parseInt(this.getAttribute("data-dia"), 10));
    });
  }
}

/* Mueve, repinta y deja el foco en el bloque que se movió: con el
   teclado, perder el foco después de cada flecha obligaría a volver a
   buscarlo para dar el segundo paso. */
function moverA(clave, dia){
  if(!clave || !Plan.mover(clave, dia)) return;
  pintarSemana();
  var v = document.querySelector('.bloque[data-clave="' + clave + '"]');
  if(v) v.focus();
}

/* Qué estás estudiando sale del CV: elegirlo acá era preguntar dos''',
u"el cableado")

# ---------------------------------------------- 3. volver al orden sugerido
t = cambiar(t,
u'''  document.getElementById("planNota").innerHTML =
    "<b>Por qué está repartido así.</b> Lo que aprendes va en bloque largo y un tema por vez: " +''',
u'''  /* El botón para deshacer sólo aparece si moviste algo. Deshacer
     tiene que existir antes de que haga falta, pero un botón que no
     hace nada es ruido las otras veces. */
  var res = document.getElementById("volverOrden");
  if(res) res.hidden = !Plan.hayMovidos();

  document.getElementById("planNota").innerHTML =
    "<b>Por qué está repartido así.</b> Lo que aprendes va en bloque largo y un tema por vez: " +''',
u"el boton de deshacer")

t = cambiar(t,
u'''    <div class="semana" id="semana"></div>''',
u'''    <p class="semana-tip">
      Arrastra un bloque a otro día para acomodarlo a tu semana, o
      muévelo con las flechas ← y → teniéndolo seleccionado.
      <button class="btn-quiet" type="button" id="volverOrden" hidden>
        Volver al orden sugerido
      </button>
    </p>
    <div class="semana" id="semana"></div>''',
u"el aviso")

t = cambiar(t,
u'''.dia.libre{ background:var(--surface-2); border-style:dashed; }''',
u'''.dia.libre{ background:var(--surface-2); border-style:dashed; }
/* El día donde va a caer, mientras arrastras: sin esto uno suelta a
   ciegas. */
.dia.cae{
  border-color:var(--accent); border-style:solid;
  background:var(--accent-soft);
}
.semana-tip{
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  margin:0 0 12px; font-size:12.5px; color:var(--text-3);
}''',
u"el estilo del dia")

t = cambiar(t,
u'''a.bloque:hover{ border-color:var(--accent); }''',
u'''a.bloque:hover{ border-color:var(--accent); }
.bloque{ cursor:grab; }
.bloque:active{ cursor:grabbing; }
/* El que estás arrastrando, apagado: lo que se ve es a dónde va, no
   de dónde salió. */
.bloque.va{ opacity:.4; }
.bloque:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }''',
u"el estilo del bloque")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"semana.html: los bloques se arrastran y se mueven con las flechas")
