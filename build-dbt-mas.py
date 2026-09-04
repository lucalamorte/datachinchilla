# -*- coding: utf-8 -*-
"""Los cursos de dbt Learn que faltaban en la ruta.

   De los cincuenta y tres links de learn.getdbt.com que quedaron
   afuera, la mayoria no entra por buenas razones:

     - treinta y tres son de administrar la plataforma paga: SSO con
       Okta y Entra, SCIM, OAuth por warehouse, "for admins" de cada
       uno. Eso lo hace el equipo de datos una vez, no quien aprende.
     - las versiones "-vs-code" son el mismo curso en otra interfaz.
     - las seis de "consultar el Semantic Layer con X" son el mismo
       tema por herramienta (Excel, Hex, Tableau, Mode, Lightdash), y
       la ruta ya tiene Semantic Layer.
     - introduction-to-sql lo cubre la ruta de SQL y Python.

   Quedan ocho que llenan huecos de verdad: Git (que la ruta no
   tenia y hace falta apenas trabajas con alguien mas), refactorizar
   SQL heredado, seeds y analyses, unit tests -que no son los data
   tests de "Testing a fondo"-, despliegue, exposures, mesh e Iceberg.

   SOBRE LAS HORAS: dbt Learn no publica duraciones y su catalogo es
   una SPA que no devuelve nada al fetch. Las de estos ocho son mias,
   estimadas por el temario de cada uno. Las de los quince que ya
   estaban tampoco son oficiales: el sitio dice 6 horas para
   Fundamentals y dbt habla de unas 5. Son ordenes de magnitud para
   que la semana pueda repartirlos, no promesas.

   Uso: python build-dbt-mas.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
P = "dbt.html"

# (id, acto, tiempo, icono, despues_de, titulo, resumen, meta, wins, slug)
NUEVOS = [
 ("d16", 2, "1 hora", "code", "d06",
  u"Git, lo justo para dbt",
  u"Curso oficial gratuito. Ramas, commits y pull requests, que es como se trabaja en dbt apenas hay alguien más en el proyecto.",
  u"Terminas este paso cuando abres un pull request con un modelo nuevo y alguien te lo revisa.",
  [u"Ramas y pull requests, que es el flujo de trabajo de dbt",
   u"Resolver un conflicto sin romper lo que ya andaba",
   u"Por qué el entorno de desarrollo es tuyo y el de producción no"],
  "git-fundamentals"),

 ("d17", 3, "3 horas", "build", "d07",
  u"Refactorizar SQL heredado",
  u"Curso oficial gratuito con proyecto de práctica. Tomar una consulta larga que ya existe y partirla en modelos que se entienden solos.",
  u"Terminas este paso cuando conviertes una consulta de trescientas líneas en modelos con nombre propio.",
  [u"El método para partir SQL viejo sin cambiar el resultado",
   u"Comparar la salida vieja y la nueva, que es lo que da confianza",
   u"Una consulta y un dataset de práctica para hacerlo vos"],
  "refactoring-sql-for-modularity"),

 ("d18", 3, "1 hora", "data", "d10",
  u"Seeds y analyses",
  u"Curso oficial gratuito. Dos cosas que dbt tiene y casi nadie usa: cargar CSV chicos como tablas versionadas, y guardar consultas de análisis que no son modelos.",
  u"Terminas este paso cuando dejas de tener el CSV de mapeos suelto en el escritorio de alguien.",
  [u"Seeds para las tablas chicas que hoy viven en un Excel",
   u"Analyses para las consultas que no van a producción",
   u"Cuándo algo es un seed y cuándo tiene que ser una tabla de verdad"],
  "analyses-and-seeds"),

 ("d19", 3, "1 h 30 min", "check", "d09",
  u"Unit tests",
  u"Curso oficial gratuito. Distinto de los data tests: acá pruebas la lógica del modelo con datos que inventas, sin esperar a que corra sobre el warehouse.",
  u"Terminas este paso cuando una regla rara del negocio tiene su test y no se rompe en silencio.",
  [u"Probar la lógica con datos de mentira, en segundos",
   u"La diferencia entre un data test y un unit test",
   u"Dónde poner cada uno para no probar dos veces lo mismo"],
  "unit-testing"),

 ("d20", 4, "2 horas", "flow", "d12",
  u"Despliegue a fondo",
  u"Curso oficial gratuito. Ambientes, corridas programadas y CI: que lo que se mergea corra solo y que lo que falla avise.",
  u"Terminas este paso cuando un merge dispara la corrida y no tienes que apretar nada.",
  [u"Separar desarrollo de producción de verdad, no de palabra",
   u"CI que corre los modelos que cambiaron y no todos",
   u"Que un fallo te llegue antes que al que usa el reporte"],
  "advanced-deployment"),

 ("d21", 4, "45 min", "school", "d13",
  u"Exposures",
  u"Curso oficial gratuito. Declarar quién consume tus modelos -un dashboard, un notebook, una API- para que el lineage llegue hasta el final.",
  u"Terminas este paso cuando sabes qué reporte se rompe antes de tocar un modelo.",
  [u"Saber a quién afecta un cambio antes de hacerlo",
   u"El lineage completo, del origen al dashboard",
   u"Documentación que se actualiza sola"],
  "exposures"),

 ("d22", 4, "2 horas", "build", "d14",
  u"dbt Mesh",
  u"Curso oficial gratuito. Varios proyectos de dbt que se referencian entre sí, con contratos y versiones, para cuando un repo solo ya no alcanza.",
  u"Terminas este paso cuando dos equipos comparten modelos sin pisarse.",
  [u"Contratos de modelo: prometer una forma y cumplirla",
   u"Versionar un modelo para no romperle el trabajo a otro equipo",
   u"Cuándo conviene partir y cuándo es complicarse al pedo"],
  "dbt-mesh"),

 ("d23", 4, "1 hora", "data", "d22",
  u"dbt sobre Apache Iceberg",
  u"Curso oficial gratuito. El formato de tabla abierto que están adoptando los warehouses, y cómo dbt materializa sobre él.",
  u"Terminas este paso cuando entiendes qué cambia y qué no al materializar sobre Iceberg.",
  [u"Qué resuelve Iceberg y por qué aparece en todas las ofertas",
   u"Materializar sobre Iceberg desde dbt",
   u"Dónde conviene y dónde es una vuelta de más"],
  "dbt-and-apache-iceberg"),
]


def nodo(c):
    cid, act, time, i, _, titulo, resumen, meta, wins, slug = c
    w = u",\n           ".join(u'"%s"' % x for x in wins)
    return (u'  {\n'
            u'    id: "%s", act: %d, time: "%s", i: "%s",\n'
            u'    title: "%s",\n'
            u'    summary: "%s",\n'
            u'    goal: "%s",\n'
            u'    wins: [%s],\n'
            u'    u: "https://learn.getdbt.com/courses/%s"\n'
            u'  }' % (cid, act, time, i, titulo, resumen, meta, w, slug))


def main():
    p = os.path.join(D, P)
    t = io.open(p, encoding="utf-8").read()

    puestos = 0
    for c in NUEVOS:
        cid, _, _, _, despues, titulo = c[0], c[1], c[2], c[3], c[4], c[5]
        if u'id: "%s"' % cid in t:
            continue

        # Se inserta despues del nodo que le corresponde, para que el
        # orden del mapa siga siendo el orden en que conviene hacerlos.
        m = re.search(r'\n  \{\n    id: "%s",' % re.escape(despues), t)
        if not m:
            print(u"  ABORTA: no encuentro el nodo %s" % despues); sys.exit(1)
        fin = t.index(u"\n  }", m.end()) + 4          # cierre de ese nodo
        t = t[:fin] + u",\n" + nodo(c) + t[fin:]
        puestos += 1

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%s: %d cursos nuevos" % (P, puestos))


main()
