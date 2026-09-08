# -*- coding: utf-8 -*-
u"""La agenda esta en la portada. Siempre. Sin condiciones.

   renderHoy() y renderHoyMini() arrancaban con un `if(!hayPlan())
   return`, asi que la agenda solo aparecia si ya tenias plan armado.
   Quien entra por primera vez, y quien esta probando el sitio con el
   estado limpio, no la ve nunca.

   Y no hacia falta: Plan.armar() con localStorage vacio ya devuelve la
   semana entera -cinco dias con bloques de practica, estudio y
   repaso-. La agenda se podia dibujar desde el primer segundo. El
   `if` no protegia de nada, solo escondia.

   Esto se pidio muchas veces. Cada vez lo mire con el estado puesto a
   mano, cada vez aparecio, y cada vez conteste que estaba. Con el
   estado limpio, que es como se entra al sitio, no estaba.

   Se van los dos `if`. Lo unico que queda condicionado es el nombre
   de las rutas al lado del titulo, que sin rutas activas no tiene que
   decir nada.

   Uso: python build-agenda-siempre.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n))
        sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()

if u"La agenda no espera a que tengas plan" in t:
    print(u"  ya estaba"); sys.exit(1)

# ------------------------------------------------------- el renglon del hero
t = cambiar(t,
u'''  var m = document.getElementById("hoyMini");
  if(!m || typeof Plan === "undefined" || !hayPlan()) return;''',
u'''  /* La agenda no espera a que tengas plan.

     Aca habia un `!hayPlan()`, asi que este renglon solo salia para
     quien ya habia armado su ruta. Con el estado limpio -o sea al
     entrar por primera vez, o probando el sitio- no salia nunca, y
     por eso la agenda "no estaba en la portada" por mas que el
     widget estuviera puesto.

     Plan.armar() sin nada guardado ya devuelve la semana entera, con
     sus bloques de practica, estudio y repaso. No habia nada que
     proteger: el `if` solo escondia. */
  var m = document.getElementById("hoyMini");
  if(!m || typeof Plan === "undefined") return;''',
u"el renglon del hero")

# ---------------------------------------------------- la agenda de siete dias
t = cambiar(t,
u'''  var caja = document.getElementById("hoy");
  if(!caja || typeof Plan === "undefined" || !hayPlan()) return;''',
u'''  /* Y la agenda de los siete dias, por lo mismo. */
  var caja = document.getElementById("hoy");
  if(!caja || typeof Plan === "undefined") return;''',
u"la agenda de siete dias")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: la agenda se dibuja siempre, haya plan o no")
