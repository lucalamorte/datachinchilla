# -*- coding: utf-8 -*-
"""Mete el onboarding en la portada.

   La portada pasa a tener dos caras y muestra una sola:

   - Si no hiciste el onboarding, lo ves a el. Cuatro pasos: donde
     estas, a donde vas, cuanto tiempo tenes, y listo.
   - Si ya lo hiciste, ves tu estado: que toca hoy, tus rutas activas
     y como venis.

   El catalogo queda abajo en los dos casos, para el que solo quiere
   mirar. La salida esta pero es chica: guiar no es encerrar.
"""
import io, sys

D = u"C:/Users/Luca/Desktop/snowflake path/"


def uno(t, a, b, q):
    if t.count(a) != 1:
        print("  ABORTA [%s]: %d veces" % (q, t.count(a)))
        sys.exit(1)
    return t.replace(a, b)


t = io.open(D + u"index.html", encoding="utf-8").read()

# ------------------------------------------------------------------ CSS
CSS = u"""
/* --- El onboarding: la unica entrada ---------------------------- */
.onb{ display:none; }
.onb.on{ display:block; }
.onb-caja{
  background:var(--surface); border:1px solid var(--divider);
  border-radius:var(--r-xl); box-shadow:var(--shadow-md);
  overflow:hidden; margin-top:26px;
}
.onb-top{
  display:flex; align-items:center; gap:14px;
  padding:15px 22px; border-bottom:1px solid var(--divider-soft);
  background:var(--surface-sunk);
}
.onb-pasos{ display:flex; gap:7px; flex:1; }
.onb-pip{
  flex:1; height:4px; border-radius:2px; background:var(--divider);
  transition:background var(--dur) ease;
}
.onb-pip.on{ background:var(--accent); }
.onb-nro{ font-size:11.5px; font-weight:800; color:var(--text-3);
  letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }
.onb-cuerpo{ padding:26px 22px 22px; }
.onb-h{ font-size:clamp(21px,3vw,27px); margin:0 0 7px; letter-spacing:-.02em; }
.onb-sub{ font-size:14.5px; color:var(--text-2); margin:0 0 20px; line-height:1.6; }
.onb-pie{
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  padding:15px 22px; border-top:1px solid var(--divider-soft);
  background:var(--surface-sunk);
}
.onb-pie .der{ margin-left:auto; display:flex; gap:10px; align-items:center; }
.onb-atras{
  background:none; border:0; padding:8px 4px; cursor:pointer;
  font:inherit; font-size:13px; color:var(--text-3);
}
.onb-atras:hover{ color:var(--text); }
.onb-salida{ font-size:12.5px; color:var(--text-3); text-decoration:none; }
.onb-salida:hover{ color:var(--accent); text-decoration:underline; }

/* Las dos formas de contar donde estas */
.onb-vias{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:12px; }
.via{
  text-align:left; padding:17px 18px; border-radius:var(--r-lg); cursor:pointer;
  background:var(--surface-2); border:1.5px solid var(--divider);
  font:inherit; color:inherit;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.via:hover{ border-color:var(--accent-line); }
.via[aria-pressed="true"]{ border-color:var(--accent); background:var(--accent-soft); }
.via b{ display:block; font-size:15px; margin-bottom:4px; }
.via span{ display:block; font-size:12.5px; color:var(--text-2); line-height:1.5; }

/* Las preguntas */
.preg{ margin-bottom:22px; }
.preg > b{ display:block; font-size:15.5px; margin-bottom:3px; }
.preg > i{ display:block; font-style:normal; font-size:12.5px;
  color:var(--text-3); margin-bottom:10px; }
.preg-ops{ display:grid; gap:7px; }
.preg-op{
  text-align:left; padding:11px 14px; border-radius:var(--r-md); cursor:pointer;
  background:var(--surface-2); border:1px solid var(--divider);
  font:inherit; font-size:13.5px; color:inherit;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.preg-op:hover{ border-color:var(--accent-line); }
.preg-op[aria-pressed="true"]{
  border-color:var(--accent); background:var(--accent-soft);
  color:var(--accent-strong); font-weight:650;
}

/* Cuanto tiempo: dias, franja y horas */
.campo{ margin-bottom:24px; }
.campo > label{ display:block; font-size:11.5px; font-weight:800;
  letter-spacing:.08em; text-transform:uppercase; color:var(--text-3);
  margin-bottom:10px; }
.dias-fila{ display:flex; gap:7px; flex-wrap:wrap; }
.dia-b{
  flex:1 1 0; min-width:44px; padding:11px 4px; border-radius:var(--r-md);
  background:var(--surface-2); border:1px solid var(--divider); cursor:pointer;
  font:inherit; font-size:12.5px; font-weight:700; color:var(--text-2);
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.dia-b[aria-pressed="true"]{
  background:var(--accent-soft); border-color:var(--accent); color:var(--accent-strong);
}
.franjas{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:8px; }
.franja-b{
  text-align:left; padding:12px 14px; border-radius:var(--r-md); cursor:pointer;
  background:var(--surface-2); border:1px solid var(--divider);
  font:inherit; color:inherit;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.franja-b[aria-pressed="true"]{ border-color:var(--accent); background:var(--accent-soft); }
.franja-b b{ display:block; font-size:13.5px; margin-bottom:2px; }
.franja-b span{ font-size:11.5px; color:var(--text-3); }

/* Las horas van con barra y no con lista: media hora es una opcion
   valida y una lista que empieza en tres deja afuera a quien tiene
   una. */
.horas-caja{ display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
.horas-val{ font-size:26px; font-weight:800; letter-spacing:-.02em;
  min-width:118px; font-variant-numeric:tabular-nums; }
.horas-val small{ font-size:13px; font-weight:600; color:var(--text-3); }
#onbHoras{ flex:1 1 220px; accent-color:var(--accent); height:26px; }
.horas-nota{ flex:1 1 100%; font-size:12.5px; color:var(--text-3); line-height:1.55; }

/* El cierre: rutas activas */
.act-lista{ display:grid; gap:8px; margin-bottom:8px; }
.act{
  display:flex; align-items:center; gap:12px; text-align:left;
  padding:12px 14px; border-radius:var(--r-md); cursor:pointer;
  background:var(--surface-2); border:1px solid var(--divider);
  font:inherit; color:inherit;
  transition:border-color var(--dur) ease, background var(--dur) ease;
}
.act[aria-pressed="true"]{ border-color:var(--accent); background:var(--accent-soft); }
.act .tick-caja{
  width:19px; height:19px; flex:none; border-radius:5px;
  border:1.5px solid var(--divider); display:grid; place-items:center;
  color:transparent;
}
.act[aria-pressed="true"] .tick-caja{
  background:var(--accent); border-color:var(--accent); color:var(--warm-ink);
}
.act .n{ flex:1; font-size:14px; font-weight:650; }
.act .c{ font-size:12px; color:var(--text-3); }

/* --- Tu estado, cuando el onboarding ya esta hecho -------------- */
.estado{ display:none; }
.estado.on{ display:block; }
.estado-cab{
  display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:16px;
}
.estado-cab h2{ font-size:clamp(22px,3vw,30px); margin:0; letter-spacing:-.02em; }
.estado-cab .cambiar{
  margin-left:auto; background:none; border:0; cursor:pointer;
  font:inherit; font-size:12.5px; color:var(--text-3); text-decoration:underline;
}
.estado-cab .cambiar:hover{ color:var(--accent); }
.estado-rutas{ display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
.estado-ruta{
  display:inline-flex; align-items:center; gap:8px;
  padding:7px 13px; border-radius:var(--r-pill);
  background:var(--surface); border:1px solid var(--divider);
  font-size:13px; font-weight:650; color:inherit; text-decoration:none;
}
.estado-ruta:hover{ border-color:var(--accent); }
.estado-ruta .p{ font-size:11.5px; color:var(--text-3); font-weight:500; }
"""
t = uno(t, u"\n/* Las tres puertas del hero.", CSS + u"\n/* Las tres puertas del hero.", "css")

