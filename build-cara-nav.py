# -*- coding: utf-8 -*-
"""La misma cara, tambien en el nav, el pie y el globo.

   El arreglo anterior toco chinchilla.css, o sea las poses. Pero el
   logo del nav, el del pie y el dibujo del globo de la guia son SVG
   escritos a mano dentro de cada HTML, con los colores puestos uno
   por uno. Ahi seguia la version vieja: cuerpo del color del acento
   -oscuro en claro- y ojo de --surface -blanco en claro-.

   Resultado: las poses con la cara nueva y el logo con la vieja, en
   la misma pantalla.

   Los tonos se suben a :root para que haya un solo lugar donde vive
   la cara, y los tres SVG de cada pagina pasan a usarlos.

   Uso: python build-cara-nav.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------- 1. los tonos, en un solo lugar
CSS_VIEJO = u""".chin-pose{
  width:104px; height:96px; overflow:visible;
  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-pata:   color-mix(in srgb, var(--accent) 86%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);
  --chin-luz:    #FFFFFF;
}
:root[data-theme="dark"] .chin-pose{
  --chin-cuerpo: var(--accent);
  --chin-pata:   var(--accent-strong);
}"""

CSS_NUEVO = u"""/* Los tonos de la cara viven aca y en ningun otro lado. Los usan las
   poses, el logo del nav, el del pie y el dibujo del globo, que son
   SVG escritos a mano dentro de cada HTML: sin esto habia que
   acordarse de tocar cuatro lugares y siempre quedaba uno viejo. */
:root{
  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-pata:   color-mix(in srgb, var(--accent) 86%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);
  --chin-luz:    #FFFFFF;
}
:root[data-theme="dark"]{
  --chin-cuerpo: var(--accent);
  --chin-pata:   var(--accent-strong);
}
.chin-pose{ width:104px; height:96px; overflow:visible; }"""

p = os.path.join(D, "chinchilla.css")
t = io.open(p, encoding="utf-8").read()
if CSS_VIEJO not in t:
    print(u"  ABORTA: no encuentro los tonos en chinchilla.css")
    sys.exit(1)
t = t.replace(CSS_VIEJO, CSS_NUEVO, 1)

# la de asoma ya no necesita las suyas: las hereda de :root
ASOMA_VIEJO = u"""/* La que se asoma en el pie, con la misma cara que las demas. */
.chin-asoma{
  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);
}
:root[data-theme="dark"] .chin-asoma{ --chin-cuerpo: var(--accent); }
"""
if ASOMA_VIEJO in t:
    t = t.replace(ASOMA_VIEJO, u"/* La que se asoma en el pie hereda los tonos de :root. */\n", 1)
io.open(p, "w", encoding="utf-8", newline="").write(t)
print(u"chinchilla.css: los tonos de la cara, en un solo lugar")

# --------------------------------------------- 2. los SVG de cada pagina
# Cada reemplazo trae el atributo entero con su coordenada, para que
# no se toque otra cosa que use el mismo color.
CAMBIOS = [
 # la cola y el pelaje de atras
 (u'<path fill="color-mix(in srgb, var(--accent) 70%, var(--surface))" d="M 6.47',
  u'<path fill="var(--chin-pata)" d="M 6.47'),
 # las orejas
 (u'<ellipse fill="var(--accent)" cx="10.4" cy="5.3"',
  u'<ellipse fill="var(--chin-cuerpo)" cx="10.4" cy="5.3"'),
 (u'<ellipse fill="var(--accent)" cx="18.0" cy="5.3"',
  u'<ellipse fill="var(--chin-cuerpo)" cx="18.0" cy="5.3"'),
 # el cuerpo y la cabeza
 (u'<ellipse fill="var(--accent)" cx="14.2" cy="17.2"',
  u'<ellipse fill="var(--chin-cuerpo)" cx="14.2" cy="17.2"'),
 (u'<circle fill="var(--accent)" cx="14.2" cy="11.3"',
  u'<circle fill="var(--chin-cuerpo)" cx="14.2" cy="11.3"'),
 # los ojos: eran --surface, que se invierte con el tema
 (u'<ellipse fill="var(--surface)" cx="12.3" cy="10.8"',
  u'<ellipse fill="var(--chin-ojo)" cx="12.3" cy="10.8"'),
 (u'<ellipse fill="var(--surface)" cx="16.3" cy="10.8"',
  u'<ellipse fill="var(--chin-ojo)" cx="16.3" cy="10.8"'),
 # el brillo: iba del color del acento sobre un ojo claro; con el ojo
 # oscuro tiene que ir claro o no se ve
 (u'<circle fill="var(--accent)" cx="12.6" cy="10.4"',
  u'<circle fill="var(--chin-luz)" cx="12.6" cy="10.4"'),
 (u'<circle fill="var(--accent)" cx="16.6" cy="10.4"',
  u'<circle fill="var(--chin-luz)" cx="16.6" cy="10.4"'),
 # el hocico
 (u'<path fill="var(--surface)" d="M13.6 12.5h1.4c',
  u'<path fill="var(--chin-ojo)" d="M13.6 12.5h1.4c'),
]

tocadas, total = 0, 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    ruta = os.path.join(D, a)
    t = io.open(ruta, encoding="utf-8").read()
    if 'fill="var(--surface)" cx="12.3"' not in t:
        continue
    n = 0
    for viejo, nuevo in CAMBIOS:
        c = t.count(viejo)
        if c:
            t = t.replace(viejo, nuevo)
            n += c
    io.open(ruta, "w", encoding="utf-8", newline="").write(t)
    tocadas += 1
    total += n

print(u"%d paginas, %d fills cambiados" % (tocadas, total))

# --------------------------------------------- 3. control: que no quede ninguno
sobran = []
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    t = io.open(os.path.join(D, a), encoding="utf-8").read()
    if 'fill="var(--surface)"' in t:
        sobran.append(a)
if sobran:
    print(u"  OJO, todavia queda un ojo pintado con --surface en: %s" % ", ".join(sobran))
else:
    print(u"no queda ninguna cara pintada con --surface")
