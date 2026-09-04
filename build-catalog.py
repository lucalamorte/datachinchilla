# -*- coding: utf-8 -*-
"""
build-catalog.py

Genera catalog.js leyendo los niveles de las tres rutas. El armador de rutas
a medida necesita la lista completa de piezas, y copiarla a mano garantizaba
que se separara de las páginas al primer cambio.

Correlo cada vez que agregues, saques o renombres un nivel:

    python build-catalog.py
"""
import io, json, re, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

RUTAS = [
    {"id": "snowpro", "nombre": "SnowPro Core", "archivo": "snowpro.html",
     "color": "#38BDF8", "icono": "snow", "orden": 2},
    {"id": "de", "nombre": "Data Engineer", "archivo": "data-engineer.html",
     "color": "#A78BFA", "icono": "data", "orden": 1},
    {"id": "cs50", "nombre": "CS50", "archivo": "cs50.html",
     "color": "#F2707F", "icono": "school", "orden": 3},
]

# los campos que necesita el armador, nada más
CAMPO = {
    "id":      re.compile(r'id:\s*"([^"]+)"'),
    "title":   re.compile(r'title:\s*"((?:[^"\\]|\\.)*)"'),
    "summary": re.compile(r'summary:\s*"((?:[^"\\]|\\.)*)"'),
    "time":    re.compile(r'time:\s*"([^"]*)"'),
    "level":   re.compile(r'level:\s*"([^"]*)"'),
    "cost":    re.compile(r'cost:\s*"([^"]*)"'),
}

def bloques(texto):
    """Corta el arreglo NODES en objetos, contando llaves."""
    i = texto.index("var NODES = [")
    i = texto.index("[", i)
    prof, ini, fuera = 0, None, []
    for pos in range(i, len(texto)):
        c = texto[pos]
        if c == "{":
            if prof == 0:
                ini = pos
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0 and ini is not None:
                fuera.append(texto[ini:pos + 1])
                ini = None
        elif c == "]" and prof == 0:
            break
    return fuera

def limpiar(t):
    return t.replace('\\"', '"').replace("\\\\", "\\")

piezas = []
for ruta in RUTAS:
    ruta_path = os.path.join(AQUI, ruta["archivo"])
    if not os.path.exists(ruta_path):
        sys.exit("falta " + ruta["archivo"])
    texto = io.open(ruta_path, encoding="utf-8").read()
    encontrados = 0
    for n, obj in enumerate(bloques(texto)):
        datos = {}
        for campo, rx in CAMPO.items():
            m = rx.search(obj)
            if m:
                datos[campo] = limpiar(m.group(1))
        if "id" not in datos or "title" not in datos:
            continue
        piezas.append({
            "id": ruta["id"] + ":" + datos["id"],
            "nodo": datos["id"],
            "ruta": ruta["id"],
            "n": n + 1,
            "t": datos["title"],
            "d": datos.get("summary", ""),
            "hs": datos.get("time", ""),
            "nivel": datos.get("level", "") or ("Curso " + str(n + 1)),
            "pago": datos.get("cost", "") == "Pago",
        })
        encontrados += 1
    print("%-16s %2d piezas" % (ruta["nombre"], encontrados))

salida = (u"/* Generado por build-catalog.py. No editar a mano: los datos viven\n"
          u"   en cada página y este archivo se regenera con un comando. */\n"
          u"var CATALOGO = " + json.dumps(piezas, ensure_ascii=False, indent=1) + u";\n\n"
          u"var CATALOGO_RUTAS = " + json.dumps(
              [{"id": r["id"], "nombre": r["nombre"], "archivo": r["archivo"],
                "color": r["color"], "icono": r["icono"], "orden": r["orden"]} for r in RUTAS],
              ensure_ascii=False, indent=1) + u";\n")

io.open(os.path.join(AQUI, "catalog.js"), "w", encoding="utf-8").write(salida)
print("catalog.js: %d piezas en total" % len(piezas))
