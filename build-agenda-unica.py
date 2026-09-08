# -*- coding: utf-8 -*-
u"""Una sola agenda en la portada, y un boton de verdad para acomodarla.

   La portada tenia tres cosas hablando de la semana:

     1. Un renglon en el hero: "Hoy: 1 h 25 · SQL y Python · Ver la
        agenda".
     2. Una puerta: "Tu semana · Cambia los dias, la franja o cuanto
        rato le dedicas · Ver la semana".
     3. La agenda de los siete dias, con "Cambiar la semana" en un
        rincon de su cabecera.

   Las tres dicen lo mismo y dos llevan al mismo lado. El renglon era
   un resumen de la agenda que estaba trescientos pixeles mas abajo, y
   la puerta era el mismo link que la agenda ya tiene en su cabecera.

   El renglon se agrego cuando la agenda entera arrancaba a 2245
   pixeles del borde: era un atajo a algo que no se veia. Ahora la
   agenda esta arriba, asi que el atajo sobra. Y sobra doblemente,
   porque decia menos: el renglon muestra hoy, la agenda muestra hoy y
   los otros seis dias.

   Queda una: la agenda de los siete dias, con hoy marcado, y un boton
   para acomodarla. Antes ese boton era un link de doce pixeles y
   medio en la esquina; ahora que es la unica forma de llegar a la
   semana desde la portada, tiene que verse como algo que se aprieta.

   Uso: python build-agenda-unica.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()
if u'id="hoyMini"' not in t:
    print(u"  ya estaba"); sys.exit(1)

# ------------------------------------------------- 1. fuera el renglon
t = cambiar(t,
u'''    <!-- Lo de hoy, sin scrollear, y antes que las puertas: para quien
         ya configuro todo, esto es lo unico de la portada que mira
         todos los dias. Las puertas -empezar por el CV, armarla a
         mano, ver el catalogo- son para quien todavia no empezo. -->
    <a class="hoy-mini" id="hoyMini" href="#hoy" hidden></a>
''',
u'''    <!-- Aca habia un renglon con lo de hoy y un link a la agenda. Se
         puso cuando la agenda entera arrancaba a 2245 pixeles del
         borde: era un atajo a algo que no se veia. Ahora la agenda
         esta justo abajo, asi que eran dos cosas diciendo lo mismo, y
         la que sobraba decia menos: el renglon mostraba hoy y la
         agenda muestra hoy y los otros seis dias. -->
''',
u"el renglon del hero")

# --------------------------------------------- 2. fuera su funcion
i = t.index(u"/* El renglon de hoy, arriba de todo.")
j = t.index(u"function renderHoy(){")
t = t[:i] + u"""/* El renglon de hoy se fue de aca: decia lo mismo que la agenda, que
   ahora esta arriba y ademas muestra los siete dias. */

""" + t[j:]

t = cambiar(t,
u'''function renderHoy(){
  renderHoyMini();
  /* Y la agenda de los siete dias, por lo mismo. */
  var caja''',
u'''function renderHoy(){
  /* La agenda de los siete dias, sin esperar a que tengas plan. */
  var caja''',
u"la llamada al renglon")

# --------------------------------------------------- 3. fuera su CSS
antes = len(t)
t = re.sub(r"/\* El renglon de hoy, en el hero\..*?@media \(max-width:560px\)\{\n"
           r"  \.hm-fl span, \.hm-fl\{ font-size:0; \}\n"
           r"  \.hm-fl svg\{ width:14px; height:14px; \}\n\}\n",
           u"", t, count=1, flags=re.S)
if u".hoy-mini{" in t or len(t) == antes:
    print(u"  ABORTA: no pude sacar el CSS del renglon"); sys.exit(1)

# ------------------------------------- 4. fuera la puerta "Tu semana"
t = cambiar(t,
u'''  h += '<a class="puerta" href="semana.html">' +
    '<span class="p-ico">' + icon("clock", 19) + '</span>' +
    '<span class="p-txt"><b>Tu semana</b>' +
      '<span>Cambia los días, la franja o cuánto rato le dedicas.</span></span>' +
    '<span class="p-ir">Ver la semana ' + icon("arrow", 12) + '</span></a>';
''',
u'''  /* La puerta "Tu semana" se fue por lo mismo que la de la practica:
     llevaba al mismo lado que un boton que ya esta en la cabecera de
     la agenda, unos centimetros mas abajo. De los tres caminos a la
     semana que habia en esta pantalla queda uno, y es el que esta al
     lado de lo que vas a querer cambiar. */
''',
u"la puerta de la semana")

# ---------------------------------- 5. el link chiquito pasa a boton
t = cambiar(t,
u'''      '<a class="ag-mas" href="semana.html">Cambiar la semana</a></div>' +''',
u'''      '<a class="ag-mas" href="semana.html">' + icon("clock", 13) +
        'Acomodar mi semana</a></div>' +''',
u"el boton de la cabecera")

t = cambiar(t,
u'''.ag-mas{ margin-left:auto; font-size:12.5px; color:var(--accent);
  text-decoration:none; font-weight:650; }
.ag-mas:hover{ text-decoration:underline; }''',
u'''/* Un boton, no un link de doce pixeles y medio en un rincon. Es la
   unica forma de acomodar la semana que queda en la portada -las
   otras dos decian lo mismo y llevaban al mismo lado- asi que tiene
   que verse como algo que se aprieta. */
.ag-mas{
  margin-left:auto; display:inline-flex; align-items:center; gap:6px;
  font-size:12.5px; font-weight:700; text-decoration:none;
  color:var(--accent-strong); background:var(--accent-soft);
  border:1px solid var(--accent-line);
  padding:6px 12px; border-radius:var(--r-pill);
}
.ag-mas svg{ width:13px; height:13px; }
.ag-mas:hover{ border-color:var(--accent); }''',
u"el estilo del boton")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: una sola agenda, con boton para acomodarla")
