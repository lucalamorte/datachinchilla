/* ============================================================
   path-sync.js
   Capa de sesión y sincronización contra Supabase, compartida por
   las dos páginas del sitio. Acá vive una sola vez todo lo que
   toca la red: entrar por mail, refrescar el token, leer y escribir
   la fila de progreso.

   Sin claves cargadas, PathSync.isOn() devuelve false y ninguna
   página intenta nada: siguen funcionando con perfiles locales.

   La anon key es pública por diseño y viaja en el navegador.
   La service role NUNCA va acá.
   ============================================================ */
var PathSync = (function(){
  "use strict";

  var KEY_SESSION = "snowpro-path/v1/cloud";
  var cfg = { url: "", key: "" };
  var ses = null;          // { access_token, refresh_token, expires_at, user_id, email }
  var lastType = "";       // que clase de link nos trajo: "recovery", "magiclink", ...

  /* ?reset en cualquier pagina: vuelve a la primera visita.

     Sin esto, probar como alguien que entra por primera vez pide
     abrir la consola, o pelear con una ventana de incognito que no
     siempre esta limpia: Chrome mantiene viva la sesion mientras
     quede cualquier ventana de incognito abierta, y la barra de
     direcciones autocompleta desde el historial normal.

     Corre antes que nada porque este es el primero de los modulos
     compartidos que se carga. */
  (function(){
    try{
      if(!/[?&]reset/.test(window.location.search)) return;
      if(!window.confirm("Se borra todo lo que guardaste en este navegador " +
                         "-tu ruta, tu semana y lo que marcaste- y el sitio " +
                         "queda como en la primera visita. ¿Seguro?")) return;
      var k, fuera = [];
      for(k in window.localStorage){
        if(k.indexOf("datachinchilla/") === 0 || k.indexOf("snowpro-path/") === 0) fuera.push(k);
      }
      for(k = 0; k < fuera.length; k++) window.localStorage.removeItem(fuera[k]);
      try{ window.sessionStorage.clear(); }catch(e){}
      window.location.replace(window.location.pathname);
    }catch(e){}
  })();

  function get(k){ try{ return window.localStorage.getItem(k); }catch(e){ return null; } }
  function set(k, v){ try{ window.localStorage.setItem(k, v); return true; }catch(e){ return false; } }
  function del(k){ try{ window.localStorage.removeItem(k); return true; }catch(e){ return false; } }

  function nowSec(){ return Math.floor(Date.now() / 1000); }
  function base(){ return cfg.url.replace(/\/+$/, ""); }

  function load(){
    try{
      var raw = get(KEY_SESSION);
      ses = raw ? JSON.parse(raw) : null;
    }catch(e){ ses = null; }
  }
  function save(){
    return ses ? set(KEY_SESSION, JSON.stringify(ses)) : del(KEY_SESSION);
  }

  function headers(withToken){
    var h = { "apikey": cfg.key, "Content-Type": "application/json" };
    if(withToken && ses) h["Authorization"] = "Bearer " + ses.access_token;
    return h;
  }

  /* Nunca asume que la respuesta es JSON: un error de infraestructura
     contesta HTML y parsearlo escondería la causa real. */
  function call(path, opts){
    opts = opts || {};
    return fetch(base() + path, {
      method: opts.method || "GET",
      headers: opts.headers || headers(true),
      body: opts.body ? JSON.stringify(opts.body) : undefined
    })["catch"](function(){
      throw new Error("no pude contactar al servidor, revisa tu conexión");
    }).then(function(r){
      return r.text().then(function(t){
        var data = null;
        if(t){
          try{ data = JSON.parse(t); }catch(e){ data = null; }
        }
        if(!r.ok){
          var msg = (data && (data.msg || data.message || data.error_description || data.error)) ||
                    ("el servidor respondió " + r.status);
          throw new Error(msg);
        }
        return data;
      });
    });
  }

  function ensureFresh(){
    if(!ses) return Promise.reject(new Error("no hay sesión"));
    if(ses.expires_at - 60 > nowSec()) return Promise.resolve();
    if(!ses.refresh_token) return Promise.reject(new Error("la sesión venció, entra de nuevo"));
    return call("/auth/v1/token?grant_type=refresh_token", {
      method: "POST",
      headers: headers(false),
      body: { refresh_token: ses.refresh_token }
    }).then(function(d){
      ses.access_token = d.access_token;
      ses.refresh_token = d.refresh_token || ses.refresh_token;
      ses.expires_at = nowSec() + (d.expires_in || 3600);
      save();
    });
  }

  /* GoTrue devuelve la sesion igual en signup, login y refresh: una sola
     funcion para guardarla evita que cada camino invente su propia forma. */
  function guardarSesion(d, email){
    ses = {
      access_token: d.access_token,
      refresh_token: d.refresh_token || "",
      expires_at: nowSec() + (d.expires_in || 3600),
      user_id: (d.user && d.user.id) || "",
      email: (d.user && d.user.email) || email || ""
    };
    save();
    return ses;
  }

  function fetchUser(){
    return call("/auth/v1/user").then(function(u){
      ses.user_id = u.id;
      ses.email = u.email || "";
      save();
      return u;
    });
  }

  return {
    /* --------------------------------------------------- arranque */
    configure: function(url, key){
      cfg.url = url || "";
      cfg.key = key || "";
      if(cfg.url && cfg.key) load();
      return cfg.url && cfg.key ? true : false;
    },
    isOn: function(){ return !!(cfg.url && cfg.key); },
    session: function(){ return ses; },

    /* Guardar avance pide cuenta. Un unico lugar que lo diga, para
       que no haya dos ideas distintas de que significa estar
       logueado repartidas por las paginas. */
    puedeGuardar: function(){ return !!ses; },

    /* --------------------------------------------------- entrar */

    /* El link del mail vuelve a la misma URL de la que salio. Abierta
       como archivo local no hay a donde volver: location.origin es la
       cadena "null" y Supabase no puede redirigir ahi. */
    canReturn: function(){
      return location.protocol === "http:" || location.protocol === "https:";
    },

    sendLink: function(email, app){
      if(location.protocol !== "http:" && location.protocol !== "https:"){
        return Promise.reject(new Error(
          "abriste la página como archivo local y el link del mail no tiene a dónde " +
          "volver. Sube la página a internet o levántala en un servidor y entra desde ahí."));
      }
      var back = location.origin + location.pathname;
      return call("/auth/v1/otp?redirect_to=" + encodeURIComponent(back), {
        method: "POST",
        headers: headers(false),
        body: { email: email, create_user: true, data: { app: app || "snowpath" } }
      });
    },

    /* --------------------------------------------------- contraseña

       Entrar con contraseña no necesita volver de ningún lado: la sesión
       llega en la misma respuesta. Registrarse y recuperar sí, porque
       pasan por un mail. */
    signIn: function(email, password){
      return call("/auth/v1/token?grant_type=password", {
        method: "POST",
        headers: headers(false),
        body: { email: email, password: password }
      }).then(function(d){ guardarSesion(d, email); return true; });
    },

    /* Si el proyecto pide confirmar el mail, Supabase no devuelve sesión.
       Se avisa en vez de dar por hecho que entró: decir "listo" y que
       después no ande es peor que pedir un paso más. */
    signUp: function(email, password, app){
      var back = location.origin + location.pathname;
      return call("/auth/v1/signup?redirect_to=" + encodeURIComponent(back), {
        method: "POST",
        headers: headers(false),
        body: { email: email, password: password, data: { app: app || "snowpath" } }
      }).then(function(d){
        if(d && d.access_token){ guardarSesion(d, email); return { entro: true }; }
        return { entro: false };
      });
    },

    /* Google se va del sitio y vuelve con los tokens en el hash, igual
       que el link del mail: por eso lo levanta el mismo captureHash.

       supabase-js hace exactamente esta llamada por dentro. Acá se
       escribe a mano porque la librería entera, para una redirección,
       no se paga sola.

       Ojo con una consecuencia: en el alta por Google la metadata la
       escribe Google, así que no lleva nuestro campo "app" y el trigger
       de origen marca account_created_here en false. */
    signInWithGoogle: function(){
      location.href = base() + "/auth/v1/authorize?provider=google&redirect_to=" +
        encodeURIComponent(location.origin + location.pathname);
    },

    /* Manda el mail para elegir una contraseña nueva. El link vuelve a
       esta misma página con type=recovery en el hash. */
    sendReset: function(email){
      var back = location.origin + location.pathname;
      return call("/auth/v1/recover?redirect_to=" + encodeURIComponent(back), {
        method: "POST",
        headers: headers(false),
        body: { email: email }
      });
    },

    /* Cambiar la contraseña necesita una sesión: la del link de
       recuperación, o la de alguien que ya entró. */
    setPassword: function(password){
      if(!ses) return Promise.reject(new Error("no hay sesión"));
      return ensureFresh().then(function(){
        return call("/auth/v1/user", { method: "PUT", body: { password: password } });
      });
    },

    /* Qué clase de link nos trajo. Sirve para saber que hay que pedir una
       contraseña nueva en vez de entrar y ya. */
    hashType: function(){ return lastType; },

    /* El link del mail vuelve con los tokens en el hash de la URL.
       Devuelve true si había una sesión nueva para tomar. */
    captureHash: function(onError){
      var h = location.hash || "";
      if(h.indexOf("access_token") < 0 && h.indexOf("error") < 0) return false;
      var out = {}, parts = h.replace(/^#/, "").split("&"), i, kv;
      for(i=0;i<parts.length;i++){
        kv = parts[i].split("=");
        out[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
      }
      if(history.replaceState) history.replaceState(null, "", location.pathname + location.search);
      if(out.error || out.error_description){
        if(onError) onError(out.error_description || out.error);
        return false;
      }
      if(!out.access_token) return false;
      lastType = out.type || "";
      ses = {
        access_token: out.access_token,
        refresh_token: out.refresh_token || "",
        expires_at: nowSec() + (parseInt(out.expires_in, 10) || 3600),
        user_id: "", email: ""
      };
      save();
      return true;
    },

    signOut: function(){
      if(ses){
        ensureFresh()
          .then(function(){ return call("/auth/v1/logout", { method: "POST" }); })
          ["catch"](function(){ /* del lado del navegador se cierra igual */ });
      }
      ses = null;
      save();
    },

    /* --------------------------------------------------- datos */
    ready: function(){
      if(!ses) return Promise.reject(new Error("no hay sesión"));
      return ensureFresh().then(function(){
        return ses.user_id ? null : fetchUser();
      });
    },

    getRow: function(table){
      return call("/rest/v1/" + table + "?select=*&user_id=eq." + encodeURIComponent(ses.user_id))
        .then(function(rows){ return (rows && rows.length) ? rows[0] : null; });
    },

    upsertRow: function(table, row){
      var h = headers(true);
      h["Prefer"] = "resolution=merge-duplicates,return=minimal";
      row.user_id = ses.user_id;
      return call("/rest/v1/" + table, { method: "POST", headers: h, body: [row] });
    },

    /* Insertar sin pisar. Las tablas que solo se agregan (eventos,
       consentimientos) no tienen una fila por persona que actualizar:
       cada registro es un hecho nuevo con su fecha. */
    insertRow: function(table, row){
      var h = headers(true);
      h["Prefer"] = "return=minimal";
      row.user_id = ses.user_id;
      return call("/rest/v1/" + table, { method: "POST", headers: h, body: [row] });
    },

    /* --------------------------------------------------- perfil y uso

       Todo lo de abajo es best-effort: si falla, la app sigue andando.
       Perder un evento de uso no puede romperle la práctica a nadie, y
       reintentarlo tampoco vale la pena. */

    guardarPerfil: function(datos){
      if(!ses) return Promise.resolve(false);
      return this.ready()
        .then(function(){
          var h = headers(true);
          h["Prefer"] = "resolution=merge-duplicates,return=minimal";
          datos.user_id = ses.user_id;
          return call("/rest/v1/usuarios", { method: "POST", headers: h, body: [datos] });
        })
        .then(function(){ return true; })
        ["catch"](function(){ return false; });
    },

    leerPerfil: function(){
      if(!ses) return Promise.resolve(null);
      return this.ready()
        .then(function(){
          return call("/rest/v1/usuarios?select=*&user_id=eq." +
                      encodeURIComponent(ses.user_id));
        })
        .then(function(filas){ return (filas && filas.length) ? filas[0] : null; })
        ["catch"](function(){ return null; });
    },

    /* Cada sí y cada no queda con su fecha. El estado en usuarios lo
       actualiza un trigger: el navegador no puede escribirlo. */
    registrarConsentimiento: function(valor, app){
      if(!ses) return Promise.resolve(false);
      var self = this;
      return this.ready()
        .then(function(){
          return self.insertRow("consentimientos", {
            tipo: "marketing", valor: !!valor, app: app || "desconocida"
          });
        })
        .then(function(){ return true; })
        ["catch"](function(){ return false; });
    },

    evento: function(app, nombre, props){
      if(!ses) return Promise.resolve(false);
      var self = this;
      return this.ready()
        .then(function(){
          return self.insertRow("eventos", {
            app: app, evento: nombre, props: props || {}
          });
        })
        .then(function(){ return true; })
        ["catch"](function(){ return false; });
    },

    /* --------------------------------------------------- panel de acceso

       Entrar, crear cuenta y recuperar la contrasena, dibujado adentro
       del contenedor que le pasen. Usa las clases que ya existen en las
       paginas (field, auth-actions, auth-note, form-err), asi hereda el
       estilo de cada una sin traer CSS propio.

       Opciones:
         app        con que nombre queda la cuenta en la base
         cls        { btn, alt } clases de los botones de esa pagina
         onEntrar   se llama cuando la persona quedo adentro
         onTitulo   se llama con (bajada, titulo) al cambiar de paso  */
    authUI: (function(){
      var vista = "login", mail = "", cont = null, op = {};

      var MAIL_OK = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
      var LARGO_MINIMO = 8;

      function esc(s){
        return String(s == null ? "" : s)
          .replace(/&/g, "&amp;").replace(/</g, "&lt;")
          .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
      }
      function clsBtn(){ return (op.cls && op.cls.btn) || "btn-done"; }
      function clsAlt(){ return (op.cls && op.cls.alt) || "btn-quiet"; }

      function campoMail(){
        return '<div class="field"><label for="inMail">Tu mail</label>' +
               '<input id="inMail" type="email" autocomplete="email" value="' +
               esc(mail) + '" placeholder="tumail@ejemplo.com"></div>';
      }
      function campoPass(id, label, auto, pista){
        return '<div class="field"><label for="' + id + '">' + label + '</label>' +
               '<input id="' + id + '" type="password" autocomplete="' + auto +
               '" placeholder="\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022">' +
               (pista ? '<span class="pista">' + pista + '</span>' : '') + '</div>';
      }
      function alt(botones){
        var h = '<div class="auth-actions" style="margin-top:10px">', i;
        for(i=0;i<botones.length;i++){
          h += '<button class="' + clsAlt() + '" type="button" data-vista="' +
               botones[i][0] + '">' + botones[i][1] + '</button>';
        }
        return h + '</div>';
      }
      function boton(txt){
        return '<div class="auth-actions"><button class="' + clsBtn() +
               '" type="submit">' + txt + '</button></div>';
      }

      /* Google se va del sitio y vuelve: como archivo local no hay a donde,
         asi que ahi no se ofrece. El logo es el oficial y no se recolorea. */
      function google(){
        if(!PathSync.canReturn()) return "";
        return '<button class="' + clsAlt() + '" type="button" id="googleBtn" ' +
            'style="width:100%;justify-content:center">' +
            '<svg width="17" height="17" viewBox="0 0 24 24" aria-hidden="true">' +
              '<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>' +
              '<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>' +
              '<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>' +
              '<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>' +
            '</svg> Continuar con Google</button>' +
            '<div class="auth-sep">o con tu mail</div>';
      }

      function titulo(){
        if(vista === "signup")   return ["Crear cuenta", "Crea tu cuenta"];
        if(vista === "forgot")   return ["Recuperar", "Elige una contraseña nueva"];
        if(vista === "recovery") return ["Recuperar", "Elige una contraseña nueva"];
        if(vista === "enviado")  return ["Revisa tu correo", "Te mandé un mail"];
        return ["Tu cuenta", "Entra a tu cuenta"];
      }

      function nota(){
        if(vista === "signup"){
          return "Con la cuenta tu avance deja de vivir solo en este navegador: entras " +
                 "con el mismo mail en otra computadora y sigue donde lo dejaste.";
        }
        if(vista === "forgot"){
          return "Te llega un link para elegir una contraseña nueva. Mientras tanto tu " +
                 "avance sigue guardado en este navegador.";
        }
        if(vista === "recovery"){
          return "Esta contraseña reemplaza a la anterior. Al guardarla ya quedas dentro.";
        }
        return "Lo que ya llevas en este navegador no se pierde: al entrar se sube y se " +
               "junta con lo que tengas guardado.";
      }

      function cuerpo(){
        if(vista === "enviado"){
          return '<div class="acct-stat"><span class="k">Te mandé un mail a <b>' +
                 esc(mail) + '</b>. Ábrelo y toca el link: vuelves a esta misma ' +
                 'página.</span></div>' +
                 '<p class="auth-note">Si no aparece en unos minutos, mira en spam. El link ' +
                 'vence al rato por seguridad, y si se pasó pides otro.</p>' +
                 alt([["login", "Volver a entrar"]]);
        }
        if(vista === "signup"){
          return google() +
            '<form id="authForm" novalidate>' +
              '<div class="field"><label for="inNombre">Tu nombre</label>' +
              '<input id="inNombre" type="text" autocomplete="given-name" ' +
              'placeholder="Cómo quieres que te llame"></div>' +
              campoMail() +
              campoPass("inPass", "Contraseña", "new-password", "Ocho caracteres o más.") +
              '<label class="check"><input type="checkbox" id="inOptin">' +
              '<span>Quiero recibir avisos cuando se agreguen rutas, contenido o ' +
              'herramientas nuevas. Un mail cada tanto, y puedes darte de baja ' +
              'desde acá mismo.</span></label>' +
              boton("Crear la cuenta") +
            '</form>' + alt([["login", "Ya tengo cuenta"]]) +
            '<p class="auth-note">' + nota() + '</p>';
        }
        if(vista === "forgot"){
          return '<form id="authForm" novalidate>' + campoMail() +
                   boton("Mandarme el link") +
                 '</form>' +
                 alt([["login", "Volver a entrar"], ["signup", "Crear una cuenta"]]) +
                 '<p class="auth-note">' + nota() + '</p>';
        }
        if(vista === "recovery"){
          return '<form id="authForm" novalidate>' +
                   campoPass("inPass", "Contraseña nueva", "new-password", "Ocho caracteres o más.") +
                   campoPass("inPass2", "Repítela", "new-password", "") +
                   boton("Guardar la contraseña") +
                 '</form>' +
                 '<p class="auth-note">' + nota() + '</p>';
        }
        return google() +
          '<form id="authForm" novalidate>' + campoMail() +
            campoPass("inPass", "Contraseña", "current-password", "") +
            boton("Entrar") +
          '</form>' +
          alt([["signup", "Crear una cuenta"], ["forgot", "Olvidé mi contraseña"]]) +
          '<p class="auth-note">' + nota() + '</p>';
      }

      function pintar(msg){
        if(!cont) return;
        var t = titulo();
        if(op.onTitulo) op.onTitulo(t[0], t[1]);
        cont.innerHTML = (msg
          ? '<p class="form-err">' + esc(msg) + '</p>'
          : "") + cuerpo();
        enganchar();
      }

      function enganchar(){
        var v = cont.querySelectorAll("[data-vista]"), i;
        for(i=0;i<v.length;i++){
          v[i].addEventListener("click", function(){
            vista = this.getAttribute("data-vista");
            pintar("");
            var foco = cont.querySelector("#inMail") || cont.querySelector("#inPass");
            if(foco) foco.focus();
          });
        }

        var g = cont.querySelector("#googleBtn");
        if(g) g.addEventListener("click", function(){
          this.setAttribute("aria-disabled", "true");
          PathSync.signInWithGoogle();
        });

        var f = cont.querySelector("#authForm");
        if(f) f.addEventListener("submit", function(ev){
          ev.preventDefault();
          enviar(f);
        });
      }

      function enviar(f){
        var cMail = cont.querySelector("#inMail");
        var cPass = cont.querySelector("#inPass");
        var cPass2 = cont.querySelector("#inPass2");
        var pass = cPass ? cPass.value || "" : "";

        if(cMail){
          var m = (cMail.value || "").trim();
          if(!MAIL_OK.test(m)) return pintar("Escribe un mail válido.");
          mail = m;
        }
        if(cPass && vista !== "login" && pass.length < LARGO_MINIMO){
          return pintar("La contraseña necesita al menos " + LARGO_MINIMO + " caracteres.");
        }
        if(cPass2 && pass !== cPass2.value){
          return pintar("Las dos contraseñas no coinciden.");
        }
        if(vista === "login" && !pass) return pintar("Escribe tu contraseña.");

        var b = f.querySelector("button[type=submit]");
        function trabajando(txt){
          if(b){ b.setAttribute("aria-disabled", "true"); b.textContent = txt; }
        }
        function fallo(pref){
          return function(e){ pintar(pref + ": " + (e.message || "prueba de nuevo")); };
        }
        function adentro(){
          vista = "login";
          if(op.onEntrar) op.onEntrar();
        }

        if(vista === "signup"){
          var nombre = (cont.querySelector("#inNombre").value || "").trim().slice(0, 60);
          var optin = cont.querySelector("#inOptin").checked;
          trabajando("Creando...");
          return PathSync.signUp(mail, pass, op.app).then(function(r){
            /* Con confirmacion de mail todavia no hay sesion, asi que el
               perfil no se puede escribir: queda pendiente y se sube al entrar. */
            PathSync.guardarAltaPendiente({ nombre: nombre, optin: optin });
            if(r.entro) return adentro();
            vista = "enviado";
            pintar("");
          })["catch"](fallo("No pude crear la cuenta"));
        }
        if(vista === "forgot"){
          trabajando("Mandando...");
          return PathSync.sendReset(mail).then(function(){
            vista = "enviado";
            pintar("");
          })["catch"](fallo("No pude mandar el link"));
        }
        if(vista === "recovery"){
          trabajando("Guardando...");
          return PathSync.setPassword(pass).then(adentro)["catch"](fallo("No pude cambiarla"));
        }

        trabajando("Entrando...");
        PathSync.signIn(mail, pass).then(adentro)["catch"](function(e){
          /* GoTrue contesta igual para mail inexistente y contrasena
             equivocada, a proposito: no se inventa cual de las dos fue. */
          var t = (e.message || "").toLowerCase();
          pintar(t.indexOf("invalid") >= 0
            ? "Ese mail y esa contraseña no coinciden. Si nunca creaste la cuenta, créala."
            : "No pude entrar: " + (e.message || "prueba de nuevo"));
        });
      }

      return {
        render: function(c, o){
          cont = c; op = o || {};
          if(o && o.vista) vista = o.vista;
          pintar("");
        },
        irA: function(v){ vista = v; pintar(""); },
        vista: function(){ return vista; },
        mensaje: function(m){ pintar(m); }
      };
    })(),

    /* --------------------------------------------------- alta pendiente

       Nombre y consentimiento elegidos al registrarse, guardados hasta
       que haya sesion. Con confirmacion de mail eso puede tardar minutos
       y en el medio la persona cierra la pestana. */
    guardarAltaPendiente: function(datos){
      set("snowpath/v1/alta", JSON.stringify(datos));
    },

    tomarAltaPendiente: function(){
      var raw = get("snowpath/v1/alta");
      if(!raw) return null;
      del("snowpath/v1/alta");
      try{ return JSON.parse(raw); }catch(e){ return null; }
    },

    /* --------------------------------------------------- perfiles locales
       Las dos páginas comparten perfil. Las reglas de guardado y de PIN
       viven acá una sola vez: si cada página tuviera las suyas, alcanzaría
       con que una cambiara el formato para que la otra dejara de reconocerte. */
    store: (function(){
      var K_PROFILES = "snowpro-path/v1/profiles";
      var K_SESSION  = "snowpro-path/v1/session";
      var K_LEGACY   = "snowpro-path/v1/done";
      var cache = null;

      /* El PIN separa perfiles en una computadora compartida. No cifra nada,
         y la pantalla que lo pide lo dice con esas palabras. */
      function hash(pin, salt){
        var h = 2166136261, str = salt + "|" + pin, i;
        for(i=0;i<str.length;i++){ h ^= str.charCodeAt(i); h = (h * 16777619) >>> 0; }
        return h.toString(16);
      }
      function salt(){ return Math.random().toString(36).slice(2, 10); }
      function id(){ return "p" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }

      function load(){
        var raw = get(K_PROFILES), parsed, out = {}, k, p;
        if(!raw){ cache = {}; return cache; }
        try{ parsed = JSON.parse(raw) || {}; }catch(e){ parsed = {}; }
        for(k in parsed){
          p = parsed[k];
          if(!p || !p.name) continue;
          // se conserva el objeto entero: cada página guarda sus propias
          // claves acá y reconstruirlo campo por campo las borraba
          p.id = k;
          p.name = String(p.name);
          p.salt = String(p.salt || "");
          p.hash = String(p.hash || "");
          if(!p.done || typeof p.done !== "object") p.done = {};
          if(!p.quiz || typeof p.quiz !== "object") p.quiz = { wrong: {} };
          p.doneAt = p.doneAt || "";
          out[k] = p;
        }
        cache = out;
        return cache;
      }
      function all(){ return cache || load(); }
      function save(){ return set(K_PROFILES, JSON.stringify(all())); }

      function sessionId(){
        var sid = get(K_SESSION);
        return (sid && all()[sid]) ? sid : null;
      }
      function active(){
        var sid = sessionId();
        return sid ? all()[sid] : null;
      }
      function setActive(pid){
        if(pid) set(K_SESSION, pid); else del(K_SESSION);
      }
      function list(){
        var out = [], k;
        for(k in all()) out.push(all()[k]);
        out.sort(function(a, b){ return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1; });
        return out;
      }
      function nameTaken(name){
        var l = list(), i;
        for(i=0;i<l.length;i++){ if(l[i].name.toLowerCase() === name.toLowerCase()) return true; }
        return false;
      }
      /* Lo que se guardo antes de que existiera este perfil.
         clave plana -> campo del perfil. Cada modulo lee su campo
         cuando hay perfil y su clave cuando no, asi que sin esto un
         perfil recien creado empieza en blanco y tapa lo anterior.
         'visto' no esta a proposito: el saludo del dia es de este
         navegador, no de quien lo usa. */
      var LOCALES = [
        ["datachinchilla/v1/onboarding", "onb"],
        ["datachinchilla/v1/plan",       "plan"],
        ["datachinchilla/v1/practica",   "practica"],
        ["datachinchilla/v1/dias",       "dias"],
        ["datachinchilla/v1/cursos",     "cursos"]
      ];
      /* 'guia' no esta y no tiene que estar: el recorrido guiado es
         de este navegador, igual que 'visto'. Reclamarlo borraba la
         clave suelta, y en la carga siguiente en la que el perfil no
         estuviera activo todavia la guia volvia a empezar de cero. */

      /* Se copia primero, se guarda, y recien ahi se borra el
         original: si el guardado falla -cuota llena- el dato sigue
         donde estaba y no se perdio nada. */
      function reclamarLocal(p){
        var tomadas = [], i, raw, dato;
        for(i=0;i<LOCALES.length;i++){
          if(p[LOCALES[i][1]] !== undefined) continue;
          raw = get(LOCALES[i][0]);
          if(!raw) continue;
          try{ dato = JSON.parse(raw); }catch(e){ continue; }
          if(!dato || typeof dato !== "object") continue;
          p[LOCALES[i][1]] = dato;
          tomadas.push(LOCALES[i][0]);
        }
        if(!tomadas.length) return 0;
        if(!save()) return 0;
        /* La copia suelta NO se borra, a proposito.
           Onb.cargar() y Plan.cargar() leen el perfil solo si hay uno
           activo. Si el puntero de sesion se pierde, la copia del
           perfil no se lee, y si ademas borre la suelta no queda
           nada: desde afuera se ve como que se perdieron la ruta, la
           semana y la agenda. Una copia vieja es mejor que ningun
           dato. */
        return tomadas.length;
      }

      function create(name){
        var sl = salt();
        var p = { id: id(), name: name, salt: sl, hash: "", done: {}, quiz: { wrong: {} } };
        all()[p.id] = p;
        reclamarLocal(p);
        return p;
      }
      function setPin(p, pin){ p.salt = salt(); p.hash = hash(pin, p.salt); }
      function checkPin(p, pin){ return hash(pin, p.salt) === p.hash; }

      /* avance guardado antes de que existieran los perfiles */
      function claimLegacy(p){
        var raw = get(K_LEGACY), n = 0, i, arr;
        if(!raw) return 0;
        try{
          arr = JSON.parse(raw);
          if(Object.prototype.toString.call(arr) === "[object Array]"){
            for(i=0;i<arr.length;i++){ p.done[arr[i]] = true; n++; }
          }
        }catch(e){ n = 0; }
        del(K_LEGACY);
        return n;
      }

      return {
        load: load, all: all, save: save, list: list,
        active: active, sessionId: sessionId, setActive: setActive,
        nameTaken: nameTaken, create: create, setPin: setPin, checkPin: checkPin,
        newId: id, claimLegacy: claimLegacy, reclamarLocal: reclamarLocal
      };
    })(),

    /* ----------------------------------------- cursos compartidos
       Un mismo curso aparece en varias rutas. La marca viaja con el
       curso, no con la ruta: la clave la pone el nodo en su campo
       "mismo". Un nivel de Data Engineer no entra acá, porque un
       nivel junta varios recursos y terminarlo no dice cuál hiciste. */
    cursos: (function(){
      var K = "datachinchilla/v1/cursos";

      function leer(){
        var perfil = PathSync.store.active();
        if(perfil) return perfil.cursos || {};
        try{ return JSON.parse(get(K) || "{}") || {}; }catch(e){ return {}; }
      }

      function marcar(clave, hecho){
        if(!clave) return false;
        var mapa = leer(), perfil = PathSync.store.active();
        /* false explícito: "ausente" queda reservado para el curso
           que nunca se tocó, que es lo que permite migrar avance viejo */
        mapa[clave] = !!hecho;
        if(perfil){ perfil.cursos = mapa; return PathSync.store.save(); }
        return set(K, JSON.stringify(mapa));
      }

      function hecho(clave){ return !!(clave && leer()[clave]); }

      /* undefined = nunca se tocó · true = hecho · false = desmarcado */
      function estado(clave){ return clave ? leer()[clave] : undefined; }

      return { leer: leer, marcar: marcar, hecho: hecho, estado: estado };
    })(),

    /* --------------------------------------------------- reglas puras */
    ts: function(v){ var t = v ? Date.parse(v) : 0; return isNaN(t) ? 0 : t; },

    /* Unión de dos mapas de marcas. Se usa para los hitos: perder
       avance es caro, así que lo marcado en cualquier lado queda. */
    union: function(a, b){
      var out = {}, k;
      for(k in (a || {})){ if(a[k]) out[k] = true; }
      for(k in (b || {})){ if(b[k]) out[k] = true; }
      return out;
    }
  };
})();
