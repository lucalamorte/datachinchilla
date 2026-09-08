/* ============================================================
   chinchilla.js

   La chinchilla, en sus poses.

   Aparece cuando no hay nada que mostrar, que es justo cuando una
   página se siente rota: una lista vacía, un día sin nada, una
   búsqueda sin resultados. En vez de un renglón gris, está ella.

   Cuatro poses, y cada una dice algo distinto:

     escarba   está buscando algo (mientras se lee un CV)
     duerme    hoy no toca nada (un día libre)
     busca     no encontró lo que le pediste
     festeja   terminaste algo

   Se dibuja en SVG con el mismo trazo del logo, y la animación va
   en CSS para que se quede quieta si el sistema pide menos
   movimiento.

   Uso:  Chin.pinta(nodo, "duerme", "Hoy no toca nada", "Descansar...")
   ============================================================ */
var Chin = (function(){
  "use strict";

  /* El cuerpo, que es el mismo en todas las poses. Cambian la cola,
     las patas y lo que hay alrededor. */
  function cuerpo(){
    return '' +
      '<ellipse class="c-cuerpo" cx="50" cy="60" rx="21" ry="19"/>' +
      '<circle class="c-cabeza" cx="50" cy="39" r="19"/>' +
      '<ellipse class="c-oreja" cx="37" cy="21" rx="9" ry="12" transform="rotate(-21 37 21)"/>' +
      '<ellipse class="c-oreja" cx="63" cy="21" rx="9" ry="12" transform="rotate(21 63 21)"/>' +
      '<ellipse class="c-oreja-in" cx="37.6" cy="23" rx="4.6" ry="6.4" transform="rotate(-21 37.6 23)"/>' +
      '<ellipse class="c-oreja-in" cx="62.4" cy="23" rx="4.6" ry="6.4" transform="rotate(21 62.4 23)"/>';
  }

  /* La cola: la misma del logo.

     Habia una inventada aca -una espina con circulos encima- y no
     hacia falta: la cola ya existia, dibujada, en el logo del nav,
     del pie y del globo. Dos dibujos de la misma cola es una que
     sobra, y encima la que sobraba era la peor.

     El path viene tal cual del logo, que esta en un lienzo de 24x24.
     La transformacion lo lleva a este, de 100x92, calculada para que
     el cuerpo del logo caiga exactamente sobre el cuerpo de la pose:
     el logo tiene el cuerpo en (14.2, 17.2) con rx 5.8 y la pose en
     (50, 60) con rx 21, o sea escala 21/5.8 = 3.6207.

     `lado` la espeja: en el logo va a la izquierda, y en algunas
     poses ese lado esta ocupado. */
  var COLA = "M 6.47 17.58 Q 6.26 19.36 5.23 17.77 Q 4.28 19.19 4.10 17.39 " +
             "Q 2.68 18.16 3.32 16.56 Q 1.79 16.60 3.03 15.53 Q 1.74 14.90 " +
             "3.24 14.54 Q 2.44 13.45 3.85 13.80 C 4.4 10.6 7.6 10.0 9.4 11.8 " +
             "C 10.6 14.2 10.4 17.2 9.6 19.4 Z";

  function cola(lado){
    var t = "translate(-1.41 -2.28) scale(3.6207)";
    /* Espejada sobre el centro del cuerpo, para que caiga igual del
       otro lado y no se corra. */
    if(lado === 1) t = "translate(100 0) scale(-1 1) " + t;
    return '<path class="c-cola" transform="' + t + '" d="' + COLA + '"/>';
  }

  function ojos(cerrados){
    if(cerrados){
      /* Dormida: dos arcos, que es lo único que hace falta. */
      return '<path class="c-ojo-l" d="M38 38q4 4 8 0"/>' +
             '<path class="c-ojo-l" d="M54 38q4 4 8 0"/>';
    }
    return '<ellipse class="c-ojo" cx="43" cy="38" rx="3" ry="3.7"/>' +
           '<ellipse class="c-ojo" cx="57" cy="38" rx="3" ry="3.7"/>' +
           '<circle class="c-brillo" cx="44" cy="36.6" r="1"/>' +
           '<circle class="c-brillo" cx="58" cy="36.6" r="1"/>';
  }

  function hocico(){
    return '<path class="c-hocico" d="M47 45h6c.9 0 1.4 1 .9 1.7l-2.4 3.2a1.1 1.1 0 0 1-1.8 0' +
           'l-2.4-3.2c-.5-.7 0-1.7.9-1.7Z"/>';
  }

  var POSES = {
    /* Escarbando: medio cuerpo adentro del pozo y la tierra saltando.
       Es lo que hace la chinchilla y lo que hace el sitio. */
    escarba: function(){
      /* Lo que sale del pozo son cursos, no tierra.

         Es lo que hace el sitio: escarba y saca cursos. Con grumos de
         tierra el dibujo era una chinchilla cavando y nada mas; con
         fichas que salen volando dice ademas para que cava. */
      function ficha(x, y, g){
        return '<g class="c-ficha" transform="translate(' + x + ' ' + y +
                 ') rotate(' + g + ')">' +
          '<rect x="-7" y="-5" width="14" height="10" rx="2.6"/>' +
          '<rect class="c-ficha-l" x="-4.4" y="-2.2" width="8.8" height="1.6" rx=".8"/>' +
          '<rect class="c-ficha-l" x="-4.4" y="1" width="5.6" height="1.6" rx=".8"/>' +
          '</g>';
      }
      return '<g class="c-cava">' +
          /* Arriba y a los costados, que es donde hay aire: abajo a la
             izquierda chocaban con la pala y las tres formas juntas se
             leian como una sola mancha. */
          '<g class="c-tierra">' + ficha(15, 30, -20) + ficha(30, 14, 10) + '</g>' +
          '<g class="c-tierra c-tierra-2">' + ficha(86, 30, 18) + '</g>' +
          /* Inclinada hacia el pozo. Derecha y con dos patas abajo
             era una chinchilla sentada detras de un monticulo: la
             postura tenia que decir "cabeza adentro" antes que
             cualquier animacion. Gira desde la cadera. */
          '<g class="c-bicho" transform="rotate(-9 50 74)">' +
            /* Y por eso la cola queda alta: es lo que mas se ve de
               una chinchilla metida en un pozo. */
            cola(1) +
            cuerpo() + ojos(false) + hocico() +
            /* Las manos apoyadas en el borde, anchas y horizontales.

               Antes eran dos brazos largos bajando del hombro. No
               hace falta describir a que se parecian: la respuesta de
               quien lo miro fue "dos penes colgando", y tenia razon.
               Cualquier cosa vertical y redondeada colgando de un
               cuerpo a esa altura se lee asi, y no hay animacion que
               lo arregle.

               Lo que dice "esta cavando" es la postura y el pozo, no
               los brazos: inclinada hacia adelante, el borde del pozo
               cruzandole el cuerpo, la tierra saltando y la cola
               arriba. Las manos solo asoman en el borde. */
            /* La pala, agarrada de verdad.

               Antes el mango bajaba por un lado y la pata estaba en
               otro: se veia una pala flotando al lado de una
               chinchilla. Ahora la pata cae SOBRE el mango, a mitad
               de camino entre el puno y la hoja, girada al angulo del
               mango. Ahi es donde se agarra una pala.

               Va del lado izquierdo porque la cola ocupa el derecho.
               El mango en T queda arriba y a la vista, y la hoja entra
               en la tierra, que es lo que se ve cuando alguien cava. */
            '<g class="c-mano-cava c-mano-izq">' +
              '<g class="c-pala">' +
                '<path class="c-pala-t" d="M10 33L23 39"/>' +
                '<path class="c-pala-m" d="M16 36L41 78"/>' +
                '<path class="c-pala-h" d="M33 62L45 56L54 72Q46 78 38 74Z"/>' +
              '</g>' +
              '<ellipse class="c-pata" cx="28" cy="56" rx="7.5" ry="5" ' +
                'transform="rotate(59 28 56)"/>' +
            '</g>' +
            /* La otra mano solo asoma en el borde. */
            '<g class="c-mano-cava c-mano-der">' +
              '<ellipse class="c-pata" cx="66" cy="76" rx="7.5" ry="4.4" ' +
                'transform="rotate(12 66 76)"/>' +
            '</g>' +
          '</g>' +
        '</g>' +
        /* El pozo, mas alto y mas hondo. Era una elipse chata al pie
           del dibujo: le tapaba cuatro pixeles y ella quedaba sentada
           encima. Ahora el borde le cruza el cuerpo, o sea que la
           mitad de abajo esta adentro, que es lo unico que hace que
           un dibujo diga "escarbando" sin que lo diga el texto. */
        '<ellipse class="c-pozo" cx="50" cy="80" rx="35" ry="11"/>';
    },

    /* Dormida, hecha un ovillo, con la cola de manta. */
    duerme: function(){
      return '<g class="c-duerme">' +
          /* La misma cola que las demas. Girarla para que hiciera de
             manta la despegaba del cuerpo y quedaba flotando al
             costado. */
          cola(1) +
          cuerpo() + ojos(true) + hocico() +
          '<g class="c-zzz">' +
            '<text x="74" y="26" class="c-z c-z1">z</text>' +
            '<text x="82" y="17" class="c-z c-z2">z</text>' +
          '</g>' +
        '</g>';
    },

    /* Buscando: la lupa y la cabeza ladeada. */
    busca: function(){
      return '<g class="c-busca">' + cola(-1) +
        cuerpo() + ojos(false) + hocico() + '</g>' +
        '<g class="c-lupa">' +
          '<circle class="c-lupa-c" cx="76" cy="58" r="12"/>' +
          '<path class="c-lupa-m" d="M85 67l9 9"/>' +
        '</g>';
    },

    /* Festejando: las patas arriba y confeti. */
    festeja: function(){
      return '<g class="c-salta">' +
          cola(1) +
          cuerpo() + ojos(false) + hocico() +
          '<ellipse class="c-pata" cx="28" cy="50" rx="6" ry="4.5" transform="rotate(-40 28 50)"/>' +
          '<ellipse class="c-pata" cx="72" cy="50" rx="6" ry="4.5" transform="rotate(40 72 50)"/>' +
        '</g>' +
        '<g class="c-fiesta">' +
          '<rect x="18" y="16" width="4" height="4" rx="1" transform="rotate(20 20 18)"/>' +
          '<rect x="78" y="22" width="4" height="4" rx="1" transform="rotate(-25 80 24)"/>' +
          '<rect x="30" y="8" width="3.4" height="3.4" rx="1" transform="rotate(40 31 9)"/>' +
          '<rect x="66" y="10" width="3.4" height="3.4" rx="1" transform="rotate(-15 67 11)"/>' +
        '</g>';
    },

    /* En cohete: para un hito de verdad, no para cada tilde.
       La ventanilla va del color del fondo para que ella salga
       recortada contra eso; con el casco del mismo tono que la
       cabeza no se entiende quien viaja. */
    cohete: function(){
      return '<g class="c-vuela">' +
          '<path class="c-ala" d="M36 50c-9 6-13 14-13 24l13-8Z"/>' +
          '<path class="c-ala" d="M64 50c9 6 13 14 13 24l-13-8Z"/>' +
          '<path class="c-casco" d="M50 6c10 9 14 22 14 35v25H36V41c0-13 4-26 14-35Z"/>' +
          '<circle class="c-buque" cx="50" cy="36" r="13"/>' +
          '<g class="c-tripulante">' +
            '<circle class="c-cabeza" cx="50" cy="37" r="8.6"/>' +
            '<ellipse class="c-oreja" cx="43.6" cy="29" rx="3.4" ry="4.6" transform="rotate(-21 43.6 29)"/>' +
            '<ellipse class="c-oreja" cx="56.4" cy="29" rx="3.4" ry="4.6" transform="rotate(21 56.4 29)"/>' +
            '<ellipse class="c-ojo" cx="47" cy="36" rx="1.4" ry="1.7"/>' +
            '<ellipse class="c-ojo" cx="53" cy="36" rx="1.4" ry="1.7"/>' +
            '<path class="c-hocico" d="M48.7 39.4h2.6c.42 0 .66.44.4.78l-1.1 1.4a.48.48 0 0 1-.8 0' +
              'l-1.1-1.4c-.26-.34 0-.78.4-.78Z"/>' +
          '</g>' +
          '<circle class="c-remache" cx="50" cy="60" r="2.4"/>' +
          '<rect class="c-faja" x="36" y="66" width="28" height="5" rx="2"/>' +
          '<g class="c-fuego">' +
          '<path class="c-llama c-llama-1" d="M50 68c8 10 12 17 12 23 0 5.4-5.4 9-12 9s-12-3.6-12-9c0-6 4-13 12-23Z"/>' +
          '<path class="c-llama c-llama-2" d="M50 74c4 6 6 10 6 13.4 0 3-2.6 5-6 5s-6-2-6-5c0-3.4 2-7.4 6-13.4Z"/>' +
          '</g>' +
        '</g>';
    },

    /* Saludando. El brazo y la mano van juntos en un grupo que gira
       desde el hombro: la mano sola, sin brazo, eran dos manchas a
       treinta pixeles una de otra. */
    saluda: function(){
      return cola(-1) + cuerpo() + ojos(false) + hocico() +
        '<ellipse class="c-pata" cx="34" cy="74" rx="6" ry="4.5"/>' +
        '<g class="c-brazo">' +
          '<path class="c-hueso" d="M66 60L75 45"/>' +
          '<ellipse class="c-pata" cx="76.5" cy="42" rx="5.4" ry="4.4"/>' +
        '</g>';
    },

    /* Con el cafe: va al lado de la invitacion, y nada mas. */
    cafe: function(){
      return '<g class="c-toma">' + cola(-1) +
          cuerpo() + ojos(false) + hocico() +
          '<ellipse class="c-pata" cx="30" cy="66" rx="6" ry="4.5"/>' +
        '</g>' +
        '<g class="c-taza">' +
          '<path class="c-vapor" d="M70 34c-3 4 3 6 0 10"/>' +
          '<path class="c-vapor c-vapor-2" d="M77 36c-3 4 3 6 0 9"/>' +
          '<path class="c-pocillo" d="M64 50h18l-2.4 14a3 3 0 0 1-3 2.6h-7.2a3 3 0 0 1-3-2.6Z"/>' +
          '<path class="c-asa" d="M82 54h3.4a4 4 0 0 1 0 8h-2.6"/>' +
        '</g>';
    }
  };

  /* Lo que dice mientras busca. Van rotando, porque un cartel fijo
     durante tres segundos parece colgado, y todas hablan de escarbar,
     que es lo que hace ella y lo que hace el sitio. */
  var ESPERAS = [
    { t: "Déjame escarbar", p: "Voy a ver qué hay ahí adentro." },
    { t: "Removiendo tierra", p: "Busco lo que ya sabes, para no ofrecértelo de nuevo." },
    { t: "Metiendo el hocico", p: "Cruzando tu experiencia con lo que pide el puesto." },
    { t: "Cavando hondo", p: "Viendo cuál de los recorridos del sitio te queda mejor." },
    { t: "Casi lo tengo", p: "Ordenando los cursos que te faltan." }
  ];

  var ultima = -1;

  /* Un mensaje, distinto del anterior. */
  function espera(){
    if(ESPERAS.length < 2) return ESPERAS[0];
    var i = ultima;
    while(i === ultima) i = Math.floor(Math.random() * ESPERAS.length);
    ultima = i;
    return ESPERAS[i];
  }

  /* Escarbando, con el texto rotando cada tanto.

     Los tiempos importan: no aparece hasta que la espera se nota, y
     si apareció se queda un rato antes de irse. Un cartel que
     parpadea se siente peor que no tener cartel.

     Devuelve con qué frenarla. Quien la arranca la frena. */
  function cavando(nodo){
    if(!nodo) return function(){};

    var ASOMA = 250;    /* antes de esto, la espera no se nota */
    var MINIMO = 900;   /* si se mostró, que se alcance a leer */

    var reloj = 0, desde = 0, muerta = false;

    var salida = setTimeout(function(){
      if(muerta) return;
      desde = Date.now();
      var e = espera();
      pinta(nodo, "escarba", e.t, e.p);

      reloj = setInterval(function(){
        var s = espera();
        var caja = nodo.querySelector(".chin-vacio");
        var b = caja && caja.querySelector("b");
        var p = caja && caja.querySelector("p");
        if(!b || !p){ clearInterval(reloj); return; }
        b.textContent = s.t;
        p.textContent = s.p;
        caja.classList.remove("chin-dice");
        void caja.offsetWidth;          /* reinicia la animación */
        caja.classList.add("chin-dice");
      }, 1900);
    }, ASOMA);

    return function(listo){
      muerta = true;
      clearTimeout(salida);
      if(!desde){ if(listo) listo(); return; }   /* nunca llegó a verse */
      var falta = Math.max(0, MINIMO - (Date.now() - desde));
      setTimeout(function(){
        clearInterval(reloj);
        if(listo) listo();
      }, falta);
    };
  }

  /* --- El festejo -------------------------------------------------

     Aparece en una esquina, dice una linea y se va sola. Sin boton de
     cerrar y sin tapar nada: si para felicitarte hay que interrumpir
     lo que estabas haciendo, deja de ser un premio.

     Se apila: marcar tres cursos seguidos no abre tres carteles, el
     ultimo reemplaza al anterior. */

  var caja = null, salida = null;

  function festejar(pose, titulo, texto){
    if(typeof document === "undefined") return;

    /* Con menos movimiento pedido, esto es puro movimiento sin
       informacion nueva: no va. */
    try{
      if(window.matchMedia &&
         window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    }catch(e){}

    if(!caja){
      caja = document.createElement("div");
      caja.className = "chin-fiesta-caja";
      caja.setAttribute("role", "status");
      caja.setAttribute("aria-live", "polite");
    }

    /* Un <dialog open> y su ::backdrop viven en el top layer, arriba
       de cualquier z-index. Los cursos se marcan justo desde esa
       hoja, así que el festejo salía atrás del velo. La única forma
       de estar por encima del top layer es estar adentro. */
    var hoja = document.querySelector("dialog[open]");
    var donde = hoja || document.body;
    if(caja.parentNode !== donde) donde.appendChild(caja);

    caja.innerHTML = svg(pose) +
      '<div class="chin-fiesta-txt"><b></b><span></span></div>';
    caja.querySelector("b").textContent = titulo || "";
    caja.querySelector("span").textContent = texto || "";

    /* El aviso que pueda haber quedado de la accion anterior ya no
       corresponde: lo que pasaba recien acaba de pasar. */
    var viejo = document.getElementById("toast");
    if(viejo) viejo.classList.remove("show", "on");

    caja.classList.remove("va", "sale");
    void caja.offsetWidth;          /* reinicia la entrada */
    caja.classList.add("va");

    clearTimeout(salida);
    salida = setTimeout(function(){
      caja.classList.add("sale");
      setTimeout(function(){ if(caja) caja.classList.remove("va", "sale"); }, 320);
    }, 3400);
  }

  function svg(pose){
    var f = POSES[pose] || POSES.busca;
    return '<svg class="chin-pose chin-' + pose + '" viewBox="0 0 100 92" ' +
           'role="img" aria-hidden="true">' + f() + '</svg>';
  }

  /* Pinta la pose con su texto en el nodo que le den. */
  function pinta(nodo, pose, titulo, texto, extra){
    if(!nodo) return;
    nodo.innerHTML =
      '<div class="chin-vacio">' + svg(pose) +
        (titulo ? '<b>' + titulo + '</b>' : "") +
        (texto ? '<p>' + texto + '</p>' : "") +
        (extra || "") +
      '</div>';
  }

  /* --- El recorrido -------------------------------------------------

     Las animaciones de arriba son de momentos: marcaste, cerraste,
     terminaste. Entre uno y otro la página es una lista quieta.

     Esto es lo que pasa mientras se la recorre. Va atado al scroll,
     que es lo que la persona está haciendo, y nunca se adelanta: un
     número que cuenta arriba de todo, fuera de la vista, contó para
     nadie.

     La clase que esconde la pone este JS y no el CSS. Sin
     IntersectionObserver, o si esto no corre, todo se ve como
     siempre: una animación que puede dejar la página en blanco no
     vale ninguna animación. */

  /* Cuenta de 0 a n mientras dura `ms`, con una curva que frena al
     final: el número se lee en el último tramo, no en el primero. */
  function contar(nodo, n, ms){
    /* Con setTimeout y no con rAF: si rAF no corre (pestaña de fondo,
       ventana minimizada) el número tiene que llegar igual a su
       valor. Un contador que se queda en cero es peor que no tener
       contador. */
    var t0 = Date.now();
    nodo.textContent = "0";
    var reloj = setInterval(function(){
      var k = Math.min(1, (Date.now() - t0) / ms);
      var suave = 1 - Math.pow(1 - k, 3);
      nodo.textContent = Math.round(n * suave);
      if(k >= 1){ clearInterval(reloj); nodo.textContent = n; }
    }, 40);
  }

  var mirando = false, ultima = 0, cierre = 0;

  /* Revela lo que ya entro en pantalla. Es la cuenta que hacia el
     IntersectionObserver, hecha en un lugar donde no puede no correr:
     si esto falla, falla el scroll de la pagina entera. */
  function revisar(){
    ultima = Date.now();
    clearTimeout(cierre); cierre = 0;
    var q = document.querySelectorAll(".chin-lejos");
    for(var i=0;i<q.length;i++){
      var c = q[i].getBoundingClientRect();
      /* Un poco antes de que llegue al borde, para que la animación
         termine cuando el elemento está a la vista y no después.

         Sin pedir que siga a la vista: con un envión del dedo la
         página salta más de una pantalla entre dos revisiones, y un
         elemento pasa de estar abajo a estar arriba sin haber estado
         nunca en el medio. Pidiéndolo, ése quedaba escondido para
         siempre, ocupando su lugar en blanco. */
      if(c.top < window.innerHeight * 0.92){
        q[i].classList.remove("chin-lejos");
        q[i].classList.add("chin-cerca");
      }
    }
    /* Se suelta cuando no queda NADA escondido, y preguntando de
       nuevo: q es la lista de antes del bucle. Con "<= 1" el ultimo
       elemento se quedaba sin nadie que lo revelara. */
    if(!document.querySelectorAll(".chin-lejos").length) soltar();
  }

  /* Directo, con un límite por tiempo, y sin rAF de por medio: lo
     que se esconde tiene que volver a aparecer sí o sí.

     La llamada que cae dentro del límite no se descarta, se agenda.
     Sin eso, en una ráfaga de scroll la última queda comida y lo que
     entró a pantalla en ese último tramo no se revela nunca. */
  function pedirRevision(){
    if(Date.now() - ultima >= 70){ revisar(); return; }
    if(cierre) return;
    cierre = setTimeout(function(){ cierre = 0; revisar(); }, 80);
  }

  function agarrar(){
    if(mirando) return;
    mirando = true;
    window.addEventListener("scroll", pedirRevision, { passive: true });
    window.addEventListener("resize", pedirRevision, { passive: true });
    /* Volver a la pestaña también cuenta como movimiento: si algo
       quedó escondido mientras no se miraba, acá aparece. */
    document.addEventListener("visibilitychange", revisar);
    /* Y una última red: pase lo que pase, a los tres segundos no
       queda nada escondido a la vista. */
    setTimeout(revisar, 3000);
  }

  /* Cuando no queda nada escondido, esto no tiene mas nada que hacer:
     se saca de encima del scroll. */
  function soltar(){
    if(!mirando) return;
    mirando = false;
    window.removeEventListener("scroll", pedirRevision);
    window.removeEventListener("resize", pedirRevision);
    document.removeEventListener("visibilitychange", revisar);
  }

  function recorrido(){
    try{
      if(window.matchMedia &&
         window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    }catch(e){}

    /* Las secciones y las tarjetas entran al llegar a ellas. */
    var entran = document.querySelectorAll(
      ".section-head, .grid-cards > *, .card-wrap, .cv-paso, .ag-dia, .reto-c");

    var k, caja, hay = 0;
    for(k=0;k<entran.length;k++){
      if(entran[k].hasAttribute("data-visto")) continue;
      entran[k].setAttribute("data-visto", "");

      /* Sólo se esconde lo que está fuera de la pantalla. Lo que ya
         se ve no se toca: nada desaparece delante de nadie. */
      caja = entran[k].getBoundingClientRect();
      if(caja.top < window.innerHeight && caja.bottom > 0) continue;

      entran[k].classList.add("chin-lejos");
      hay++;
    }

    /* Los números grandes cuentan hasta su valor la primera vez que
       se los ve. Los de dos dígitos aparecen y ya está: contarlos
       sería un parpadeo. */
    var cand = document.querySelectorAll(".meter-label .num b, .cuenta-grande");
    for(k=0;k<cand.length;k++){
      if(cand[k].hasAttribute("data-visto")) continue;
      cand[k].setAttribute("data-visto", "");
      var v = parseInt(cand[k].textContent, 10);
      if(v >= 10) contar(cand[k], v, 900);
    }

    if(hay) agarrar();
  }

  /* Una huella sola, para marcar cosas chicas: el eyebrow de una
     seccion, la esquina de una tarjeta. */
  function huella(){
    return '<svg class="chin-h1" viewBox="-6 -8 12 16" aria-hidden="true">' +
      '<path d="M0 0c1.6 0 2.9 1.5 2.9 3.3S1.6 6.6 0 6.6-2.9 5.1-2.9 3.3-1.6 0 0 0Z"/>' +
      '<circle cx="-3.4" cy="-4.4" r="1.15"/>' +
      '<circle cx="-1.2" cy="-6.1" r="1.15"/>' +
      '<circle cx="1.2" cy="-6.1" r="1.15"/>' +
      '<circle cx="3.4" cy="-4.4" r="1.15"/>' +
    '</svg>';
  }

  /* Un nodo cuenta como visible si ocupa lugar. offsetParent no
     alcanza: devuelve null tambien para position:fixed. */
  function visible(n){
    if(n.hidden) return false;
    return !!(n.offsetWidth || n.offsetHeight || n.getClientRects().length);
  }

  /* Una tira de huellas contra una seccion escondida no se lee como
     rastro, se lee como error. Se van. */
  /* Ya no se insertan: esto solo barre las que hayan quedado. */
  function limpiarHuellas(){
    var q = document.querySelectorAll(".chin-paso"), i;
    for(i=0;i<q.length;i++){
      if(q[i].parentNode) q[i].parentNode.removeChild(q[i]);
    }
  }

  /* --- Volver ---------------------------------------------------

     Volver es lo mas dificil de un sitio de estudio, y no pasaba
     nada cuando alguien lo hacia. Saluda una vez por dia, y solo a
     quien ya tenia algo empezado: saludar a quien entra por primera
     vez no es reconocerlo, es ruido. */
  var KDIA = "datachinchilla/v1/visto";

  function hoyTexto(){
    var d = new Date(), m = d.getMonth() + 1, x = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m +
           "-" + (x < 10 ? "0" : "") + x;
  }

  function saludar(){
    var hoy = hoyTexto(), antes;
    try{
      antes = localStorage.getItem(KDIA);
      localStorage.setItem(KDIA, hoy);
    }catch(e){ return; }          /* sin storage, no saluda y listo */

    if(!antes || antes === hoy) return;      /* primera vez, o ya hoy */

    /* Solo a quien tiene algo empezado. Con cargar() antes: esto
       corre en DOMContentLoaded y el init de la página llama a
       Onb.cargar() después, así que sin esto se leía el estado
       inicial, vacío, y no saludaba nunca. */
    /* Y solo a quien tiene cuenta. Saludar con "volviste" a alguien
       anonimo suena a que el sitio sabe quien es, y no lo sabe: desde
       que guardar avance pide cuenta, el reconocimiento tiene que
       venir del mismo lado. */
    var tiene = false;
    try{
      if(window.PathSync && PathSync.puedeGuardar && !PathSync.puedeGuardar()) return;
      if(typeof Onb !== "undefined"){
        Onb.cargar();
        tiene = Onb.estado.rutas.length > 0;
      }
    }catch(e){}
    if(!tiene) return;

    var dias = Math.round(
      (new Date(hoy) - new Date(antes)) / 86400000);
    setTimeout(function(){
      festejar("saluda", "Volviste",
        dias > 6 ? "Tu avance está donde lo dejaste. Se sigue por donde quieras."
                 : "Ahí abajo está lo de hoy.");
    }, 900);
  }

  /* --- Las huellas ---------------------------------------------------

     Dos patitas, repetidas en diagonal. Van entre seccion y seccion,
     como si hubiera cruzado por ahi mientras nadie miraba. */
  function huellas(){
    var p = '<path class="c-huella" d="M0 0c1.6 0 2.9 1.5 2.9 3.3S1.6 6.6 0 6.6-2.9 5.1-2.9 3.3-1.6 0 0 0Z"/>';
    var dedo = '<circle class="c-huella" r="1.15"/>';
    var pisada = function(x, y, giro){
      return '<g transform="translate(' + x + ' ' + y + ') rotate(' + giro + ')">' +
        p +
        '<g transform="translate(-3.4 -4.4)">' + dedo + '</g>' +
        '<g transform="translate(-1.2 -6.1)">' + dedo + '</g>' +
        '<g transform="translate(1.2 -6.1)">' + dedo + '</g>' +
        '<g transform="translate(3.4 -4.4)">' + dedo + '</g>' +
      '</g>';
    };
    /* En diagonal y alternando lado, que es como camina algo con
       cuatro patas y no como se estampa un sello. */
    return '<svg class="chin-huellas" viewBox="0 0 200 40" aria-hidden="true">' +
      pisada(18, 26, 16) + pisada(38, 16, 22) +
      pisada(72, 24, 14) + pisada(92, 14, 20) +
      pisada(126, 25, 15) + pisada(146, 15, 21) +
      pisada(180, 23, 13) +
    '</svg>';
  }

  /* Una que se asoma por el borde de arriba del pie: el final de la
     pagina, que es donde no habia nada. */
  function asomada(){
    return '<div class="chin-asoma" aria-hidden="true">' +
      '<svg viewBox="0 0 100 46">' +
        '<ellipse class="c-oreja" cx="37" cy="16" rx="9" ry="12" transform="rotate(-21 37 16)"/>' +
        '<ellipse class="c-oreja" cx="63" cy="16" rx="9" ry="12" transform="rotate(21 63 16)"/>' +
        '<ellipse class="c-oreja-in" cx="37.6" cy="18" rx="4.6" ry="6.4" transform="rotate(-21 37.6 18)"/>' +
        '<ellipse class="c-oreja-in" cx="62.4" cy="18" rx="4.6" ry="6.4" transform="rotate(21 62.4 18)"/>' +
        '<circle class="c-cabeza" cx="50" cy="34" r="19"/>' +
        '<ellipse class="c-ojo" cx="43" cy="33" rx="3" ry="3.7"/>' +
        '<ellipse class="c-ojo" cx="57" cy="33" rx="3" ry="3.7"/>' +
        '<circle class="c-brillo" cx="44" cy="31.6" r="1"/>' +
        '<circle class="c-brillo" cx="58" cy="31.6" r="1"/>' +
        '<path class="c-hocico" d="M47 40h6c.9 0 1.4 1 .9 1.7l-2.4 3.2a1.1 1.1 0 0 1-1.8 0' +
          'l-2.4-3.2c-.5-.7 0-1.7.9-1.7Z"/>' +
      '</svg>' +
    '</div>';
  }

  /* --- El pie y el globo -------------------------------------------

     Dos decoraciones que viven en las veinte páginas. Van acá y no en
     cada HTML porque serían veinte copias del mismo cambio, y veinte
     lugares donde una se puede quedar vieja.

     No pisa nada: sólo agrega, y sólo si encuentra dónde. */
  function decorar(){
    var i;

    /* En el pie queda solo la marca y la que se asoma por el borde:
       tres chinchillas en el mismo renglón no es identidad, es
       ruido. Las poses `cafe` y `saluda` se usan en otro lado, donde
       dicen algo en vez de decorar un link. */

    /* --- La chinchilla, sin que haya que hacer nada -------------

       Hasta acá sólo aparecía cuando faltaba algo (una lista vacía)
       o cuando tocabas algo (marcar un curso). En una página que
       anda bien y que solo estás leyendo no estaba en ningún lado. */

    /* En el encabezado, escarbando al lado del texto de entrada.

       Va ADENTRO del párrafo y no flotando sobre el hero: en esa
       esquina no hay hueco libre (abajo están las tarjetas, arriba
       el título ocupa todo el ancho). Con float el texto la rodea,
       y el acomodo lo hace el navegador en cada ancho de ventana. */
    var lead = document.querySelector(".hero .hero-lead");
    if(lead && !lead.querySelector(".chin-hero")){
      var caja = document.createElement("span");
      caja.className = "chin-hero";
      caja.setAttribute("aria-hidden", "true");
      caja.innerHTML = svg("escarba");
      lead.insertBefore(caja, lead.firstChild);
    }

    /* Las huellas entre seccion y seccion se fueron. La intencion
       era una marca de la casa, pero se leian como un indicador de
       carga -aparecen y desaparecen en bucle, una atras de la otra,
       igual que un spinner- y sumaban 54px entre cada par de
       secciones sin decir nada. limpiarHuellas() se queda para sacar
       las que hayan quedado de una version anterior. */

    /* Y las que hayan quedado colgadas de una pasada anterior. */
    limpiarHuellas();

    /* Una huella al lado del rótulo de cada sección: así cada bloque
       de la página queda marcado, y no solo el encabezado de arriba. */
    /* Dos clases para lo mismo: .eyebrow en los rótulos de sección
       y .lema en el del encabezado de página. Van las dos. */
    var ojos = document.querySelectorAll(".eyebrow, .lema");
    for(i=0;i<ojos.length;i++){
      if(ojos[i].querySelector(".chin-h1")) continue;
      /* Los del CV llevan el número del paso adelante: ahí el número
         ya marca el renglón y dos marcas juntas son ruido. */
      if(ojos[i].querySelector(".cv-num")) continue;
      ojos[i].insertAdjacentHTML("afterbegin", huella());
    }

    /* Y asomándose por el borde del pie, al final de todo.

       Adentro del pie y no antes: el pie tiene 48px de margen arriba,
       así que puesta afuera quedaba a esa distancia, flotando. */
    var pie = document.querySelector(".foot");
    if(pie && !pie.querySelector(".chin-asoma")){
      pie.insertAdjacentHTML("afterbegin", asomada());
    }

    /* Y lo que acompaña mientras se recorre la página. */
    recorrido();
    saludar();
  }

  if(typeof document !== "undefined"){
    if(document.readyState === "loading"){
      document.addEventListener("DOMContentLoaded", decorar);
    }else{
      decorar();
    }
    /* El catálogo, los retos y la agenda los pinta el init() de cada
       página, que corre después. Sin estas dos pasadas más, en la
       portada esto agarraba dos elementos de veintiuno: los únicos
       que están escritos en el HTML. */
    window.addEventListener("load", recorrido);
    setTimeout(recorrido, 400);
    /* Y la red: a los dos segundos se apagan las animaciones de
       entrada. Si el reloj de animaciones nunca arranco -pestana que
       no se pinto, vuelta desde el cache- lo que quedo en el primer
       fotograma aparece. Los timers corren igual, que es por lo que
       esto sirve. */
    setTimeout(function(){
      document.documentElement.classList.add("chin-sin-entrada");
    }, 2000);
  }

  return { svg: svg, pinta: pinta, cavando: cavando, espera: espera,
           festejar: festejar, decorar: decorar,
           limpiarHuellas: limpiarHuellas, POSES: POSES };
})();
