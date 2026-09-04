# -*- coding: utf-8 -*-
"""Saca reglas CSS repetidas dentro de una misma pagina.

   Los scripts que fueron insertando bloques de estilo terminaron
   pegando el mismo bloque varias veces. El navegador aplica el
   ultimo, asi que no siempre se nota, pero:

     - el archivo crece al pedo,
     - editar "la" regla puede tocar la copia que no gana,
     - y depurar se vuelve adivinanza.

   Deja la ultima aparicion de cada selector, que es la que el
   navegador estaba usando: asi la pagina se ve igual despues de
   limpiar.

   Uso: python dedup-css.py [--escribir]
"""
import io, os, re, sys, glob

D = os.path.dirname(os.path.abspath(__file__))

# Una regla: el selector, la llave que abre, lo de adentro y la que
# cierra. No entra en @media ni en anidados, a proposito: ahi el
# mismo selector puede repetirse con toda razon.
REGLA = re.compile(r"^([.#][A-Za-z][^{}\n]{0,120}?)\{([^{}]*)\}[ \t]*$", re.M)


def limpiar(texto):
    """Devuelve (texto sin duplicados, cuantos saco)."""
    bloques = []
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", texto, re.S):
        bloques.append((m.start(1), m.end(1)))
    if not bloques:
        return texto, 0

    fuera = 0
    # De atras para adelante, para no correr los indices.
    for ini, fin in reversed(bloques):
        css = texto[ini:fin]
        vistos = {}
        for m in REGLA.finditer(css):
            clave = (m.group(1).strip(), m.group(2).strip())
            vistos.setdefault(clave, []).append(m.span())

        # De cada regla identica, se borran todas menos la ultima.
        borrar = []
        for clave, spans in vistos.items():
            if len(spans) > 1:
                borrar.extend(spans[:-1])
        if not borrar:
            continue
        borrar.sort()
        nuevo, ultimo = [], 0
        for a, b in borrar:
            nuevo.append(css[ultimo:a])
            ultimo = b
            # comerse el salto que queda solo
            while ultimo < len(css) and css[ultimo] == "\n":
                ultimo += 1
        nuevo.append(css[ultimo:])
        css2 = "".join(nuevo)
        fuera += len(borrar)
        texto = texto[:ini] + css2 + texto[fin:]

    return texto, fuera


def main():
    escribir = "--escribir" in sys.argv
    total = 0
    for p in sorted(glob.glob(os.path.join(D, "*.html"))):
        t = io.open(p, encoding="utf-8").read()
        t2, n = limpiar(t)
        if not n:
            continue
        total += n
        ahorro = (len(t) - len(t2)) / 1024.0
        print(u"%-22s %3d reglas repetidas  (%.1f KB)" % (
            os.path.basename(p), n, ahorro))
        if escribir:
            io.open(p, "w", encoding="utf-8", newline="").write(t2)

    if not total:
        print(u"sin reglas repetidas")
    elif not escribir:
        print(u"\n%d reglas repetidas en total. Corre con --escribir para sacarlas." % total)
    else:
        print(u"\n%d reglas repetidas, fuera." % total)


main()
