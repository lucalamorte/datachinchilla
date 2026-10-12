# -*- coding: utf-8 -*-
u"""Que la barra se entere de que entraste. Y de que saliste.

   Entrabas y el chip de arriba seguia diciendo "Entrar" hasta
   recargar. No era un lugar: era el mismo olvido en tres momentos
   distintos, que son los tres en los que cambia la sesion.

   1. ENTRAR CON MAIL. El callback onEntrar repintaba el modal
      -renderAccount- pero no la barra -paintAccount-. Las veintidos
      paginas de ruta si lo llamaban; las ocho de la aplicacion no.
      Nadie lo noto porque en las rutas andaba.

   2. VOLVER DE GOOGLE. captureHash es asincrono: canjea el token
      contra Firebase y eso tarda. El init llamaba a refreshSes() y
      paintAccount() en la linea siguiente, o sea antes de que la
      sesion existiera. Pintaba el estado viejo y nadie volvia a
      mirar. Esto no se arreglaba agregando una llamada mas: habia
      que esperar la promesa.

   3. SALIR. Se borraba la sesion y se repintaba el modal, no la
      barra: cerrabas sesion y tu nombre seguia arriba.

   Los tres son la misma pregunta mal contestada: quien repinta la
   barra cuando cambia la sesion. Ahora, los tres.

   Uso: python build-repintar.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))


def bloque_onEntrar(t, desde):
    u"""El cuerpo de un onEntrar, contando llaves: los cuerpos tienen
       llaves adentro y cortar con una expresion regular agarraba de
       menos en unas paginas y de mas en otras."""
    i = t.index("{", desde)
    nivel, j = 0, i
    while j < len(t):
        if t[j] == "{": nivel += 1
        elif t[j] == "}":
            nivel -= 1
            if nivel == 0: return i, j
        j += 1
    return None, None


n_entrar = n_hash = n_salir = 0

for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if "paintAccount" not in t:
        continue
    antes = t

    # ---------------------------------------------------- 1. entrar
    pos = 0
    while True:
        k = t.find("onEntrar: function(", pos)
        if k < 0: break
        i, j = bloque_onEntrar(t, k)
        if i is None: break
        cuerpo = t[i:j+1]
        if "paintAccount" not in cuerpo:
            nuevo = cuerpo[:-1].rstrip()
            if not nuevo.endswith(";"): nuevo += ";"
            nuevo += ("\n      /* Y la barra, que es donde se ve si entraste. Repintar\n"
                      "         solo el modal dejaba el chip diciendo \"Entrar\" con la\n"
                      "         sesion ya abierta, hasta recargar. */\n"
                      "      paintAccount();\n    }")
            t = t[:i] + nuevo + t[j+1:]
            n_entrar += 1
            pos = i + len(nuevo)
        else:
            pos = j + 1

    # ------------------------------------------------- 2. de Google
    v = u'''  PathSync.captureHash(function(m){ toast("El link del mail no sirvió: " + m); });
  refreshSes();'''
    if v in t:
        t = t.replace(v,
u'''  /* captureHash es asincrono: canjea el token de Google contra
     Firebase y eso tarda. Lo de abajo corria en la linea siguiente,
     o sea antes de que la sesion existiera, asi que pintaba el estado
     viejo y nadie volvia a mirar. Por eso tambien se repinta cuando
     la promesa termina. */
  PathSync.captureHash(function(m){ toast("El link del mail no sirvió: " + m); })
    .then(function(){ refreshSes(); paintAccount(); });
  refreshSes();''', 1)
        n_hash += 1

    # --------------------------------------------------- 3. salir
    v2 = u'''    PathSync.signOut();
    refreshSes();
    renderAccount("");'''
    if v2 in t:
        t = t.replace(v2,
u'''    PathSync.signOut();
    refreshSes();
    renderAccount("");
    /* Y la barra: sin esto cerrabas sesion y tu nombre seguia arriba. */
    paintAccount();''', 1)
        n_salir += 1

    if t != antes:
        io.open(p, "w", encoding="utf-8", newline="").write(t)

print(u"entrar: %d callbacks | de Google: %d paginas | salir: %d paginas"
      % (n_entrar, n_hash, n_salir))
