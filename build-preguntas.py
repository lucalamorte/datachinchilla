# -*- coding: utf-8 -*-
"""Las preguntas frecuentes, en su propia pagina.

   Estaban en la portada y no venian a cuento: la portada es el home
   de la aplicacion, no un folleto. Ocho acordeones en el medio son
   justo el tipo de cosa que la ensucia.

   Se van a preguntas.html, se enlazan desde el pie, y en la portada
   no queda nada de esto.

   Ademas se rehace la respuesta de la plata. Estaban las tres
   primeras diciendo lo mismo con otras palabras -no cuesta, no va a
   costar, de que vive- y leidas juntas suenan a alguien defendiendose.
   Queda una sola, y dice lo que de verdad pasa: es un aporte, se
   puede colaborar si a alguien le sirvio, y esta la puerta abierta.

   Y se saca de la ultima respuesta el detalle de que cinco problemas
   pasaron a ser de pago. A quien pregunta no le sirve saber eso y
   deja al sitio pareciendo menos confiable de lo que es.

   Se arma copiando armar.html, que es la pagina mas simple que hay.

   Uso: python build-preguntas.py
"""
import io, os, json, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(D, "armar.html")
SALE = os.path.join(D, "preguntas.html")
INDEX = os.path.join(D, "index.html")

FAQ = [
 (u"¿Esto cuesta algo?",
  u"No, y no hay una versión de pago más adelante. Es un aporte: junté en un "
  u"lugar el material gratuito que ya existe suelto por internet y le puse un "
  u"orden. Si te sirvió y te dan ganas, podés "
  u"<a href=\"https://ko-fi.com/lucalamorte\" target=\"_blank\" rel=\"noopener\">invitarme un café</a> "
  u"o <a href=\"https://www.linkedin.com/in/lclamorte/\" target=\"_blank\" rel=\"noopener\">saludarme por LinkedIn</a>, "
  u"que siempre alegra. Ninguna de las dos cosas destraba nada: quien no las "
  u"toca ve exactamente el mismo sitio.",
  u"No, y no hay version de pago mas adelante. Es un aporte a la comunidad: "
  u"material gratuito que ya existe, ordenado en un lugar. Se puede colaborar "
  u"con un cafe si alguien quiere, pero no destraba ninguna funcion."),

 (u"¿Quién dicta los cursos?",
  u"Quien los hizo. Harvard, la Universidad de Helsinki, dbt Labs, Anthropic, "
  u"AWS, CognitiveClass y varios más. Acá no se dicta ninguno: se eligen, se "
  u"ponen en orden, se dice cuánto lleva cada uno y qué te deja, y se te lleva "
  u"la cuenta de por dónde vas.",
  u"Quien los hizo: Harvard, la Universidad de Helsinki, dbt Labs, Anthropic, "
  u"AWS y otros. DataChinchilla no dicta cursos: los ordena."),

 (u"¿Qué pasa con mi CV?",
  u"Se lee en tu navegador y no se sube a ningún lado. El texto se cruza contra "
  u"una lista de temas que está en el mismo sitio, y de ahí sale la ruta. Si "
  u"cerrás la pestaña sin guardar, no queda nada.",
  u"Se lee en el navegador y no se sube a ningun servidor. Si se cierra la "
  u"pestana sin guardar, no queda nada."),

 (u"¿Para qué necesito una cuenta?",
  u"Sólo para que tu avance te siga a otra computadora. Podés recorrer todo el "
  u"sitio, leer las rutas, ver los problemas y sacar tu ruta del CV sin crear "
  u"nada. La cuenta hace falta recién cuando querés que lo que marcaste quede "
  u"guardado.",
  u"Solo para guardar el avance y que siga en otro dispositivo. Se puede "
  u"recorrer todo el sitio sin crear cuenta."),

 (u"¿Los certificados los emiten ustedes?",
  u"No. El que vale lo emite quien dicta el curso, y se baja de su sitio. Acá "
  u"hay una constancia de que recorriste una ruta, que dice en la misma hoja "
  u"que no es un certificado oficial ni acredita conocimiento.",
  u"No. El certificado que vale lo emite quien dicta el curso. DataChinchilla "
  u"emite una constancia de recorrido que aclara que no es oficial."),

 (u"¿Y si un curso deja de ser gratis o el link se cae?",
  u"Se saca o se reemplaza por algo gratis que sirva igual. Si encontrás uno "
  u"roto o con candado, "
  u"<a href=\"mailto:luca.lamorte@kcc.com?subject=Un%20link%20roto%20en%20DataChinchilla\">escribime</a> "
  u"y lo miro.",
  u"Se saca o se reemplaza por algo gratis equivalente. Se puede avisar por "
  u"correo."),

 (u"¿Puedo sumar material?",
  u"Sí, y es bienvenido: un curso, un canal, un dataset o un apunte tuyo, "
  u"mientras sea gratis y se pueda enlazar. "
  u"<a href=\"mailto:luca.lamorte@kcc.com?subject=Material%20para%20DataChinchilla\">Escribime</a> "
  u"y lo miro.",
  u"Si. Se puede proponer por correo cualquier material gratuito y enlazable."),
]


