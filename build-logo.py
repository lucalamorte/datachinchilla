# -*- coding: utf-8 -*-
"""
build-logo.py

La chinchilla vive acá y en ningún otro lado. Este script escribe los dos
archivos sueltos, mete la marca en la barra y el pie de las cuatro páginas,
y deja el favicon en build-brand.py.

    python build-logo.py

Hay dos versiones a propósito. La completa lleva tablet y manos y sirve de
32 px para arriba: es la del og.png. La simple saca la tablet, porque a 16 y
20 px se convierte en una mancha, y es la que va en la barra y el favicon.
"""
import io, math, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- la cola
def cola(cx, cy, r_pico, r_valle, a_ini, a_fin, lobulos, cierre, afina=1.0):
    """Contorno con lóbulos que entran y salen, afinándose hacia la punta.

    La primera versión eran tres círculos y se leían como tres círculos. Un
    pelaje se dibuja con el borde ondulado, no con bultos sueltos: cada tramo
    sale hasta r_pico y vuelve a entrar hasta r_valle. Y una cola se afina,
    así que los lóbulos se achican de la base a la punta: con todos iguales
    queda un chorizo, no una cola.
    """
    def punto(ang, r):
        a = math.radians(ang)
        return (cx + r * math.cos(a), cy - r * math.sin(a))

    def escala(t):
        return 1.0 - (1.0 - afina) * t

    paso = (a_fin - a_ini) / float(lobulos)
    x, y = punto(a_ini, r_valle)
    d = [u"M %.2f %.2f" % (x, y)]
    for i in range(lobulos):
        a0 = a_ini + paso * i
        k0 = escala(i / float(lobulos))
        k1 = escala((i + 0.5) / float(lobulos))
        k2 = escala((i + 1) / float(lobulos))
        medio = punto(a0 + paso / 2.0, r_pico * k1)
        fin = punto(a0 + paso, r_valle * k2)
        d.append(u"Q %.2f %.2f %.2f %.2f" % (medio[0], medio[1], fin[0], fin[1]))
    d.append(cierre)
    d.append(u"Z")
    return u" ".join(d)


# el borde peludo mira a la izquierda; el lado derecho lo tapa el cuerpo
COLA = cola(cx=5.2, cy=15.2, r_pico=4.4, r_valle=2.7,
            a_ini=298, a_fin=134, lobulos=6, afina=0.72,
            cierre=u"C 4.4 10.6 7.6 10.0 9.4 11.8 C 10.6 14.2 10.4 17.2 9.6 19.4")

OREJAS = (u'<ellipse {B} cx="10.4" cy="5.3" rx="2.8" ry="3.4" transform="rotate(-21 10.4 5.3)"/>'
          u'<ellipse {B} cx="18.0" cy="5.3" rx="2.8" ry="3.4" transform="rotate(21 18.0 5.3)"/>'
          u'<ellipse {S} cx="10.6" cy="5.7" rx="1.4" ry="1.8" transform="rotate(-21 10.6 5.7)"/>'
          u'<ellipse {S} cx="17.8" cy="5.7" rx="1.4" ry="1.8" transform="rotate(21 17.8 5.7)"/>')

CUERPO = (u'<ellipse {B} cx="14.2" cy="17.2" rx="5.8" ry="5.2"/>'
          u'<circle {B} cx="14.2" cy="11.3" r="5.4"/>')

CARA = (u'<ellipse {K} cx="12.3" cy="10.8" rx=".85" ry="1.05"/>'
        u'<ellipse {K} cx="16.3" cy="10.8" rx=".85" ry="1.05"/>'
        u'<circle {B} cx="12.6" cy="10.4" r=".3"/>'
        u'<circle {B} cx="16.6" cy="10.4" r=".3"/>'
        u'<path {K} d="M13.6 12.5h1.4c.26 0 .41.29.25.5l-.7.92a.31.31 0 0 1-.5 0'
        u'l-.7-.92a.31.31 0 0 1 .25-.5Z"/>')

# Las manos van bien adentro de la tablet y con los dedos marcados: pegadas
# al borde se fundían con el cuerpo y no se veía que la agarra.
TABLET = (u'<rect {K} x="10.8" y="16.8" width="7.4" height="4.0" rx=".9" '
          u'transform="rotate(-15 14.5 18.8)"/>'
          u'<rect {S} x="11.6" y="17.5" width="4.4" height=".66" rx=".33" '
          u'transform="rotate(-15 14.5 18.8)"/>'
          u'<g transform="rotate(-15 14.5 18.8)">'
          u'<rect {B} x="10.5" y="18.6" width="2.7" height="2.5" rx="1.25"/>'
          u'<rect {K} x="11.35" y="18.7" width=".26" height="1.1" rx=".13"/>'
          u'<rect {K} x="12.2" y="18.75" width=".26" height="1.0" rx=".13"/>'
          u'<rect {B} x="15.8" y="18.6" width="2.7" height="2.5" rx="1.25"/>'
          u'<rect {K} x="16.65" y="18.7" width=".26" height="1.1" rx=".13"/>'
          u'<rect {K} x="17.5" y="18.75" width=".26" height="1.0" rx=".13"/>'
          u'</g>')


