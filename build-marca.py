# -*- coding: utf-8 -*-
u"""Que el sitio no cambie de color entero en cada pagina.

   Cada ruta tiene su acento -CS50 el carmesi de Harvard, dbt el
   naranja, Airflow el verde azulado- y eso esta bien: sirve para
   saber de un vistazo en cual estas. El problema es que ese acento
   era el unico color del sitio, asi que se lo llevaba TODO: el logo,
   la chinchilla del nav, la del pie, la de los globos, los botones de
   la barra, el menu y el pie.

   O sea que la marca cambiaba de color en cada pagina. Una marca que
   cambia de color no es una marca.

   La separacion:

   - `--marca` es DataChinchilla, y es la misma en las 30 paginas: el
     violeta de la portada. La lleva todo lo que es el sitio y no la
     pagina -el logo, la chinchilla, la barra, el menu, el pie-.

   - `--accent` sigue siendo el color de la ruta, y se queda con lo
     que es de la ruta: el titulo, el mapa, los nodos, la barra de
     avance, las insignias. Ahi el color distingue, que es para lo que
     estaba.

   La chinchilla es el caso mas claro: es la cara del sitio, no un
   adorno de la pagina. Que fuera carmesi en CS50 y naranja en dbt la
   convertia en un elemento decorativo mas.

   Se tocan las 30 paginas y los generadores, para que las que vengan
   nazcan bien.

   Uso: python build-marca.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

# El violeta de la portada, que ya era el de la marca.
MARCA_CLARO = (u"  /* La marca, igual en las 30 páginas. El acento de abajo es de\n"
               u"     esta página; esto es del sitio. */\n"
               u"  --marca:         #6D28D9;\n"
               u"  --marca-strong:  #5B21B6;\n"
               u"  --marca-soft:    #EDE9FE;\n")
MARCA_OSCURO = (u"  --marca:         #A78BFA;\n"
                u"  --marca-strong:  #C4B5FD;\n"
                u"  --marca-soft:    #2A1D4D;\n")

# El chrome: lo que es del sitio y no de la pagina.
CHROME = [
 (u'.icon-btn:hover{ color:var(--accent-strong); border-color:var(--accent); }',
  u'.icon-btn:hover{ color:var(--marca-strong); border-color:var(--marca); }'),
 (u'.acct:hover{ color:var(--accent-strong); border-color:var(--accent); }',
  u'.acct:hover{ color:var(--marca-strong); border-color:var(--marca); }'),
 (u'.foot .foot-links a:hover{ color:var(--accent-strong); }',
  u'.foot .foot-links a:hover{ color:var(--marca-strong); }'),
 (u'.menu-i.aqui{ background:var(--accent-soft); }',
  u'.menu-i.aqui{ background:var(--marca-soft); }'),
 (u'.menu-i.aqui b{ color:var(--accent-strong); }',
  u'.menu-i.aqui b{ color:var(--marca-strong); }'),
]


def poner_tokens(t, archivo):
    """Los tokens de marca, adentro de los dos :root que ya existen."""
    if u"--marca:" in t:
        return t, 0
    m = re.search(r"(:root\{\n)(.*?)(\n\})", t, re.S)
    if not m:
        print(u"  ABORTA en %s: no encuentro el :root claro" % archivo); sys.exit(1)
    t = t[:m.start(2)] + MARCA_CLARO + m.group(2) + t[m.end(2):]

    m = re.search(r"(:root\[data-theme=\"dark\"\]\{\n)(.*?)(\n\})", t, re.S)
    if not m:
        print(u"  ABORTA en %s: no encuentro el :root oscuro" % archivo); sys.exit(1)
    t = t[:m.start(2)] + MARCA_OSCURO + m.group(2) + t[m.end(2):]
    return t, 1


n_pag = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_") or a == "og.html":
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if u"--accent:" not in t:
        continue
    antes = t

    t, _ = poner_tokens(t, a)

    # Las orejas de la cara del nav, del pie y del globo: van con la marca.
    t = t.replace(u'fill="var(--accent-soft)"', u'fill="var(--marca-soft)"')

    for viejo, nuevo in CHROME:
        t = t.replace(viejo, nuevo)

    if t != antes:
        io.open(p, "w", encoding="utf-8", newline="").write(t)
        n_pag += 1

print(u"%d paginas con la marca aparte del acento" % n_pag)


# ------------------------------------------------------- la chinchilla
C = os.path.join(D, "chinchilla.css")
c = io.open(C, encoding="utf-8").read()
if u"--marca" in c:
    print(u"  chinchilla.css: ya estaba")
else:
    v = u'''  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-pata:   color-mix(in srgb, var(--accent) 86%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);'''
    n = u'''  /* De la marca y no del acento de la pagina. Era carmesi en CS50 y
     naranja en dbt: la cara del sitio cambiando de color en cada
     pagina es un adorno, no una cara. */
  --chin-cuerpo: color-mix(in srgb, var(--marca) 68%, #FFFFFF);
  --chin-pata:   color-mix(in srgb, var(--marca) 86%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--marca) 26%, #0E0A16);'''
    if c.count(v) != 1:
        print(u"  ABORTA en chinchilla.css: los tonos claros aparecen %d veces" % c.count(v)); sys.exit(1)
    c = c.replace(v, n, 1)

    v2 = u'''  --chin-cuerpo: var(--accent);
  --chin-pata:   var(--accent-strong);'''
    n2 = u'''  --chin-cuerpo: var(--marca);
  --chin-pata:   var(--marca-strong);'''
    if c.count(v2) != 1:
        print(u"  ABORTA en chinchilla.css: los tonos oscuros aparecen %d veces" % c.count(v2)); sys.exit(1)
    c = c.replace(v2, n2, 1)

    # Lo que rodea a la chinchilla y es de ella, no de la pagina.
    for viejo, nuevo in [
      (u'.chin-pose .c-oreja-in{ fill:var(--accent-soft); }',
       u'.chin-pose .c-oreja-in{ fill:var(--marca-soft); }'),
      (u'.chin-pose .c-z{\n  fill:var(--accent-strong);',
       u'.chin-pose .c-z{\n  fill:var(--marca-strong);'),
      (u'.chin-pose .c-fiesta rect{ fill:var(--accent-strong); }',
       u'.chin-pose .c-fiesta rect{ fill:var(--marca-strong); }'),
      (u'.chin-pose .c-tierra circle{ fill:color-mix(in srgb, var(--accent) 55%, transparent); }',
       u'.chin-pose .c-tierra circle{ fill:color-mix(in srgb, var(--marca) 55%, transparent); }'),
      (u'.chin-pose .c-lupa-c{\n  fill:color-mix(in srgb, var(--accent) 12%, transparent);\n  stroke:var(--accent-strong); stroke-width:3.4;\n}',
       u'.chin-pose .c-lupa-c{\n  fill:color-mix(in srgb, var(--marca) 12%, transparent);\n  stroke:var(--marca-strong); stroke-width:3.4;\n}'),
      (u'.chin-pose .c-lupa-m{\n  stroke:var(--accent-strong); stroke-width:4; stroke-linecap:round; fill:none;\n}',
       u'.chin-pose .c-lupa-m{\n  stroke:var(--marca-strong); stroke-width:4; stroke-linecap:round; fill:none;\n}'),
      (u'.chin-pose .c-hueso{\n  fill:none; stroke:var(--accent); stroke-width:7.5; stroke-linecap:round;\n}',
       u'.chin-pose .c-hueso{\n  fill:none; stroke:var(--marca); stroke-width:7.5; stroke-linecap:round;\n}'),
      (u'.chin-pose .c-remache{ fill:var(--accent-strong); }',
       u'.chin-pose .c-remache{ fill:var(--marca-strong); }'),
      (u'.chin-pose .c-faja{ fill:var(--accent-strong); }',
       u'.chin-pose .c-faja{ fill:var(--marca-strong); }'),
    ]:
        if c.count(viejo) != 1:
            print(u"  ABORTA en chinchilla.css: %r x%d" % (viejo[:44], c.count(viejo))); sys.exit(1)
        c = c.replace(viejo, nuevo, 1)

    io.open(C, "w", encoding="utf-8", newline="").write(c)
    print(u"chinchilla.css: la cara es de la marca, no de la pagina")


# ------------------------------------------------- y los generadores
for gen, cambios in [
  ("build-menu.py", [
    (u'.menu-i.aqui{ background:var(--accent-soft); }',
     u'.menu-i.aqui{ background:var(--marca-soft); }'),
    (u'.menu-i.aqui b{ color:var(--accent-strong); }',
     u'.menu-i.aqui b{ color:var(--marca-strong); }'),
  ]),
  ("build-cara-nav.py", [(u'var(--accent-soft)', u'var(--marca-soft)')]),
  ("build-cara.py",     [(u'var(--accent-soft)', u'var(--marca-soft)')]),
]:
    p = os.path.join(D, gen)
    if not os.path.exists(p):
        continue
    g = io.open(p, encoding="utf-8").read()
    antes = g
    for viejo, nuevo in cambios:
        g = g.replace(viejo, nuevo)
    if g != antes:
        io.open(p, "w", encoding="utf-8", newline="").write(g)
        print(u"%-20s al dia" % gen)
