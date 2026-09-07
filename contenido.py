# -*- coding: utf-8 -*-
u"""Cuanto contenido hay, y para quien alcanza.

   El sitio promete una ruta por puesto. Esa promesa se puede medir:
   cada puesto pide unos temas con un peso, cada tema tiene o no
   tiene pasos, y de ahi sale que porcentaje del puesto se puede
   ensenar de verdad.

   Lo que este informe contesta:

   - Cuanto hay: rutas, pasos, horas, problemas.
   - Que cubre cada puesto, y con cuanto material.
   - Que temas piden los puestos y no tienen ni un paso. Son los
     agujeros: un puesto que necesita algo que no existe no se puede
     recorrer entero, por mas rutas que haya.
   - Que temas tienen poco material para lo que se les pide.
   - Que rutas estan flacas al lado del resto.

   No inventa criterio: sale todo de temas.js y pasos.js, que se
   generan leyendo las paginas.

   Uso: python contenido.py
"""
import io, os, re, json, sys

D = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def leer_js(archivo, marca):
    t = io.open(os.path.join(D, archivo), encoding="utf-8").read()
    i = t.index("=", t.index(marca)) + 1
    while t[i] in " \t\r\n":
        i += 1
    j = i
    abre, cierra = ("[", "]") if t[j] == "[" else ("{", "}")
    prof, k = 0, j
    while k < len(t):
        if t[k] == abre:
            prof += 1
        elif t[k] == cierra:
            prof -= 1
            if prof == 0:
                break
        k += 1
    return json.loads(t[j:k + 1])


TEMAS = leer_js("temas.js", "var TEMAS")
PASOS = leer_js("pasos.js", "var PASOS")
try:
    PROBLEMAS = leer_js("problemas.js", "var PROBLEMAS")
except Exception:
    PROBLEMAS = []

nombre_tema = {t["id"]: t["nombre"] for t in TEMAS["temas"]}
por_tema = TEMAS["pasosPorTema"]


def horas(mins):
    return int(round(mins / 60.0))


def linea(c="-", n=64):
    print(c * n)


# ------------------------------------------------------- cuanto hay
tot_pasos = sum(len(r["pasos"]) for r in PASOS)
tot_min = sum(p["min"] for r in PASOS for p in r["pasos"])
tot_probs = sum(len(b.get("items", [])) for b in PROBLEMAS)

print()
print(u"CUANTO HAY")
linea()
print(u"  %d rutas, %d pasos, %d horas de material" % (len(PASOS), tot_pasos, horas(tot_min)))
print(u"  %d problemas de practica en %d bancos" % (tot_probs, len(PROBLEMAS)))
print(u"  %d temas en el vocabulario, %d puestos" % (len(TEMAS["temas"]), len(TEMAS["puestos"])))

# ------------------------------------------------------- por puesto
print()
print(u"QUE TAN ENTERO SE PUEDE RECORRER CADA PUESTO")
linea()
print(u"  Cubierto = del peso que el puesto pide, cuanto tiene material.")
print()

filas = []
for p in TEMAS["puestos"]:
    peso = 0.0
    cubierto = 0.0
    huecos, flacos = [], []
    for k, pide in p["temas"].items():
        peso += pide
        pasos = por_tema.get(k, [])
        if not pasos:
            huecos.append(k)
            continue
        # Un tema no esta cubierto por tener UN paso. La primera
        # version contaba asi y daba 100% en los ocho puestos, con
        # MLOps -un paso, una hora- contando igual que SQL, que tiene
        # veintisiete. Se cuenta con credito parcial: un tema pedido
        # en nivel 3 con un solo paso cubre un tercio de lo que se le
        # pide, no todo.
        parte = min(1.0, len(pasos) / float(pide))
        cubierto += pide * parte
        if parte < 1.0:
            flacos.append(k)
    filas.append({
        "id": p["id"], "nombre": p["nombre"],
        "pct": int(round(100.0 * cubierto / peso)) if peso else 0,
        "temas": len(p["temas"]), "huecos": huecos, "flacos": flacos,
    })

