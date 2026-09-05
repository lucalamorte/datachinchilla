# -*- coding: utf-8 -*-
"""pasos.js: los pasos de cada ruta, en un solo archivo.

   El planificador semanal necesita saber por donde va cada uno y cual
   es el proximo paso. Esa informacion vive dentro de cada pagina, en
   su array NODES, y copiarla a mano seria tener dos verdades.

   Este script la extrae de las paginas y la escribe en pasos.js. Si se
   agrega una ruta o se cambia un paso, se corre de nuevo.

   Tambien anota donde guarda su avance cada ruta: no todas usan la
   misma clave dentro del perfil, y snowpro guarda suelto porque fue la
   primera.
"""
import io, os, re, json, sys

AQUI = u"C:/Users/Luca/Desktop/snowflake path/"

# archivo -> (clave de avance en el perfil, nombre corto)
RUTAS = [
    ("sql-python.html",     "sqlpy",        u"SQL y Python"),
    ("data-engineer.html",  "de",           u"Data Engineer"),
    ("snowpro.html",        "__suelto__",   u"SnowPro Core"),
    ("cs50.html",           "cs50",         u"CS50"),
    ("dbt.html",            "dbt",          u"dbt"),
    ("bigdata.html",        "bigdata",      u"Big Data"),
    ("data-science.html",   "data_science", u"Data Science"),
    ("arquitectura.html",   "arquitectura", u"Arquitectura"),
    ("subir-nivel.html",    "subirnivel",   u"Subir de nivel"),
    ("ai-fundamentos.html", "aifund",       u"AI: fundamentos"),
    ("claude.html",         "claude",       u"Trabajar con Claude"),
    ("deep-learning.html",  "deeplearning", u"Deep learning"),
    ("llm-agentes.html",    "llmagentes",   u"LLMs y agentes"),
    ("ml-aplicado.html",    "mlaplicado",   u"ML aplicado"),
    ("web3.html",           "web3",         u"Web3"),
    ("fullstack.html",      "fullstack",    u"Full Stack Open"),
]

# Cuánto dura un paso, en minutos. El texto viene como lo escribe cada
# ruta ("3 horas", "45 min", "1 día", "a tu ritmo"), así que hay que
# traducirlo para poder repartirlo en la semana.
def minutos(txt):
    t = (txt or u"").lower().strip()
    m = re.match(r'^(\d+)\s*h(?:ora)?s?(?:\s*y\s*(?:(\d+)\s*min|(media|cuarto)))?', t)
    if m:
        n = int(m.group(1)) * 60
        if m.group(2): n += int(m.group(2))
        elif m.group(3) == u"media": n += 30
        elif m.group(3) == u"cuarto": n += 15
        return n
    m = re.match(r'^(\d+)\s*h\s*(\d+)\s*min', t)
    if m: return int(m.group(1)) * 60 + int(m.group(2))
    m = re.match(r'^(\d+)\s*min', t)
    if m: return int(m.group(1))
    m = re.match(r'^(\d+)\s*lecciones?', t)
    if m: return int(m.group(1)) * 20          # las de Alchemy: ~20 min cada una
    m = re.match(r'^(\d+)\s*semanas?', t)
    if m: return int(m.group(1)) * 300         # una semana de curso: ~5 h de estudio
    m = re.match(r'^(\d+)\s*d[íi]as?', t)
    if m: return int(m.group(1)) * 300
    return 90                                   # "a tu ritmo", "video" y demás


# Desde donde se puede empezar cada ruta. Sale de PATHS, en la
# portada, que es donde se elige a mano. Lo necesita el motor del CV:
# una ruta puede cubrir justo lo que te falta y aun asi no ser para
# vos, porque arranca donde todavia no llegaste.
NIVELES = {
    "ai-fundamentos.html": u"Desde cero",
    "claude.html": u"Con Python sabido",
    "arquitectura.html": u"Con experiencia",
    "bigdata.html": u"Con Python sabido",
    "cs50.html": u"Desde cero",
    "data-engineer.html": u"Desde cero",
    "data-science.html": u"Desde cero",
    "dbt.html": u"Con SQL sabido",
    "deep-learning.html": u"Con Python sabido",
    "llm-agentes.html": u"Con Python sabido",
    "ml-aplicado.html": u"Con Python sabido",
    "snowpro.html": u"Con SQL sabido",
    "sql-python.html": u"Desde cero",
    "subir-nivel.html": u"Con experiencia",
    "web3.html": u"Desde cero",
    "fullstack.html": u"Con programación sabida",
}

