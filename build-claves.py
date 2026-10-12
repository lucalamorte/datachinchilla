# -*- coding: utf-8 -*-
u"""Las claves de Firebase, en las treinta paginas de una vez.

   Son tres valores y estan repetidos en cada pagina, porque el sitio
   no tiene bundler: cada HTML lleva su propio CONFIG. Pegarlos a mano
   treinta veces es como se cuela un error que despues no se encuentra.

   Los tres son publicos por diseno y viajan en el navegador. Lo que
   protege los datos son las reglas de Firestore, que estan en
   FIREBASE.md; esconder la apiKey no protege nada.

   Sin argumentos, los vacia: con eso el sitio vuelve a funcionar
   local, que es como esta antes de que exista el proyecto.

   Uso:
     python build-claves.py <apiKey> <projectId> [googleClientId]
     python build-claves.py --vaciar
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--vaciar":
        api = pid = gid = u""
    elif len(args) >= 2:
        api, pid = args[0], args[1]
        gid = args[2] if len(args) > 2 else u""
    else:
        print(__doc__); sys.exit(1)

    for v, nombre in ((api, "apiKey"), (pid, "projectId"), (gid, "googleClientId")):
        if '"' in v:
            print(u"  ABORTA: %s tiene comillas" % nombre); sys.exit(1)
    if api and not api.startswith("AIza"):
        print(u'  OJO: la apiKey de Firebase suele empezar con "AIza". Sigo igual.')
    if gid and not gid.endswith(".apps.googleusercontent.com"):
        print(u'  OJO: el client id suele terminar en ".apps.googleusercontent.com". Sigo igual.')

    n = 0
    for a in sorted(os.listdir(D)):
        if not a.endswith(".html"):
            continue
        p = os.path.join(D, a)
        t = io.open(p, encoding="utf-8").read()
        if "firebaseApiKey" not in t:
            continue
        antes = t
        t = re.sub(r'(firebaseApiKey:\s*")[^"]*(")',    lambda m: m.group(1) + api + m.group(2), t, count=1)
        t = re.sub(r'(firebaseProjectId:\s*")[^"]*(")', lambda m: m.group(1) + pid + m.group(2), t, count=1)
        t = re.sub(r'(googleClientId:\s*")[^"]*(")',    lambda m: m.group(1) + gid + m.group(2), t, count=1)
        if t != antes:
            io.open(p, "w", encoding="utf-8", newline="").write(t)
            n += 1

    if not api:
        print(u"%d paginas con las claves vacias: el sitio funciona local" % n)
    else:
        print(u"%d paginas apuntando a %s%s" % (n, pid, u"" if gid else u" (sin Google)"))
    print(u"\nFalta sellar: python sellar.py")


main()
