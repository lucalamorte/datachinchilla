# -*- coding: utf-8 -*-
u"""Producto: recursos, no una ruta.

   Se pidio agregar product manager junto a tester y analista
   funcional. Los otros dos entraron como rutas; este no, y la razon
   es la misma que hace que el sitio valga: cada paso de una ruta es
   un curso concreto, gratis, con horas y con algo al final. Para
   producto eso practicamente no existe. Lo bueno son libros,
   articulos y anos de equipo, y los cursos gratuitos que hay son
   folletos de escuelas pagas.

   Una ruta de producto quedaria floja al lado de las veinte, y una
   ruta floja no resta una ruta: resta credibilidad a las veinte.

   Lo que si se puede hacer bien es esto: mandar a las cuatro o cinco
   fuentes que la gente de producto de verdad lee. Marty Cagan, Shape
   Up de Basecamp, Lenny, Mind the Product. Son abiertas, son buenas y
   no pretenden ser un curso.

   De paso, la pagina tenia voseo -"si construis", "tenes uno",
   "escribime"- y el sitio es de tuteo en todos lados.

   Uso: python build-producto.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "recursos.html")

t = io.open(P, encoding="utf-8").read()
if "svpg.com" in t:
    print(u"  ya estaba"); sys.exit(1)

FLECHA = (u'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          u'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          u'<path d="M5 12h14M13 5l7 7-7 7"/></svg>')

# (titulo, etiqueta, que es, cuando sirve, url)
R = [
 (u"Silicon Valley Product Group",
  u"Artículos · en inglés",
  u"Marty Cagan escribe acá desde hace veinte años y es de donde salió media terminología que "
  u"usa la industria: equipos de producto contra equipos de funcionalidades, descubrimiento "
  u"contra entrega, por qué la mayoría de las hojas de ruta no sirven. Son artículos sueltos, "
  u"no un curso, y ésa es la forma honesta de aprender esto.",
  u"Cuando quieras entender qué hace un product manager que no sea administrar un tablero de tickets.",
  "https://www.svpg.com/articles/"),

 (u"Shape Up, de Basecamp",
  u"Libro completo · gratis · en inglés",
  u"El libro entero, abierto en la web. Cómo Basecamp arma su trabajo en ciclos de seis semanas "
  u"sin estimaciones ni sprints: apuestas en vez de compromisos, y alcance que se recorta en "
  u"lugar de plazos que se corren. Estés o no de acuerdo, discute lo que todos dan por sentado.",
  u"Cuando el proceso que tienes no funciona y no sabes qué otra cosa existe.",
  "https://basecamp.com/shapeup"),

 (u"Lenny's Newsletter",
  u"Newsletter · en inglés",
  u"Entrevistas y desgloses de cómo trabajan equipos de producto de empresas que conoces. Una "
  u"parte es de pago; lo abierto ya es más de lo que se lee en un año.",
  u"Cuando quieras saber cómo se hace algo concreto en una empresa que ya lo resolvió.",
  "https://www.lennysnewsletter.com/"),

 (u"Mind the Product",
  u"Artículos y charlas · en inglés",
  u"La comunidad más grande de producto que hay, con sus charlas y artículos abiertos. Es donde "
  u"se ve la variedad del oficio: no se parece nada un PM de una empresa de herramientas a uno "
  u"de una aplicación de consumo.",
  u"Cuando quieras ver el ancho del trabajo antes de decidir si es para ti.",
  "https://www.mindtheproduct.com/"),
]


def tarjeta(titulo, tag, que, cuando, url):
    return (u'      <article class="rec">\n'
            u'        <div class="rec-cab">\n'
            u'          <h3>%s</h3>\n'
            u'          <span class="rec-tag">%s</span>\n'
            u'        </div>\n'
            u'        <p>%s</p>\n'
            u'        <p class="rec-para"><b>Cuándo te sirve.</b> %s</p>\n'
            u'        <a class="rec-ir" href="%s" target="_blank" rel="noopener">Abrirlo %s</a>\n'
            u'      </article>\n' % (titulo, tag, que, cuando, url, FLECHA))


NUEVAS = u"".join(tarjeta(*r) for r in R)

# Van en su propio grupo, con su titulo: son de otra cosa que Laws of
# UX, y mezclarlas en la misma lista seria una pila.
BLOQUE = (u'    </div>\n\n'
          u'    <!-- Producto va como recursos y no como ruta: cada paso de una\n'
          u'         ruta es un curso concreto con horas y con algo al final, y\n'
          u'         para producto eso casi no existe. Lo bueno son libros y\n'
          u'         articulos, y esto es lo que la gente de producto lee. -->\n'
          u'    <div class="rec-grupo">\n'
          u'      <h2>Producto</h2>\n'
          u'      <p>No hay ruta de producto acá, y es a propósito: lo que se aprende de esto '
          u'no está en cursos, está en estos cuatro lugares. Una ruta floja al lado de las '
          u'veinte que sí lo son no ayudaría a nadie.</p>\n'
          u'    </div>\n'
          u'    <div class="recs">\n'
          + NUEVAS)

VIEJO_CIERRE = u'''      </article>
    </div>
    <p class="aporte" style="margin-top:18px">'''

NUEVO_CIERRE = (u'      </article>\n' + BLOQUE +
                u'    </div>\n'
                u'    <p class="aporte" style="margin-top:18px">')

if t.count(VIEJO_CIERRE) != 1:
    print(u"  ABORTA: el cierre de la lista aparece %d veces" % t.count(VIEJO_CIERRE))
    sys.exit(1)
t = t.replace(VIEJO_CIERRE, NUEVO_CIERRE, 1)

# --- el voseo que tenia la pagina
VOSEO = [
 (u"Si construís cualquier cosa que use alguien que no seas vos.",
  u"Si construyes cualquier cosa que use alguien que no seas tú."),
 (u"<b>¿Tenés uno que debería estar acá?</b>",
  u"<b>¿Tienes uno que debería estar acá?</b>"),
 (u">Escribime</a>", u">Escríbeme</a>"),
]
for v, n in VOSEO:
    if t.count(v) == 1:
        t = t.replace(v, n)

CSS = u'''
/* El titulo de un grupo de recursos. Producto no es lo mismo que una
   referencia de diseno: van separados y dichos. */
.rec-grupo{ margin:38px 0 16px; }
.rec-grupo h2{ font-size:20px; letter-spacing:-.02em; }
.rec-grupo p{ margin-top:6px; font-size:13.5px; color:var(--text-2); max-width:62ch; }
'''
t = t.replace(u"\n</style>", CSS + u"\n</style>", 1)

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"recursos.html: producto, y el voseo fuera")
