# -*- coding: utf-8 -*-
"""Marca, metadata e indexacion. Nombre y dominio viven en las dos
constantes de abajo: se cambian, se corre el script, y las tres paginas
mas el sitemap quedan al dia."""
import io, os, sys, urllib.parse

AQUI = u"C:/Users/Luca/Desktop/snowflake path/"

# Un solo lugar donde vive el dominio. Si cambia, se cambia acá y se corre de nuevo.
# El dominio va en las cinco etiquetas de cada pagina, en el sitemap
# y en robots.txt. Se puede cambiar sin tocar este archivo:
#
#   DC_SITIO=https://datachinchilla.pages.dev python build-brand.py
#
# Hace falta mientras el sitio no este en su dominio final: si las
# etiquetas apuntan a un dominio y el sitio vive en otro, Google no lo
# indexa y las tarjetas de WhatsApp y LinkedIn muestran una pagina que
# no existe.
SITIO = os.environ.get("DC_SITIO", u"https://datachinchilla.com").rstrip("/")
MARCA = u"DataChinchilla"
LEMA  = u"No planificar es planificar el fracaso"

FAVICON = u"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#0B1E2E"/><g transform="translate(12 12.2) scale(.88) translate(-12 -12.2)"><path fill="#2A8DBB" d="M 6.47 17.58 Q 6.26 19.36 5.23 17.77 Q 4.28 19.19 4.10 17.39 Q 2.68 18.16 3.32 16.56 Q 1.79 16.60 3.03 15.53 Q 1.74 14.90 3.24 14.54 Q 2.44 13.45 3.85 13.80 C 4.4 10.6 7.6 10.0 9.4 11.8 C 10.6 14.2 10.4 17.2 9.6 19.4 Z"/><ellipse fill="#38BDF8" cx="10.4" cy="5.3" rx="2.8" ry="3.4" transform="rotate(-21 10.4 5.3)"/><ellipse fill="#38BDF8" cx="18.0" cy="5.3" rx="2.8" ry="3.4" transform="rotate(21 18.0 5.3)"/><ellipse fill="#BAE6FD" cx="10.6" cy="5.7" rx="1.4" ry="1.8" transform="rotate(-21 10.6 5.7)"/><ellipse fill="#BAE6FD" cx="17.8" cy="5.7" rx="1.4" ry="1.8" transform="rotate(21 17.8 5.7)"/><ellipse fill="#38BDF8" cx="14.2" cy="17.2" rx="5.8" ry="5.2"/><circle fill="#38BDF8" cx="14.2" cy="11.3" r="5.4"/><ellipse fill="#0B1E2E" cx="12.3" cy="10.8" rx=".85" ry="1.05"/><ellipse fill="#0B1E2E" cx="16.3" cy="10.8" rx=".85" ry="1.05"/><circle fill="#38BDF8" cx="12.6" cy="10.4" r=".3"/><circle fill="#38BDF8" cx="16.6" cy="10.4" r=".3"/><path fill="#0B1E2E" d="M13.6 12.5h1.4c.26 0 .41.29.25.5l-.7.92a.31.31 0 0 1-.5 0l-.7-.92a.31.31 0 0 1 .25-.5Z"/></g></svg>"""
FAVICON_URI = u"data:image/svg+xml," + urllib.parse.quote(FAVICON, safe="")

PAGINAS = {
    "index.html": {
        "titulo": MARCA + u" · el camino completo para trabajar en tech",
        "desc": u"Diez rutas de estudio gratuitas y ordenadas: Snowflake, dbt, Big Data, machine learning, CS50 y más. Todo el material bueno de internet, con el orden que conviene.",
        "color": u"#0C0818",
        "ogtitulo": u"El camino completo para trabajar en tech",
    },
    "snowpro.html": {
        "titulo": u"SnowPro Core paso a paso · " + MARCA,
        "desc": u"Ruta gratuita para aprobar la certificación SnowPro Core (COF-C03): dieciséis hitos en orden, simulacro de 263 preguntas con corrección y control por tema antes de avanzar.",
        "color": u"#04101B",
        "ogtitulo": u"SnowPro Core, ordenado de principio a fin",
    },
    "data-engineer.html": {
        "titulo": u"Ruta de Data Engineer · " + MARCA,
        "desc": u"El camino completo para trabajar de data engineer: seis niveles en orden, del SQL de todos los días al proyecto corriendo en la nube. Material gratuito de Snowflake, CS50, freeCodeCamp y DataExpert.",
        "color": u"#0C0818",
        "ogtitulo": u"El camino completo para trabajar de data engineer",
    },
    "cv.html": {
        "titulo": u"Tu ruta desde tu CV · " + MARCA,
        "desc": u"Pega tu CV y elige el puesto al que apuntas: te queda la lista corta de lo que te falta, sin el catálogo entero. El CV no se sube a ningún lado.",
        "color": u"#2C1D05",
        "ogtitulo": u"La ruta que te falta, sacada de tu CV",
    },
    "mi-ruta.html": {
        "titulo": u"Tu ruta · " + MARCA,
        "desc": u"La ruta que sale de tu CV: los tramos son lo que te falta para el puesto que eligiós, y los cursos, los que lo cubren.",
        "color": u"#241640",
        "ogtitulo": u"Tu ruta, armada con lo que te falta",
    },
    "practica.html": {
        "titulo": u"La práctica · " + MARCA,
        "desc": u"Los 75 de Blind y las consultas de entrevistas, con tu avance. El enunciado se lee en LeetCode o StrataScratch; acá queda por dónde vas.",
        "color": u"#2C0A14",
        "ogtitulo": u"Practicar sin perder la cuenta",
    },
    "semana.html": {
        "titulo": u"Tu semana · " + MARCA,
        "desc": u"Dinos cuánto tiempo tienes y a qué apuntas, y te queda la semana escrita: qué día, cuánto rato y qué exactamente.",
        "color": u"#04120E",
        "ogtitulo": u"Tu semana de estudio, ya repartida",
    },
    "armar.html": {
        "titulo": u"Arma tu ruta a medida · " + MARCA,
        "desc": u"Elige los niveles que te sirven de cualquier ruta del sitio, ponlos en el orden que quieras y te queda tu propio camino, con su mapa, su avance y un link para compartirlo. Todo material gratuito.",
        "color": u"#08120F",
        "ogtitulo": u"Arma tu propia ruta con las piezas que ya están",
    },
    "cs50.html": {
        "titulo": u"Los once cursos de CS50, ordenados · " + MARCA,
        "desc": u"El catálogo abierto de CS50 de Harvard en un mapa: de Scratch a inteligencia artificial, con qué enseña cada curso, cuánto lleva y para quién es. Todo gratis.",
        "color": u"#150809",
        "ogtitulo": u"Los once cursos abiertos de CS50, en orden",
    },
    "deep-learning.html": {
        "titulo": u"Deep learning y PyTorch, gratis y en orden · " + MARCA,
        "desc": u"Veintiséis pasos gratuitos de CognitiveClass en cinco credenciales: deep learning, PyTorch de cero a redes convolucionales, y visión por computadora.",
        "color": u"#1A1206",
        "ogtitulo": u"Deep learning y PyTorch, en orden",
    },
    "llm-agentes.html": {
        "titulo": u"LLMs y agentes, gratis y en orden · " + MARCA,
        "desc": u"Veintiocho pasos gratuitos de CognitiveClass en cuatro credenciales: prompt engineering, RAG sobre tus datos y agentes con LangGraph, CrewAI y AutoGen.",
        "color": u"#04141C",
        "ogtitulo": u"LLMs y agentes, en orden",
    },
    "ml-aplicado.html": {
        "titulo": u"Machine learning aplicado, gratis y en orden · " + MARCA,
        "desc": u"Treinta y un proyectos guiados de CognitiveClass en seis credenciales: agrupamiento, recomendadores, NLP, AI embebida, refuerzo y modelos explicables.",
        "color": u"#170610",
        "ogtitulo": u"Machine learning aplicado, en orden",
    },
    "sql-python.html": {
        "titulo": u"SQL y Python para entrevistas · " + MARCA,
        "desc": u"Los dos learning paths gratuitos de StrataScratch: doce módulos de SQL y Python pensados para entrevistas de datos, con más de trescientos ejercicios.",
        "color": u"#050C1C",
        "ogtitulo": u"SQL y Python para entrevistas",
    },
    "ai-fundamentos.html": {
        "titulo": u"AI: fundamentos, gratis y en orden · " + MARCA,
        "desc": u"Nueve cursos gratuitos de CognitiveClass en tres credenciales: qué es la AI, cómo se entrena un modelo y machine learning con Python.",
        "color": u"#120726",
        "ogtitulo": u"AI: fundamentos, en orden",
    },
    "claude.html": {
        "titulo": u"Trabajar con Claude, gratis y en orden · " + MARCA,
        "desc": u"Dieciséis cursos gratuitos de Anthropic con insignia: usar Claude, construir con la API, conectar tus sistemas con MCP y llevarlo a producción.",
        "color": u"#1A0B05",
        "ogtitulo": u"Trabajar con Claude, en orden",
    },
    "recursos.html": {
        "titulo": u"Recursos gratis que conviene tener a mano · " + MARCA,
        "desc": u"Material gratuito que no entra en ninguna ruta porque no se recorre: se consulta. Empezando por Laws of UX, en español.",
        "color": u"#0C0818",
        "ogtitulo": u"Recursos gratis",
    },
    "preguntas.html": {
        "titulo": u"Preguntas frecuentes · " + MARCA,
        "desc": u"Si cuesta algo, quién dicta los cursos, qué pasa con tu CV y para qué hace falta una cuenta. Es gratis y no hay versión de pago.",
        "color": u"#0C0818",
        "ogtitulo": u"Preguntas frecuentes",
    },
    "airflow.html": {
        "titulo": u"Airflow gratis, en orden · " + MARCA,
        "desc": u"Orquestación con Apache Airflow sin pagar nada: los caminos de Astronomer Academy y los cinco tutoriales oficiales de Apache, en orden.",
        "color": u"#04171A",
        "ogtitulo": u"Airflow, en orden",
    },
    "fullstack.html": {
        "titulo": u"Full Stack Open, gratis y en orden · " + MARCA,
        "desc": u"Las quince partes del curso gratuito de la Universidad de Helsinki: React, Node, pruebas, TypeScript, contenedores y CI/CD, con certificado y sin examen.",
        "color": u"#08121C",
        "ogtitulo": u"Full Stack Open, en orden",
    },
    "web3.html": {
        "titulo": u"Web3 y blockchain, gratis y en orden · " + MARCA,
        "desc": u"Los seis cursos gratuitos de Alchemy University en orden: de qué es una blockchain a contratos inteligentes y cuentas modulares.",
        "color": u"#0C1505",
        "ogtitulo": u"Web3 y blockchain, en orden",
    },
    "subir-nivel.html": {
        "titulo": u"Subir de nivel como data engineer · " + MARCA,
        "desc": u"Para quien ya trabaja con datos: diecisiete cursos gratuitos que cierran los huecos que el mercado pide, sin volver a empezar por SQL.",
        "color": u"#04181F",
        "ogtitulo": u"Subir de nivel como data engineer",
    },
    "bigdata.html": {
        "titulo": u"Big Data con Hadoop y Spark, gratis y en orden · " + MARCA,
        "desc": u"Diecisiete cursos gratuitos de CognitiveClass en orden: del vocabulario de Big Data a Spark y Scala, hasta operar el clúster, con badge de Credly en cada tramo.",
        "color": u"#061513",
        "ogtitulo": u"Big Data con Hadoop y Spark, en orden",
    },
    "data-science.html": {
        "titulo": u"Data Science con IBM, gratis y en orden · " + MARCA,
        "desc": u"Doce cursos gratuitos de Data Science de CognitiveClass, en orden: qué es el oficio, y después Python, R y los primeros modelos, con la credencial Data Science Essentials.",
        "color": u"#0B0A1A",
        "ogtitulo": u"Empezar en Data Science, en orden",
    },
    "arquitectura.html": {
        "titulo": u"Contenedores y sistemas distribuidos, gratis y en orden · " + MARCA,
        "desc": u"Diez cursos gratuitos de CognitiveClass: contenedores, Kubernetes e Istio, y los seis de arquitectura reactiva, del manifiesto a CQRS.",
        "color": u"#170610",
        "ogtitulo": u"Contenedores y sistemas distribuidos, en orden",
    },
    "dbt.html": {
        "titulo": u"Aprender dbt gratis, en orden · " + MARCA,
        "desc": u"Veintitrés pasos gratuitos para aprender dbt, en el orden que conviene: del primer modelo a un proyecto con tests, documentación y control de versiones.",
        "color": u"#0F0A06",
        "ogtitulo": u"Aprender dbt gratis, en orden",
    },
}

def sin_html(archivo):
    """La direccion de verdad de una pagina.

       Cloudflare Pages redirige /cv.html a /cv y no deja apagarlo, asi
       que la canonica y el sitemap tienen que decir /cv. Si dicen otra
       cosa, cada URL que le damos a Google le devuelve un redirect.
    """
    if archivo == "index.html":
        return u""                      # la portada es la raiz
    return archivo[:-5] if archivo.endswith(".html") else archivo


def cabeza(archivo, d):
    url = SITIO + u"/" + sin_html(archivo)
    return u"""<title>%(TIT)s</title>
