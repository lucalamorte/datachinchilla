# -*- coding: utf-8 -*-
"""Prueba de humo: abre cada pagina y comprueba que se pinte.

   Existe porque rompi la pagina del CV dos veces con el mismo tipo de
   error: una variable que quedo sin declarar despues de un reemplazo.
   La sintaxis estaba bien, asi que node --check no lo veia; el error
   solo aparecia al ejecutar, y ahi ya lo habia entregado.

   Levanta un servidor local, abre cada pagina en Chrome headless y
   junta lo que la consola escupe. No hace clics: alcanza con que
   cargar la pagina no explote, que es lo que fallaba.

   Uso: python humo.py
"""
import io, os, re, json, sys, time, socket, subprocess, tempfile, shutil
import threading
import http.server
import socketserver

D = os.path.dirname(os.path.abspath(__file__))

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PAGINAS = [
    "index.html", "cv.html", "semana.html", "practica.html", "armar.html", "snowpro.html",
    "data-engineer.html", "dbt.html", "subir-nivel.html", "bigdata.html",
    "arquitectura.html", "cs50.html", "data-science.html", "sql-python.html",
    "ai-fundamentos.html", "deep-learning.html", "llm-agentes.html",
    "claude.html",
    "ml-aplicado.html", "web3.html", "fullstack.html", "airflow.html",
    "testing.html",
    "mi-ruta.html",
    "preguntas.html",
    "recursos.html",
]

# Ruido que no es culpa de la pagina.
IGNORAR = (
    "favicon",
    "net::ERR_INTERNET_DISCONNECTED",
    "Failed to load resource: net::ERR_NAME_NOT_RESOLVED",
)


def puerto_libre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def translate_path(self, path):
        path = path.split("?", 1)[0].split("#", 1)[0]
        return os.path.join(D, path.lstrip("/"))


def servir(puerto):
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", puerto), Silencioso)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# Que tiene que haber en el DOM de cada pagina despues de que corra
# su init. Si init muere a mitad, esto queda vacio.
MARCAS = {
    "index.html":  [("pathList", "el catalogo")],
    "cv.html":     [("puestos", "las tarjetas de puesto")],
    "semana.html": [("semana", "la grilla de la semana")],
    "practica.html": [("probs", "la lista de problemas"), ("bancos", "los bancos")],
    "armar.html":  [("catalogo", "el catalogo de piezas")],
    # No es una ruta del catalogo: es la que se arma para vos.
    "mi-ruta.html": [("mapa", "el mapa de tu ruta")],
    # No es una ruta: no pinta mapa. Lo que tiene que estar son
    # las preguntas, y estan en el HTML sin depender de ningun init.
    "preguntas.html": [("preguntas", "las preguntas")],
    "recursos.html": [("recursos", "los recursos")],
}
# El resto son rutas: todas pintan su mapa en #map.
# snowpro fue la primera ruta y usa map; las demas mapa.
POR_PAGINA_EXTRA = {"snowpro.html": [("map", "el mapa de la ruta")]}
POR_DEFECTO = [("mapa", "el mapa de la ruta")]


def revisar(url, pagina, perfil):
    """Carga la pagina y devuelve que quedo sin llenarse."""
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--user-data-dir=" + perfil,
        "--virtual-time-budget=5000",
        "--dump-dom", url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=45, errors="replace")
    except subprocess.TimeoutExpired:
        return ["se colgo al cargar"]

    dom = r.stdout or ""
    if len(dom) < 500:
        return ["no devolvio DOM"]

    fallos = []
    for ident, que in MARCAS.get(pagina, POR_PAGINA_EXTRA.get(pagina, POR_DEFECTO)):
        m = re.search(r'id="%s"[^>]*>(.*?)</' % re.escape(ident), dom, re.S)
        if not m:
            fallos.append("no encontre #%s (%s)" % (ident, que))
        elif len(m.group(1).strip()) < 40:
            fallos.append("#%s quedo vacio: no se pinto %s" % (ident, que))
    return fallos


def main():
    if not os.path.exists(CHROME):
        print("  no encontre Chrome en %s" % CHROME)
        sys.exit(2)

    puerto = puerto_libre()
    srv = servir(puerto)
    base = "http://127.0.0.1:%d/" % puerto
    perfil = tempfile.mkdtemp(prefix="humo-")

    rotas = []
    try:
        for pag in PAGINAS:
            if not os.path.exists(os.path.join(D, pag)):
                print("  %-22s no existe" % pag)
                continue
            errores = revisar(base + pag, pag, perfil)
            if errores:
                rotas.append((pag, errores))
                print("ROTA  %-22s %s" % (pag, errores[0]))
                for e in errores[1:3]:
                    print("      %-22s %s" % ("", e))
            else:
                print("ok    %s" % pag)
    finally:
        srv.shutdown()
        shutil.rmtree(perfil, ignore_errors=True)

    print()
    if rotas:
        print("%d de %d paginas no terminan de pintarse" % (len(rotas), len(PAGINAS)))
        sys.exit(1)
    print("las %d paginas se pintan enteras" % len(PAGINAS))


main()