filas.sort(key=lambda f: f["pct"])
for f in filas:
    marca = u"  " if f["pct"] >= 85 else (u"! " if f["pct"] >= 65 else u"!!")
    print(u"%s%-26s %3d%%  de %d temas" % (marca, f["nombre"], f["pct"], f["temas"]))
    if f["huecos"]:
        print(u"      sin material: %s"
              % ", ".join(nombre_tema.get(h, h) for h in f["huecos"]))
    if f["flacos"]:
        print(u"      poco para lo que pide: %s"
              % ", ".join(nombre_tema.get(h, h) for h in f["flacos"]))

# ------------------------------------------------------- por tema
print()
print(u"CADA TEMA: cuanto material tiene y cuanto se lo pide")
linea()
print(u"  Pedido = la suma de lo que le piden los ocho puestos.")
print()

pedido = {}
for p in TEMAS["puestos"]:
    for k, v in p["temas"].items():
        pedido[k] = pedido.get(k, 0) + v

orden = sorted(nombre_tema, key=lambda k: (-pedido.get(k, 0), k))
for k in orden:
    pasos = por_tema.get(k, [])
    mins = sum(x.get("min", 0) for x in pasos)
    pd = pedido.get(k, 0)
    if not pd and not pasos:
        continue
    aviso = u""
    if pd and not pasos:
        aviso = u"   <- AGUJERO: se lo piden y no hay nada"
    elif pd >= 8 and len(pasos) < 4:
        aviso = u"   <- flaco para lo que se le pide"
    elif pasos and not pd:
        aviso = u"   <- hay material y ningun puesto lo pide"
    print(u"  %-32s %2d pasos %4d h   pedido %2d%s"
          % (nombre_tema.get(k, k), len(pasos), horas(mins), pd, aviso))

# ------------------------------------------------------- por ruta
print()
print(u"CADA RUTA")
linea()
rutas = sorted(PASOS, key=lambda r: len(r["pasos"]))
for r in rutas:
    mins = sum(p["min"] for p in r["pasos"])
    aviso = u"   <- corta" if len(r["pasos"]) < 6 else u""
    print(u"  %-24s %2d pasos %4d h%s" % (r["nombre"], len(r["pasos"]), horas(mins), aviso))

# ------------------------------------------------- el tamano del paso
print()
print(u"CUANTO DURA UN PASO, POR RUTA")
linea()
print(u"  El planificador reparte la semana en minutos: una ruta cuyos")
print(u"  pasos duran cuarenta horas no se puede repartir en bloques.")
print()
tam = []
for r in PASOS:
    n_p = len(r["pasos"])
    if not n_p:
        continue
    tam.append((sum(x["min"] for x in r["pasos"]) / float(n_p) / 60.0, r["nombre"], n_p))
tam.sort()
for h, nom, n_p in tam:
    aviso = u""
    if h > 12:
        aviso = u"   <- pasos enormes, no entran en un bloque"
    elif h < 1:
        aviso = u"   <- pasos muy chicos, la ruta es una lista larga"
    print(u"  %-24s %5.1f h por paso  (%d pasos)%s" % (nom, h, n_p, aviso))

# ------------------------------------------------------- el minimo
print()
print(u"PARA LANZAR")
linea()
peor = filas[0]
agujeros = sorted({h for f in filas for h in f["huecos"]})
print(u"  El puesto peor cubierto es %s, con %d%%." % (peor["nombre"], peor["pct"]))
if agujeros:
    print(u"  Temas que algun puesto pide y no tienen un solo paso: %d" % len(agujeros))
    for h in agujeros:
        quienes = [f["nombre"] for f in filas if h in f["huecos"]]
        print(u"    - %-28s lo piden: %s" % (nombre_tema.get(h, h), ", ".join(quienes)))
else:
    print(u"  No hay tema pedido sin material.")
print()
