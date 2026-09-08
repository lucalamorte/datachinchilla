# -*- coding: utf-8 -*-
u"""La ruta de credenciales de nube.

   Es la unica ruta del sitio armada alrededor de un examen. La razon
   es que en la nube la credencial vale de verdad: hay puestos donde
   te la piden por escrito, y el material para estudiarla es gratis
   aunque el examen no lo sea.

   De donde sale cada cosa:

   - Microsoft Learn es el que mas pesa, y no por casualidad: es el
     unico de los tres grandes que publica su formacion entera gratis,
     sin creditos, sin suscripcion, sin cuenta para leerla y en
     espanol. AZ-900 y DP-900 se estudian enteros ahi.
   - AWS publica Cloud Practitioner Essentials gratis, en su sitio de
     formacion digital y en Skill Builder. Skill Builder tiene ademas
     una parte paga; los dos pasos de aca son de la gratis.
   - Google pide crear una cuenta gratuita para ver su ruta de Cloud
     Digital Leader, y se dice.

   Los examenes cuestan, los tres. Va en el pie del hero con los
   precios de lista, porque un sitio que promete que todo es gratis
   tiene que ser el primero en decir donde empieza a costar. Y va
   dicho lo otro: aprender esto no necesita el examen.

   Ojo con un link: cloudskillsboost.google redirige a skills.google.
   Es el mismo producto renombrado, y por eso aca ya va el nuevo. El
   viejo sigue en el catalogo de la portada y hay que mudarlo.

   Uso: python build-nube.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = "airflow.html"
SALE = "nube.html"

ACTS = u'''var ACTS = [
  { n: 1, title: "Qué es la nube", desc: "Los conceptos, que son los mismos en los tres" },
  { n: 2, title: "AWS", desc: "El que más se pide en los avisos" },
  { n: 3, title: "Datos en la nube", desc: "La credencial que cruza con el resto del sitio" },
  { n: 4, title: "Google", desc: "El tercero, y el que menos material abierto tiene" }
];'''

C = [
 # ------------------------------------------------ 1. que es la nube
 ("n01", 1, "5 h", "cloud", True, "AZ-900",
  u"Conceptos de nube",
  u"Qué es la nube y qué no: modelos de servicio, modelos de despliegue, en qué cambia pagar por uso. Es la mitad del examen AZ-900 y es lo único de todo esto que no depende del proveedor.",
  u"Terminas esta parte cuando explicas la diferencia entre IaaS, PaaS y SaaS con un ejemplo tuyo.",
  [u"El vocabulario que los tres proveedores comparten",
   u"Por qué la nube cambia el costo de equivocarse, que es de lo que se trata",
   u"Gratis, en español y sin cuenta para leerlo"],
  "https://learn.microsoft.com/es-es/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/"),

 ("n02", 1, "6 h", "flow", False, "AZ-900",
  u"Arquitectura y servicios",
  u"Las piezas concretas: regiones, zonas, cómputo, red y almacenamiento. Los nombres cambian entre proveedores, las piezas no.",
  u"Terminas esta parte cuando dibujas dónde vive cada cosa de una aplicación en la nube.",
  [u"Regiones y zonas: por qué importa dónde está tu servidor",
   u"Cómputo, red y almacenamiento, que es de lo que está hecho todo",
   u"Aprender los conceptos en uno te sirve en los tres"],
  "https://learn.microsoft.com/es-es/training/paths/azure-fundamentals-describe-azure-architecture-services/"),

 ("n03", 1, "4 h", "shield", False, "AZ-900",
  u"Administración y gobernanza",
  u"Lo que nadie estudia y todos necesitan: cuánto va a costar, quién puede tocar qué, y cómo no llevarte una sorpresa a fin de mes.",
  u"Terminas esta parte cuando puedes estimar el costo de algo antes de encenderlo.",
  [u"Calcular el costo antes, no después de la factura",
   u"Permisos: quién puede hacer qué, que es la mitad de la seguridad",
   u"Con esto cierras el temario completo de AZ-900"],
  "https://learn.microsoft.com/es-es/training/paths/describe-azure-management-governance/"),

 # ------------------------------------------------ 2. aws
 ("n04", 2, "6 h", "cloud", True, "AWS CCP",
  u"AWS Cloud Practitioner Essentials",
  u"El curso oficial y gratuito de AWS para su credencial de entrada. Los mismos conceptos del tramo anterior, con los nombres de AWS, que son los que aparecen en los avisos de trabajo.",
  u"Terminas esta parte cuando lees un aviso que pide EC2, S3 y VPC y sabes de qué habla.",
  [u"Los nombres de AWS, que es lo que se pide por nombre",
   u"El modelo de responsabilidad compartida, que entra en el examen y en la vida",
   u"Es el curso oficial: no hay intermediario"],
  "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/"),

 ("n05", 2, "5 h", "school", False, "AWS CCP",
  u"El mismo curso en Skill Builder",
  u"La versión con seguimiento de avance y prácticas. Skill Builder tiene una parte paga; ésta no lo es. Pide crear una cuenta gratuita.",
  u"Terminas esta parte cuando das el examen de práctica y te alcanza.",
  [u"Ejercicios y examen de práctica, que es lo que falta para presentarse",
   u"Tu avance queda guardado del lado de AWS",
   u"Cuenta gratuita: lo pago de Skill Builder es otra cosa"],
  "https://explore.skillbuilder.aws/learn/courses/134/aws-cloud-practitioner-essentials"),

 # ------------------------------------------------ 3. datos en la nube
 ("n06", 3, "8 h", "data", True, "DP-900",
  u"Fundamentos de datos en Azure",
  u"DP-900: datos relacionales y no relacionales, analítica, y qué servicio se usa para qué. Es la credencial que más cruza con el resto de este sitio.",
  u"Terminas esta parte cuando eliges entre una base relacional y una de documentos con un argumento.",
  [u"Relacional contra no relacional, decidido y no adivinado",
   u"Qué servicio hace qué, que es la pregunta de todos los días",
   u"Se cruza con SQL y con modelado, que ya están acá"],
  "https://learn.microsoft.com/es-es/training/courses/dp-900t00"),

 ("n07", 3, "4 h", "chart", False, "",
  u"Microsoft Fabric",
  u"La plataforma con la que Microsoft juntó todo lo de datos en un solo lugar. Está apareciendo en los avisos y casi no hay material ordenado en español.",
  u"Terminas esta parte cuando sabes qué reemplaza Fabric y qué no.",
  [u"Qué es y qué junta, sin el folleto",
   u"Dónde encaja si ya sabes SQL y modelado",
   u"Es reciente: saberlo distingue"],
  "https://learn.microsoft.com/es-es/training/paths/get-started-fabric/"),

 ("n08", 3, "5 h", "flow", False, "",
  u"Empezar en ingeniería de datos",
  u"El camino de Microsoft para el rol, con los servicios de datos en la nube. Es el puente entre esta ruta y la de Data Engineer.",
  u"Terminas esta parte cuando entiendes cómo se arma un pipeline con servicios administrados en vez de con tu propio servidor.",
  [u"Pipelines sin mantener servidores",
   u"Cómo se ve el trabajo de datos del lado de la nube",
   u"Conecta con la ruta de Data Engineer que ya está acá"],
  "https://learn.microsoft.com/es-es/training/paths/get-started-data-engineering/"),

 # ------------------------------------------------ 4. google
 ("n09", 4, "8 h", "school", True, "Cloud Digital Leader",
  u"Cloud Digital Leader, de Google",
  u"La ruta oficial de Google para su credencial de entrada. Seis actividades sobre nube, datos e IA. Pide crear una cuenta gratuita para verla.",
  u"Terminas esta parte cuando puedes comparar los tres proveedores sin repetir lo que dice cada folleto.",
  [u"El tercero de los tres grandes, con sus nombres",
   u"Nube, datos e IA juntos, que es como Google la vende",
   u"Cuenta gratuita: los laboratorios con créditos son aparte y no hacen falta acá"],
  "https://skills.google/paths/9"),
]

TEXTOS = [
 (u"""  /* Airflow. Medido contra los fondos de verdad: 5.17:1 sobre
     --bg-2 en claro, 8.74:1 sobre --surface en oscuro. */
  --accent:        #0E6B78;
  --accent-strong: #0A545F;
  --accent-soft:   #E4F2F4;
  --accent-line:   #BBDDE2;""",
  u"""  /* Credenciales de nube. Azul acero: ninguna de las otras
     dieciocho lo usa, y no se confunde con el violeta del sitio. */
  --accent:        #1E5F9E;
  --accent-strong: #17497B;
  --accent-soft:   #E7F0F9;
  --accent-line:   #C0D8EE;""", 1),

 (u"""  --accent:        #5EC7D6;
  --accent-strong: #86D6E2;
  --accent-soft:   #0C2E33;
  --accent-line:   #17505A;""",
  u"""  --accent:        #7DB3E8;
  --accent-strong: #A5CBF1;
  --accent-soft:   #0E2438;
  --accent-line:   #1B4670;""", 1),

 (u'<span class="brand-sub">/ Airflow</span>',
  u'<span class="brand-sub">/ Credenciales de nube</span>', 1),

 (u'<h1>Orquestar con <span class="grad">Airflow</span></h1>',
  u'<h1>Certificarte en la <span class="grad">nube</span></h1>', 1),

 (u'<span class="dest">academy.astronomer.io</span>',
  u'<span class="dest">learn.microsoft.com</span>', 1),

 (u"los ocho pasos de Airflow", u"los nueve pasos de la nube", 1),

 (u"Se desbloquea cuando cierres los ocho pasos del mapa. La certificación "
  u"oficial de Astronomer es aparte y cuesta 150 dólares: no hace falta para "
  u"aprender esto.",
  u"Se desbloquea cuando cierres los nueve pasos del mapa. Los exámenes de "
  u"verdad -AZ-900, DP-900, AWS Cloud Practitioner y Cloud Digital Leader- son "
  u"aparte y se pagan a cada proveedor: lo que está acá es todo el "
  u"material con el que se estudian.", 1),

 (u"<h2>Tres tramos, ocho pasos</h2>", u"<h2>Cuatro tramos, nueve pasos</h2>", 1),

 (u'id="startDest">Airflow 101<', u'id="startDest">los conceptos de nube<', 1),

 (u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Los de Astronomer dejan constancia en su academia; los de Apache "
  u"son documentación y no dejan nada más que saberlo.",
  u"Toca cualquiera para ver qué te llevas y por qué está acá. "
  u"Los que llevan una sigla al lado son el temario de ese examen: el material "
  u"es gratis, el examen se paga aparte.", 1),
]

