# -*- coding: utf-8 -*-
u"""De "constancia" a "compartí tu logro".

   La tarjeta estaba dibujada como un diploma: emisor, tipo, nombre, y
   un pie chiquito aclarando que no acredita nada. Eso es un
   certificado que pide disculpas por no serlo.

   Pero terminar una ruta de cuatrocientas horas SI es un logro, y lo
   que uno quiere hacer con un logro es contarlo. El problema no era
   la tarjeta: era que estaba imitando la cosa equivocada.

   Entonces deja de imitar un diploma y pasa a ser lo que es: algo
   para compartir. "Terminé la ruta de dbt", tu nombre, y los botones
   para mandarlo por WhatsApp, LinkedIn o copiarlo.

   Y la aclaracion sube, de pie de pagina a parte del texto. Decir que
   no es un certificado oficial en letra chica al final es la forma
   que tiene un sitio de decirlo sin que se lea. Si el sitio se
   sostiene en que lo que dice es verdad, esto va a la vista.

   LOS BOTONES, por que esos y no mas:

     WhatsApp   es por donde la gente comparte de verdad, y acepta
                texto armado.
     LinkedIn   es donde esto suma, y solo acepta una URL: el texto lo
                saca de las etiquetas og de la pagina, que ya estan.
     Copiar     para cualquier otro lado, sin depender de nadie.

   No va Twitter/X: compartir una ruta de estudio ahi no es lo que
   hace nadie, y un boton que no se usa es ruido.

   Uso: python build-compartir.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))

CSS = u'''
/* --- Compartir el logro ----------------------------------------- */
/* La tarjeta era un diploma que pedia disculpas por no serlo: emisor,
   tipo, y un pie chiquito aclarando que no acredita nada. Terminar
   una ruta es un logro de verdad; lo que uno quiere con un logro es
   contarlo, no enmarcarlo. */
.cert-compartir{
  display:flex; flex-wrap:wrap; gap:9px; justify-content:center;
  margin-top:18px;
}
.cert-compartir a, .cert-compartir button{
  display:inline-flex; align-items:center; gap:7px;
  padding:9px 14px; border-radius:var(--r-pill);
  font-size:13px; font-weight:700; font-family:inherit;
  text-decoration:none; cursor:pointer;
  color:var(--text); background:var(--surface-2);
  border:1px solid var(--divider);
}
.cert-compartir a:hover, .cert-compartir button:hover{ border-color:var(--accent); }
.cert-compartir svg{ width:15px; height:15px; }
/* El aviso sube de pie de pagina a parte del texto: decir en letra
   chica que esto no acredita nada es la forma de decirlo sin que se
   lea. */
.cert-aviso{
  position:relative; margin:14px 0 0; font-size:12px; line-height:1.5;
  color:var(--text-3);
}
'''


def bloque(clave, nombre_ruta):
    u"""La tarjeta nueva. El texto de arriba lo arma cada pagina."""
    return (
u'''          <p class="cert-nombre" data-cert-nombre>Tu nombre</p>
          <p class="cert-linea" data-cert-linea>terminó la ruta de <b>%(nombre)s</b> en DataChinchilla.</p>
          <p class="cert-aviso">No es un certificado ni acredita conocimientos: lo emito yo
            y dice lo que hiciste. Las credenciales de verdad las dejan los cursos, y en el
            mapa se avisa cuáles.</p>
        </div>
        <div class="cert-compartir">
          <a data-compartir="wa" href="#" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.4 0-1 .1-3.3-.9-2.8-1.2-4.5-4-4.6-4.2-.1-.2-1-1.4-1-2.6s.6-1.8.9-2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .6l-.3.5-.3.3c-.1.1-.3.3-.1.6.1.3.6 1.1 1.4 1.8 1 .9 1.8 1.1 2 1.2.3.1.4.1.6-.1l.8-1c.2-.2.4-.2.6-.1l1.8.9c.2.1.4.2.5.3 0 .1 0 .6-.2 1.2z"/></svg>
            WhatsApp</a>
          <a data-compartir="in" href="#" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.1 21 14.2V21h-4v-6c0-1.43-.03-3.27-2-3.27-2 0-2.3 1.56-2.3 3.17V21H9z"/></svg>
            LinkedIn</a>
          <button type="button" data-compartir="copiar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>
            Copiar</button>
        </div>''' % {"nombre": nombre_ruta})


JS = u'''
/* Los botones de compartir.

   El texto se arma en el momento porque el nombre sale del perfil y
   puede cambiar sin recargar: dejarlo escrito en el HTML lo dejaba
   diciendo "Tu nombre" a quien acababa de entrar.

   LinkedIn solo acepta una URL -el texto lo saca de las etiquetas og
   de esta pagina, que ya estan puestas-. WhatsApp acepta el texto
   armado, que es lo que hace que ahi se lea bien. */
(function(){
  "use strict";
  function texto(){
    var n = document.querySelector("[data-cert-nombre]");
    var l = document.querySelector("[data-cert-linea]");
    var quien = (n && n.textContent || "").trim();
    /* Sin el punto final: la frase sigue con el signo de cierre y
       despues el link, y "DataChinchilla. ¡" quedaba raro. */
    var que = (l && l.textContent || "").trim().replace(/\.\s*$/, "");
    if(!quien || quien === "Tu nombre"){
      return "¡Terminé " + que.replace(/^terminó /, "") + "!";
    }
    return "¡" + quien + " " + que + "!";
  }
  function url(){ return location.origin + location.pathname; }

  function enganchar(){
    var wa = document.querySelector('[data-compartir="wa"]');
    var inn = document.querySelector('[data-compartir="in"]');
    var cp = document.querySelector('[data-compartir="copiar"]');
    if(wa) wa.setAttribute("href",
      "https://wa.me/?text=" + encodeURIComponent(texto() + " " + url()));
    if(inn) inn.setAttribute("href",
      "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url()));
    if(cp && !cp.dataset.listo){
      cp.dataset.listo = "1";
      cp.addEventListener("click", function(){
        var t = texto() + " " + url();
        var ok = function(){
          var antes = cp.lastChild.nodeValue;
          cp.lastChild.nodeValue = " Copiado";
          window.setTimeout(function(){ cp.lastChild.nodeValue = antes; }, 1600);
        };
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(t).then(ok, function(){});
        }else{
          /* Sin portapapeles -http sin cifrar, navegadores viejos- se
             selecciona para que al menos se pueda copiar a mano. */
          var a = document.createElement("textarea");
          a.value = t; document.body.appendChild(a); a.select();
          try{ document.execCommand("copy"); ok(); }catch(e){}
          a.remove();
        }
      });
    }
  }
  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", function(){ window.setTimeout(enganchar, 140); });
  }else{
    window.setTimeout(enganchar, 140);
  }
  /* Y de nuevo cuando cambia el nombre: el perfil puede llegar
     despues, o podes entrar sin recargar. */
  document.addEventListener("click", function(){ window.setTimeout(enganchar, 300); });
})();
'''

n = 0
for a in sorted(os.listdir(D)):
    if not a.endswith(".html"):
        continue
    p = os.path.join(D, a)
    t = io.open(p, encoding="utf-8").read()
    # Solo las que tienen la tarjeta, no las que solo heredaron su
    # CSS: cv.html define .cert-linea y no dibuja ninguna.
    if u'<p class="cert-linea">' not in t:
        continue
    if u"cert-compartir" in t:
        print(u"  %s: ya estaba" % a); continue

    # el nombre de la ruta sale de la propia linea que ya estaba
    m = re.search(r'<p class="cert-linea">(.*?)</p>', t, re.S)
    if not m:
        print(u"  ABORTA en %s: no encuentro la linea" % a); sys.exit(1)
    mn = re.search(r"<b>(.*?)</b>", m.group(1))
    nombre = mn.group(1) if mn else u"esta ruta"

    # 1. la tarjeta
    v = re.search(r'          <p class="cert-nombre" data-cert-nombre>Tu nombre</p>\n'
                  r'          <p class="cert-linea">.*?</p>\n'
                  r'          <p class="cert-pie">.*?</p>\n'
                  r'        </div>', t, re.S)
    if not v:
        print(u"  ABORTA en %s: la tarjeta no tiene la forma esperada" % a); sys.exit(1)
    t = t[:v.start()] + bloque(a, nombre) + t[v.end():]

    # 2. el titulo de la seccion
    t = t.replace(u"<h2>La constancia de esta ruta</h2>",
                  u"<h2>Cuando termines, contalo</h2>", 1)
    t = t.replace(u"Esta constancia la emito yo y solo dice que recorriste la guía. "
                  u"Los cursos que dejan credencial propia lo avisan en su paso del mapa.",
                  u"Terminar esta ruta es un logro y merece contarse. No es un "
                  u"certificado: es lo que hiciste, dicho por el sitio donde lo hiciste. "
                  u"Los cursos que sí dejan credencial propia lo avisan en su paso del mapa.", 1)
    t = t.replace(u'<span class="cert-tag">De esta guía</span>',
                  u'<span class="cert-tag">Para compartir</span>', 1)

    # 3. el estilo y el script
    k = t.index(u"</style>")
    t = t[:k] + CSS + t[k:]
    k2 = t.rindex(u"</script>")
    t = t[:k2 + len(u"</script>")] + u"\n<script>" + JS + u"</script>" + t[k2 + len(u"</script>"):]

    io.open(p, "w", encoding="utf-8", newline="").write(t)
    n += 1

print(u"%d rutas con el logro para compartir" % n)
