# -*- coding: utf-8 -*-
"""problemas.js: la lista curada de problemas para practicar.

   Los enunciados son de LeetCode y de StrataScratch y ahi se quedan:
   copiarlos seria apropiarse de contenido ajeno y romper lo unico que
   el sitio afirma sobre si mismo. Lo que vive aca es la lista, el
   orden, el patron de cada uno y si lo hiciste o no.

   Eso es lo que hoy no tiene nadie: podes hacer los 75 de Blind
   salteados entre dos plataformas y no tener idea de cuantos llevas
   ni cuales te faltan.

   Los datos salen de las listas que paso Luca, no de mi memoria.

   Uso: python build-problemas.py
"""
import io, os, re, json, sys, unicodedata

D = os.path.dirname(os.path.abspath(__file__))
FUENTE = ("C:/Users/Luca/AppData/Local/Temp/claude/"
          "C--Users-Luca-Desktop-snowflake-path/"
          "4febdbb4-c158-4190-b00f-f074ccb9d175/scratchpad/listas.txt")

# El patron de cada problema de Blind 75, por numero. La lista esta
# organizada asi desde siempre y el patron es lo que de verdad se
# aprende: dos problemas del mismo patron se resuelven igual.
PATRON = {
    "Arrays y hashing": [1, 217, 242, 49, 347, 238, 271, 128],
    "Dos punteros":     [125, 15, 11],
    "Ventana movil":    [121, 3, 424, 76],
    "Pila":             [20],
    "Busqueda binaria": [33, 153],
    "Lista enlazada":   [206, 21, 141, 143, 19, 23],
    "Arboles":          [226, 104, 100, 572, 105, 98, 230, 102, 124, 297, 235],
    "Trie":             [208, 211, 212],
    # 261, 323 y 269 pasaron a LeetCode Premium, igual que 252 y 253.
    # Van reemplazos gratis con el mismo patron: 684 union-find,
    # 547 componentes, 210 orden topologico, 986 cruce de
    # intervalos y 1094 barrido. El sitio promete que todo es
    # gratis, asi que un problema con candado no puede quedarse
    # por respeto a la lista original.
    "Grafos":           [200, 133, 417, 207, 684, 547, 210],
    "Intervalos":       [57, 56, 435, 986, 1094],
    "Programacion dinamica": [70, 198, 213, 139, 300, 322, 62, 91, 152, 53, 5, 647, 1143],
    "Matrices":         [73, 54, 48, 79],
    "Bits":             [191, 338, 190, 268, 371],
    "Codicioso":        [55],
    "Backtracking":     [39],
    "Monticulo":        [295],
}

# De numero a patron, para buscar rapido.
DE_NUMERO = {}
for pat, nums in PATRON.items():
    for n in nums:
        DE_NUMERO[n] = pat


def slug(titulo):
    """El slug de LeetCode: minusculas y guiones. Es como arma sus
       URLs desde siempre, asi que el link se puede derivar."""
    s = titulo.lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", "-", s.strip())


def leer_fuente():
    if not os.path.exists(FUENTE):
        print("  ABORTA: no encuentro las listas en %s" % FUENTE)
        sys.exit(1)
    return io.open(FUENTE, encoding="utf-8").read()


def blind(t):
    """Numero, titulo, aceptacion y dificultad, como los pego Luca."""
    DIF = {"Easy": "facil", "Med.": "medio", "Hard": "dificil"}
    out, vistos = [], set()
    for m in re.finditer(r"(\d+)\. ([^\n]+)\n([\d.]+)%\n(Easy|Med\.|Hard)", t):
        n = int(m.group(1))
        if n in vistos:
            continue
        vistos.add(n)
        titulo = m.group(2).strip()
        out.append({
            "n": n,
            "t": titulo,
            "d": DIF[m.group(4)],
            "ac": float(m.group(3)),
            "p": DE_NUMERO.get(n, "Otros"),
            "u": "https://leetcode.com/problems/%s/" % slug(titulo),
        })
    return out