def formas(completa, b, s, k, t=None):
    """{T} es el tono de la cola.

    Del mismo color que el cuerpo se fundian en una sola mancha y la cola
    dejaba de leerse. Va un tono mezclado contra la superficie: en tema
    oscuro sale mas oscura que el cuerpo y en tema claro mas clara, asi que
    se despega en los dos sin necesidad de un color nuevo en la paleta.
    """
    partes = (u'<path {T} d="' + COLA + u'"/>') + OREJAS + CUERPO + CARA
    if completa:
        partes += TABLET
    return (partes.replace(u"{B}", b).replace(u"{S}", s)
                  .replace(u"{K}", k).replace(u"{T}", t or b))


def archivo(completa):
    """Versión suelta: se pinta sola si nadie le pasa variables."""
    return (u'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"\n'
            u'     fill="none" role="img" aria-label="DataChinchilla">\n'
            u'  <style>\n'
            u'    .body{fill:var(--accent,#38BDF8)}\n'
            u'    .soft{fill:var(--accent-soft,#BAE6FD)}\n'
            u'    .ink{fill:var(--surface,#0B1E2E)}\n'
            u'    .tail{fill:color-mix(in srgb, var(--accent,#38BDF8) 70%%, var(--surface,#0B1E2E))}\n'
            u'  </style>\n  %s\n</svg>\n'
           ) % formas(completa, u'class="body"', u'class="soft"', u'class="ink"',
                      u'class="tail"')


def enlinea(size, acc, soft):
    """Dentro de la página los colores van en el atributo.

    Un bloque <style> adentro de un SVG en línea se aplica a TODO el
    documento: clases como .body chocarían con el resto de la hoja.
    """
    return (u'<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" aria-hidden="true">%s</svg>'
           ) % (size, size, formas(False, u'fill="%s"' % acc, u'fill="%s"' % soft,
                                   u'fill="var(--surface)"',
                                   u'fill="color-mix(in srgb, %s 70%%, var(--surface))"' % acc))


if __name__ == "__main__":
    io.open(os.path.join(AQUI, "datachinchilla-mascot.svg"), "w", encoding="utf-8").write(archivo(True))
    io.open(os.path.join(AQUI, "datachinchilla-mark.svg"), "w", encoding="utf-8").write(archivo(False))
    print("datachinchilla-mascot.svg  y  datachinchilla-mark.svg")

    # index no tiene --accent: su acento se llama --ice
    COLOR = {
        "index.html":         (u"var(--ice)",    u"var(--ice-soft)"),
        "data-engineer.html": (u"var(--accent)", u"var(--accent-soft)"),
        "cs50.html":          (u"var(--accent)", u"var(--accent-soft)"),
        "armar.html":         (u"var(--accent)", u"var(--accent-soft)"),
    }
    VIEJA = re.compile(r'<svg width="(\d+)" height="\d+" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
                       r'(?:(?!</svg>).)*?cy="11\.3"(?:(?!</svg>).)*?</svg>', re.S)
    for pag, (acc, soft) in COLOR.items():
        p = os.path.join(AQUI, pag)
        t = io.open(p, encoding="utf-8").read()
        n = len(VIEJA.findall(t))
        if n != 2:
            sys.exit("%s: esperaba 2 chinchillas, hay %d" % (pag, n))
        t = VIEJA.sub(lambda m: enlinea(int(m.group(1)), acc, soft), t)
        io.open(p, "w", encoding="utf-8").write(t)
        print("%-22s barra y pie" % pag)

    # el favicon lleva colores fijos: no hay página que le pase variables
    FAV = (u'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
           u'<rect width="24" height="24" rx="5" fill="#0B1E2E"/>'
           u'<g transform="translate(12 12.2) scale(.88) translate(-12 -12.2)">'
           + formas(False, u'fill="#38BDF8"', u'fill="#BAE6FD"', u'fill="#0B1E2E"',
                     u'fill="#2A8DBB"') +
           u'</g></svg>')
    ruta = os.path.join(AQUI, "build-brand.py")
    b = io.open(ruta, encoding="utf-8").read()
    patron = re.compile(r'FAVICON = u""".*?"""', re.S)
    # lo que se chequea es que el patrón exista, no que el texto cambie:
    # correr el script dos veces seguidas no es un error
    if not patron.search(b):
        sys.exit("no encontré la línea FAVICON en build-brand.py")
    b2 = patron.sub(lambda m: u'FAVICON = u"""' + FAV + u'"""', b, count=1)
    io.open(ruta, "w", encoding="utf-8").write(b2)
    print("build-brand.py         favicon")
    print()
    print("Ahora corre:  python build-brand.py")
