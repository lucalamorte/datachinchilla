# -*- coding: utf-8 -*-
"""Pasar de ejercicio sin entrar a la practica.

   Las dos tarjetas de la portada muestran siempre el siguiente sin
   hacer. Si ese no te convence hoy, la unica salida era entrar al
   listado completo.

   Entran dos flechas y un contador. Y con ellas aparece un problema
   que antes no existia: "Lo resolvi" marcaba lo que devolviera
   Practica.siguiente(), o sea el primero pendiente. Navegando, eso ya
   no es el que estas viendo: marcarias otro. Ahora marca el que esta
   en pantalla.

   El indice no se guarda: es de esta visita. Al recargar vuelve al
   primero pendiente, que es lo que uno espera de "la practica de
   hoy".

   Uso: python build-flechas.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "index.html")

VIEJO_INI = u"function renderRetos(){"
VIEJO_FIN = u"  var bt = cont.querySelectorAll(\"[data-hecho]\"), j;"

NUEVO = u'''/* Por que ejercicio va cada banco en esta visita. No se guarda: al
   recargar vuelve al primero pendiente, que es lo que uno espera de
   "la practica de hoy". */
var retoEn = {};

function renderRetos(){
  var cont = document.getElementById("retos");
  if(!cont || typeof Practica === "undefined") return;

  var bs = Practica.bancos(), h = "", i;
  for(i=0;i<bs.length;i++){
    var b = bs[i];
    var lleva = Practica.hoyCuantos(b.id), listo = lleva >= Practica.POR_DIA;
    var av = Practica.avance(b.id);

    /* Los que quedan, en orden. Se calcula aca y no en practica.js
       porque es lo unico que hace falta: la lista de pendientes. */
    var pend = [], k;
    for(k=0;k<b.items.length;k++){
      if(!Practica.hecho(b.id, b.items[k])) pend.push(b.items[k]);
    }
    var en = retoEn[b.id] || 0;
    if(en >= pend.length) en = 0;
    retoEn[b.id] = en;
    var s = pend.length ? pend[en] : null;

    h += '<div class="reto-c' + (listo ? " ok" : "") + '">' +
      '<div class="reto-top">' +
        '<span class="lang">' + esc(b.lang || b.nombre) + '</span>' +
        '<span class="cuenta">' + lleva + " de " + Practica.POR_DIA +
        (listo ? " \\u00b7 hecho" : " hoy") + '</span>' +
      '</div>' +
      (s
        ? '<a class="reto-p" href="' + esc(s.u) + '" target="_blank" rel="noopener">' +
            '<span class="t">' + (s.n ? s.n + ". " : "") + esc(s.t) + '</span>' +
            '<span class="d ' + s.d + '">' + s.d + '</span>' +
            '<span class="ir">' + icon("open", 13) + '</span></a>'
        : '<p class="reto-fin">Los hiciste todos.</p>') +
      '<div class="reto-pie">' +
        '<button class="reto-hecho" type="button" data-hecho="' + b.id + '"' +
          (s ? "" : " disabled") + '>' + icon("check", 12) + 'Lo resolvi</button>' +
        (pend.length > 1
          ? '<span class="reto-nav">' +
              '<button class="reto-fl" type="button" data-ir="-1" data-banco="' + b.id + '" ' +
                'aria-label="El anterior"' + (en <= 0 ? " disabled" : "") + '>' +
                '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>' +
              '<span class="reto-n">' + (en + 1) + " de " + pend.length + '</span>' +
              '<button class="reto-fl" type="button" data-ir="1" data-banco="' + b.id + '" ' +
                'aria-label="El siguiente"' + (en >= pend.length - 1 ? " disabled" : "") + '>' +
                '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button>' +
            '</span>'
          : '<span class="reto-av">' + av.hechos + " de " + av.total + '</span>') +
      '</div></div>';
  }
  cont.innerHTML = h;

  var tot = 0, z;
  for(z=0;z<bs.length;z++) tot += bs[z].items.length;
  var n = document.getElementById("cuantosProb");
  if(n) n.textContent = tot;

  /* Las flechas mueven el indice de su banco y vuelven a pintar. */
  var fl = cont.querySelectorAll("[data-ir]"), q;
  for(q=0;q<fl.length;q++){
    fl[q].addEventListener("click", function(){
      var id = this.getAttribute("data-banco");
      retoEn[id] = (retoEn[id] || 0) + parseInt(this.getAttribute("data-ir"), 10);
      if(retoEn[id] < 0) retoEn[id] = 0;
      renderRetos();
    });
  }

'''


def main():
    t = io.open(P, encoding="utf-8").read()
    if "retoEn" in t:
        print(u"  ya estaba puesto"); sys.exit(1)
    i = t.index(VIEJO_INI)
    j = t.index(VIEJO_FIN)
    t = t[:i] + NUEVO + t[j:]

    # "Lo resolvi" tiene que marcar el que esta en pantalla, no el
    # primero pendiente: navegando ya no son el mismo.
    v = u'''      var id = this.getAttribute("data-hecho");
      var s = Practica.siguiente(id);
      if(!s) return;'''
    n = u'''      var id = this.getAttribute("data-hecho");
      /* El que esta en pantalla, no el primero pendiente: con las
         flechas ya no son el mismo, y marcar otro seria mentirle a
         quien acaba de resolver este. */
      var bb = Practica.bancoDe(id), pp = [], w;
      for(w=0;w<bb.items.length;w++){
        if(!Practica.hecho(id, bb.items[w])) pp.push(bb.items[w]);
      }
      var s = pp[retoEn[id] || 0] || null;
      if(!s) return;'''
    if t.count(v) != 1:
        print(u"  ABORTA: el handler de marcar aparece %d veces" % t.count(v)); sys.exit(1)
    t = t.replace(v, n, 1)

    CSS = u'''
/* Las flechas para pasar de ejercicio sin entrar al listado. */
.reto-nav{ margin-left:auto; display:inline-flex; align-items:center; gap:6px; }
.reto-fl{
  display:grid; place-items:center; width:26px; height:26px; padding:0;
  border:1px solid var(--divider); border-radius:8px;
  background:var(--surface); color:var(--text-3); cursor:pointer;
}
.reto-fl:hover:not(:disabled){ border-color:var(--accent); color:var(--accent); }
.reto-fl:disabled{ opacity:.35; cursor:default; }
.reto-n{
  font-size:11px; font-weight:700; color:var(--text-3);
  font-variant-numeric:tabular-nums; min-width:6ch; text-align:center;
}
'''
    t = t.replace("\n</style>", CSS + "\n</style>", 1)

    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print(u"index.html: flechas en la practica del dia")


main()
