# -*- coding: utf-8 -*-
"""Lo que quedo hablando de la ruta de la que se copio.

   La pagina se arma copiando claude.html, y cuatro textos y una
   variable siguieron diciendo lo de Claude: dieciseis cursos de
   Anthropic, y la clave de ruta con la que el boton "sumar a tu
   semana" decide que esta activando. Esa ultima es la peor, porque
   no se ve: el boton de Full Stack Open activaba la ruta de Claude.

   Los cuatro numeros los encontro cuentas.py. La clave no, porque
   nadie la estaba mirando: se agrega a la lista de lo que se
   verifica.

   Uso: python build-fullstack-textos.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "fullstack.html")

CAMBIOS = [
 # la variable que decide que ruta activa el boton del hero
 (u'var MI_RUTA = "claude";', u'var MI_RUTA = "fullstack";', 1),

 (u"<h2>Cinco tramos, dieciséis cursos</h2>",
  u"<h2>Cinco tramos, quince partes</h2>", 1),

 (u'<p class="hero-foot">Los dieciséis cursos son de Anthropic y se hacen en su academia. '
  u'Yo no los doy: esta página elige cuáles de los veinticinco te sirven y en qué orden. '
  u'Quedan afuera las ocho versiones de AI Fluency para otras audiencias y el de despliegue '
  u'para equipos de IT.</p>',
  u'<p class="hero-foot">Las quince partes son de la Universidad de Helsinki y se hacen en '
  u'su sitio. Yo no las doy: esta página las pone en orden, marca dónde termina el curso '
  u'base y te lleva la cuenta de por dónde vas. El certificado lo emite Helsinki, no yo.</p>', 1),

 (u'"Los dieciséis cursos"', u'"Las quince partes"', 1),
]

t = io.open(P, encoding="utf-8").read()
for viejo, nuevo, veces in CAMBIOS:
    n = t.count(viejo)
    if n != veces:
        print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:52], n, veces))
        sys.exit(1)
    t = t.replace(viejo, nuevo)
io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"fullstack.html: %d textos que hablaban de la otra ruta" % len(CAMBIOS))
