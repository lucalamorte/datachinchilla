# -*- coding: utf-8 -*-
"""La chinchilla en los estados vacios.

   Una pagina vacia se siente rota. Con ella ahi se siente vacia a
   proposito, que es distinto, y de paso dice que hacer.

   Donde entra:
     - el catalogo, cuando la busqueda no da nada     -> busca
     - la practica, cuando no queda ninguno con esos filtros -> busca
     - la practica, cuando los hiciste todos          -> festeja
     - tu ruta, cuando todavia no la armaste          -> escarba
     - el CV, mientras lee el archivo                 -> escarba

   Uso: python build-poses.py
"""
import io, os, re, sys, glob

D = os.path.dirname(os.path.abspath(__file__))

# Donde hace falta el modulo y la hoja de estilo.
PAGINAS = ["index.html", "cv.html", "practica.html", "mi-ruta.html", "armar.html"]


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


CAMBIOS = {
 # --- el catalogo sin resultados
 "index.html": [
   ('''    <p class="sin-rutas" id="sinRutas" hidden>Ninguna ruta coincide. Prueba con otra palabra o toca Todo.</p>''',
    '''    <div class="sin-rutas" id="sinRutas" hidden></div>'''),

   ('''  document.getElementById("sinRutas").hidden = lista.length > 0;''',
    '''  var vacio = document.getElementById("sinRutas");
  vacio.hidden = lista.length > 0;
  if(!lista.length && typeof Chin !== "undefined"){
    Chin.pinta(vacio, "busca", "Acá no hay nada",
      "Ninguna ruta coincide con eso. Prueba con otra palabra, o mira todas.");
  }'''),
 ],

 # --- la practica: sin resultados, o todos hechos
 "practica.html": [
   ('''  var c = document.getElementById("probs");
  c.innerHTML = h || '<li><p class="vacio">' +
    (fEstado === "pendientes" ? "Ninguno pendiente con esos filtros. Cambia a Todos para ver los hechos."
                              : "Ninguno coincide.") + '</p></li>';''',
    '''  var c = document.getElementById("probs");
  if(h){
    c.innerHTML = h;
  }else if(typeof Chin !== "undefined"){
    /* Dos vacíos distintos: no quedan pendientes (que es bueno) o no
       hay ninguno que coincida (que es un filtro de más). */
    var todos = Practica.avance(bancoActual);
    var listo = fEstado === "pendientes" && todos.hechos >= todos.total;
    c.innerHTML = "<li>" + (listo
      ? '<div class="chin-vacio-caja"></div>'
      : '<div class="chin-vacio-caja"></div>') + "</li>";
    Chin.pinta(c.querySelector(".chin-vacio-caja"),
      listo ? "festeja" : "busca",
      listo ? "Los hiciste todos" : "Nada con esos filtros",
      listo
        ? "Los " + todos.total + " del banco, resueltos. Cambia de banco, o repasa el que quieras."
        : "Ninguno coincide. Saca algún filtro, o cambia a Todos para ver también los hechos.");
  }'''),
 ],
}


def hacer(archivo):
    p = os.path.join(D, archivo)
    if not os.path.exists(p):
        return "no existe"
    t = io.open(p, encoding="utf-8").read()

    t, err = sumar_recursos(t)
    if err:
        return err

    hechos = 0
    for viejo, nuevo in CAMBIOS.get(archivo, []):
        if nuevo.strip() in t:
            continue
        if t.count(viejo) != 1:
            print("    ojo: el ancla aparece %d veces en %s" % (t.count(viejo), archivo))
            continue
        t = t.replace(viejo, nuevo)
        hechos += 1

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    return "listo (%d cambios)" % hechos


for a in PAGINAS:
    print(u"%-16s %s" % (a, hacer(a)))
