# -*- coding: utf-8 -*-
u"""Comprueba que cada link de afuera siga vivo.

   El sitio es una lista de links a material de otros. Los links de
   otros se rompen solos: un curso se archiva, una pagina se muda, un
   ejercicio pasa a ser de pago. Y quien se entera primero es el que
   estaba estudiando, que hace clic y se come un 404.

   Ya paso: un link roto de LeetCode y cinco ejercicios que habian
   pasado a Premium los encontro Luca. Esto existe para que no los
   encuentre el.

   Que hace:

   - Junta cada http(s) de las paginas y de los .js de datos.
   - Prueba con HEAD y, si no le gusta, con GET: hay servidores que a
     HEAD le contestan cualquier cosa.
   - Reporta lo que no da 200, y aparte lo que redirige a otro lado:
     una redireccion es un link que todavia anda pero ya se mudo, y el
     atajo puede desaparecer.

   Tres cosas que aprendio a la mala en su primera corrida:

   1. Va de a un pedido por servidor, en fila. La primera version
      disparo cien pedidos a StrataScratch en medio minuto y se comio
      sesenta y cinco 429. Un 429 nunca es un link roto: es este
      script portandose mal.
   2. Los namespaces de XML no son links. www.w3.org/2000/svg esta en
      cada <svg> del sitio y no lleva a ningun lado.
   3. Recortar la cola de la URL hay que hacerlo con cuidado. Recortar
      los caracteres de "&quot" uno por uno dejaba
      "...tasks-intro" en "...tasks-intr" e inventaba siete 404 que no
      existian.

   Lo que NO es un problema:

   - 403 en hosts con proteccion de robots: Udemy, LeetCode, Ko-fi,
     Astronomer y LinkedIn le contestan 403 a cualquier cosa que no
     sea un navegador de verdad. Estan en BLINDADOS. Que un host este
     en esa lista no dice que sus links esten bien: dice que este
     script no puede opinar y hay que mirarlos a mano.
   - Los links de la propia casa: los revisa publicar.py, que sabe si
     el archivo existe.

   Uso:  python links.py            todo
         python links.py leetcode   solo lo que contenga eso
         python links.py --mudados  ademas, los que se mudaron
"""
import io, os, re, ssl, sys, time
import collections
import concurrent.futures as futuros
import urllib.request, urllib.error

D = os.path.dirname(os.path.abspath(__file__))

# Hosts que le contestan 403 a cualquier cosa que no sea un navegador.
# No dice que sus links esten bien: dice que este script no puede
# opinar, y que hay que mirarlos a mano.
BLINDADOS = (
    "academy.astronomer.io",
    "www.astronomer.io",
    "www.linkedin.com",
    "leetcode.com",
    "www.udemy.com",
    "ko-fi.com",
    # Contesta 429 a todo lo que no sea un navegador, incluso a un
    # pedido cada ocho segundos. No es que vayamos rapido: se
    # comprobo abriendo uno de los sesenta y cinco en un navegador de
    # verdad y carga perfecto.
    "platform.stratascratch.com",
)

# Paginas de la propia casa: las revisa publicar.py.
PROPIOS = ("datachinchilla.com", "datachinchilla.pages.dev")

# Direcciones que estan en el codigo pero nadie visita: son la puerta
# de una API, no una pagina. La de Supabase contesta 404 a la raiz,
# que es lo correcto, y salia como link roto en veinticinco paginas.
NO_SON_LINKS = ("supabase.co",)

# No son links: son identificadores de espacio de nombres. Estan en
# cada <svg> y en el JSON-LD, y nadie hace clic en ellos.
NAMESPACES = ("www.w3.org/", "schema.org/", "ogp.me/")

NAVEGADOR = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/126.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

URL = re.compile(r"https?://[^\s\"'<>)\\]+")

# Un pedido por servidor cada tanto. Sin esto, un host con cien links
# -StrataScratch tiene ciento treinta- contesta 429 y el informe se
# llena de errores que puso este script.
ESPERA = 0.7


def limpiar(u):
    u"""La cola de una URL sacada de HTML.

       Con cuidado: recortar los caracteres de "&quot" uno por uno
       dejaba ".../tasks-intro" en ".../tasks-intr" e inventaba 404
       que no existian. Se saca la entidad entera o nada."""
    for cola in ("&quot;", "&quot", "&amp;", "&#39;"):
        if u.endswith(cola):
            u = u[:-len(cola)]
    return u.rstrip(".,;:")


def juntar():
    u"""Cada link de afuera, con las paginas donde aparece."""
    donde = {}
    for a in sorted(os.listdir(D)):
        if not (a.endswith(".html") or a.endswith(".js")):
            continue
        if a == "og.html":
            continue
        t = io.open(os.path.join(D, a), encoding="utf-8", errors="replace").read()
        for m in URL.finditer(t):
            u = limpiar(m.group(0))
            if any(n in u for n in NAMESPACES):
                continue
            host = u.split("/")[2].lower()
            if any(host.endswith(p) for p in PROPIOS):
                continue
            if any(host.endswith(n) for n in NO_SON_LINKS):
                continue
            donde.setdefault(u, set()).add(a)
    return donde


