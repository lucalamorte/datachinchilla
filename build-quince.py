# -*- coding: utf-8 -*-
u"""Siete rutas decian "Las quince partes" al terminarlas.

   Es el texto del boton grande cuando ya cerraste todos los pasos:
   "Catalogo completo / Las quince partes". Quince es de Full Stack
   Open, que tiene quince. Lo heredaron Airflow -que tiene ocho y esta
   publicada- y las cinco rutas que se armaron copiandola: testing,
   nube, funcional, mlops y visualizacion.

   Es la quinta vez que una pagina copiada se trae un dato de la
   original. Las cuatro anteriores se arreglaron poniendo el valor
   correcto; esta se arregla sacando el numero: NODES.length esta ahi
   al lado. Un numero que se cuenta no se puede heredar mal.

   cuentas.py no lo veia porque busca numeros escritos con letra en
   los lugares donde la ruta habla de si misma, y este estaba adentro
   de una asignacion de JavaScript. Despues de esto ya no hay numero
   que buscar.

   Uso: python build-quince.py
"""
import io, os

D = os.path.dirname(os.path.abspath(__file__))

VIEJO = u'document.getElementById("startDest").textContent = "Las quince partes";'
NUEVO = (u'/* Contado, no escrito: este texto decia "quince" en siete rutas\n'
         u'       porque se heredo de Full Stack Open al copiar la pagina. */\n'
         u'    document.getElementById("startDest").textContent =\n'
         u'      "Los " + NODES.length + " pasos";')

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if t.count(VIEJO) != 1:
        continue
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(VIEJO, NUEVO, 1))
    print(u"%-24s cuenta en vez de decir" % a)
    n += 1

print(u"%d rutas al dia" % n)
