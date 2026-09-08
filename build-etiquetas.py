# -*- coding: utf-8 -*-
u"""Etiquete de mas las rutas nuevas, y una salio recomendada donde no va.

   Se vio probando el puesto de Cloud Engineer: un CV de sysadmin que
   dice "nunca use la nube ni contenedores" recibia la ruta de TESTING.

   La causa es mia. Al dar de alta las rutas nuevas etiquete cada
   tramo con todo lo que el tramo TOCA, en vez de con lo que ENSENA:

   - testing tramo 3 llevaba "web" y "backend" porque se prueba una
     aplicacion web y una API. Pero aprender Playwright no es aprender
     desarrollo web, y probar una API con Postman no es aprender a
     escribir backend.
   - testing tramo 4 llevaba "cloud" porque hay un paso de GitHub
     Actions. Integracion continua no es infraestructura en la nube.
   - mlops llevaba "python" en el tramo de MLflow y DVC, y "cloud" en
     el de servir modelos. Esas herramientas se usan desde Python y
     corren en algun lado, pero no ensenan ninguna de las dos cosas.
   - viz llevaba "sql" en el tramo de Metabase, que se apoya en SQL
     pero no lo ensena.
   - funcional llevaba "modelado" por BPMN: BPMN modela procesos, no
     datos, que es lo que quiere decir ese tema.
   - nube llevaba "sql" por DP-900, que habla de bases relacionales
     como concepto y no escribe una consulta.

   Con eso, la ruta de testing terminaba cubriendo calidad, prog, web,
   backend y cloud: cinco de los cinco temas que pide Cloud Engineer.
   Le ganaba a la ruta de la nube, que solo cubre nube, y por goleada.

   La regla, y queda escrita arriba de la tabla: se etiqueta lo que el
   tramo ensena. Si etiquetas lo que roza, la ruta empieza a competir
   por puestos que no sirve.

   Uso: python build-etiquetas.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "build-temas.py")

CAMBIOS = [
 (u' ("mlops", 2):        ["mlops", "python"],\n'
  u' ("mlops", 3):        ["mlops", "cloud"],',
  u' ("mlops", 2):        ["mlops"],\n'
  u' ("mlops", 3):        ["mlops"],'),

 (u' ("viz", 3):          ["viz", "sql"],',
  u' ("viz", 3):          ["viz"],'),

 (u' ("funcional", 3):    ["producto", "modelado"],',
  u' ("funcional", 3):    ["producto"],'),

 (u' ("nube", 3):         ["cloud", "sql", "modelado", "pipelines"],',
  u' ("nube", 3):         ["cloud", "modelado", "pipelines"],'),

 (u' ("testing", 3):      ["calidad", "web", "backend"],\n'
  u' ("testing", 4):      ["calidad", "cloud"],',
  u' ("testing", 3):      ["calidad"],\n'
  u' ("testing", 4):      ["calidad"],'),
]

REGLA = u'''# Se etiqueta lo que el tramo ENSENA, no lo que toca.
#
# Paso al reves y costo caro: las rutas nuevas quedaron etiquetadas
# con todo lo que rozaban -testing con web, backend y cloud porque se
# prueban aplicaciones web, APIs y se corre en GitHub Actions- y la
# ruta de testing termino cubriendo cinco de los cinco temas que pide
# Cloud Engineer. Un CV de sysadmin que decia "nunca use la nube"
# recibia la ruta de testing en vez de la de la nube.
#
# Aprender Playwright no es aprender desarrollo web. Si etiquetas lo
# que roza, la ruta empieza a competir por puestos que no sirve.
POR_TRAMO = {'''

t = io.open(P, encoding="utf-8").read()
if "Se etiqueta lo que el tramo ENSENA" in t:
    print(u"  ya estaba"); sys.exit(1)

for viejo, nuevo in CAMBIOS:
    if t.count(viejo) != 1:
        print(u"  ABORTA: %r x%d, esperaba 1" % (viejo[:46], t.count(viejo)))
        sys.exit(1)
    t = t.replace(viejo, nuevo)

if t.count(u"POR_TRAMO = {") != 1:
    print(u"  ABORTA: no encuentro la tabla"); sys.exit(1)
t = t.replace(u"POR_TRAMO = {", REGLA, 1)

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"build-temas.py: se etiqueta lo que ensena, no lo que toca")