PIE = (u'<p class="hero-foot">Ésta es la única ruta del sitio armada alrededor de un examen, '
       u'porque en la nube la credencial se pide por escrito. El material para estudiarla es '
       u'gratis: Microsoft Learn publica AZ-900 y DP-900 enteros, en español, sin cuenta y sin '
       u'créditos, y AWS publica su curso de entrada igual. Los exámenes sí cuestan y los cobra '
       u'cada proveedor: rondan los 100 dólares para AZ-900 y DP-900, y los 100 para el de AWS. '
       u'Aprender todo esto no necesita ninguno.</p>')

LEAD = (u'<p class="hero-lead">La nube es donde corre casi todo, y es de las pocas cosas de este '
        u'oficio donde un papel te abre una puerta. Acá va de qué es la nube a tener el temario '
        u'completo de cuatro credenciales de entrada -Azure, datos en Azure, AWS y Google-, con '
        u'el material oficial de cada uno y sin pagar nada por estudiarlo.</p>')


def nodo(c):
    cid, act, time, i, boss, cert, titulo, resumen, meta, wins, url = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s"%s,\n'
            u'    cert: "%s",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "%s"\n'
            u'  }' % (cid, act, time, i, u", boss: true" if boss else u"",
                      cert, titulo, resumen, meta, w, url))


def main():
    t = io.open(os.path.join(D, BASE), encoding="utf-8").read()

    nodos = u"var NODES = [\n" + u",\n\n".join(nodo(c) for c in C) + u"\n];"
    t = re.sub(r"var ACTS = \[.*?\n\];", lambda m: ACTS, t, count=1, flags=re.S)
    t = re.sub(r"var NODES = \[.*?\n\];", lambda m: nodos, t, count=1, flags=re.S)

    for viejo, nuevo, veces in TEXTOS:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA: %r aparece %d veces, esperaba %d" % (viejo[:52], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)

    v = re.search(r'<p class="hero-foot">.*?</p>', t, re.S)
    t = t[:v.start()] + PIE + t[v.end():]
    v2 = re.search(r'<p class="hero-lead">.*?</p>', t, re.S)
    t = t[:v2.start()] + LEAD + t[v2.end():]

    t = t.replace(u'var MI_RUTA = "airflow"', u'var MI_RUTA = "nube"')
    t = t.replace(u'var MI_CLAVE = "airflow"', u'var MI_CLAVE = "nube"')

    io.open(os.path.join(D, SALE), "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d pasos en 4 tramos" % (SALE, len(C)))


main()
