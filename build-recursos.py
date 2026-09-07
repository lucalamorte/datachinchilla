# -*- coding: utf-8 -*-
"""Recursos: lo gratis que no es un curso.

   Laws of UX no entra en ninguna ruta y no porque falte una de
   diseno: es una referencia, no un curso. No tiene horas, no tiene
   orden, no se termina. Meterlo como paso de una ruta obligaria a
   inventarle una duracion y un "terminas esto cuando...", que seria
   mentir sobre lo que es.

   Asi que entra una pagina para lo que es gratis, sirve, y se
   consulta en vez de recorrerse. Es tambien donde va a vivir lo que
   dan gratis por ser estudiante, que es de la misma especie.

   Se arma sobre preguntas.html, que ya tiene el arranque minimo. No
   sobre armar.html: copiar una pagina con comportamiento para hacer
   una que no lo tiene fue el error de la vez pasada.

   Uso: python build-recursos.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(D, "preguntas.html")
SALE = os.path.join(D, "recursos.html")

# (titulo, que es, para quien, url, etiqueta)
RECURSOS = [
 (u"Laws of UX",
  u"Los principios que explican por qué una interfaz se entiende o no: "
  u"la ley de Hick sobre cuántas opciones tolera alguien, la de Fitts sobre "
  u"el tamaño de lo que hay que tocar, la carga cognitiva, el efecto de "
  u"posición serial. Cada uno con su ejemplo y su origen.",
  u"Si construís cualquier cosa que use alguien que no seas vos.",
  u"https://lawsofux.com/es/",
  u"Referencia · en español"),
]


def tarjeta(r):
    titulo, que, para, url, etiqueta = r
    return (
        u'      <article class="rec">\n'
        u'        <div class="rec-cab">\n'
        u'          <h3>%s</h3>\n'
        u'          <span class="rec-tag">%s</span>\n'
        u'        </div>\n'
        u'        <p>%s</p>\n'
        u'        <p class="rec-para"><b>Cuándo te sirve.</b> %s</p>\n'
        u'        <a class="rec-ir" href="%s" target="_blank" rel="noopener">Abrirlo '
        u'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        u'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        u'<path d="M5 12h14M13 5l7 7-7 7"/></svg></a>\n'
        u'      </article>' % (titulo, etiqueta, que, para, url))


CUERPO = (
    u'<section class="hero" id="top">\n'
    u'  <div class="wrap">\n'
    u'    <span class="eyebrow">Gratis y no es un curso</span>\n'
    u'    <h1>Cosas que <span class="grad">conviene tener a mano</span></h1>\n'
    u'    <p class="hero-lead">Material gratuito que no entra en ninguna ruta porque no se '
    u'recorre: se consulta. Sin horas, sin orden y sin terminar.</p>\n'
    u'  </div>\n'
    u'</section>\n\n'
    u'<section class="section" id="recursos">\n'
    u'  <div class="wrap">\n'
    u'    <div class="recs">\n' +
    u"\n".join(tarjeta(r) for r in RECURSOS) +
    u'\n    </div>\n'
    u'    <p class="aporte" style="margin-top:18px">\n'
    u'      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    u'stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    u'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg>\n'
    u'      <span><b>¿Tenés uno que debería estar acá?</b> '
    u'<a href="mailto:luca.lamorte@kcc.com?subject=Un%20recurso%20para%20DataChinchilla">Escribime</a>: '
    u'mientras sea gratis y se pueda enlazar, lo miro.</span>\n'
    u'    </p>\n'
    u'  </div>\n'
    u'</section>\n')

CSS = u'''
/* --- Recursos sueltos --------------------------------------------- */
.recs{ display:grid; gap:12px; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); }
.rec{
  display:flex; flex-direction:column; gap:9px; padding:20px;
  background:var(--surface); border:1px solid var(--divider);
  border-radius:var(--r-lg); box-shadow:var(--shadow-sm);
}
.rec-cab{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; }
.rec-cab h3{ margin:0; font-size:17px; letter-spacing:-.01em; }
.rec-tag{
  font-size:10.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
  color:var(--accent-strong); background:var(--accent-soft);
  padding:4px 9px; border-radius:var(--r-pill);
}
.rec p{ margin:0; font-size:13.5px; color:var(--text-2); line-height:1.6; }
.rec-para b{ color:var(--text); }
.rec-ir{
  margin-top:auto; padding-top:6px; display:inline-flex; align-items:center; gap:7px;
  font-size:13px; font-weight:800; color:var(--accent-strong); text-decoration:none;
}
.rec-ir:hover{ gap:10px; }
/* El pedido de material, igual que en las rutas. */
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


def main():
    if not os.path.exists(BASE):
        print(u"  ABORTA: falta preguntas.html, que es la base")
        sys.exit(1)
    t = io.open(BASE, encoding="utf-8").read()

    i = t.index("</header>") + len("</header>")
    j = t.index("<footer")
    t = t[:i] + u"\n\n" + CUERPO + u"\n" + t[j:]

    for viejo, nuevo in [
        (u'<span class="brand-sub">/ Preguntas</span>',
         u'<span class="brand-sub">/ Recursos</span>'),
        (u"<title>Preguntas frecuentes",
         u"<title>Recursos gratis"),
    ]:
        if viejo not in t:
            print(u"  ABORTA: no encuentro %r" % viejo[:40]); sys.exit(1)
        t = t.replace(viejo, nuevo, 1)

    if "\n</style>" not in t:
        print(u"  ABORTA: sin donde poner el estilo"); sys.exit(1)
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    io.open(SALE, "w", encoding="utf-8", newline="").write(t)
    print(u"recursos.html: %d recurso" % len(RECURSOS))


main()
