# -*- coding: utf-8 -*-
"""Los acentos escapados vuelven a ser acentos.

   Los archivos son UTF-8, asi que escribir "Dej" + escape + "1" en
   vez de "Deja" no aporta nada y ademas esconde el texto del chequeo
   de tuteo, que busca la tilde: el voseo escapado pasaba como limpio.

   Se corre junto con tuteo.py cuando se toca copy generado por JS.
"""
import io, re, glob, os

D = u"C:/Users/Luca/Desktop/snowflake path/"

# Solo las letras del espanol y unos signos. Cualquier otro escape se
# deja como esta: puede estar ahi por una razon.
TABLA = {
    "e1": u"\u00e1", "e9": u"\u00e9", "ed": u"\u00ed",
    "f3": u"\u00f3", "fa": u"\u00fa", "fc": u"\u00fc",
    "f1": u"\u00f1", "d1": u"\u00d1",
    "c1": u"\u00c1", "c9": u"\u00c9", "cd": u"\u00cd",
    "d3": u"\u00d3", "da": u"\u00da",
    "bf": u"\u00bf", "a1": u"\u00a1", "b7": u"\u00b7",
}

PAT = re.compile(r"\\u00([0-9a-fA-F]{2})")


def cambiar(m):
    return TABLA.get(m.group(1).lower(), m.group(0))


total = 0
for p in sorted(glob.glob(D + u"*.html")) + sorted(glob.glob(D + u"*.js")):
    t = io.open(p, encoding="utf-8").read()
    t2 = PAT.sub(cambiar, t)
    if t2 != t:
        n = len(PAT.findall(t)) - len(PAT.findall(t2))
        io.open(p, "w", encoding="utf-8", newline="").write(t2)
        print(u"%-20s %d" % (os.path.basename(p), n))
        total += n

print(u"%d escapes convertidos" % total if total else u"nada escapado")