LINKS = ("C:/Users/Luca/AppData/Local/Temp/claude/"
         "C--Users-Luca-Desktop-snowflake-path/"
         "4febdbb4-c158-4190-b00f-f074ccb9d175/scratchpad/links_strata.txt")


def normalizar(s):
    """Un titulo o un slug, reducidos a lo mismo, para poder cruzarlos."""
    s = unicodedata.normalize("NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().replace("-", " ")
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def links_directos():
    """Los links que paso Luca, indexados por el slug de la URL.

       StrataScratch arma sus URLs como <id>-<slug> y el id es interno:
       no se puede derivar del titulo. Sin esta lista lo unico honesto
       era mandar a la busqueda."""
    if not os.path.exists(LINKS):
        return {}
    out = {}
    for linea in io.open(LINKS, encoding="utf-8"):
        linea = linea.strip()
        m = re.search(r"/coding/(\d+)-([a-z0-9\-]+)", linea)
        if not m:
            continue
        out[normalizar(m.group(2))] = linea
    return out


# Palabras que no distinguen nada y solo agregan ruido al cruce.
VACIAS = set(u"""the a an of in on for to and or with which that this
those these all find calculate get show list number are is was were
by from as at their its it s per total each every who whose whom
""".split())


def claves(s):
    """Las palabras con las que vale la pena comparar."""
    return set(w for w in normalizar(s).split()
               if w and w not in VACIAS and len(w) > 2)


def buscar_link(titulo, mapa):
    """El link de un titulo.

       Exacto cuando se puede; si no, por solapamiento de palabras.
       En la lista los problemas vienen con su nombre corto
       ("MacBookPro User Event Count") y en la URL con la pregunta
       entera ("count the number of user events performed by
       macbookpro users"): son el mismo problema con dos nombres."""
    k = normalizar(titulo)
    if k in mapa:
        return mapa[k]

    # A mano, los que el cruce no puede resolver solo porque el nombre
    # corto y la pregunta larga no comparten casi ninguna palabra.
    # Los cuatro ultimos los confirmo Luca uno por uno: "April Admin
    # Employees" y "Olympics Events List By Age" no compartian nada
    # con su URL (una dice "admin department" sin abril, y la otra
    # "by height" contra "By Age"), asi que no habia forma de saberlo
    # sin preguntar.
    A_MANO = {
        "first names with six letters ending in h": "9842",
        "artist appearance count": "9992",
        "count occurrences of words in drafts": "9817",
        "april admin employees": "9845",
        "olympics events list by age": "9943",
        "titanic survivors and non survivors": "9881",
    }
    if k in A_MANO:
        for slug_k, url in mapa.items():
            if "/" + A_MANO[k] + "-" in url:
                return url

    mias, mejor, puntaje = claves(titulo), "", 0.0
    if not mias:
        return ""
    for slug_k, url in mapa.items():
        suyas = claves(slug_k)
        if not suyas:
            continue
        comunes = len(mias & suyas)
        if not comunes:
            continue
        # Sobre la lista mas corta: el nombre corto entra entero
        # adentro de la pregunta larga, no al reves.
        p = comunes / float(min(len(mias), len(suyas)))
        if p > puntaje:
            puntaje, mejor = p, url
    # Dos tercios de la lista corta en comun: por debajo son parecidos
    # de casualidad y prefiero la busqueda antes que un link errado.
    return mejor if puntaje >= 0.67 else ""


def strata(t):
    """Las de StrataScratch: titulo, dificultad y empresa.

       El link directo sale de la lista que paso Luca; para las que no
       estan ahi va la busqueda por titulo, que es lo unico honesto
       sin conocer su id interno."""
    DIF = {"Easy": "facil", "Medium": "medio", "Hard": "dificil"}
    i = t.find("Title\n\nDifficulty\n\nCompany")
    if i < 0:
        i = t.find("64\nquestions")
    if i < 0:
        return []
    mapa_links = links_directos()
    # Linea por linea y no con una regex sola: la empresa a veces va
    # pegada a la dificultad y a veces en la linea de abajo (cuando
    # son varias, StrataScratch escribe "Apple+2"). Una regex que
    # contemple las dos formas termina comiendose el titulo siguiente.
    lineas = [x.rstrip() for x in t[i:].split("\n")]
    out, vistos = [], set()
    saltar = ("title", "difficulty", "company", "")

    for k, linea in enumerate(lineas):
        partes = linea.split("\t")
        dif = partes[0].strip()
        if dif not in DIF:
            continue

        # El titulo es la linea de arriba con texto.
        titulo, j = "", k - 1
        while j >= 0 and not titulo:
            if lineas[j].strip().lower() not in saltar:
                titulo = lineas[j].strip()
            j -= 1
        if not titulo or titulo in vistos or titulo in DIF:
            continue
        vistos.add(titulo)

        # La empresa: lo que sigue al tab, o la primera linea con
        # texto de abajo si ahi no habia nada.
        empresa = partes[1].strip() if len(partes) > 1 else ""
        j = k + 1
        while not empresa and j < len(lineas) and j < k + 4:
            cand = lineas[j].strip()
            if cand and cand not in DIF:
                empresa = cand
            j += 1
        empresa = empresa.rstrip("+0123456789").strip()

        directo = buscar_link(titulo, mapa_links)
        out.append({
            "t": titulo,
            "d": DIF[dif],
            "co": empresa,
            "p": "SQL",
            # Marcado, para poder decir cuáles abren el problema y
            # cuáles caen en la búsqueda.
            "dir": bool(directo),
            "u": directo or ("https://platform.stratascratch.com/coding?search=" +
                             re.sub(r"\s+", "%20", titulo[:60])),
        })
    return out


def main():
    t = leer_fuente()
    b = blind(t)
    s = strata(t)

    if len(b) < 70:
        print("  ABORTA: solo %d de Blind 75, algo se perdio al parsear" % len(b))
        sys.exit(1)

    sin_patron = [x["n"] for x in b if x["p"] == "Otros"]
    if sin_patron:
        print("  ojo, sin patron asignado: %s" % sin_patron)

    bancos = [
        {"id": "blind75", "nombre": "Blind 75", "lang": "Python",
         "fuente": "LeetCode", "url": "https://leetcode.com/problemset/",
         "d": "Los 75 que cubren los patrones que se repiten en las entrevistas de algoritmos. Cinco de los originales pasaron a LeetCode Premium, así que van cinco gratis que entrenan el mismo patrón: acá no entra nada que se pague.",
         "items": b},
        {"id": "strata", "nombre": "Consultas de entrevistas", "lang": "SQL",
         "fuente": "StrataScratch", "url": "https://platform.stratascratch.com/coding",
         "d": "Tomadas de entrevistas reales, con la empresa que la preguntó.",
         "items": s},
    ]

    js = (u"/* ============================================================\n"
          u"   problemas.js\n\n"
          u"   Lo genera build-problemas.py. No se edita a mano.\n\n"
          u"   La lista, el patrón y el link. El enunciado se lee en la\n"
          u"   plataforma de origen, que es de quien es; acá vive el orden\n"
          u"   y tu avance, que es lo que allá no queda.\n"
          u"   ============================================================ */\n"
          u"var PROBLEMAS = " + json.dumps(bancos, ensure_ascii=False, indent=1) + u";\n")
    io.open(os.path.join(D, "problemas.js"), "w", encoding="utf-8", newline="").write(js)

    print(u"Blind 75:        %d problemas" % len(b))
    for pat in PATRON:
        n = len([x for x in b if x["p"] == pat])
        if n:
            print(u"   %-22s %2d" % (pat, n))
    print(u"StrataScratch:   %d consultas" % len(s))
    print(u"\nproblemas.js escrito")


main()
