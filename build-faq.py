# -*- coding: utf-8 -*-
"""Las preguntas frecuentes, y la plata contestada de frente.

   El pedido: que quede claro que no se paga, que no es freemium, que
   no hay forma de que te cobren. Y sin decirlo explicitamente, porque
   un cartel que grita GRATIS es exactamente lo que hacen las que
   despues cobran.

   La forma de decirlo sin gritarlo es contestar la pregunta que la
   persona tiene de verdad, tres veces y desde angulos distintos:
   cuanto sale, si va a salir algo mas adelante, y de que vive esto.
   Una respuesta concreta convence mas que un adjetivo.

   Las otras preguntas no son relleno: son las que alguien se hace
   antes de dejar su CV o crear una cuenta. Un sitio que no las
   contesta se siente amateur aunque funcione bien.

   Va con datos estructurados de tipo FAQPage. Sirve para dos cosas:
   que los buscadores muestren las respuestas, y que los modelos de
   lenguaje que hoy recomiendan sitios tengan de donde sacar que esto
   es gratis. Es la parte de GEO que se pidio hace unos dias.

   El JSON-LD va en el cuerpo y no en la cabeza a proposito:
   build-brand.py reescribe la cabeza entera y se lo llevaria puesto.
   Ya paso con tema.css.

   Uso: python build-faq.py
"""
import io, os, json, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")

# (pregunta, respuesta en HTML, respuesta en texto plano para el JSON-LD)
FAQ = [
 (u"¿Cuánto cuesta?",
  u"Nada, y no hay una versión de pago escondida. No vas a encontrar un "
  u"precio, un plan, un botón de suscripción ni un límite que se destrabe "
  u"pagando, porque no existen. Tampoco hay tarjeta que cargar en ningún "
  u"momento.",
  u"Nada. No hay version de pago, ni plan, ni suscripcion, ni limites que "
  u"se destraben pagando. Nunca se pide una tarjeta."),

 (u"¿Y más adelante me van a cobrar?",
  u"No. Los cursos son de universidades y de las empresas que hacen las "
  u"herramientas, y son gratis en su propio sitio: acá no se puede cobrar "
  u"por algo que es de otro y que además está abierto. Lo que este sitio "
  u"agrega es el orden y tu avance, y eso es lo que se comparte.",
  u"No. Los cursos son de universidades y empresas, y son gratis en su "
  u"propio sitio. Lo que agrega DataChinchilla es el orden y el avance."),

 (u"¿De qué vive esto, entonces?",
  u"De nada. Es un proyecto de una persona, hecho a un costado del "
  u"trabajo. Hay un enlace para invitar un café si a alguien le sirvió, "
  u"que es opcional y no destraba absolutamente nada: quien no lo toca ve "
  u"exactamente el mismo sitio.",
  u"De nada. Es un proyecto personal. Hay un enlace opcional para invitar "
  u"un cafe que no destraba ninguna funcion."),

 (u"¿Quién dicta los cursos?",
  u"Quien los hizo. Harvard, la Universidad de Helsinki, dbt Labs, "
  u"Anthropic, AWS, CognitiveClass y varios más. Acá no se dicta ninguno: "
  u"se eligen, se ponen en orden, se dice cuánto lleva cada uno y qué te "
  u"deja, y se te lleva la cuenta de por dónde vas.",
  u"Quien los hizo: Harvard, la Universidad de Helsinki, dbt Labs, "
  u"Anthropic, AWS y otros. DataChinchilla no dicta cursos: los ordena."),

 (u"¿Qué pasa con mi CV?",
  u"Se lee en tu navegador y no se sube a ningún lado. El texto se cruza "
  u"contra una lista de temas que está en el mismo sitio, y de ahí sale la "
  u"ruta. Si cierras la pestaña sin guardar, no queda nada.",
  u"Se lee en el navegador y no se sube a ningun servidor. Si cierras la "
  u"pestana sin guardar, no queda nada."),

 (u"¿Para qué necesito una cuenta?",
  u"Sólo para que tu avance te siga a otra computadora. Podés recorrer "
  u"todo el sitio, leer las rutas, ver los problemas y sacar tu ruta del CV "
  u"sin crear nada. La cuenta hace falta recién cuando querés que lo que "
  u"marcaste quede guardado.",
  u"Solo para guardar tu avance y que te siga en otro dispositivo. Se "
  u"puede recorrer todo el sitio sin crear cuenta."),

 (u"¿Los certificados los emiten ustedes?",
  u"No. El que vale lo emite quien dicta el curso, y se baja de su sitio. "
  u"Acá hay una constancia de que recorriste una ruta, que dice en la misma "
  u"hoja que no es un certificado oficial ni acredita conocimiento.",
  u"No. El certificado que vale lo emite quien dicta el curso. "
  u"DataChinchilla emite una constancia de recorrido que aclara que no es "
  u"oficial."),

 (u"¿Y si un curso deja de ser gratis o el link se cae?",
  u"Se saca o se reemplaza. Ya pasó: cinco problemas de práctica pasaron a "
  u"ser de pago y se cambiaron por otros gratis que entrenan lo mismo. Si "
  u"encontrás uno roto o con candado, escribime y lo miro.",
  u"Se saca o se reemplaza por algo gratis equivalente. Se puede avisar por "
  u"correo si se encuentra un link roto o de pago."),
]


