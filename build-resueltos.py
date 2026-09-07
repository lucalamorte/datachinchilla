# -*- coding: utf-8 -*-
u"""Ver los que ya resolviste, y decir bien lo del CV.

   Dos cosas sueltas.

   1. En la practica habia dos filtros: "Por hacer" y "Todos". Faltaba
      el tercero, que es el que uno busca cuando quiere repasar: los
      que ya resolvio. Con "Todos" aparecen mezclados con los
      cuarenta que faltan, asi que para encontrar uno hecho habia que
      ir a ojo.

      Los tres llevan su numero, igual que los del catalogo: un filtro
      que no dice cuanto hay adentro obliga a apretarlo para saber si
      valia la pena.

   2. "Se lee aca, en tu navegador. Tu CV no sale de esta pestana."
      Suena a explicacion casera para algo que es una promesa sobre
      los datos de alguien. Se dice como corresponde, y sin mentir:
      el texto se guarda en el navegador -si no, habria que pegarlo
      de nuevo cada vez-, pero no se sube a ningun lado. Lo comprobe:
      cv.html no llama a upsertRow, y lo unico que viaja al servidor
      son las marcas de avance de las rutas y el nombre.

   Uso: python build-resueltos.py
"""
import io, os, sys

D = os.path.dirname(os.path.abspath(__file__))


def parchar(archivo, cambios):
    p = os.path.join(D, archivo)
    t = io.open(p, encoding="utf-8").read()
    for viejo, nuevo, veces in cambios:
        n = t.count(viejo)
        if n != veces:
            print(u"  ABORTA en %s: %r x%d, esperaba %d"
                  % (archivo, viejo[:46], n, veces))
            sys.exit(1)
        t = t.replace(viejo, nuevo)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print(u"%-18s %d cambios" % (archivo, len(cambios)))


# ------------------------------------------------ 1. el filtro que faltaba
parchar("practica.html", [
 (u'''    '<button class="filtro" type="button" data-est="pendientes" ' +
      'aria-pressed="' + (fEstado === "pendientes") + '">Por hacer</button>' +
    '<button class="filtro" type="button" data-est="todo" ' +
      'aria-pressed="' + (fEstado === "todo") + '">Todos</button>';''',
  u'''    /* Los tres estados, con su numero. Faltaba el de los resueltos,
       que es el que uno busca para repasar: con "Todos" quedan
       mezclados con los que faltan y hay que buscarlos a ojo.

       El numero va porque un filtro que no dice cuanto hay adentro
       obliga a apretarlo para saber si valia la pena. */
    (function(){
      var av = Practica.avance(bancoActual);
      var pend = av.total - av.hechos;
      return '<button class="filtro" type="button" data-est="pendientes" ' +
          'aria-pressed="' + (fEstado === "pendientes") + '">Por hacer ' +
          '<span class="fn">' + pend + '</span></button>' +
        '<button class="filtro" type="button" data-est="hechos" ' +
          'aria-pressed="' + (fEstado === "hechos") + '">Resueltos ' +
          '<span class="fn">' + av.hechos + '</span></button>' +
        '<button class="filtro" type="button" data-est="todo" ' +
          'aria-pressed="' + (fEstado === "todo") + '">Todos ' +
          '<span class="fn">' + av.total + '</span></button>';
    })();''', 1),

 (u'''  if(fEstado === "pendientes" && Practica.hecho(bancoActual, x)) return false;''',
  u'''  if(fEstado === "pendientes" && Practica.hecho(bancoActual, x)) return false;
  if(fEstado === "hechos" && !Practica.hecho(bancoActual, x)) return false;''', 1),

 # el vacio: ahora hay un tercer caso, y decia el de otro filtro
 (u'''    var todos = Practica.avance(bancoActual);
    var listo = fEstado === "pendientes" && todos.hechos >= todos.total;
    c.innerHTML = "<li>" + (listo
      ? '<div class="chin-vacio-caja"></div>'
      : '<div class="chin-vacio-caja"></div>') + "</li>";
    Chin.pinta(c.querySelector(".chin-vacio-caja"),
      listo ? "festeja" : "busca",
      listo ? "Los hiciste todos" : "Nada con esos filtros",
      listo
        ? "Los " + todos.total + " del banco, resueltos. Cambia de banco, o repasa el que quieras."
        : "Ninguno coincide. Saca algún filtro, o cambia a Todos para ver también los hechos.");''',
  u'''    /* Tres vacíos distintos, y cada uno quiere que hagas otra cosa:
       no queda ninguno pendiente (que es bueno), todavía no
       resolviste ninguno (que es el principio), o los filtros no
       dejan pasar nada (que es un filtro de más). */
    var todos = Practica.avance(bancoActual);
    var sinFiltros = fDif === "todo" && fPat === "todo" && !busca;
    var listo   = fEstado === "pendientes" && sinFiltros && todos.hechos >= todos.total;
    var ninguno = fEstado === "hechos"     && sinFiltros && todos.hechos === 0;
    c.innerHTML = '<li><div class="chin-vacio-caja"></div></li>';
    var caja = c.querySelector(".chin-vacio-caja");
    if(listo){
      Chin.pinta(caja, "festeja", "Los hiciste todos",
        "Los " + todos.total + " del banco, resueltos. Cambia de banco, o repasa el que quieras.");
    }else if(ninguno){
      Chin.pinta(caja, "duerme", "Todavía ninguno",
        "Acá van a aparecer los que marques como resueltos. Empieza por los que faltan.");
    }else{
      Chin.pinta(caja, "busca", "Nada con esos filtros",
        "Ninguno coincide. Saca algún filtro, o cambia a Todos para ver el banco entero.");
    }''', 1),

 # el numerito del filtro
 (u"\n</style>",
  u'''
/* El número de cada filtro de estado. Va tenue: es un dato del botón,
   no lo que el botón dice. */
.filtro .fn{
  margin-left:5px; font-size:11px; font-weight:800;
  color:var(--text-3); font-variant-numeric:tabular-nums;
}
.filtro[aria-pressed="true"] .fn{ color:inherit; opacity:.7; }
''' + u"\n</style>", 1),
])

# ------------------------------------------------ 2. lo del CV, como corresponde
parchar("cv.html", [
 (u'''        <span><b>Se lee acá, en tu navegador.</b> Tu CV no sale de esta pestaña.</span>''',
  u'''        <span><b>Tu CV no se envía a ningún servidor.</b> Se procesa en tu navegador, queda guardado sólo en este dispositivo para que no tengas que pegarlo de nuevo, y no se comparte con nadie.</span>''', 1),
])

parchar("guia.js", [
 (u'''             "quieres, y te lo dejo en orden. Se lee acá en tu navegador.",''',
  u'''             "quieres, y te lo dejo en orden. No se envía a ningún servidor: " +
             "se procesa en tu navegador.",''', 1),
])
