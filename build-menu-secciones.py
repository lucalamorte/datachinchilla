# -*- coding: utf-8 -*-
u"""El menu, por secciones, con iconos y el tema adentro.

   Era una lista de ocho links seguidos, todos con el mismo peso: "Tu
   CV" al lado de "Preguntas" al lado de "Tu semana", sin que nada
   dijera que las tres primeras son tu camino y las dos ultimas son el
   sitio. Ocho cosas planas se leen como ocho cosas planas, y hay que
   leerlas todas para encontrar una.

   Ahora van en tres grupos con su rotulo, y cada uno con su icono. El
   rotulo hace el trabajo: mirando "TU CAMINO" ya sabes que abajo esta
   lo tuyo, sin leer las tres.

     TU CAMINO   tu CV, armarla a mano, tu semana
     ESTUDIAR    las rutas, la practica
     EL SITIO    recursos, preguntas

   Inicio queda arriba y suelto, que es de donde se vuelve.

   Y el tema pasa adentro, que es donde uno lo busca cuando ya
   aprendio que la barra es para lo que estas haciendo. El boton es EL
   MISMO, con su mismo id: todas las paginas lo enganchan por
   getElementById sin guardarse de que no exista, asi que se muda, no
   se duplica ni se reemplaza.

   Uso: python build-menu-secciones.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def i(d, w=17):
    return (u'<svg class="mi-ico" width="%d" height="%d" viewBox="0 0 24 24" '
            u'fill="none" stroke="currentColor" stroke-width="2" '
            u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            u'%s</svg>' % (w, w, d))


# (archivo, etiqueta, que es, icono)
GRUPOS = [
 (None, [
   ("index.html", u"Inicio", u"Por dónde empezar",
    u'<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>'),
 ]),
 (u"Tu camino", [
   ("cv.html", u"Tu CV", u"Tu ruta salida de tu experiencia",
    u'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>'),
   ("armar.html", u"Ármala a mano", u"Elegís los niveles y los ordenás",
    u'<path d="M4 6h7M4 12h16M4 18h11"/><circle cx="15" cy="6" r="2"/><circle cx="19" cy="18" r="2"/>'),
   ("semana.html", u"Tu semana", u"Qué día, cuánto rato y con qué",
    u'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
 ]),
 (u"Estudiar", [
   ("index.html#rutas", u"Todas las rutas", u"El catálogo entero",
    u'<path d="M4 19V6a2 2 0 0 1 2-2h13v15"/><path d="M6 17h13v4H6a2 2 0 0 1 0-4z"/>'),
   ("practica.html", u"Práctica diaria", u"Blind 75 y consultas de entrevistas",
    u'<path d="M9 6 4 12l5 6M15 6l5 6-5 6"/>'),
 ]),
 (u"El sitio", [
   ("recursos.html", u"Recursos", u"Gratis y no son cursos",
    u'<path d="M12 3 3 8l9 5 9-5z"/><path d="M3 13.5 12 18l9-4.5"/>'),
   ("preguntas.html", u"Preguntas", u"Si cuesta algo, qué pasa con tu CV",
    u'<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 1 1 3.4 2.5c-.6.2-.9.7-.9 1.3v.4"/><path d="M12 17.2h.01"/>'),
 ]),
]

TEMA = u'''  <div class="menu-sep"></div>
  <div class="menu-tema">
    <span class="mi-ico-caja">%s</span>
    <b>Modo oscuro</b>
%s  </div>
''' % (i(u'<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'), u"%s")


def panel(archivo, boton_tema):
    out = []
    for titulo, filas in GRUPOS:
        if titulo:
            out.append(u'  <p class="menu-t">%s</p>' % titulo)
        for destino, etiqueta, que, icono in filas:
            # Exacto y nada mas: en la portada, "Inicio" y "Todas las
            # rutas" empiezan los dos con index.html y se encendian
            # los dos. Donde estas es un solo lugar.
            aqui = (destino == archivo)
            out.append(
                u'  <a class="menu-i%s" href="%s"%s>'
                u'<span class="mi-ico-caja">%s</span>'
                u'<span class="mi-txt"><b>%s</b><span>%s</span></span></a>'
                % (u" aqui" if aqui else u"", destino,
                   u' aria-current="page"' if aqui else u"",
                   i(icono), etiqueta, que))
    out.append(TEMA % boton_tema)
    return (u'<nav class="menu" id="menuPanel" hidden aria-label="Secciones del sitio">\n' +
            u"\n".join(out) + u'\n</nav>\n')


CSS = u'''
/* --- El menu, por secciones ------------------------------------- */
/* Era una lista de ocho links con el mismo peso. Ocho cosas planas se
   leen como ocho cosas planas: hay que leerlas todas para encontrar
   una. Los rotulos hacen el trabajo de agrupar, y los iconos el de
   reconocer sin leer. */
.menu-t{
  margin:12px 12px 4px; font-size:10px; font-weight:800;
  letter-spacing:.1em; text-transform:uppercase; color:var(--text-3);
}
.menu-t:first-child{ margin-top:4px; }
/* En fila: el icono al lado del texto, no encima. `.menu-i` venia en
   columna de cuando la fila era solo <b> y <span>. */
.menu-i{ flex-direction:row; align-items:center; gap:11px; }
.mi-ico-caja{
  display:grid; place-items:center; flex-shrink:0;
  width:30px; height:30px; border-radius:var(--r-md);
  background:var(--surface-2); color:var(--text-2);
}
.menu-i.aqui .mi-ico-caja{ background:var(--marca-soft); color:var(--marca-strong); }
.mi-txt{ display:flex; flex-direction:column; gap:1px; min-width:0; }
.menu-sep{ height:1px; margin:8px 12px 4px; background:var(--divider); }
.menu-tema{
  display:flex; align-items:center; gap:11px;
  padding:8px 12px; margin:0 4px 4px;
}
.menu-tema b{ font-size:13.5px; font-weight:750; }
/* El boton del tema se mudo acá desde la barra. Es el mismo elemento
   con el mismo id: todas las paginas lo enganchan por getElementById
   sin guardarse de que no exista. */
.menu-tema #themeBtn{ margin-left:auto; }
'''


def main():
    n = 0
    for a in sorted(os.listdir(D)):
        if not a.endswith(".html"):
            continue
        p = os.path.join(D, a)
        t = io.open(p, encoding="utf-8").read()
        if u'id="menuPanel"' not in t or u'id="themeBtn"' not in t:
            continue
        if u"menu-t" in t:
            print(u"  %s: ya estaba" % a); continue

        # 1. sacar el boton del tema de la barra, guardandolo tal cual
        m = re.search(r'    <button class="icon-btn" id="themeBtn".*?</button>\n', t, re.S)
        if not m:
            print(u"  ABORTA en %s: no encuentro el boton del tema" % a); sys.exit(1)
        boton = m.group(0)
        t = t[:m.start()] + t[m.end():]
        # y sangrarlo para su lugar nuevo
        boton = boton.replace(u"    <button", u"    <button", 1)

        # 2. cambiar el panel entero
        m2 = re.search(r'<nav class="menu" id="menuPanel".*?</nav>\n', t, re.S)
        if not m2:
            print(u"  ABORTA en %s: no encuentro el panel" % a); sys.exit(1)
        t = t[:m2.start()] + panel(a, boton) + t[m2.end():]

        # 3. el estilo, al final del <style>
        k = t.index(u"</style>")
        t = t[:k] + CSS + t[k:]

        io.open(p, "w", encoding="utf-8", newline="").write(t)
        n += 1
    print(u"%d paginas con el menu por secciones y el tema adentro" % n)


main()
