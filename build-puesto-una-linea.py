# -*- coding: utf-8 -*-
u"""Una descripcion por puesto, y ninguna tarjeta elegida de arranque.

   1. DOS DESCRIPCIONES. Cada tarjeta mostraba `resumen` -que dice que
      hace el puesto- y abajo `distingue` -que dice en que se
      diferencia del de al lado-. Son dos, y en varios casos dicen lo
      mismo con otras palabras. En dos son la misma frase:

        Frontend  R: "...que se entienda, que responda y que funcione
                      en cualquier pantalla."
                  D: "Su problema es que se entienda y funcione en
                      cualquier pantalla."

        Backend   R: "...las APIs, los datos y que aguante cuando
                      entra gente de verdad."
                  D: "Su problema es que aguante y que los datos esten
                      bien."

      `distingue` se agrego para que no se confundieran Data Engineer,
      Cloud Engineer, Big Data y AI Engineer. Pero mirando los cuatro,
      el `resumen` ya los separa solo: pipelines y modelo de datos,
      infraestructura que no cueste una fortuna, datos que no entran
      en una maquina, y modelos en produccion. La segunda linea no
      agregaba la distincion: la repetia.

      Queda `resumen`, que es el que contesta "que es este puesto",
      que es la pregunta que uno tiene mirando trece tarjetas.

   2. LA TARJETA ELEGIDA DE ARRANQUE. `puestoElegido` arranca en
      "data_engineer", y el aria-pressed salia de esa variable. O sea
      que Data Engineer se veia elegido sin que nadie lo eligiera,
      mientras el globo decia "Elige un puesto para seguir" y el boton
      no avanzaba. La tarjeta decia una cosa y el recorrido otra, y
      quien no probaba dos veces se quedaba trabado ahi.

      El aria-pressed pasa a salir de lo que hay guardado, que es lo
      unico que cuenta como haber elegido. La variable sigue con su
      valor por defecto, que es lo que se usa para calcular mientras
      no elegiste.

   Uso: python build-puesto-una-linea.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "cv.html")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n))
        sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()
if u"una sola descripcion por tarjeta" in t:
    print(u"  ya estaba"); sys.exit(1)

# --------------------------------------------- 1. una sola descripcion
t = cambiar(t,
u'''    html += '<button class="puesto" type="button" data-puesto="' + p.id + '" ' +
      'aria-pressed="' + (p.id === puestoElegido ? "true" : "false") + '">' +
      '<b>' + esc(p.nombre) + '</b><span>' + esc(p.resumen) + '</span>' +
      /* En qué se diferencia del de al lado. Va aparte del resumen
         porque son dos preguntas distintas -qué hace, y en qué se
         distingue- y quien elige entre dos parecidos necesita la
         segunda. */
      (p.distingue ? '<span class="distingue">' + esc(p.distingue) + '</span>' : "") +''',
u'''    /* Elegido es lo que esta guardado, no la variable.

       `puestoElegido` arranca en "data_engineer" para poder calcular,
       y de aca salia el aria-pressed: Data Engineer se veia elegido
       sin que nadie lo eligiera, mientras el globo pedia elegir uno y
       el boton no avanzaba. */
    var elegido = (typeof Onb !== "undefined" && Onb.estado.puesto) || "";

    /* Una sola descripcion por tarjeta.

       Habia dos: `resumen` -que hace- y `distingue` -en que se
       diferencia del de al lado-. En varios puestos decian lo mismo, y
       en Frontend y Backend eran la misma frase. `distingue` se puso
       para separar Data Engineer de Cloud, Big Data y AI Engineer,
       pero el resumen de esos cuatro ya los separa solo. */
    html += '<button class="puesto" type="button" data-puesto="' + p.id + '" ' +
      'aria-pressed="' + (p.id === elegido ? "true" : "false") + '">' +
      '<b>' + esc(p.nombre) + '</b><span>' + esc(p.resumen) + '</span>' +''',
u"la tarjeta del puesto")

# --------------------------------------------- 2. el CSS que queda sin uso
t = cambiar(t,
u'''.puesto[aria-pressed="true"] .distingue{ border-top-color:var(--accent-line); }''',
u'''/* La regla de .distingue se fue con la segunda descripcion. */''',
u"la regla de .distingue elegida")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"cv.html: una descripcion por puesto, y ninguno elegido de arranque")
