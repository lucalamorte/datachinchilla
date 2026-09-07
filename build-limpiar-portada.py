# -*- coding: utf-8 -*-
"""Sacar de la portada lo que sobra, y pedir material desde las rutas.

   Tres cortes y un agregado:

   1. "Las bloqueadas todavia no existen. Escribeme cual te sirve y
      armo esa primero." Se va. Habla de rutas que no existen, o sea
      de lo que el sitio NO tiene, justo despues de mostrar dieciseis
      que si tiene.

   2. La banda "Ya sabes la mitad de esto?" se va entera. Lleva al
      mismo lado que la tarjeta "Armala a mano" de arriba: es la
      misma accion dos veces en la misma pagina. De las dos, la de
      arriba forma parte de las tres puertas, que son una estructura
      pensada; esta es un agregado. Y de paso se resuelve que el
      texto no se entendia: no hay texto que arreglar.

      Lo que esa banda decia bien -que sirve si ya sabes parte- pasa
      a la tarjeta de arriba, que es donde se decide.

   3. "Todas las rutas" y "Armar la mia" salen del pie. Si alguien
      tiene que llegar al pie para encontrar las dos cosas
      principales, el problema es la pagina, no el pie.

   4. Y entra, en cada ruta, el pedido de material. Va en las rutas y
      no en la portada porque es donde alguien ya vio lo que hay de un
      tema y puede darse cuenta de que falta algo.

   Uso: python build-limpiar-portada.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
CORREO = "luca.lamorte@kcc.com"


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r aparece %d veces, esperaba %d"
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-22s %d cambios" % (archivo, len(cambios)))


PEDIR_VIEJO = u'''    <p class="pedir">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg>
      <span>Las bloqueadas todavía no existen. <a href="mailto:luca.lamorte@kcc.com?subject=Qu%C3%A9%20ruta%20armar%20primero">Escríbeme cuál te sirve</a> y armo esa primero.</span>
    </p>
'''

BANDA_VIEJA = u'''<section class="section" id="armar">
  <div class="wrap">
    <div class="armar-band">
      <span class="ico">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M4 6h7M4 12h11M4 18h6"/><path d="M18 9v10M14.5 15.5L18 19l3.5-3.5"/>
        </svg>
      </span>
      <div>
        <h2>¿Ya sabes la mitad de esto?</h2>
        <p>El armador abre todas las rutas en piezas sueltas: eliges, ordenas y te queda tu camino, con su avance y un link para compartirlo.</p>
      </div>
      <a class="btn-done" href="armar.html">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        Armar la mía
      </a>
    </div>
  </div>
</section>
'''

parchar("index.html", [
 (PEDIR_VIEJO, u"", 1),
 (BANDA_VIEJA, u"", 1),

 # el pie, sin las dos que ya estan arriba
 (u'''      <a href="#rutas">Todas las rutas</a>
      <a href="armar.html">Armar la mía</a>
''', u"", 1),

 # y lo que la banda decia bien, en la tarjeta de arriba
 (u"'<span>Eliges los niveles que quieras de cualquier ruta y los ordenas tú.</span></span>' +",
  u"'<span>Si ya sabes parte, elige sueltos los niveles que te faltan de cualquier ruta y los ordenas tú.</span></span>' +", 1),
])

# ------------------------------------------------- el pedido, en cada ruta
PEDIDO = u'''
<section class="section" id="aportar">
  <div class="wrap">
    <p class="aporte">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg>
      <span><b>¿Conoces algo gratis que debería estar acá?</b>
      <a href="mailto:%s?subject=Material%%20para%%20DataChinchilla">Escríbeme y lo miro</a>: un curso, un canal, un dataset o un apunte tuyo, mientras sea gratis y se pueda enlazar. También si encontraste un link caído.</span>
    </p>
  </div>
</section>
''' % CORREO

CSS_PEDIDO = u'''
/* El pedido de material, al final de cada ruta. Va tenue: es una
   invitacion, no una accion del recorrido. */
.aporte{
  display:flex; gap:11px; align-items:flex-start;
  margin:0; padding:16px 18px;
  border:1px dashed var(--divider); border-radius:var(--r-lg);
  font-size:13.5px; color:var(--text-2); line-height:1.6;
}
.aporte > svg{ flex:none; margin-top:2px; color:var(--text-3); }
.aporte b{ color:var(--text); font-weight:800; }
.aporte a{ color:var(--accent-strong); font-weight:700; }
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html") or a.startswith("_"):
        continue
    if a in ("index.html", "og.html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    if 'id="aportar"' in t or "<footer" not in t:
        continue
    i = t.index("<footer")
    ini = t.rfind("\n", 0, i)
    t = t[:ini] + u"\n" + PEDIDO + t[ini:]
    if ".aporte{" not in t:
        t = t.replace("\n</style>", CSS_PEDIDO + "\n</style>", 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%-22s %d paginas con el pedido de material" % ("las rutas", n))