def cuerpo():
    filas = []
    for i, (q, r, _) in enumerate(FAQ):
        filas.append(
            u'      <details class="faq-i"%s>\n'
            u'        <summary>%s</summary>\n'
            u'        <p>%s</p>\n'
            u'      </details>' % (u" open" if i == 0 else u"", q, r))
    datos = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": pl}}
                       for q, _, pl in FAQ],
    }
    return (
        u'<section class="hero" id="top">\n'
        u'  <div class="wrap">\n'
        u'    <span class="eyebrow">Preguntas frecuentes</span>\n'
        u'    <h1>Antes de que lo <span class="grad">preguntes</span></h1>\n'
        u'    <p class="hero-lead">Lo que suele preguntarse antes de empezar. Si te queda '
        u'algo afuera, escribime y lo agrego.</p>\n'
        u'  </div>\n'
        u'</section>\n\n'
        u'<section class="section" id="preguntas">\n'
        u'  <div class="wrap">\n'
        u'    <div class="faq">\n' + u"\n".join(filas) + u'\n    </div>\n'
        u'  </div>\n'
        u'  <script type="application/ld+json">' +
        json.dumps(datos, ensure_ascii=False) + u'</script>\n'
        u'</section>\n')


def main():
    t = io.open(BASE, encoding="utf-8").read()

    # el cuerpo entre el header y el pie
    i = t.index("</header>") + len("</header>")
    j = t.index("<footer")
    t = t[:i] + u"\n\n" + cuerpo() + u"\n" + t[j:]

    # lo propio de la pagina
    for viejo, nuevo, veces in [
        (u'<span class="brand-sub">/ Arma tu ruta</span>',
         u'<span class="brand-sub">/ Preguntas</span>', 1),
    ]:
        if t.count(viejo) != veces:
            print(u"  ABORTA: %r aparece %d veces" % (viejo[:44], t.count(viejo)))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    io.open(SALE, "w", encoding="utf-8", newline="").write(t)
    print(u"preguntas.html: %d preguntas" % len(FAQ))

    # --- y la portada se queda sin la seccion
    x = io.open(INDEX, encoding="utf-8").read()
    a = x.index(u'\n<section class="section" id="faq">')
    b = x.index(u"</section>", x.index(u"</script>", a)) + len(u"</section>\n")
    x = x[:a] + x[b:]
    # el enlace, en el pie, que quedo con lugar
    viejo_pie = u'      <a href="https://ko-fi.com/lucalamorte"'
    x = x.replace(viejo_pie,
                  u'      <a href="preguntas.html">Preguntas frecuentes</a>\n' + viejo_pie, 1)
    io.open(INDEX, "w", encoding="utf-8", newline="").write(x)
    print(u"index.html: la seccion sale de la portada y queda el enlace en el pie")


main()
