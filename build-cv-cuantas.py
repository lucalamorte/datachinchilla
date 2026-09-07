# -*- coding: utf-8 -*-
u""""Quince rutas es mucho catalogo" cuando ya son diecisiete.

   Es el mismo numero escrito a mano que tenia el armador, en otra
   pagina. Cada ruta nueva lo deja mas viejo, y nadie va a acordarse
   de subirlo.

   cv.html ya carga pasos.js. El numero sale de ahi.

   Uso: python build-cv-cuantas.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cv.html")

VIEJO = u'''    <p class="hero-lead">Quince rutas es mucho catálogo para alguien'''
NUEVO = u'''    <p class="hero-lead"><b id="cuantasRutas">17</b> rutas es mucho catálogo para alguien'''

# el script, junto al resto del arranque de la pagina
ANCLA = u'''<script src="pasos.js'''

RELLENO = u'''<script>
/* El numero del titulo sale de pasos.js. Escrito a mano decia quince
   cuando ya eran diecisiete: el mismo error que tenia el armador, en
   otra pagina. */
window.addEventListener("DOMContentLoaded", function(){
  var n = document.getElementById("cuantasRutas");
  if(n && typeof PASOS !== "undefined" && PASOS.length) n.textContent = PASOS.length;
});
</script>
'''

t = io.open(P, encoding="utf-8").read()
if 'id="cuantasRutas"' in t:
    print(u"  ya estaba"); sys.exit(1)
if t.count(VIEJO) != 1:
    print(u"  ABORTA: el titulo aparece %d veces" % t.count(VIEJO)); sys.exit(1)
t = t.replace(VIEJO, NUEVO, 1)

i = t.rindex("</body>")
t = t[:i] + RELLENO + t[i:]

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cv.html: el numero de rutas sale de pasos.js")
