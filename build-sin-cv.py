# -*- coding: utf-8 -*-
u"""Sin CV tambien se puede: las preguntas dejan de ser inalcanzables.

   La pagina dice, en tres lugares distintos, que si no tenes el CV a
   mano las preguntas alcanzan. El globo del recorrido lo dice tambien
   en su paso 4: "Pega tu CV o contesta las preguntas para seguir".

   Y las preguntas viven adentro de la seccion de resultado, que solo
   se abre cuando hay treinta caracteres de CV leidos. O sea que para
   contestar las preguntas hacia falta el CV, que es exactamente lo
   que las preguntas venian a reemplazar.

   Sin CV el recorrido se traba en el paso 4 y no hay forma de seguir.
   Es el mismo tipo de callejon que el paso 9: el globo pide una accion
   que la pagina no deja hacer.

   El arreglo es un boton que lo diga: "No tengo el CV a mano". Abre el
   resultado con lo que haya -que puede no ser nada- y con eso quedan a
   la vista los skills, para agregarlos a mano, y las preguntas.

   No hace falta nada mas: la seccion de skills ya sabe estar vacia
   -"Todavia no reconoci ningun tema. Nombra las herramientas que
   usaste, o agregalas a mano aca abajo"- y el motor ya sabe armar una
   ruta a partir de respuestas sin CV.

   Uso: python build-sin-cv.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cv.html")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()
if u'id="sinCv"' in t:
    print(u"  ya estaba"); sys.exit(1)

# ------------------------------------------------------- 1. el boton
t = cambiar(t,
u'''      <p class="cv-corto" id="cvCorto" hidden role="status"></p>
''',
u'''      <p class="cv-corto" id="cvCorto" hidden role="status"></p>

      <!-- Sin esto, las preguntas no se podian contestar: viven en la
           seccion de resultado, que solo se abre con el CV leido. La
           pagina ofrecia las preguntas como reemplazo del CV y para
           llegar a ellas pedia el CV. -->
      <p class="cv-sincv">
        <button class="btn-quiet" type="button" id="sinCv">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
          No tengo el CV a mano
        </button>
        <span>Sigue igual: pones tus skills a mano y contestas unas preguntas.</span>
      </p>
''',
u"el boton")

# ------------------------------------------------------- 2. su estilo
t = cambiar(t,
u'''.cv-privado{''',
u'''/* El camino sin CV, al lado del que lo pide y con el mismo peso que
   "o pega el texto directamente": es una alternativa, no un descarte. */
.cv-sincv{
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  margin:14px 0 0;
}
.cv-sincv span{ font-size:12.5px; color:var(--text-3); }

.cv-privado{''',
u"el estilo")

# --------------------------------------------- 3. la puerta en pintar
t = cambiar(t,
u'''  if((!texto || largo < 30) && !hayPreg){
    caja.classList.remove("on");
    return;
  }''',
u'''  /* `sinCv` lo prende el boton "No tengo el CV a mano". Sin el, esta
     puerta dejaba las preguntas del otro lado: estan adentro de esta
     seccion, y esta seccion solo se abria con el CV leido. */
  if((!texto || largo < 30) && !hayPreg && !sinCv){
    caja.classList.remove("on");
    return;
  }''',
u"la puerta")

t = cambiar(t,
u'''    var corto = largo > 0 && largo < 30 && !hayPreg;''',
u'''    var corto = largo > 0 && largo < 30 && !hayPreg && !sinCv;''',
u"el aviso de texto corto")

# ------------------------------------------------- 4. el estado y el handler
t = cambiar(t,
u'''function pintar(texto){
  ultimoTexto = texto;''',
u'''/* Que dijiste que no tenes CV. No se guarda: es de esta visita, y si
   volves con el CV cargado la pagina lo lee y esto sobra. */
var sinCv = false;

function pintar(texto){
  ultimoTexto = texto;''',
u"la variable")

t = cambiar(t,
u'''  document.getElementById("guardarRuta").addEventListener("click", guardarComoRuta);''',
u'''  /* Abre el resultado con lo que haya, que puede no ser nada: con eso
     quedan a la vista los skills para ponerlos a mano y las preguntas,
     que es todo lo que hace falta para armar la ruta. */
  document.getElementById("sinCv").addEventListener("click", function(){
    sinCv = true;
    pintar(ultimoTexto || "");
    var p = document.getElementById("pasoPreg");
    if(p) p.scrollIntoView({ block: "center", behavior: "smooth" });
  });

  document.getElementById("guardarRuta").addEventListener("click", guardarComoRuta);''',
u"el handler")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cv.html: se puede seguir sin CV")
