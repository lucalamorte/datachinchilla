# -*- coding: utf-8 -*-
"""Cinco de los setenta y cinco problemas necesitan LeetCode Premium.

   El sitio promete que todo es gratis y estos cinco no lo son: se
   abren y aparece un candado. Son los clasicos de Blind 75 que
   LeetCode movio a su plan pago.

     252 Meeting Rooms
     253 Meeting Rooms II
     261 Graph Valid Tree
     269 Alien Dictionary
     323 Number of Connected Components in an Undirected Graph

   Se reemplazan por cinco gratis que entrenan el mismo patron. No es
   una traicion a la lista: la pagina describe el banco como "los 75
   que cubren los patrones que se repiten en las entrevistas", y el
   patron es lo que importa. Lo que si seria una traicion es mandar a
   alguien a una pagina que le pide la tarjeta.

     252 -> 986  Interval List Intersections   (intervalos, cruce)
     253 -> 1094 Car Pooling                   (intervalos, barrido)
     261 -> 684  Redundant Connection          (grafos, union-find)
     269 -> 210  Course Schedule II            (grafos, orden topologico)
     323 -> 547  Number of Provinces           (grafos, componentes)

   Se reemplaza bloque por bloque y no reserializando el archivo, para
   no tocar el formato ni el orden de lo que no cambia.

   El porcentaje de aceptacion viejo se saca: era el del problema
   anterior y dejarlo seria inventar un dato.

   Uso: python build-sin-paywall.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "problemas.js")

# (n viejo, titulo viejo, slug viejo) -> (n nuevo, titulo nuevo, dif, slug)
CAMBIOS = [
 (252, u"Meeting Rooms", u"meeting-rooms",
  986, u"Interval List Intersections", u"medio", u"interval-list-intersections"),
 (253, u"Meeting Rooms II", u"meeting-rooms-ii",
  1094, u"Car Pooling", u"medio", u"car-pooling"),
 (261, u"Graph Valid Tree", u"graph-valid-tree",
  684, u"Redundant Connection", u"medio", u"redundant-connection"),
 (269, u"Alien Dictionary", u"alien-dictionary",
  210, u"Course Schedule II", u"medio", u"course-schedule-ii"),
 (323, u"Number of Connected Components in an Undirected Graph",
  u"number-of-connected-components-in-an-undirected-graph",
  547, u"Number of Provinces", u"medio", u"number-of-provinces"),
]

t = io.open(P, encoding="utf-8").read()

for nv, tv, sv, nn, tn, dn, sn in CAMBIOS:
    viejo_n = u'"n": %d,' % nv
    viejo_t = u'"t": "%s",' % tv
    viejo_u = u'"u": "https://leetcode.com/problems/%s/"' % sv
    for x in (viejo_n, viejo_t, viejo_u):
        if t.count(x) != 1:
            print(u"  ABORTA: %r aparece %d veces, esperaba 1" % (x[:44], t.count(x)))
            sys.exit(1)
    # el bloque entero, desde su "n" hasta su "u"
    i = t.index(viejo_n)
    j = t.index(viejo_u, i) + len(viejo_u)
    bloque = t[i:j]
    if viejo_t not in bloque:
        print(u"  ABORTA: el bloque de %d no trae su titulo" % nv)
        sys.exit(1)
    # se conserva el patron, que es lo que hace que el reemplazo valga
    pat = None
    for linea in bloque.split("\n"):
        if '"p":' in linea:
            pat = linea.strip().rstrip(",")
    if not pat:
        print(u"  ABORTA: el bloque de %d no trae patron" % nv)
        sys.exit(1)
    nuevo = (u'"n": %d,\n    "t": "%s",\n    "d": "%s",\n    %s,\n    '
             u'"u": "https://leetcode.com/problems/%s/"'
             % (nn, tn, dn, pat, sn))
    t = t[:i] + nuevo + t[j:]

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"problemas.js: %d problemas con paywall cambiados por gratis" % len(CAMBIOS))
