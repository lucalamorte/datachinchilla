# -*- coding: utf-8 -*-
"""La cara de la chinchilla se invertia con el tema.

   Los ojos, el hocico y los parpados estaban pintados con --surface.
   En oscuro --surface es casi negro, asi que el ojo quedaba oscuro
   sobre un cuerpo claro y se leia como pupila. En claro --surface es
   blanco y el cuerpo es el acento, que es oscuro: la misma chinchilla
   quedaba con los ojos y el hocico en blanco, sin pupila. Se veia
   rara y era eso.

   El arreglo no es cambiar el ojo: es que la cara no dependa del
   tema. El cuerpo pasa a ser siempre un tono claro del acento y el
   ojo siempre oscuro, que es como se leia en oscuro, el que esta
   bien.

   Los numeros salen de medir, no de probar: con el cuerpo al 68% del
   acento sobre blanco, el ojo queda entre 4.4 y 5.4 contra el cuerpo
   en las cinco familias de acento del sitio, y el cuerpo entre 2.6 y
   3.5 contra el fondo claro. En oscuro el cuerpo sigue siendo el
   acento, que ya es claro.

   Uso: python build-cara.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "chinchilla.css")

VIEJO = u""".chin-pose{ width:104px; height:96px; overflow:visible; }
.chin-pose .c-cuerpo,
.chin-pose .c-cabeza{ fill:var(--accent); }
.chin-pose .c-oreja{ fill:var(--accent); }
.chin-pose .c-oreja-in{ fill:var(--marca-soft); }
.chin-pose .c-ojo{ fill:var(--surface); }
.chin-pose .c-brillo{ fill:var(--accent); }
.chin-pose .c-hocico{ fill:var(--surface); }
.chin-pose .c-pata{ fill:var(--accent-strong); }
.chin-pose .c-cola{
  fill:none; stroke:var(--accent-strong); stroke-width:7; stroke-linecap:round;
}
.chin-pose .c-ojo-l{
  fill:none; stroke:var(--surface); stroke-width:2.4; stroke-linecap:round;
}"""

NUEVO = u"""/* --- La cara, que no depende del tema ----------------------------

   Estaba pintada con --surface. En oscuro eso es casi negro: el ojo
   quedaba oscuro sobre un cuerpo claro y se leia como pupila. En
   claro es blanco y el cuerpo es el acento, que es oscuro: la misma
   chinchilla quedaba con los ojos en blanco.

   Asi que el cuerpo es siempre claro y el ojo siempre oscuro, en los
   dos temas. En oscuro el acento ya es claro y se usa tal cual; en
   claro es oscuro y se aclara.

   El 68% sale de medir: con ese valor el ojo queda entre 4.4 y 5.4
   contra el cuerpo en las cinco familias de acento del sitio, y el
   cuerpo entre 2.6 y 3.5 contra el fondo. Mas claro y el ojo se
   pierde; mas oscuro y el cuerpo se confunde con el fondo. */
.chin-pose{
  width:104px; height:96px; overflow:visible;
  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-pata:   color-mix(in srgb, var(--accent) 86%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);
  --chin-luz:    #FFFFFF;
}
:root[data-theme="dark"] .chin-pose{
  --chin-cuerpo: var(--accent);
  --chin-pata:   var(--accent-strong);
}
.chin-pose .c-cuerpo,
.chin-pose .c-cabeza{ fill:var(--chin-cuerpo); }
.chin-pose .c-oreja{ fill:var(--chin-cuerpo); }
.chin-pose .c-oreja-in{ fill:var(--marca-soft); }
.chin-pose .c-ojo{ fill:var(--chin-ojo); }
/* El brillo va claro porque ahora el ojo es oscuro. Antes el ojo era
   claro y el brillo llevaba el acento; invertido, no se veia. */
.chin-pose .c-brillo{ fill:var(--chin-luz); }
.chin-pose .c-hocico{ fill:var(--chin-ojo); }
.chin-pose .c-pata{ fill:var(--chin-pata); }
.chin-pose .c-cola{
  fill:none; stroke:var(--chin-pata); stroke-width:7; stroke-linecap:round;
}
.chin-pose .c-ojo-l{
  fill:none; stroke:var(--chin-ojo); stroke-width:2.4; stroke-linecap:round;
}"""

VIEJO_ASOMA = u""".chin-asoma .c-cabeza, .chin-asoma .c-oreja{ fill:var(--accent); }
.chin-asoma .c-oreja-in{ fill:var(--marca-soft); }
.chin-asoma .c-ojo, .chin-asoma .c-hocico{ fill:var(--surface); }
.chin-asoma .c-brillo{ fill:var(--accent); }"""

NUEVO_ASOMA = u"""/* La que se asoma en el pie, con la misma cara que las demas. */
.chin-asoma{
  --chin-cuerpo: color-mix(in srgb, var(--accent) 68%, #FFFFFF);
  --chin-ojo:    color-mix(in srgb, var(--accent) 26%, #0E0A16);
}
:root[data-theme="dark"] .chin-asoma{ --chin-cuerpo: var(--accent); }
.chin-asoma .c-cabeza, .chin-asoma .c-oreja{ fill:var(--chin-cuerpo); }
.chin-asoma .c-oreja-in{ fill:var(--marca-soft); }
.chin-asoma .c-ojo, .chin-asoma .c-hocico{ fill:var(--chin-ojo); }
.chin-asoma .c-brillo{ fill:#FFFFFF; }"""

t = io.open(P, encoding="utf-8").read()
for viejo, nuevo in [(VIEJO, NUEVO), (VIEJO_ASOMA, NUEVO_ASOMA)]:
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %r aparece %d veces, esperaba 1" % (viejo[:48], n))
        sys.exit(1)
    t = t.replace(viejo, nuevo, 1)

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"chinchilla.css: la cara ya no se invierte con el tema")
