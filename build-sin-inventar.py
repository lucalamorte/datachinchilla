# -*- coding: utf-8 -*-
u"""No armar una agenda antes de saber quien sos.

   Alguien que nunca conto nada abria la portada y encontraba una
   semana completa: cinco dias de "SQL y Python, mezclados" y bloques
   de "Fundamentos de SQL". Nadie se lo pregunto. Si esa persona
   quiere ser full stack, lo primero que ve el sitio es una semana de
   cosas que no le sirven.

   Salia de dos lugares:

     activas()      si no hay rutas elegidas, devuelve rutaDe(estado.ruta),
                    y estado.ruta arranca en "sqlpy" por defecto.
     quePracticar() sin temas conocidos devuelve "SQL y Python, mezclados".

   Los dos estaban puestos para que la agenda no saliera vacia. Pero
   una agenda llena de algo que no elegiste es peor que una vacia: la
   vacia dice la verdad.

   Ahora armar() avisa `sinRuta` cuando no hay ninguna elegida, y en
   ese caso no hay bloques. La agenda sigue en la portada -sigue
   mostrando los siete dias, que es el marco- y en vez de cursos
   inventados dice que falta armar la ruta y como.

   La practica tambien: recomendar SQL y Python a alguien que no dijo
   a que apunta es adivinar. Cuando sepamos el puesto, la practica
   sale de ahi.

   Uso: python build-sin-inventar.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def cambiar(t, viejo, nuevo, que, archivo):
    n = t.count(viejo)
    if n != 1:
        print(u"  ABORTA en %s: %s x%d, esperaba 1" % (archivo, que, n)); sys.exit(1)
    return t.replace(viejo, nuevo, 1)


# ================================================================ plan.js
P = os.path.join(D, "plan.js")
t = io.open(P, encoding="utf-8").read()
if u"sinRuta" in t:
    print(u"  ya estaba"); sys.exit(1)

t = cambiar(t,
u'''    if(!out.length){
      r = rutaDe(estado.ruta);
      if(r) out.push(r);
    }''',
u'''    /* Y si no elegiste ninguna, ninguna.

       Aca se devolvia rutaDe(estado.ruta), que arranca en "sqlpy" por
       defecto: alguien que nunca conto nada abria la portada y
       encontraba una semana entera de SQL y Python. Si esa persona
       quiere ser full stack, lo primero que ve el sitio es una semana
       de cosas que no le sirven.

       Estaba puesto para que la agenda no saliera vacia. Pero una
       agenda llena de algo que no elegiste es peor que una vacia: la
       vacia dice la verdad. */
    if(!out.length && estado.ruta && rutaElegidaAMano()){
      r = rutaDe(estado.ruta);
      if(r) out.push(r);
    }''',
u"la ruta por defecto", "plan.js")

t = cambiar(t,
u'''  function quePracticar(){''',
u'''  /* Que la ruta del plan la hayas elegido vos y no sea el valor con
     el que nace el estado. Se sabe porque quedo guardada: cargar()
     solo la pisa si venia en lo guardado. */
  function rutaElegidaAMano(){
    var pf = perfil(), crudo = null;
    if(pf && pf.plan) crudo = pf.plan;
    else { try{ crudo = JSON.parse(get(K) || "null"); }catch(e){ crudo = null; } }
    return !!(crudo && crudo.ruta);
  }

  function quePracticar(){''',
u"rutaElegidaAMano", "plan.js")

t = cambiar(t,
u'''  function armar(){
    var lista = activas();
    var ruta = lista[0] || rutaDe(estado.ruta);''',
u'''  function armar(){
    var lista = activas();

    /* Sin ruta elegida no se arma nada. Devuelve la semana vacia -los
       siete dias siguen ahi, que es el marco- y avisa por que, para
       que quien la pinte diga la verdad en vez de mostrar bloques de
       algo que nadie pidio. */
    if(!lista.length){
      var vacia = [], v;
      for(v=0;v<7;v++) vacia.push({ dia: v, bloques: [] });
      return { semana: vacia, ruta: null, rutas: [], practica: 0,
               estudio: 0, repaso: 0, practicar: null, sobran: 0,
               sinRuta: true };
    }

    var ruta = lista[0];''',
u"la salida sin ruta", "plan.js")

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"plan.js: sin ruta elegida, no se inventa la semana")


# ============================================================== index.html
X = os.path.join(D, "index.html")
t = io.open(X, encoding="utf-8").read()

t = cambiar(t,
u'''  Plan.cargar();
  var r = Plan.armar(), hoy = Plan.hoy(), d, i, b;

  var html = "";''',
u'''  Plan.cargar();
  var r = Plan.armar(), hoy = Plan.hoy(), d, i, b;

  /* Sin ruta elegida, la agenda dice que falta elegirla. Antes se
     llenaba sola con SQL y Python, que es lo que trae el estado por
     defecto: una semana entera de cosas que nadie pidio. */
  if(r.sinRuta){
    document.getElementById("hoyCard").innerHTML =
      '<div class="ag-cab"><h3>Tu agenda</h3>' +
        '<span class="ag-sub">Todavía vacía</span></div>' +
      '<div class="ag-nada-aun">' +
        '<p><b>Acá va tu semana, cuando tengas ruta.</b> No te armo una ' +
        'agenda antes de saber a qué apuntas: lo que te sirve a vos no ' +
        'es lo que le sirve a cualquiera.</p>' +
        '<a class="ag-mas" href="cv.html">' + icon("user", 13) +
          'Armar mi ruta</a>' +
      '</div>';
    caja.classList.add("on");
    return;
  }

  var html = "";''',
u"la agenda vacia", "index.html")

t = cambiar(t,
u'''.ag{ list-style:none; margin:0; padding:0; }''',
u'''/* La agenda cuando todavia no hay ruta. Dice que falta y como, en vez
   de llenarse con la ruta que trae el estado por defecto. */
.ag-nada-aun{
  display:flex; flex-direction:column; align-items:flex-start; gap:14px;
  padding:20px 18px 22px;
}
.ag-nada-aun p{ margin:0; font-size:13.5px; color:var(--text-2); max-width:62ch; }
.ag-nada-aun .ag-mas{ margin-left:0; }

.ag{ list-style:none; margin:0; padding:0; }''',
u"el estilo", "index.html")

io.open(X, "w", encoding="utf-8", newline="").write(t)
print(u"index.html: la agenda vacia dice que falta la ruta")
