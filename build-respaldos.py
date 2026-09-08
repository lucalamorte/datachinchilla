# -*- coding: utf-8 -*-
u"""Los numeros de respaldo tambien envejecen.

   Tres textos dicen cuantas rutas y cuantos niveles hay, y los tres se
   arreglaron para que el numero saliera de los datos en vez de estar
   escrito. Pero el HTML quedo con un valor de respaldo, el que habia
   el dia que se hizo el cambio: "17 rutas" y "263 niveles".

   El JavaScript los corrige al cargar, asi que nadie los ve mas que un
   instante. Pero un instante alcanza, y sobre todo: el sitio hoy tiene
   22 rutas y 343 niveles, o sea que el respaldo volvio a estar mal
   exactamente igual que antes. Arreglar un numero escrito a mano
   dejando otro escrito a mano no arregla nada.

   Este script los pone al dia leyendo pasos.js y catalog.js, que es de
   donde salen. Se corre despues de build-catalog.py, como sellar.py.

   La portada no aparece: ahi el elemento ya esta vacio y lo llena el
   JavaScript, que es lo correcto y es lo que estos tres tendrian que
   haber hecho.

   Uso: python build-respaldos.py
"""
import io, os, re, json, sys

D = os.path.dirname(os.path.abspath(__file__))


def cuantos():
    t = io.open(os.path.join(D, "pasos.js"), encoding="utf-8").read()
    rutas = len(json.loads(t[t.index("["):t.rindex("]") + 1]))
    c = io.open(os.path.join(D, "catalog.js"), encoding="utf-8").read()
    niveles = len(json.loads(c[c.index("["):c.index("];") + 1]))
    return rutas, niveles


def main():
    rutas, niveles = cuantos()
    n = 0
    for archivo, cual, valor in (("armar.html", "cuantasRutas", rutas),
                                 ("armar.html", "cuantasPiezas", niveles),
                                 ("cv.html", "cuantasRutas", rutas)):
        p = os.path.join(D, archivo)
        t = io.open(p, encoding="utf-8").read()
        pat = r'(id="%s">)(\d*)(</b>)' % cual
        m = re.search(pat, t)
        if not m:
            print(u"  ABORTA: no encuentro %s en %s" % (cual, archivo)); sys.exit(1)
        if m.group(2) == str(valor):
            continue
        t = t[:m.start(2)] + str(valor) + t[m.end(2):]
        io.open(p, "w", encoding="utf-8", newline="").write(t)
        print(u"%-14s %-14s %s -> %d" % (archivo, cual, m.group(2) or "(vacio)", valor))
        n += 1
    print(u"%d respaldos al dia" % n if n else u"los respaldos ya estaban al dia")


main()
