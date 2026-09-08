# -*- coding: utf-8 -*-
u"""Tres puestos mas, y que cada uno diga en que se diferencia.

   Dos cosas del mismo pedido.

   1. Faltaban tipos. "Data Engineer" tapaba tres oficios que en un
      aviso de trabajo se piden por separado: el que arma pipelines
      sobre un almacen, el que los arma cuando los datos no entran en
      una maquina, y el que sostiene la infraestructura donde corre
      todo. Entran Big Data Engineer y Cloud Engineer.

      Y entra desarrollador Web3, que era el caso al reves: habia una
      ruta de seis pasos y sesenta y nueve horas que ningun puesto
      pedia, o sea material que nadie iba a encontrar desde su CV.

   2. Cada puesto dice ahora en que se distingue del de al lado. El
      resumen contaba que hace; faltaba lo otro, que es lo que
      alguien necesita para elegir entre dos que se parecen. Un data
      scientist y un ML engineer se describen casi igual y hacen
      cosas distintas: uno investiga y el otro sostiene lo que el
      primero encontro.

      Va en un campo aparte y no pegado al resumen, porque son dos
      preguntas distintas -que hace, y en que se diferencia- y en la
      tarjeta se leen distinto.

   Los pesos de los tres nuevos salen del material que ya existe, no
   al reves: bigdata tiene diecinueve pasos, cloud cuarenta y dos, y
   web3 cinco. Ninguno de los tres inventa un tema.

   Uso: python build-puestos.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r x%d, esperaba %d"
                  % (archivo, viejo[:50], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-24s %d cambios" % (archivo, len(cambios)))


# ---------------------------------------------------- 1. los tres nuevos
parchar("build-temas.py", [
 (u' {"id": "analista_funcional", "nombre": u"Analista funcional",',
  u' {"id": "cloud_engineer", "nombre": u"Cloud Engineer",\n'
  u'  "resumen": u"Sostener la infraestructura sobre la que corre todo lo dem\\u00e1s, y que no cueste una fortuna.",\n'
  u'  "distingue": u"No escribe la aplicaci\\u00f3n: hace que tenga d\\u00f3nde correr, que aguante y que se pueda pagar.",\n'
  u'  "temas": {"cloud": 3, "prog": 2, "calidad": 2, "backend": 1,\n'
  u'            "pipelines": 1}},\n\n'
  u' {"id": "bigdata_engineer", "nombre": u"Big Data Engineer",\n'
  u'  "resumen": u"Procesar datos que no entran en una m\\u00e1quina: Spark, streaming y sistemas distribuidos.",\n'
  u'  "distingue": u"Es Data Engineer cuando el volumen ya no deja hacerlo de la forma simple.",\n'
  u'  "temas": {"bigdata": 3, "sql": 3, "python": 3, "cloud": 2,\n'
  u'            "pipelines": 2, "modelado": 2, "prog": 1}},\n\n'
  u' {"id": "web3_dev", "nombre": u"Desarrollador Web3",\n'
  u'  "resumen": u"Contratos inteligentes y aplicaciones sobre blockchain, de Solidity para arriba.",\n'
  u'  "distingue": u"Es desarrollo backend donde un error no se arregla con otro deploy: el contrato ya est\\u00e1 publicado.",\n'
  u'  "temas": {"web3": 3, "prog": 3, "web": 2, "backend": 2, "calidad": 2,\n'
  u'            "cloud": 1}},\n\n'
  u' {"id": "analista_funcional", "nombre": u"Analista funcional",', 1),
])

# ---------------------------------------------------- 2. el campo nuevo
# (id, en que se distingue del de al lado)
DISTINGUE = {
 "data_engineer":  u"Mueve y ordena los datos para que otros los usen. No los analiza ni entrena modelos con ellos.",
 "data_analyst":   u"Usa los datos que otro preparó. Su producto es una respuesta, no un sistema que queda corriendo.",
 "data_scientist": u"Investiga y prueba hipótesis. Llevar a producción lo que encuentra es trabajo del ML Engineer.",
 "ml_engineer":    u"Lo que el científico entrenó, éste lo hace correr todos los días y avisar cuando falla.",
 "ai_engineer":    u"No entrena modelos: usa los que ya existen y arma algo alrededor que resuelva un problema.",
 "fullstack":      u"Toca las dos mitades. Sabe menos de cada una que el especialista, y llega solo hasta el final.",
 "frontend":       u"Termina donde empieza el servidor. Su problema es que se entienda y funcione en cualquier pantalla.",
 "backend_dev":    u"Nunca se ve, y si falla se nota en todo. Su problema es que aguante y que los datos estén bien.",
 "tester":         u"No construye: rompe a propósito, y deja escrito cómo se rompió para que no vuelva a pasar.",
 "analista_funcional": u"No programa. Su trabajo es que lo que se construya sea lo que hacía falta.",
}

p = os.path.join(D, "build-temas.py")
t = io.open(p, encoding="utf-8").read()
puestos = 0
for pid, texto in DISTINGUE.items():
    marca = u'{"id": "%s", "nombre":' % pid
    i = t.find(marca)
    if i < 0:
        print(u"  ABORTA: no encuentro el puesto %s" % pid); sys.exit(1)
    j = t.find(u'"temas":', i)
    if j < 0 or u'"distingue"' in t[i:j]:
        continue
    t = t[:j] + u'"distingue": u"%s",\n  ' % texto + t[j:]
    puestos += 1
io.open(p, "w", encoding="utf-8", newline="").write(t)
print(u"%-24s %d con su diferencia" % ("los puestos de antes", puestos))

# ---------------------------------------------------- 3. que salga en la tarjeta
parchar("cv.html", [
 (u"""      '<b>' + esc(p.nombre) + '</b><span>' + esc(p.resumen) + '</span>' +""",
  u"""      '<b>' + esc(p.nombre) + '</b><span>' + esc(p.resumen) + '</span>' +
      /* En qué se diferencia del de al lado. Va aparte del resumen
         porque son dos preguntas distintas -qué hace, y en qué se
         distingue- y quien elige entre dos parecidos necesita la
         segunda. */
      (p.distingue ? '<span class="distingue">' + esc(p.distingue) + '</span>' : "") +""", 1),

 (u"\n</style>",
  u'''
/* La diferencia entre un puesto y el de al lado. Más tenue que el
   resumen: se lee cuando dudas entre dos, no antes. */
.puesto .distingue{
  font-size:11.5px; color:var(--text-3); line-height:1.45;
  padding-top:5px; border-top:1px solid var(--divider-soft);
}
.puesto[aria-pressed="true"] .distingue{ border-top-color:var(--accent-line); }
''' + u"\n</style>", 1),
])
