# -*- coding: utf-8 -*-
"""Pone al dia el ?v= de cada script local en cada pagina.

   Los archivos compartidos (tema.css, path-sync.js, pasos.js, plan.js,
   temas.js, cv.js) se piden con un ?v= que es el hash del contenido, para que el
   navegador no sirva una version vieja. Cuando uno se regenera, ese
   numero queda mentido en las paginas que lo cargan y el navegador
   entrega lo de antes: el sintoma es una pagina que "no toma" un
   cambio que si esta en el archivo.

   Se corre despues de tocar cualquier .js o .css compartido.
"""
import io, os, re, glob, hashlib

D = u"C:/Users/Luca/Desktop/snowflake path/"

hashes = {}
for f in glob.glob(D + u"*.js") + glob.glob(D + u"*.css"):
    nombre = os.path.basename(f)
    hashes[nombre] = hashlib.md5(io.open(f, "rb").read()).hexdigest()[:8]

cambios, tocados = 0, []
for p in sorted(glob.glob(D + u"*.html")):
    t = io.open(p, encoding="utf-8").read()
    t0 = t

    def sellar(m):
        global cambios
        nombre, viejo = m.group(1), m.group(2)
        nuevo = hashes.get(nombre)
        if not nuevo or nuevo == viejo:
            return m.group(0)
        cambios += 1
        return u'<script src="%s?v=%s">' % (nombre, nuevo)

    t = re.sub(r'<script src="([a-z0-9\-]+\.js)(?:\?v=([a-f0-9]+))?">', sellar, t)

    def sellar_css(m):
        global cambios
        nombre, viejo = m.group(1), m.group(2)
        nuevo = hashes.get(nombre)
        if not nuevo or nuevo == viejo:
            return m.group(0)
        cambios += 1
        return u'<link rel="stylesheet" href="%s?v=%s">' % (nombre, nuevo)

    t = re.sub(r'<link rel="stylesheet" href="([a-z0-9\-]+\.css)(?:\?v=([a-f0-9]+))?">',
               sellar_css, t)
    if t != t0:
        io.open(p, "w", encoding="utf-8", newline="").write(t)
        tocados.append(os.path.basename(p))

if cambios:
    print(u"%d referencias actualizadas en: %s" % (cambios, ", ".join(tocados)))
else:
    print(u"todo al dia, nada que sellar")

# Un script que se pide sin ?v= se cachea para siempre: conviene verlo.
sueltos = []
for p in sorted(glob.glob(D + u"*.html")):
    t = io.open(p, encoding="utf-8").read()
    for m in re.finditer(r'<script src="([a-z0-9\-]+\.js)">', t):
        sueltos.append((os.path.basename(p), m.group(1)))
if sueltos:
    print(u"\n  sin ?v= (se cachean sin control):")
    for a, b in sueltos:
        print(u"    %-16s %s" % (a, b))