def contexto():
    """El almacen de certificados.

       El que trae Python en esta maquina tiene raices vencidas: daba
       CERTIFICATE_VERIFY_FAILED en treinta y seis links que curl abre
       sin chistar, o sea treinta y seis errores inventados. Si esta
       certifi, que se actualiza con pip, se usa ese."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = contexto()


def pedir(u, metodo):
    req = urllib.request.Request(u, method=metodo, headers=NAVEGADOR)
    r = urllib.request.urlopen(req, timeout=25, context=CTX)
    return r.getcode(), r.geturl()


def mirar(u):
    u"""(codigo, destino, comentario). El codigo es 0 si ni contesto."""
    for metodo in ("HEAD", "GET"):
        try:
            codigo, fin = pedir(u, metodo)
            if codigo == 200 or metodo == "GET":
                return codigo, fin, ""
        except urllib.error.HTTPError as e:
            # Hay servidores que no saben contestar un HEAD: si dice
            # que no, se pregunta con GET antes de creerle.
            if metodo == "GET":
                return e.code, u, ""
        except Exception as e:
            if metodo == "GET":
                # El motivo entero: "URLError" a secas no dice si el
                # sitio no esta o si el problema es de esta maquina.
                return 0, u, str(getattr(e, "reason", e))[:70]
    return 0, u, "sin respuesta"


def main():
    args = [a for a in sys.argv[1:]]
    ver_mudados = "--mudados" in args
    filtro = ([a for a in args if not a.startswith("--")] or [""])[0].lower()

    donde = juntar()
    urls = sorted(x for x in donde if filtro in x.lower())
    if not urls:
        print(u"no hay links que digan %r" % filtro)
        return 0

    # Por servidor. Cada uno va en fila y los servidores en paralelo:
    # asi ninguno recibe una rafaga y el conjunto igual termina.
    por_host = collections.OrderedDict()
    for u in urls:
        por_host.setdefault(u.split("/")[2].lower(), []).append(u)

    print(u"%d links de afuera en %d servidores, desde %d paginas\n"
          % (len(urls), len(por_host), len(set().union(*donde.values()))))

    hecho, t0 = [0], time.time()

    def fila(lista):
        u"""Los links de un servidor, de a uno y al ritmo que aguante.

           Si contesta 429 es que vamos rapido para el: se espera mas
           y se vuelve a preguntar, y a partir de ahi el resto de su
           fila va mas lento. Sin esto StrataScratch -sesenta y cinco
           links- quedaba entero sin comprobar."""
        salida, espera = [], ESPERA
        for i, u in enumerate(lista):
            if i:
                time.sleep(espera)
            r = mirar(u)
            if r[0] == 429 and espera < 8:
                espera *= 3
                time.sleep(espera)
                r = mirar(u)
            salida.append((u,) + r)
            hecho[0] += 1
            if hecho[0] % 25 == 0:
                sys.stdout.write("  %d de %d\r" % (hecho[0], len(urls)))
                sys.stdout.flush()
        return salida

    resultados = []
    with futuros.ThreadPoolExecutor(max_workers=10) as pool:
        for lote in pool.map(fila, por_host.values()):
            resultados.extend(lote)

    rotos, mudados, ciegos = [], [], []
    for u, codigo, fin, nota in resultados:
        host = u.split("/")[2].lower()
        blindado = any(host.endswith(b) for b in BLINDADOS)
        if codigo == 200:
            if fin and fin.rstrip("/") != u.rstrip("/"):
                mudados.append((u, fin))
            continue
        # Un 429 nunca es un link roto: es este script yendo rapido.
        if codigo == 429 or (blindado and codigo in (0, 403, 999)):
            ciegos.append((u, codigo))
            continue
        rotos.append((u, codigo, nota))

    print(u"  %d de %d, en %d s\n" % (len(urls), len(urls), int(time.time() - t0)))

    if rotos:
        print(u"ROTOS (%d)" % len(rotos))
        for u, codigo, nota in sorted(rotos, key=lambda x: (-x[1], x[0])):
            print(u"  %s  %s" % (codigo or "sin respuesta", u))
            if nota:
                print(u"        %s" % nota)
            print(u"        en %s" % ", ".join(sorted(donde[u])))
        print()

    if mudados:
        print(u"SE MUDARON (%d) · andan, pero el link ya no es el bueno" % len(mudados))
        if ver_mudados:
            for u, fin in mudados:
                print(u"  %s\n    -> %s" % (u, fin))
        else:
            cuenta = collections.Counter(u.split("/")[2] for u, _ in mudados)
            for h, n in cuenta.most_common():
                print(u"  %-32s %d" % (h, n))
            print(u"  (con --mudados salen uno por uno)")
        print()

    if ciegos:
        print(u"NO PUEDO OPINAR (%d) · el servidor bloquea robots o me freno"
              % len(ciegos))
        cuenta = collections.Counter(u.split("/")[2] for u, _ in ciegos)
        for h, n in cuenta.most_common():
            print(u"  %-32s %d" % (h, n))
        print()

    print(u"ningun link roto" if not rotos else
          u"%d links rotos" % len(rotos))
    return 1 if rotos else 0


sys.exit(main())
