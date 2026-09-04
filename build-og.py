# -*- coding: utf-8 -*-
"""
build-og.py

Arma og.png, la imagen que se ve cuando alguien comparte el link. Escribe
un HTML de 1200x630 y lo fotografia con Chrome en modo headless, asi la
portada sale del mismo codigo y los mismos colores que las paginas en vez
de mantenerse a mano en un editor de imagenes.

    python build-og.py

La mascota viene de build-logo.py: si cambia el dibujo, se corre esto de
nuevo y la portada queda al dia.
"""
import io, os, subprocess, sys, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))

# build-logo.py lleva guion, asi que no se puede importar por nombre
_spec = importlib.util.spec_from_file_location("build_logo", os.path.join(AQUI, "build-logo.py"))
_logo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_logo)
formas = _logo.formas

BG      = u"#08192A"
ACC     = u"#38BDF8"
SOFT    = u"#BAE6FD"
INK     = u"#08192A"
COLA    = u"#2A8DBB"
TEXTO   = u"#F1F8FD"
TEXTO_2 = u"#93B4CA"

# los cuatro hitos del camino, con el color de su ruta
NODOS = [
    (u"#38BDF8", u'<path d="M12 2v20M2 12h20M4.9 4.9l14.2 14.2M19.1 4.9L4.9 19.1"/>'),
    (u"#A78BFA", u'<path d="M9 18l-6-6 6-6"/><path d="M15 6l6 6-6 6"/>'),
    (u"#F2707F", u'<ellipse cx="12" cy="5.5" rx="8" ry="3"/>'
                 u'<path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13"/>'
                 u'<path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
    (u"#34D399", u'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'),
]

# el camino serpentea igual que el mapa de las rutas, por abajo:
# cruzado con el titulo tapaba el texto
CURVA = (u"M 60 580 C 200 580 230 505 380 505 C 530 505 560 588 720 588 "
         u"C 880 588 910 498 1120 498")
PUNTOS = [(60, 580), (380, 505), (720, 588), (1120, 498)]


def nodo(x, y, color, icono):
    return (u'<g transform="translate(%d %d)">'
            u'<circle r="30" fill="%s" fill-opacity=".16" stroke="%s" stroke-width="2.5"/>'
            u'<g transform="translate(-12 -12)" fill="none" stroke="%s" stroke-width="2.2" '
            u'stroke-linecap="round" stroke-linejoin="round">%s</g>'
            u'</g>') % (x, y, color, color, color, icono)


def pagina():
    mascota = formas(True,
                     u'fill="%s"' % ACC, u'fill="%s"' % SOFT,
                     u'fill="%s"' % INK, u'fill="%s"' % COLA)
    camino = u"".join([nodo(p[0], p[1], NODOS[i][0], NODOS[i][1])
                       for i, p in enumerate(PUNTOS)])
    return u"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<style>
  *{ box-sizing:border-box; margin:0; padding:0; }
  body{
    width:1200px; height:630px; overflow:hidden; position:relative;
    background:
      radial-gradient(760px 520px at 82%% 12%%, rgba(56,189,248,.16), transparent 62%%),
      %(BG)s;
    color:%(TEXTO)s;
    font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;
  }
  .grilla{
    position:absolute; inset:0; opacity:.30;
    background-image:
      linear-gradient(rgba(147,180,202,.13) 1px, transparent 1px),
      linear-gradient(90deg, rgba(147,180,202,.13) 1px, transparent 1px);
    background-size:48px 48px;
  }
  .camino{ position:absolute; inset:0; }
  .txt{ position:absolute; left:74px; top:150px; width:600px; }
  h1{ font-size:76px; font-weight:800; letter-spacing:-.035em; line-height:1; }
  h1 .a{ color:%(ACC)s; }
  p.lead{ margin-top:26px; font-size:29px; line-height:1.34; color:%(TEXTO_2)s; }
  .lema{
    display:inline-block; margin-top:34px; padding:13px 26px;
    border:2px solid rgba(56,189,248,.55); border-radius:999px;
    font-size:21px; font-weight:600; color:%(ACC)s;
  }
  .bicho{ position:absolute; right:96px; top:172px; }
</style></head><body>
  <div class="grilla"></div>
  <svg class="camino" width="1200" height="630" viewBox="0 0 1200 630" fill="none">
    <path d="%(CURVA)s" stroke="%(ACC)s" stroke-opacity=".42" stroke-width="7"
          stroke-linecap="round" fill="none"/>
    %(CAMINO)s
  </svg>
  <div class="txt">
    <h1>Data<span class="a">Chinchilla</span></h1>
    <p class="lead">Rutas de estudio gratuitas y ordenadas para trabajar con datos.</p>
    <span class="lema">No planificar es planificar el fracaso</span>
  </div>
  <svg class="bicho" width="290" height="290" viewBox="0 0 24 24" fill="none">%(MASCOTA)s</svg>
</body></html>
""" % {"BG": BG, "TEXTO": TEXTO, "TEXTO_2": TEXTO_2, "ACC": ACC,
       "CURVA": CURVA, "CAMINO": camino, "MASCOTA": mascota}


CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

if __name__ == "__main__":
    html = os.path.join(AQUI, "og.html")
    png = os.path.join(AQUI, "og.png")
    io.open(html, "w", encoding="utf-8").write(pagina())
    print("og.html escrito")

    exe = None
    for c in CHROME:
        if os.path.exists(c):
            exe = c
            break
    if not exe:
        sys.exit("no encontre Chrome ni Edge: abri og.html y sacale una captura de 1200x630")

    subprocess.call([exe, "--headless", "--disable-gpu", "--hide-scrollbars",
                     "--screenshot=" + png, "--window-size=1200,630",
                     "--virtual-time-budget=2500",
                     "file:///" + html.replace("\\", "/")],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(png):
        print("og.png listo, %d KB" % (os.path.getsize(png) // 1024))
    else:
        sys.exit("la captura no salio")
