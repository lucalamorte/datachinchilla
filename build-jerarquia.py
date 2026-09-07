# -*- coding: utf-8 -*-
"""Jerarquia visual del catalogo.

   Las dieciseis tarjetas llevaban la clase "own", que es el estilo
   mas fuerte del sitio: borde de acento de 2px, degradado y un halo
   de 4px alrededor. Estaba pensado para destacar UNA y se aplicaba a
   todas, asi que todas parecian seleccionadas y ninguna destacaba.

   La jerarquia, de menor a mayor, y cada nivel con una sola razon de
   ser:

     base      todas las rutas. Borde gris, fondo plano, sombra chica.
     en tu semana   borde de acento tenue. Ya lo dice la cinta, asi
                    que el borde solo acompaña.
     tu ruta   borde de acento y degradado. Es UNA: la que salio de tu
               CV. Es el unico lugar del catalogo que grita.
     hover     borde de acento. Reservado para la interaccion, no
               para el estado.

   La regla de fondo: el acento marca "esto responde ahora" o "esto es
   tuyo", nunca "esto existe". Antes marcaba las tres cosas a la vez y
   por eso no significaba nada.

   Ademas se va la cinta "Lista para hacer". Estaba en las dieciseis:
   una etiqueta que llevan todas no distingue nada, y ocupaba el mismo
   lugar que "En tu semana", que si dice algo.

   Uso: python build-jerarquia.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")

CAMBIOS = [
 # --- la tarjeta deja de nacer destacada
 (u"""    html += '<div class="card-wrap' + (mia ? " es-mia" : "") + '">' + estrella + marca + (p.listo
      ? '<a class="card own" href="' + p.u + '">' + cinta + cuerpo +""",
  u"""    html += '<div class="card-wrap' + (mia ? " es-mia" : "") + '">' + estrella + marca + (p.listo
      ? '<a class="card" href="' + p.u + '">' + cinta + cuerpo +""", 1),

 # --- la cinta, solo cuando dice algo
 (u"""    /* Una sola cinta arriba: si la ruta es tuya lo dice, y si no,
       dice que está lista. Antes había dos etiquetas encimadas. */
    var cinta = mia
      ? '<span class="own-ribbon mia-ribbon">' + icon("check", 11) + 'En tu semana</span>'
      : '<span class="own-ribbon">' + icon("arrow", 11) + 'Lista para hacer</span>';""",
  u"""    /* Cinta solo cuando dice algo. "Lista para hacer" estaba en las
       dieciséis: una etiqueta que llevan todas no distingue nada, y
       ocupaba el mismo lugar que ésta, que sí. */
    var cinta = mia
      ? '<span class="own-ribbon mia-ribbon">' + icon("check", 11) + 'En tu semana</span>'
      : '';""", 1),

 # --- el estilo destacado, ahora reservado
 (u""".card.own{
  border-color:var(--accent); border-width:2px;
  background:linear-gradient(145deg, var(--surface) 40%, var(--accent-soft));
  box-shadow:0 0 0 4px color-mix(in srgb, var(--accent) 14%, transparent), var(--shadow-md);
}
.card.own .ico{ background:var(--accent); color:var(--surface); }""",
  u"""/* --- Jerarquia del catalogo ---------------------------------------

   De menor a mayor, y cada nivel con una sola razon de ser:

     base            todas las rutas. Borde gris, fondo plano.
     .es-mia         en tu semana. Borde de acento tenue: la cinta ya
                     lo dice, el borde solo acompaña.
     .tuya           la que salio de tu CV. Es UNA, y es el unico
                     lugar del catalogo que grita.
     :hover          borde de acento, reservado a la interaccion.

   El acento marca "esto responde ahora" o "esto es tuyo", nunca
   "esto existe". Antes marcaba las tres cosas y no significaba
   nada: las dieciseis llevaban la clase .own y parecian todas
   seleccionadas. */
.card.own{
  border-color:var(--accent); border-width:2px;
  background:linear-gradient(145deg, var(--surface) 40%, var(--accent-soft));
  box-shadow:0 0 0 4px color-mix(in srgb, var(--accent) 14%, transparent), var(--shadow-md);
}
.card.own .ico{ background:var(--accent); color:var(--surface); }""", 1),

 # --- en tu semana: un susurro, no un grito
 (u""".card-wrap.es-mia .card{ border-color:var(--accent); }""",
  u"""/* En tu semana: borde tenue. Con el acento entero competia con la
   ruta que de verdad es tuya, y si tenias cuatro rutas en la semana
   quedaban cuatro tarjetas gritando lo mismo. */
.card-wrap.es-mia .card{ border-color:var(--accent-line); }""", 1),
]

t = io.open(P, encoding="utf-8").read()
for viejo, nuevo, veces in CAMBIOS:
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:50], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)
io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: jerarquia definida, %d cambios" % len(CAMBIOS))
