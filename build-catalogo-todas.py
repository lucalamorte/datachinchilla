# -*- coding: utf-8 -*-
"""El armador conocia tres rutas de diecisiete.

   build-catalog.py trae su lista de rutas escrita a mano, y decia
   -en su propia docstring- "leyendo los niveles de las tres rutas".
   Se quedo ahi mientras el sitio pasaba a diecisiete: el armador
   ofrecia 36 piezas de 263. Todo lo que agregamos desde entonces
   -dbt, Big Data, Claude, Full Stack Open, Airflow- no se podia usar
   para armar una ruta a mano.

   El arreglo no es agregar catorce entradas a mano, porque el mes que
   viene vuelve a pasar. La lista pasa a salir de pasos.js, que ya se
   genera leyendo las paginas: agregar una ruta la mete en el armador
   sin que nadie se acuerde.

   El color sale del --accent de cada pagina, que es el que la ruta ya
   usa. El icono, del catalogo de la portada. Ninguno de los dos se
   copia a mano por la misma razon.

   Uso: python build-catalogo-todas.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "build-catalog.py")

VIEJO_INI = u"RUTAS = ["
VIEJO_FIN = u"]\n\n# los campos que necesita el armador"

NUEVO = u'''# --- Las rutas salen de pasos.js, no de una lista a mano ------------
#
# Esta lista estaba escrita a mano con tres rutas, y se quedo ahi
# mientras el sitio llegaba a diecisiete: el armador ofrecia 36 piezas
# de 263. Agregar catorce a mano habria durado hasta la ruta
# siguiente.
#
# pasos.js ya se genera leyendo cada pagina, asi que es la fuente
# correcta. El color sale del --accent de la propia pagina y el icono
# del catalogo de la portada: los dos ya existen en algun lado, y
# copiarlos aca seria tener dos verdades.

def _rutas_del_sitio():
    import json
    p = os.path.join(AQUI, "pasos.js")
    if not os.path.exists(p):
        sys.exit("falta pasos.js: corre build-pasos.py primero")
    crudo = io.open(p, encoding="utf-8").read()
    rutas = json.loads(crudo[crudo.index("["):crudo.rindex("]") + 1])

    # el icono de cada ruta, del catalogo de la portada
    iconos = {}
    idx = io.open(os.path.join(AQUI, "index.html"), encoding="utf-8").read()
    b = idx[idx.index("var PATHS"):]
    b = b[:b.index(chr(10) + "];")]
    for ent in b.split(chr(10) + "  {")[1:]:
        mu = re.search(r'u:\\s*"([^"]+)"', ent)
        mi = re.search(r'i:\\s*"([^"]+)"', ent)
        if mu and mi:
            iconos[mu.group(1)] = mi.group(1)

    out = []
    for n, r in enumerate(rutas):
        arch = r["archivo"]
        color = "#7C8AA0"
        pag = os.path.join(AQUI, arch)
        if os.path.exists(pag):
            m = re.search(r"--accent:\\s*(#[0-9A-Fa-f]{6})",
                          io.open(pag, encoding="utf-8").read())
            if m:
                color = m.group(1)
        out.append({
            "id": r["clave"], "nombre": r["nombre"], "archivo": arch,
            "color": color, "icono": iconos.get(arch, "code"),
            "orden": n + 1,
        })
    return out


RUTAS = _rutas_del_sitio()

'''

t = io.open(P, encoding="utf-8").read()
i = t.index(VIEJO_INI)
j = t.index(VIEJO_FIN) + 2
if "_rutas_del_sitio" in t:
    print(u"  ya estaba"); sys.exit(1)
t = t[:i] + NUEVO + t[j:]

# la docstring, que dice "las tres rutas"
t = t.replace(
    u"Genera catalog.js leyendo los niveles de las tres rutas.",
    u"Genera catalog.js leyendo los niveles de todas las rutas del sitio.\nLa lista sale de pasos.js: agregar una ruta la mete aca sola.")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"build-catalog.py: la lista sale de pasos.js")
