# -*- coding: utf-8 -*-
u"""La guia describia una pagina que ya no existe.

   cv.html tiene cinco secciones, en este orden:

     1. A que apuntas          #puestos
     2. Carga tu CV            #cvZona
     3. Esto ya lo tienes      #sabe, y el boton de agregar
     4. Cinco preguntas        #pasoPreg
     5. Lo que te falta        #guardarRuta

   La guia tenia cuatro pasos y saltaba del 3 al 5: la seccion de las
   preguntas no existia para el recorrido. El globo hablaba de los
   skills, y despues aparecia una seccion de preguntas de la que nadie
   habia dicho nada, entre medio de las dos cosas que si nombraba.

   Y el paso del CV decia "si no lo tienes a mano, contesta las cuatro
   preguntas de abajo". Son cinco desde que se rehicieron, y abajo del
   CV ya no estan: estan dos secciones mas abajo, despues de los
   skills. O sea que el recorrido te mandaba a buscar algo donde no
   estaba, y lo que encontrabas ahi era otra cosa.

   Las dos cosas juntas son el desorden: te pide el CV, te manda a unas
   preguntas que no estan donde dice, te habla de skills, y despues
   aparece la seccion de preguntas sin anunciar.

   Tambien se corrige el paso de los skills, que solo hablaba de
   sacar. Se pueden agregar desde que se pidio, y el globo era el
   unico lugar que seguia sin decirlo.

   El recorrido pasa de nueve pasos a diez. El numero no esta escrito
   en ningun lado: sale de PASOS.length.

   Uso: python build-guia-al-dia.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "guia.js")


def cambiar(t, viejo, nuevo, que):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA: %s aparece %d veces, esperaba 1" % (que, n))
        sys.exit(1)
    return t.replace(viejo, nuevo, 1)


t = io.open(P, encoding="utf-8").read()
if u'id: "preguntas"' in t:
    print(u"  ya estaba"); sys.exit(1)

# ------------------------------------- 1. el paso del CV, sin mandar a un lugar equivocado
t = cambiar(t,
u'''      texto: "Arrastra el CV o pega el texto. Si no lo tienes a mano, contesta " +
             "las cuatro preguntas de abajo y sale lo mismo. En cuanto lo lea te " +
             "muestro qué reconocí y cuál de las rutas te sirve.",''',
u'''      /* Decia "las cuatro preguntas de abajo". Son cinco, y abajo del
         CV ya no estan: quedaron dos secciones mas abajo, despues de
         los skills. Mandaba a buscar algo donde no estaba. */
      texto: "Arrastra el CV o pega el texto. Si no lo tienes a mano no pasa " +
             "nada: sigue igual y más adelante te hago unas preguntas que " +
             "sirven para lo mismo. En cuanto lea algo te muestro qué reconocí.",''',
u"el texto del paso del CV")

# ------------------------------------- 2. el paso de los skills tambien deja agregar
t = cambiar(t,
u'''      texto: "Lo que reconocí en lo que contaste, y que por eso no te voy a " +
             "ofrecer. Si alguno no corresponde, sácalo con su cruz y rehago la " +
             "ruta sin él.",
      accion: "Está bien así",''',
u'''      /* Solo hablaba de sacar. Agregar se puede desde que se pidio, y
         este globo era el unico lugar que no lo decia. */
      texto: "Lo que reconocí en lo que contaste, y que por eso no te voy a " +
             "ofrecer. Si alguno no corresponde, sácalo con su cruz; y si me " +
             "falta alguno que sabes, agrégalo tú. Rehago la ruta con eso.",
      accion: "Está bien así",''',
u"el texto del paso de los skills")

# ------------------------------------- 3. el paso que faltaba: las preguntas
t = cambiar(t,
u'''    {
      id: "guardar",
      donde: "cv",''',
u'''    {
      /* Este paso no existia y la seccion si. El recorrido saltaba de
         los skills a la ruta, y en el medio aparecia una seccion de
         preguntas de la que no habia hablado nadie. */
      id: "preguntas",
      donde: "cv",
      titulo: "Cinco preguntas, de a una",
      texto: "Para afinar lo que te falta. Van de a una y se contestan rápido; " +
             "lo que respondas se suma a lo que ya reconocí. Si prefieres, " +
             "puedes seguir sin contestarlas.",
      accion: "Seguir",
      lleva: "",
      ancla: "#pasoPreg"
    },
    {
      id: "guardar",
      donde: "cv",''',
u"el paso de las preguntas")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"guia.js: el recorrido sigue el orden real de la pagina (10 pasos)")
