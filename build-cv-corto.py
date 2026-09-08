# -*- coding: utf-8 -*-
u"""Un CV demasiado corto no se lee, y hasta ahora no lo decia.

   pintar() vuelve sin hacer nada cuando el texto tiene menos de 30
   caracteres sin contar espacios. Es una decision razonable -con
   veinte letras no hay nada que leer- pero se tomaba en silencio: no
   aparecia el resultado, no aparecia un aviso, no aparecia nada.

   Desde afuera eso es indistinguible de "lo lei y no reconoci nada",
   que es una respuesta completamente distinta y bastante mas
   preocupante. En el reporte de prueba figura asi: se pego "No solo
   Python, tambien R." y se anoto que no reconocia nada, ni Python ni
   R. El motor reconoce Python en esa frase -esta comprobado con
   node-; lo que pasaba es que la frase tiene 22 caracteres y nunca
   llego al motor.

   Ahora lo dice, y dice cuanto falta. Solo cuando escribiste algo:
   con la caja vacia no hay nada que avisar.

   Uso: python build-cv-corto.py
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
if u'id="cvCorto"' in t:
    print(u"  ya estaba"); sys.exit(1)

# ------------------------------------------------------------- el aviso
t = cambiar(t,
u'''      <div class="cv-privado">''',
u'''      <p class="cv-corto" id="cvCorto" hidden role="status"></p>

      <div class="cv-privado">''',
u"el lugar del aviso")

# ------------------------------------------------------------- su estilo
t = cambiar(t,
u'''.cv-privado{''',
u'''/* Cuando escribiste algo pero es muy poco para leer. Antes esto no
   existia y la pagina se quedaba callada, que desde afuera es igual
   que "lo lei y no reconoci nada". */
.cv-corto{
  margin:10px 0 0; font-size:12.5px; color:var(--text-3);
}
.cv-corto b{ color:var(--text-2); font-weight:750; }
.cv-privado{''',
u"el estilo del aviso")

# ------------------------------------------------------- y que se muestre
t = cambiar(t,
u'''function pintar(texto){
  ultimoTexto = texto;
  var caja = document.getElementById("resultado");
  var hayPreg = Object.keys(Onb.estado.respuestas || {}).length >= 2;
  if((!texto || texto.replace(/\\s/g, "").length < 30) && !hayPreg){
    caja.classList.remove("on");
    return;
  }
''',
u'''function pintar(texto){
  ultimoTexto = texto;
  var caja = document.getElementById("resultado");
  var hayPreg = Object.keys(Onb.estado.respuestas || {}).length >= 2;
  var largo = texto ? texto.replace(/\\s/g, "").length : 0;

  /* Decirlo, en vez de no hacer nada.

     Con menos de 30 caracteres no hay nada que leer y la funcion
     volvia en silencio. Desde afuera eso es igual que "lo lei y no
     reconoci nada", que es otra respuesta y bastante peor. */
  var aviso = document.getElementById("cvCorto");
  if(aviso){
    var corto = largo > 0 && largo < 30 && !hayPreg;
    aviso.hidden = !corto;
    if(corto){
      aviso.innerHTML = "<b>Es muy poco para leer.</b> Escribe unas l\\u00edneas m\\u00e1s " +
        "-las herramientas que usaste alcanzan- o salta al paso 3 y agrega tus " +
        "skills a mano.";
    }
  }

  if((!texto || largo < 30) && !hayPreg){
    caja.classList.remove("on");
    return;
  }
''',
u"el cuerpo de pintar")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cv.html: un CV muy corto lo dice en vez de callarse")