<meta name="description" content="%(DESC)s">
<link rel="canonical" href="%(URL)s">
<meta name="theme-color" content="%(COLOR)s">
<link rel="icon" href="%(ICON)s">
<meta name="author" content="Luca Lamorte">
<meta name="robots" content="index, follow">

<!-- Los neutros, los radios y el ritmo, compartidos por todas las páginas.
     Cada una define encima solo su acento. Va acá dentro y no a mano en el
     HTML: esta plantilla reescribe toda la cabecera en cada corrida. -->
<link rel="stylesheet" href="tema.css">
<!-- Las poses de la chinchilla y las animaciones del sitio. Va acá por
     lo mismo: si lo escribe otro script en el HTML, la próxima corrida
     de esta plantilla se lo lleva. Ya pasó con tema.css y con este. -->
<link rel="stylesheet" href="chinchilla.css">

<!-- Cómo se ve al compartirla. El dominio vive en build-catalog.py y en
     estas etiquetas: si cambia, es un reemplazo en los tres archivos. -->
<meta property="og:site_name" content="%(MARCA)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_LA">
<meta property="og:title" content="%(OGTIT)s">
<meta property="og:description" content="%(DESC)s">
<meta property="og:url" content="%(URL)s">
<meta property="og:image" content="%(SITIO)s/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(OGTIT)s">
<meta name="twitter:description" content="%(DESC)s">
<meta name="twitter:image" content="%(SITIO)s/og.png">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "%(MARCA)s",
  "url": "%(SITIO)s/",
  "description": "%(LEMA)s. Rutas de estudio gratuitas y ordenadas para trabajar con datos.",
  "inLanguage": "es",
  "author": { "@type": "Person", "name": "Luca Lamorte", "url": "https://www.linkedin.com/in/lclamorte/" }
}
</script>""" % {"TIT": d["titulo"], "DESC": d["desc"], "URL": url, "COLOR": d["color"],
                "ICON": FAVICON_URI, "MARCA": MARCA, "OGTIT": d["ogtitulo"],
                "SITIO": SITIO, "LEMA": LEMA}

for archivo, d in PAGINAS.items():
    p = AQUI + archivo
    s = io.open(p, encoding="utf-8").read()
    i = s.index(u"<title>")
    j = s.index(u"\n", s.index(u"</head>") - 400)
    # se reemplaza desde <title> hasta la última meta que haya antes de <style>
    # la etiqueta de estilo va sola en su línea: buscarla suelta hacía
    # que una mención dentro de un comentario cortara en el lugar erróneo
    fin = s.index(u"\n<style>\n") + 1
    s = s[:i] + cabeza(archivo, d) + u"\n" + s[fin:]
    io.open(p, "w", encoding="utf-8").write(s)
    print("%-22s cabecera lista" % archivo)

# ---------------------------------------------------------------- robots y sitemap
io.open(AQUI + "robots.txt", "w", encoding="utf-8").write(
u"""User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITIO)

urls = u"".join([u"""  <url>
    <loc>%s/%s</loc>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>
""" % (SITIO, sin_html(a),
       "1.0" if a == "data-engineer.html" else ("0.9" if a == "armar.html" else "0.8"))
   for a in PAGINAS if a != "index.html"])

io.open(AQUI + "sitemap.xml", "w", encoding="utf-8").write(
u"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>%s/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
%s</urlset>
""" % (SITIO, urls))

print("robots.txt y sitemap.xml escritos")

# La cabecera se reescribe entera, asi que el ?v= de tema.css se
# pierde en cada corrida y el navegador vuelve a servir el CSS viejo.
# Sellar aca cierra ese agujero sin que haya que acordarse.
import subprocess, os
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "sellar.py")])