# ----------------------------------------------------------------- HTML
HTML = u"""
<section class="section onb" id="onb">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Empecemos por acá</p>
      <h2>Antes de mostrarte quince rutas</h2>
      <p>Cuatro respuestas y te queda armado qué estudiar y cuándo. Se cambia después las veces que quieras.</p>
    </div>

    <div class="onb-caja">
      <div class="onb-top">
        <div class="onb-pasos" id="onbPips"></div>
        <span class="onb-nro" id="onbNro"></span>
      </div>
      <div class="onb-cuerpo" id="onbCuerpo"></div>
      <div class="onb-pie">
        <button class="onb-atras" type="button" id="onbAtras">Atrás</button>
        <a class="onb-salida" href="#rutas" id="onbSalida">Solo quiero ver el catálogo</a>
        <span class="der">
          <button class="btn-primary" type="button" id="onbSigue">
            <span class="stack"><span class="verb">Seguir</span><span class="dest" id="onbSigueTxt">Continuar</span></span>
          </button>
        </span>
      </div>
    </div>
  </div>
</section>

<section class="section estado" id="estado">
  <div class="wrap">
    <div class="estado-cab">
      <h2 id="estadoTitulo"></h2>
      <button class="cambiar" type="button" id="onbEditar">Cambiar mis datos</button>
    </div>
    <p id="estadoSub" class="hero-lead" style="margin:0"></p>
    <div class="estado-rutas" id="estadoRutas"></div>
  </div>
</section>
"""
t = uno(t, u'\n<section class="section hoy" id="hoy">',
        HTML + u'\n<section class="section hoy" id="hoy">', "html")

# -------------------------------------------------------------- scripts
t = uno(t, u'<script src="plan.js',
        u'<script src="temas.js"></script>\n'
        u'<script src="cv.js"></script>\n'
        u'<script src="onboarding.js"></script>\n'
        u'<script src="plan.js', "scripts")

io.open(D + u"index.html", "w", encoding="utf-8", newline="").write(t)
print(u"index.html: sección del onboarding, estado y scripts")
