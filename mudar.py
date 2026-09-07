# -*- coding: utf-8 -*-
u"""Apunta al lugar nuevo los links que se mudaron.

   links.py encuentra los que redirigen. Redirigir no es estar roto,
   pero es un link que ya no es el bueno: el atajo lo mantiene el otro
   sitio y lo puede sacar cuando quiera, y ahi si se rompe. Ciento
   veintiseis del sitio estan asi, casi todos de cognitiveclass, que
   paso de identificadores -course-v1:IBM+BD0141EN+v1- a nombres.

   Cuidado con el ancla. Un "#load-history" no viaja al servidor, asi
   que el destino de la redireccion nunca lo trae: copiarlo tal cual
   perderia el punto exacto de la pagina al que apuntaba el link. Se
   vuelve a pegar.

   No toca:

   - Redirecciones que solo agregan o sacan la barra final: es la
     misma pagina y cambiarlas es ruido.
   - Las que cambian de dominio, que se listan aparte: que un curso
     pase a otro sitio es una decision de contenido, no un arreglo
     mecanico.

   Uso:  python mudar.py         muestra lo que haria
         python mudar.py --ya    lo hace
"""
import io, os, re, sys
import collections

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

# links.py corre al importarse (termina en sys.exit), asi que se le
# saca lo que hace falta leyendo el archivo. Es feo, pero es una sola
# verdad: las reglas de que es un link viven ahi.
_fuente = io.open(os.path.join(D, "links.py"), encoding="utf-8").read()
_ns = {"io": io, "os": os, "re": re, "sys": sys, "D": D,
       "collections": collections,
       "__file__": os.path.join(D, "links.py")}
exec(compile(_fuente[:_fuente.index("def main()")], "links.py", "exec"), _ns)

juntar, mirar = _ns["juntar"], _ns["mirar"]


def sin_ancla(u):
    i = u.find("#")
    return (u[:i], u[i:]) if i >= 0 else (u, "")


def misma(a, b):
    u"""Si dos URLs son la misma pagina para lo que nos importa."""
    return a.rstrip("/") == b.rstrip("/")


# Donde puede terminar una URL dentro del archivo. Lo que siga a la
# URL tiene que ser uno de estos, o no es la URL entera.
FIN = "\"'<> \t\r\n)"


def cambiar(texto, viejo, nuevo):
    u"""Reemplaza la URL entera, no el pedazo.

       Un replace pelado rompio doce links de verdad: ".../learn" es
       prefijo de ".../learn/comprehensive-sql/introduction", asi que
       al mudar el corto se le inyecto el tramo en el medio a los doce
       largos y quedaron en 404. Lo encontro links.py en la corrida
       siguiente, que para eso esta.

       Ahora la URL solo se cambia si lo que viene detras es un cierre
       de comilla, un espacio o el fin del texto."""
    salida, i = [], 0
    while True:
        j = texto.find(viejo, i)
        if j < 0:
            salida.append(texto[i:])
            return "".join(salida)
        fin = j + len(viejo)
        sigue = texto[fin] if fin < len(texto) else ""
        salida.append(texto[i:j])
        salida.append(nuevo if (sigue == "" or sigue in FIN) else viejo)
        i = fin


# Una redireccion a una pantalla de sesion no dice que el link se
# mudo: dice que el que pregunta no esta logueado. El link de
# compartir en LinkedIn redirige al login para este script y anda
# perfecto para quien tiene la sesion abierta; cambiarlo por el login
# habria roto un boton que funciona.
SESION = ("login", "signin", "sign-in", "session_redirect", "/uas/", "oauth",
          "accounts.google", "/checkpoint")


def es_sesion(u):
    b = u.lower()
    return any(s in b for s in SESION)


def main():
    aplicar = "--ya" in sys.argv
    donde = juntar()

    cambios, dominio, n = [], [], 0
    urls = sorted(donde)
    print(u"mirando %d links...\n" % len(urls))

    por_host = collections.OrderedDict()
    for u in urls:
        por_host.setdefault(u.split("/")[2].lower(), []).append(u)

    import concurrent.futures as futuros
    import time

    def fila(lista):
        out, espera = [], _ns["ESPERA"]
        for i, u in enumerate(lista):
            if i:
                time.sleep(espera)
            out.append((u,) + mirar(u))
        return out

    res = []
    with futuros.ThreadPoolExecutor(max_workers=10) as pool:
        for lote in pool.map(fila, por_host.values()):
            res.extend(lote)

    for u, codigo, fin, _nota in res:
        if codigo != 200 or not fin:
            continue
        base, ancla = sin_ancla(u)
        if misma(fin, base) or misma(fin, u):
            continue
        if es_sesion(fin):
            continue
        # Un link con parametros suele redirigir por lo que sabe el
        # servidor de quien pregunta, no porque la pagina se haya
        # mudado. No es un arreglo mecanico.
        if "?" in base:
            continue
        # El ancla no viaja al servidor: se vuelve a pegar, o se
        # perderia el punto exacto al que apuntaba el link.
        nuevo = fin + ancla if ("#" not in fin and ancla) else fin
        if u.split("/")[2].lower() != fin.split("/")[2].lower():
            dominio.append((u, nuevo))
            continue
        cambios.append((u, nuevo))

    if dominio:
        print(u"CAMBIAN DE SITIO (%d) · no los toco, decidilos vos" % len(dominio))
        for u, nuevo in dominio:
            print(u"  %s\n    -> %s\n    en %s" % (u, nuevo, ", ".join(sorted(donde[u]))))
        print()

    if not cambios:
        print(u"nada que mudar")
        return 0

    print(u"SE MUDARON DENTRO DEL MISMO SITIO (%d)" % len(cambios))
    cuenta = collections.Counter(u.split("/")[2] for u, _ in cambios)
    for h, c in cuenta.most_common():
        print(u"  %-32s %d" % (h, c))
    print()

    if not aplicar:
        print(u"esto es un ensayo: con --ya se aplica")
        return 0

    for a in sorted(os.listdir(D)):
        if not (a.endswith(".html") or a.endswith(".js")) or a == "og.html":
            continue
        p = os.path.join(D, a)
        t = io.open(p, encoding="utf-8").read()
        antes = t
        for u, nuevo in cambios:
            t = cambiar(t, u, nuevo)
        if t != antes:
            io.open(p, "w", encoding="utf-8", newline="").write(t)
            n += 1

    # Que no haya aparecido ninguna URL que nadie pidio. Es la red
    # contra lo que ya paso una vez: una URL que es prefijo de otra y
    # un reemplazo que le mete un tramo en el medio a doce vecinas.
    # Se comprueba sin red: cada link que quede tiene que ser uno de
    # los de antes o uno de los destinos previstos.
    conocidos = set(donde) | set(nuevo for _, nuevo in cambios)
    intrusos = sorted(u for u in juntar() if u not in conocidos)
    if intrusos:
        print()
        print(u"CUIDADO: quedaron %d links que nadie pidio" % len(intrusos))
        for u in intrusos[:20]:
            print(u"  %s" % u)
        print(u"  revisa el reemplazo antes de publicar")
        return 1

    print(u"%d archivos al dia, y ningun link de mas" % n)
    return 0


sys.exit(main())
