# -*- coding: utf-8 -*-
"""El tema claro se veia plano al lado del oscuro.

   Tres causas, medidas y no opinadas:

   1. Las tarjetas no tenian sombra. En oscuro la separacion la hace
      el borde, que es mas claro que el fondo y se lee solo. En claro
      un borde palido sobre casi blanco no alcanza: la profundidad de
      una interfaz clara la hace la sombra. .puerta, .ir-ruta, .reto-c
      y .card-wrap tenian box-shadow: none, o sea que las tarjetas
      eran una linea dibujada y nada mas.

   2. El borde era demasiado suave: #D8DEE6 sobre blanco da 1.35, que
      es casi nada. Pasa a #C8D2DE, que da 1.53.

   3. El degradado del fondo casi no se veia. El acento entraba al 14%
      y al 7%; en oscuro el mismo 9% se nota mucho mas porque el
      acento es mucho mas claro que el fondo, y en claro es mas oscuro
      y queda tapado. Sube a 26% y 14%.

   Lo que NO se toca: --bg. Bajarlo a un gris mas profundo separaba
   mejor las tarjetas -1.10 a 1.17- pero dejaba --text-3 en 4.29,
   abajo del minimo AA de 4.5. La profundidad se paga con sombra, no
   con contraste de texto.

   Uso: python build-claro.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "tema.css")

CAMBIOS = [
 # --- 1. el borde, que casi no se veia sobre blanco
 (u"  --divider:       #D8DEE6;",
  u"  /* 1.53:1 sobre blanco. Estaba en #D8DEE6, que daba 1.35 y dejaba\n"
  u"     las tarjetas sin contorno visible. */\n"
  u"  --divider:       #C8D2DE;", 1),

 # --- 2. el degradado del fondo
 (u"""body{
  margin:0;
  background:
    radial-gradient(1200px 680px at 82% -16%,
      color-mix(in srgb, var(--accent) 14%, transparent), transparent 60%),
    radial-gradient(900px 520px at -6% 4%,
      color-mix(in srgb, var(--accent) 7%, transparent), transparent 58%),
    var(--bg);""",
  u"""body{
  margin:0;
  /* En claro el acento es mas oscuro que el fondo, asi que un 14% se
     pierde; en oscuro es mas claro y con 9% ya se nota. Por eso los
     dos temas no llevan el mismo numero. */
  background:
    radial-gradient(1200px 680px at 82% -16%,
      color-mix(in srgb, var(--accent) 26%, transparent), transparent 60%),
    radial-gradient(900px 520px at -6% 4%,
      color-mix(in srgb, var(--accent) 14%, transparent), transparent 58%),
    var(--bg);""", 1),
]

EXTRA = u"""
/* --- Profundidad en el tema claro ---------------------------------

   En oscuro la separacion la hace el borde: es mas claro que el fondo
   y el ojo lo lee solo. En claro un borde palido sobre casi blanco no
   alcanza, y la profundidad la tiene que hacer la sombra, que es como
   funcionan las interfaces claras.

   Estas cuatro estaban con box-shadow: none, asi que las tarjetas
   quedaban dibujadas con una linea y la pagina se veia plana al lado
   del tema oscuro.

   Va solo en claro: en oscuro las sombras casi no se ven y el trabajo
   ya lo hace el borde. */
:root:not([data-theme="dark"]) .puerta,
:root:not([data-theme="dark"]) .ir-ruta,
:root:not([data-theme="dark"]) .reto-c,
:root:not([data-theme="dark"]) .ra-card,
:root:not([data-theme="dark"]) .grid-cards .card-wrap > .card,
:root:not([data-theme="dark"]) .cv-paso{
  box-shadow: var(--shadow-sm);
}
:root:not([data-theme="dark"]) .puerta:hover,
:root:not([data-theme="dark"]) .ir-ruta:hover{
  box-shadow: var(--shadow-md);
}
"""

t = io.open(P, encoding="utf-8").read()
for viejo, nuevo, veces in CAMBIOS:
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:48], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)

if "Profundidad en el tema claro" in t:
    print(u"  ya estaba puesto")
    sys.exit(1)
t = t.rstrip() + u"\n" + EXTRA

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"tema.css: sombras en claro, borde mas firme y degradado que se ve")
