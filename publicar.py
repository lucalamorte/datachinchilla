# -*- coding: utf-8 -*-
"""Arma la carpeta que se sube, con lo que el sitio usa y nada mas.

   La carpeta de trabajo tiene veintisiete scripts de build, consultas
   .sql, apuntes en markdown, un demo de veinticinco megas y archivos
   personales sueltos (un PDF, un .docx). Subir la carpeta entera
   publicaria todo eso en internet.

   Asi que se copia lo que el sitio pide y se verifica que no falte
   nada: cada href, src y url() de cada pagina tiene que existir en la
   carpeta armada, o esto aborta.

   Uso: python publicar.py
        y despues se sube la carpeta 'publicar/'
"""
import io, os, re, shutil, sys

D = os.path.dirname(os.path.abspath(__file__))
SALE = os.path.join(D, "publicar")

# Lo que se copia. Todo lo demas se queda afuera por defecto: es mas
# seguro olvidarse de publicar algo que publicar algo de mas.
EXT = (".html", ".js", ".css", ".svg", ".png", ".jpg", ".webp",
       ".ico", ".xml", ".txt", ".woff", ".woff2")

# Lo que nunca va, aunque tenga una extension de las de arriba.
FUERA = ("cv_prueba.pdf", "_poses.html", "_cv_real.pdf")

# Paginas del sitio que NO cargan tema.css y aun asi se publican.
# og.html es la plantilla con la que se genera og.png.
SUELTAS = ("og.html",)


def archivos_del_sitio():
    """Los que se copian: por extension, menos los excluidos."""
    out = []
    for n in sorted(os.listdir(D)):
        if os.path.isdir(os.path.join(D, n)):
            continue
        if n in FUERA or n.startswith("_"):
            continue
        if n.lower().endswith(EXT):
            out.append(n)
    return out


def html_del_sitio(nombre):
    """Una pagina del sitio carga tema.css. Lo demas no es el sitio.

       Sin esto entra cualquier .html que quede en la carpeta: hoy se
       colo un informe de auditoria de 290 kB, que se habria publicado
       en internet sin que nadie lo notara.
    """
    if nombre in SUELTAS:
        return True
    return "tema.css" in io.open(os.path.join(D, nombre), encoding="utf-8").read()


def referencias(html):
    """Los archivos locales que una pagina pide.

       Se saltea lo que arma el JavaScript: href="' + p.u + '" es una
       plantilla, no una ruta, y buscarla como archivo da veintidos
       avisos falsos. Se queda solo lo que parece un nombre de archivo
       de verdad: sin espacios, sin comillas, y con extension.
    """
    out = set()
    for pat in (r'href="([^"#?:]+)', r'src="([^"#?:]+)', r'url\(([^)"\']+)\)'):
        for u in re.findall(pat, html):
            u = u.strip("'\" ").split("?")[0].split("#")[0]
            if not u or u.startswith(("http", "//", "data:", "mailto:")):
                continue
            if "+" in u or "'" in u or " " in u:      # lo arma el JS
                continue
            if "." not in os.path.basename(u):        # no es un archivo
                continue
            out.add(u)
    return out


def main():
    if os.path.isdir(SALE):
        shutil.rmtree(SALE)
    os.makedirs(SALE)

    copiados = archivos_del_sitio()

    ajenas = [n for n in copiados if n.endswith(".html") and not html_del_sitio(n)]
    if ajenas:
        print(u"Estos .html no son del sitio y estaban por publicarse:")
        for n in ajenas:
            print(u"   %s" % n)
        print(u"\nSacalos de la carpeta o agregalos a SUELTAS si de verdad van.")
        sys.exit(1)

    for n in copiados:
        shutil.copy2(os.path.join(D, n), os.path.join(SALE, n))

    # --- que no falte nada de lo que las paginas piden
    hay = set(os.listdir(SALE))
    faltan = {}
    for n in copiados:
        if not n.endswith(".html"):
            continue
        t = io.open(os.path.join(D, n), encoding="utf-8").read()
        for r in referencias(t):
            if r not in hay:
                faltan.setdefault(r, []).append(n)

    print(u"%d archivos en publicar/" % len(copiados))
    for e in (".html", ".js", ".css", ".svg", ".png", ".xml", ".txt"):
        c = len([x for x in copiados if x.endswith(e)])
        if c:
            print(u"   %-6s %d" % (e, c))

    peso = sum(os.path.getsize(os.path.join(SALE, x)) for x in hay)
    print(u"\npeso total: %.1f MB" % (peso / 1048576.0))

    if faltan:
        print(u"\nFALTAN, y las paginas los piden:")
        for r in sorted(faltan):
            print(u"   %-28s lo pide %s" % (r, ", ".join(faltan[r][:3])))
        sys.exit(1)

    print(u"\nnada roto: cada href y src apunta a un archivo que esta")


main()
