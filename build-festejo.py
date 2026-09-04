# -*- coding: utf-8 -*-
"""La chinchilla festeja lo que sale bien.

   Hasta ahora solo aparecia cuando NO habia nada: la busqueda vacia,
   la ruta sin armar, la lista sin resultados. Es la mitad del trabajo.
   La otra mitad es estar cuando algo sale bien, que es el momento en
   que alguien decide si vuelve manana.

   Donde entra:
     - marcar un curso                 -> festeja
     - un tramo redondo (cada 5)       -> cohete
     - la ruta entera                  -> cohete
     - el reto del dia, completo       -> cohete
     - la bienvenida                   -> saluda

   El aviso de texto que habia en cada uno se va: decir lo mismo dos
   veces, en dos esquinas distintas, no es el doble de festejo.

   Uso: python build-festejo.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

# Las rutas del catalogo, mas la que arma el CV.
RUTAS = ["mi-ruta.html", "subir-nivel.html", "snowpro.html", "data-engineer.html",
         "dbt.html", "bigdata.html", "arquitectura.html", "cs50.html",
         "data-science.html", "sql-python.html", "ai-fundamentos.html",
         "deep-learning.html", "llm-agentes.html", "ml-aplicado.html", "web3.html"]

OTRAS = ["index.html", "practica.html", "semana.html", "cv.html", "armar.html"]


def sumar_recursos(t):
    """El .js y el .css de la chinchilla, si faltan."""
    if 'src="chinchilla.js' not in t:
        m = re.search(r'<script src="path-sync\.js[^"]*"></script>', t)
        if not m:
            return t, "sin path-sync"
        t = t[:m.start()] + '<script src="chinchilla.js"></script>\n' + t[m.start():]
    if 'chinchilla.css' not in t:
        m = re.search(r'<link rel="stylesheet" href="tema\.css[^"]*">', t)
        if not m:
            return t, "sin tema.css"
        t = (t[:m.end()] +
             '\n<link rel="stylesheet" href="chinchilla.css">' + t[m.end():])
    return t, ""


# El final de toggleDone, que es donde se avisaba con un toast.
VIEJO = re.compile(
    r'  var c = doneCount\(\);\n'
    r'  if\(c === NODES\.length\)\{[^\n]*\n'
    r'  else if\(done\[id\]\)\{[^\n]*\n'
    r'\}', re.M)

NUEVO = '''  var c = doneCount();

  /* Un cartel en una esquina y nada mas. El festejo que interrumpe
     lo que estabas haciendo deja de ser un premio. */
  if(typeof Chin === "undefined"){ return; }
  if(c === NODES.length){
    Chin.festejar("cohete", "La terminaste entera",
      "Los " + c + " cursos de esta ruta, completos. Poca gente llega.");
  }else if(done[id] && c %% 5 === 0){
    Chin.festejar("cohete", c + " cursos hechos",
      "Quedan " + (NODES.length - c) + ". Vas bien.");
  }else if(done[id]){
    Chin.festejar("festeja", "Uno menos",
      "Quedan " + (NODES.length - c) + " en esta ruta.");
  }
}'''


def hacer(archivo, con_festejo):
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        return "no existe"
    t = io.open(p, encoding="utf-8").read()

    t, err = sumar_recursos(t)
    if err:
        return err

    hechos = 0
    if con_festejo and 'Chin.festejar("festeja"' not in t:
        t, n = VIEJO.subn(NUEVO.replace("%%", "%"), t, count=1)
        hechos += n
        if not n:
            return "el final de toggleDone no coincide"

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo (%d)" % hechos


for a in RUTAS:
    print(u"%-22s %s" % (a, hacer(a, True)))
for a in OTRAS:
    print(u"%-22s %s" % (a, hacer(a, False)))