def bloque_html():
    filas = []
    for i, (q, r, _) in enumerate(FAQ):
        filas.append(
            u'      <details class="faq-i"%s>\n'
            u'        <summary>%s</summary>\n'
            u'        <p>%s</p>\n'
            u'      </details>' % (u" open" if i == 0 else u"", q, r))
    datos = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": plano}}
            for q, _, plano in FAQ
        ],
    }
    return (
        u'\n<section class="section" id="faq">\n'
        u'  <div class="wrap">\n'
        u'    <div class="section-head">\n'
        u'      <span class="eyebrow">Lo que suelen preguntar</span>\n'
        u'      <h2>Antes de que lo preguntes</h2>\n'
        u'      <p>La primera duda de casi todos es la misma, así que va primera.</p>\n'
        u'    </div>\n'
        u'    <div class="faq">\n' + u"\n".join(filas) + u'\n    </div>\n'
        u'  </div>\n'
        u'  <script type="application/ld+json">' +
        json.dumps(datos, ensure_ascii=False) +
        u'</script>\n'
        u'</section>\n')


CSS = u'''
/* --- Las preguntas frecuentes -------------------------------------
   Con <details> del navegador y no con JavaScript: si el script
   falla, las respuestas siguen ahi y se pueden abrir. Para algo que
   contesta "esto cuesta algo?", que la respuesta dependa de que corra
   un script seria justo al reves de lo que hace falta. */
.faq{ display:flex; flex-direction:column; gap:9px; }
.faq-i{
  border:1px solid var(--divider); border-radius:var(--r-lg);
  background:var(--surface); overflow:hidden;
}
.faq-i > summary{
  cursor:pointer; padding:15px 18px; font-weight:800; font-size:15px;
  list-style:none; display:flex; align-items:center; gap:10px;
}
.faq-i > summary::-webkit-details-marker{ display:none; }
.faq-i > summary::after{
  content:""; margin-left:auto; flex:none;
  width:9px; height:9px; border-right:2.4px solid var(--text-3);
  border-bottom:2.4px solid var(--text-3); transform:rotate(45deg);
  transition:transform var(--dur) ease;
}
.faq-i[open] > summary::after{ transform:rotate(-135deg); }
.faq-i > summary:hover{ color:var(--accent-strong); }
.faq-i > p{
  margin:0; padding:0 18px 16px; font-size:14px; color:var(--text-2);
  line-height:1.65; max-width:70ch;
}
'''


def main():
    t = io.open(P, encoding="utf-8").read()
    if 'id="faq"' in t:
        print(u"  ya estaba puesto")
        sys.exit(1)
    if "<footer" not in t:
        print(u"  ABORTA: no encuentro el pie")
        sys.exit(1)

    i = t.index("<footer")
    ini = t.rfind("\n", 0, i)
    t = t[:ini] + bloque_html() + t[ini:]

    if "\n</style>" not in t:
        print(u"  ABORTA: no encuentro donde poner el estilo")
        sys.exit(1)
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print(u"index.html: %d preguntas, con datos estructurados FAQPage" % len(FAQ))


main()
