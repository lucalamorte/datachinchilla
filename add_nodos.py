# -*- coding: utf-8 -*-
"""Suma nodos nuevos a las rutas que ya existen.

   Contenido que entra en esta corrida:

   - Los tutoriales oficiales de Airflow, en "Subir de nivel". No dan
     certificado y no alcanzan para una ruta propia, pero son la
     documentacion del proyecto y cubren cosas que el curso de
     Astronomer no toca. Van antes de Astronomer, sin cert.

   - Las cuatro microcredenciales de AWS, gratis desde abril de 2026.
     Son evaluaciones practicas en una cuenta real, no cursos, asi que
     van al final de su tramo y como boss: se rinden cuando el tramo
     ya se sabe. Repartidas y no en una ruta propia, porque cuatro
     examenes sin material que los prepare son una lista, no un camino.

   Inserta respetando el orden por acto y aborta si el id ya existe.
"""
import io, re, sys

D = u"C:/Users/Luca/Desktop/snowflake path/"


def nodo(d):
    """Un nodo, escrito como los que ya estan en el archivo."""
    s = u'  {\n    id: "%s", act: %d, time: "%s", i: "%s",%s\n' % (
        d["id"], d["act"], d["time"], d["i"],
        u' boss: true,' if d.get("boss") else u"")
    if d.get("cert"):
        s += u'    cert: "%s",\n' % d["cert"]
    s += u'    title: "%s",\n' % d["title"]
    s += u'    summary: "%s",\n' % d["summary"]
    s += u'    goal: "%s",\n' % d["goal"]
    s += u'    wins: [' + u",\n           ".join(
        u'"%s"' % w for w in d["wins"]) + u"],\n"
    s += u'    u: "%s"\n  }' % d["u"]
    return s


def insertar(archivo, nuevos):
    p = D + archivo
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r"var NODES = \[\n(.*?)\n\];", t, re.S)
    if not m:
        print("  ABORTA: sin NODES en %s" % archivo)
        sys.exit(1)

    bloques = re.split(r",\n(?=  \{\n)", m.group(1))

    def acto_de(b):
        a = re.search(r"act:\s*(\d+)", b)
        return int(a.group(1)) if a else 0

    for d in nuevos:
        if re.search(r'id:\s*"%s"' % d["id"], t):
            print("  ABORTA: %s ya tiene el id %s" % (archivo, d["id"]))
            sys.exit(1)

        # Detras del ultimo nodo de su acto, o del ultimo de un acto
        # anterior si el acto todavia no tiene ninguno.
        pos = 0
        for k, b in enumerate(bloques):
            if acto_de(b) <= d["act"]:
                pos = k + 1
        # Si va antes de otro nodo del mismo acto, se dice con "antes".
        if d.get("antes"):
            for k, b in enumerate(bloques):
                if re.search(r'id:\s*"%s"' % d["antes"], b):
                    pos = k
                    break
        bloques.insert(pos, nodo(d))

    t = t[:m.start()] + u"var NODES = [\n" + u",\n".join(bloques) + u"\n];" + t[m.end():]
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s +%d nodos" % (archivo, len(nuevos)))


# ------------------------------------------------------- Subir de nivel
insertar(u"subir-nivel.html", [
 {"id": "x09a", "act": 2, "time": "4 horas", "i": "flow", "antes": "x09",
  "title": u"Los tutoriales oficiales de Airflow",
  "summary": u"La documentación del proyecto, que es de donde sale lo que después repiten los cursos. Cinco tutoriales que se hacen con Airflow corriendo al lado, no mirando.",
  "goal": u"Terminas esto cuando tienes Airflow local y escribiste un pipeline leyendo la doc y no un video.",
  "wins": [u"Airflow 101, tu primer workflow de punta a punta",
           u"TaskFlow API, que es como se escriben los DAGs hoy",
           u"Un pipeline de datos simple, armado por ti",
           u"Object storage, que es por donde pasan los datos ahora",
           u"Human-in-the-loop, para los pasos que aprueba una persona"],
  "u": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html"},

 {"id": "x13a", "act": 4, "time": "1 hora", "i": "cloud", "boss": True,
  "cert": u"Microcredencial oficial de AWS",
  "title": u"AWS Serverless Demonstrated",
  "summary": u"Una evaluación dentro de una cuenta de AWS de verdad: Lambda, API Gateway, Step Functions y DynamoDB. No hay multiple choice, se configura y se arregla igual que en el trabajo.",
  "goal": u"Terminas esto cuando resolviste el escenario y tienes la microcredencial en tu perfil.",
  "wins": [u"Una credencial oficial de AWS, gratis desde abril de 2026",
           u"Se rinde haciendo, no eligiendo la opción correcta",
           u"Lambda, API Gateway, Step Functions y DynamoDB"],
  "u": "https://skillbuilder.aws/learn/XV3B4RGA8Q/aws-serverless-demonstrated/BYD5SH8R5C"},
])


# --------------------------------------------------------- Arquitectura
# Application Networking cierra el tramo de contenedores: es
# exactamente lo que se opera cuando eso ya esta desplegado.
insertar(u"arquitectura.html", [
 {"id": "a03a", "act": 1, "time": "1 hora", "i": "cloud", "boss": True,
  "cert": u"Microcredencial oficial de AWS",
  "title": u"AWS Application Networking Demonstrated",
  "summary": u"Una evaluación dentro de una cuenta de AWS de verdad: entregar la aplicación, optimizar su rendimiento y sostener la arquitectura que la aguanta.",
  "goal": u"Terminas esto cuando resolviste el escenario y tienes la microcredencial en tu perfil.",
  "wins": [u"Una credencial oficial de AWS, gratis desde abril de 2026",
           u"Se rinde configurando y arreglando, no eligiendo opciones",
           u"Entrega, rendimiento y arquitectura de aplicaciones"],
  "u": "https://skillbuilder.aws/learn/EM5GTXEQB6/aws-application-networking-demonstrated/GS9ZN623HY"},
])

# ------------------------------------------------------- LLMs y agentes
# Agentic AI Demonstrated cierra el tramo de agentes con la unica
# credencial oficial que existe sobre esto.
insertar(u"llm-agentes.html", [
 {"id": "l27a", "act": 4, "time": "1 hora", "i": "brain", "boss": True,
  "cert": u"Microcredencial oficial de AWS",
  "title": u"AWS Agentic AI Demonstrated",
  "summary": u"Una evaluación práctica sobre agentes hechos con Amazon Bedrock: hay que arreglarlos, integrarlos y mejorarlos, que es lo que se hace cuando el agente ya existe y falla.",
  "goal": u"Terminas esto cuando arreglaste el agente que te dan y tienes la microcredencial.",
  "wins": [u"Una credencial oficial de AWS, gratis desde abril de 2026",
           u"Depurar un agente ajeno, que es el trabajo real",
           u"Integrar y mejorar agentes sobre Amazon Bedrock"],
  "u": "https://skillbuilder.aws/learn/32Y249P272/aws-agentic-ai-demonstrated/TTAJ5WKYTS"},
])
