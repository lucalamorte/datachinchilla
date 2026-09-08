# -*- coding: utf-8 -*-
u"""La colita pomposa, en todas las poses. Y que se note que escarba.

   1. LA COLA. Solo la tenia la pose de dormir, y ahi era una manta:
      un trazo curvo alrededor del cuerpo. En las otras seis no habia
      nada. Una chinchilla sin cola no se lee como chinchilla, se lee
      como un raton gordo.

      La cola va como funcion, no copiada seis veces: una espina
      curva de trazo grueso con tres mechones encima, que a este
      tamano es lo que hace "pomposa" en vez de "de raton". Recibe
      hacia que lado va y desde donde sale, porque en cada pose el
      lugar libre es otro: en la lupa esta ocupada la derecha, en el
      cafe tambien, y saludando el brazo va por ahi.

      Va ANTES del cuerpo en cada pose, para que salga por detras.

   2. QUE SE NOTE QUE ESCARBA. Las dos patas eran dos ovalos iguales
      abajo del cuerpo, a la misma altura: eso son pies parado, no
      brazos cavando. Y con el pozo delante, lo que se veia era una
      chinchilla sentada atras de un monticulo.

      Ahora los brazos salen del hombro y bajan hacia adentro del
      pozo, como el brazo del saludo, que ya demostro que a este
      tamano un trazo grueso con una mano al final se lee como brazo.
      Se mueven alternados: uno baja mientras el otro sube, que es lo
      que hace cualquier bicho cavando. El cuerpo se inclina hacia
      adelante en vez de saltar en el lugar, y la cola queda arriba,
      que es la postura de cabeza adentro del pozo.

   El cohete no lleva cola a proposito: ahi de ella se ve la cabeza
   por la ventanilla y nada mas. Ponerle una cola al cohete no es
   ponerle la cola a la chinchilla.

   Uso: python build-cola.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s aparece %d veces, esperaba 1"
              % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# =================================================== chinchilla.js
P = os.path.join(D, "chinchilla.js")
t = io.open(P, encoding="utf-8").read()
if u"function cola(" in t:
    print(u"  ya estaba"); sys.exit(1)

# --- 1. la funcion, al lado del cuerpo
t = cambiar(t,
u'''  function ojos(cerrados){''',
u'''  /* La cola pomposa.

     Una chinchilla sin cola se lee como un raton gordo. La tenia solo
     la pose de dormir, y ahi hace de manta.

     Es una espina curva de trazo grueso con tres mechones encima: a
     104 pixeles, eso es lo que separa "pomposa" de "de raton". Un
     solo trazo, por grueso que sea, sale liso.

     `lado` es -1 o 1 porque el lugar libre cambia en cada pose: la
     lupa ocupa la derecha, la taza tambien, y el brazo del saludo va
     por ahi. `alto` sube la punta cuando el cuerpo esta inclinado.

     Va antes del cuerpo en cada pose, para salir por detras. */
  function cola(lado, x, y, alto){
    var d = lado || 1, ax = x || 66, ay = y || 64, up = alto || 0;
    function p(dx, dy){ return (ax + d * dx) + " " + (ay + dy - up); }
    return '<g class="c-cola-g">' +
      '<path class="c-cola" d="M' + p(0, 0) +
        'Q' + p(20, -2) + " " + p(21, -18) + '"/>' +
      '<circle class="c-mecha" cx="' + (ax + d * 9)  + '" cy="' + (ay - 4 - up)  + '" r="6.4"/>' +
      '<circle class="c-mecha" cx="' + (ax + d * 17) + '" cy="' + (ay - 10 - up) + '" r="6"/>' +
      '<circle class="c-mecha" cx="' + (ax + d * 21) + '" cy="' + (ay - 19 - up) + '" r="5.2"/>' +
      '</g>';
  }

  function ojos(cerrados){''',
u"la funcion de la cola", "chinchilla.js")

# --- 2. escarbando, de nuevo
t = cambiar(t,
u'''          '<g class="c-bicho">' + cuerpo() + ojos(false) + hocico() +
            '<ellipse class="c-pata" cx="34" cy="72" rx="6" ry="4.5"/>' +
            '<ellipse class="c-pata" cx="66" cy="72" rx="6" ry="4.5"/>' +
          '</g>' +''',
u'''          '<g class="c-bicho">' +
            /* La cola arriba: es la postura de tener la cabeza
               adentro del pozo, y de paso es lo que mas se ve de una
               chinchilla escarbando. */
            cola(1, 68, 58, 10) +
            cuerpo() + ojos(false) + hocico() +
            /* Brazos, no pies. Eran dos ovalos iguales a la misma
               altura abajo del cuerpo: eso es estar parada. Salen del
               hombro y bajan al pozo, como el brazo del saludo, y se
               mueven alternados. */
            '<g class="c-brazo-cava c-brazo-izq">' +
              '<path class="c-hueso" d="M38 62L30 76"/>' +
              '<ellipse class="c-pata" cx="29" cy="78" rx="5.6" ry="4.4"/>' +
            '</g>' +
            '<g class="c-brazo-cava c-brazo-der">' +
              '<path class="c-hueso" d="M62 62L70 76"/>' +
              '<ellipse class="c-pata" cx="71" cy="78" rx="5.6" ry="4.4"/>' +
            '</g>' +
          '</g>' +''',
u"la pose de escarbar", "chinchilla.js")

# --- 3. la cola en las otras poses
for viejo, nuevo, que in [
  # dormida: la manta se queda, pero ahora es pomposa
  (u'''          '<path class="c-cola" d="M74 62q16 -4 14 10q-2 12 -16 8"/>' +
          cuerpo() + ojos(true) + hocico() +''',
   u'''          /* Acá hace de manta, enroscada, así que no usa cola():
             es la única pose donde la cola no va detrás sino
             alrededor. Los mechones la hacen pomposa igual. */
          '<path class="c-cola" d="M74 62q16 -4 14 10q-2 12 -16 8"/>' +
          '<circle class="c-mecha" cx="84" cy="64" r="6"/>' +
          '<circle class="c-mecha" cx="88" cy="72" r="5.6"/>' +
          '<circle class="c-mecha" cx="82" cy="79" r="5.2"/>' +
          cuerpo() + ojos(true) + hocico() +''',
   u"la cola de la dormida"),

  # buscando: la lupa ocupa la derecha
  (u'''      return '<g class="c-busca">' + cuerpo() + ojos(false) + hocico() + '</g>' +''',
   u'''      return '<g class="c-busca">' + cola(-1, 34, 64, 0) +
        cuerpo() + ojos(false) + hocico() + '</g>' +''',
   u"la cola de la que busca"),

  # festejando: las patas van arriba, la cola detras
  (u'''      return '<g class="c-salta">' +
          cuerpo() + ojos(false) + hocico() +''',
   u'''      return '<g class="c-salta">' +
          cola(1, 66, 66, 0) +
          cuerpo() + ojos(false) + hocico() +''',
   u"la cola de la que festeja"),

  # saludando: el brazo va por la derecha
  (u'''    saluda: function(){
      return cuerpo() + ojos(false) + hocico() +''',
   u'''    saluda: function(){
      return cola(-1, 34, 64, 0) + cuerpo() + ojos(false) + hocico() +''',
   u"la cola de la que saluda"),

  # el cafe: la taza ocupa la derecha
  (u'''      return '<g class="c-toma">' + cuerpo() + ojos(false) + hocico() +''',
   u'''      return '<g class="c-toma">' + cola(-1, 34, 64, 0) +
          cuerpo() + ojos(false) + hocico() +''',
   u"la cola de la del cafe"),
]:
    t = cambiar(t, viejo, nuevo, que, "chinchilla.js")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"chinchilla.js: cola en seis poses, y escarbar con brazos")


# =================================================== chinchilla.css
C = os.path.join(D, "chinchilla.css")
c = io.open(C, encoding="utf-8").read()

c = cambiar(c,
u'''.chin-pose .c-cola{
  fill:none; stroke:var(--chin-pata); stroke-width:7; stroke-linecap:round;
}''',
u'''.chin-pose .c-cola{
  fill:none; stroke:var(--chin-pata); stroke-width:7; stroke-linecap:round;
}
/* Los mechones. Del mismo tono que la espina y encima de ella: es lo
   que hace que la cola se lea pomposa y no como un cable. Separados
   no se tocan bien; superpuestos forman un solo bulto irregular, que
   es lo que uno quiere. */
.chin-pose .c-mecha{ fill:var(--chin-pata); }''',
u"el estilo de los mechones", "chinchilla.css")

c = cambiar(c,
u'''.c-tierra{ animation:tierra 1.1s ease-out infinite; }''',
u'''/* Los brazos, alternados: uno baja mientras el otro sube. Un bicho
   cavando no mueve los dos brazos a la vez, y con los dos iguales
   parecia que hacia flexiones. */
.c-brazo-cava{ animation:cavabrazo 1.1s ease-in-out infinite; }
.c-brazo-izq{ transform-origin:38px 62px; }
.c-brazo-der{ transform-origin:62px 62px; animation-delay:.55s; }
@keyframes cavabrazo{
  0%, 100%{ transform:rotate(0deg); }
  50%{ transform:rotate(-16deg); }
}
.c-tierra{ animation:tierra 1.1s ease-out infinite; }''',
u"la animacion de los brazos", "chinchilla.css")

# El cuerpo, inclinado hacia adelante en vez de saltando en el lugar.
c = cambiar(c,
u'''@keyframes cava{
  0%, 100%{ transform:translateY(0) rotate(0deg); }
  30%{ transform:translateY(7px) rotate(-4deg); }
  60%{ transform:translateY(2px) rotate(3deg); }
}''',
u'''/* Inclinada hacia adelante y hundiendose, no saltando en el lugar:
   la cabeza entra en el pozo y vuelve. Antes se movia entera de
   arriba abajo, que a ojo es un salto. */
@keyframes cava{
  0%, 100%{ transform:translateY(0) rotate(0deg); }
  35%{ transform:translateY(8px) rotate(-3deg); }
  70%{ transform:translateY(3px) rotate(1.5deg); }
}''',
u"la animacion del cuerpo", "chinchilla.css")

# Y que se quede quieta si el sistema lo pide.
c = cambiar(c,
u'''  .c-bicho, .c-tierra, .c-pozo, .c-duerme, .c-z, .c-busca, .c-lupa,''',
u'''  .c-bicho, .c-tierra, .c-pozo, .c-duerme, .c-z, .c-busca, .c-lupa,
  .c-brazo-cava,''',
u"la lista de lo que se queda quieto", "chinchilla.css")

io.open(C, "w", encoding="utf-8", newline="").write(c)
print(u"chinchilla.css: mechones, brazos alternados y el cuerpo inclinado")