ORDEN_NIVEL = {
    u"Desde cero": 0,
    u"Con SQL sabido": 1,
    u"Con Python sabido": 2,
    u"Con programación sabida": 2,
    u"Con experiencia": 3,
}


def nodos_de(archivo):
    p = AQUI + archivo
    if not os.path.exists(p): return None
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r'var NODES = \[(.*?)\n\];', t, re.S)
    if not m: return None
    out = []
    for bloque in re.split(r'\n(?=  \{\n)', m.group(1)):
        i = re.search(r'id:\s*"([^"]+)"', bloque)
        ti = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', bloque)
        tm = re.search(r'time:\s*"([^"]*)"', bloque)
        ac = re.search(r'act:\s*(\d+)', bloque)
        if not (i and ti): continue

        def campo(nombre, b=bloque):
            # Anclado a principio de linea: algunos nodos traen un
            # "tambien: { u: ... }" anidado y sin el ancla se agarraba
            # ese en vez del campo del nodo.
            m = re.search(r"^\s*" + nombre + r':\s*"((?:[^"\\]|\\.)*)"',
                          b, re.M)
            return m.group(1).replace('\\"', '"') if m else u""

        # Las conclusiones, que la ruta muestra al abrir el curso.
        wins = []
        mw = re.search(r"wins:\s*\[(.*?)\]", bloque, re.S)
        if mw:
            wins = [x.replace('\\"', '"') for x in
                    re.findall(r'"((?:[^"\\]|\\.)*)"', mw.group(1))]

        out.append({
            "id": i.group(1),
            "t": ti.group(1).replace('\\"', '"'),
            "min": minutos(tm.group(1) if tm else u""),
            "act": int(ac.group(1)) if ac else 0,
            # Lo que hace falta para pintar el curso como en su ruta:
            # sin esto, lo que sale del CV es un indice y no un camino.
            "time": tm.group(1) if tm else u"",
            "sum": campo("summary"),
            "goal": campo("goal"),
            "cert": campo("cert"),
            "i": campo("i"),
            "u": campo("u"),
            "boss": bool(re.search(r"boss:\s*true", bloque)),
            "wins": wins,
        })
    return out


def actos_de(archivo):
    t = io.open(AQUI + archivo, encoding="utf-8").read()
    m = re.search(r'var ACTS = \[(.*?)\n\];', t, re.S)
    if not m: return []
    return [x.replace('\\"', '"') for x in re.findall(r'title:\s*"((?:[^"\\]|\\.)*)"', m.group(1))]


salida = []
for archivo, clave, nombre in RUTAS:
    ns = nodos_de(archivo)
    if ns is None:
        print("  sin NODES: %s" % archivo); continue
    salida.append({
        "archivo": archivo, "clave": clave, "nombre": nombre,
        "actos": actos_de(archivo), "pasos": ns,
        "nivel": NIVELES.get(archivo, u"Desde cero"),
        "nivelN": ORDEN_NIVEL.get(NIVELES.get(archivo, u"Desde cero"), 0),
    })
    print("%-22s %2d pasos, %2d tramos, %d h en total" % (
        archivo, len(ns), len(actos_de(archivo)), round(sum(n["min"] for n in ns) / 60)))

if not salida:
    print("  ABORTA: no salio nada"); sys.exit(1)

cuerpo = json.dumps(salida, ensure_ascii=False, indent=1)
js = (u"/* ============================================================\n"
      u"   pasos.js\n\n"
      u"   Lo genera build-pasos.py leyendo el array NODES de cada ruta.\n"
      u"   No se edita a mano: se corre el script y queda al día.\n\n"
      u"   Existe para el planificador semanal, que necesita saber cuál\n"
      u"   es tu próximo paso y cuánto lleva sin abrir todas las páginas.\n"
      u"   ============================================================ */\n"
      u"var PASOS = " + cuerpo + u";\n")
io.open(AQUI + u"pasos.js", "w", encoding="utf-8", newline="").write(js)
print("\npasos.js escrito: %d rutas, %d pasos" % (
    len(salida), sum(len(r["pasos"]) for r in salida)))
