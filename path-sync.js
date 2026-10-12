/* ============================================================
   path-sync.js
   Capa de sesión y sincronización contra Firebase, compartida por
   todas las páginas del sitio. Acá vive una sola vez todo lo que
   toca la red: entrar, refrescar el token, leer y escribir.

   Era Supabase. El proyecto se borró, así que se cambió la capa de
   red y nada más: los veintinueve nombres que exporta PathSync y sus
   contratos son los mismos, y por eso ninguna página cambió una
   línea.

   Sin claves cargadas, PathSync.isOn() devuelve false y ninguna
   página intenta nada: siguen funcionando con perfiles locales, que
   es como está el sitio hasta que haya proyecto nuevo.

   Sin SDK, a propósito: la librería de Firebase pesa más que este
   archivo entero para hacer lo que hacen cuatro fetch.

   La apiKey es pública por diseño y viaja en el navegador: lo que
   protege los datos son las reglas de Firestore, no esconderla.
   ============================================================ */
var PathSync = (function(){
  "use strict";

  var KEY_SESSION = "snowpro-path/v1/cloud";
  var cfg = { apiKey: "", projectId: "", googleClientId: "" };
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
      var m = /[?&]reset(?:=([^&]*))?/.exec(window.location.search);
      if(!m) return;
      /* ?reset pregunta; ?reset=ya borra directo. La segunda existe
         para poder verificar esto con un navegador automatizado, que
         rechaza los dialogos solo. */
      if(m[1] !== "ya" &&
         !window.confirm("Se borra todo lo que guardaste en este navegador " +
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

  /* Las dos APIs de Firebase que se usan. Identity Toolkit autentica
     y se identifica con la apiKey en la query; Firestore guarda y se
     identifica con el token de la persona en la cabecera. */
  var AUTH_API  = "https://identitytoolkit.googleapis.com/v1/";
  var TOKEN_API = "https://securetoken.googleapis.com/v1/token";
  function fsBase(){
    return "https://firestore.googleapis.com/v1/projects/" + cfg.projectId +
           "/databases/(default)/documents";
  }

  function load(){
    try{
      var raw = get(KEY_SESSION);
      ses = raw ? JSON.parse(raw) : null;
    }catch(e){ ses = null; }
  }
  function save(){
    return ses ? set(KEY_SESSION, JSON.stringify(ses)) : del(KEY_SESSION);
  }

  /* Nunca asume que la respuesta es JSON: un error de infraestructura
     contesta HTML y parsearlo escondería la causa real. */
  function pedir(url, opts){
    opts = opts || {};
    return fetch(url, {
      method: opts.method || "GET",
      headers: opts.headers || { "Content-Type": "application/json" },
      body: opts.body ? JSON.stringify(opts.body) : undefined
    })["catch"](function(){
      throw new Error("no pude contactar al servidor, revisa tu conexión");
    }).then(function(r){
      return r.text().then(function(txt){
        var data = null;
        if(txt){ try{ data = JSON.parse(txt); }catch(e){ data = null; } }
        if(!r.ok) throw new Error(mensajeDe(data, r.status));
        return data;
      });
    });
  }

  /* Firebase contesta con códigos en inglés y en mayúsculas. Dejarlos
     pasar tal cual sería mostrarle "EMAIL_NOT_FOUND" a alguien que
     solo se equivocó de mail. */
  var DICE = {
    EMAIL_EXISTS: "ese mail ya tiene cuenta",
    EMAIL_NOT_FOUND: "ese mail no tiene cuenta",
    INVALID_PASSWORD: "la contraseña no es ésa",
    INVALID_LOGIN_CREDENTIALS: "el mail o la contraseña no son ésos",
    USER_DISABLED: "esa cuenta está deshabilitada",
    WEAK_PASSWORD: "la contraseña tiene que tener al menos seis caracteres",
    INVALID_EMAIL: "ese mail no parece un mail",
    EXPIRED_OOB_CODE: "el link venció, pedí uno nuevo",
    INVALID_OOB_CODE: "el link no sirve, pedí uno nuevo",
    TOO_MANY_ATTEMPTS_TRY_LATER: "demasiados intentos, probá de nuevo en un rato",
    OPERATION_NOT_ALLOWED: "esa forma de entrar no está activada en el proyecto"
  };
  function mensajeDe(data, status){
    var m = data && data.error && data.error.message;
    if(!m) return "el servidor respondió " + status;
    var corto = String(m).split(" : ")[0];
    return DICE[corto] || corto;
  }

  function authCall(metodo, cuerpo){
    return pedir(AUTH_API + metodo + "?key=" + encodeURIComponent(cfg.apiKey),
                 { method: "POST", body: cuerpo });
  }

  function ensureFresh(){
    if(!ses) return Promise.reject(new Error("no hay sesión"));
    if(ses.expires_at - 60 > nowSec()) return Promise.resolve();
    if(!ses.refresh_token) return Promise.reject(new Error("la sesión venció, entra de nuevo"));
    /* Este es el unico endpoint de Firebase que no habla JSON: pide
       el cuerpo como formulario. Por eso va con fetch directo y no
       con pedir(), que serializa JSON. */
    return fetch(TOKEN_API + "?key=" + encodeURIComponent(cfg.apiKey), {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "grant_type=refresh_token&refresh_token=" +
            encodeURIComponent(ses.refresh_token)
    })["catch"](function(){
      throw new Error("no pude contactar al servidor, revisa tu conexión");
    }).then(function(r){
      return r.text().then(function(txt){
        var d = null;
        if(txt){ try{ d = JSON.parse(txt); }catch(e){ d = null; } }
        if(!r.ok || !d || !d.id_token){
          /* Un refresh que no sirve es una sesion que se termino, y
             hay que decirlo: dejarla a medias hace que el siguiente
             guardado falle en silencio. */
          ses = null; save();
          throw new Error("la sesión venció, entra de nuevo");
        }
        ses.access_token = d.id_token;
        ses.refresh_token = d.refresh_token || ses.refresh_token;
        ses.expires_at = nowSec() + (parseInt(d.expires_in, 10) || 3600);
        save();
      });
    });
  }

  /* Identity Toolkit devuelve lo mismo en alta, login y canje de
     Google: una sola funcion para guardarlo evita que cada camino
     invente su propia forma. */
  function guardarSesion(d, email){
    ses = {
      access_token: d.idToken || "",
      refresh_token: d.refreshToken || "",
      expires_at: nowSec() + (parseInt(d.expiresIn, 10) || 3600),
      user_id: d.localId || "",
      email: d.email || email || ""
    };
    save();
    return ses;
  }

  function fetchUser(){
    return authCall("accounts:lookup", { idToken: ses.access_token })
      .then(function(d){
        var u = (d.users && d.users[0]) || {};
        ses.user_id = u.localId || ses.user_id;
        ses.email = u.email || ses.email;
        save();
        return u;
      });
  }

  /* --------------------------------------------------- Firestore

     Firestore no guarda JSON: guarda valores con su tipo declarado.
     Estas dos funciones traducen en los dos sentidos, para que el
     resto del archivo siga hablando en objetos comunes. */
  function aFire(v){
    if(v === null || v === undefined) return { nullValue: null };
    if(typeof v === "boolean") return { booleanValue: v };
    if(typeof v === "number"){
      return (v % 1 === 0) ? { integerValue: String(v) } : { doubleValue: v };
    }
    if(Object.prototype.toString.call(v) === "[object Array]"){
      var arr = [], i;
      for(i=0;i<v.length;i++) arr.push(aFire(v[i]));
      return { arrayValue: { values: arr } };
    }
    if(typeof v === "object"){
      var campos = {}, k;
      for(k in v){ if(Object.prototype.hasOwnProperty.call(v, k)) campos[k] = aFire(v[k]); }
      return { mapValue: { fields: campos } };
    }
    return { stringValue: String(v) };
  }

  function deFire(f){
    if(!f) return null;
    if("nullValue" in f) return null;
    if("booleanValue" in f) return f.booleanValue;
    if("integerValue" in f) return parseInt(f.integerValue, 10);
    if("doubleValue" in f) return f.doubleValue;
    if("timestampValue" in f) return f.timestampValue;
    if("stringValue" in f) return f.stringValue;
    if("arrayValue" in f){
      var vals = (f.arrayValue && f.arrayValue.values) || [], out = [], i;
      for(i=0;i<vals.length;i++) out.push(deFire(vals[i]));
      return out;
    }
    if("mapValue" in f) return deFireCampos((f.mapValue && f.mapValue.fields) || {});
    return null;
  }
  function deFireCampos(campos){
    var out = {}, k;
    for(k in campos) out[k] = deFire(campos[k]);
    return out;
  }
  function aFireCampos(obj){
    var out = {}, k;
    for(k in obj){ if(Object.prototype.hasOwnProperty.call(obj, k)) out[k] = aFire(obj[k]); }
    return out;
  }

  function fsHeaders(){
    return { "Content-Type": "application/json",
             "Authorization": "Bearer " + (ses ? ses.access_token : "") };
  }

  /* Un documento, por su camino. Si no existe devuelve null en vez de
     reventar: "todavia no guardaste nada" no es un error. */
  function fsLeer(camino){
    return pedir(fsBase() + "/" + camino, { headers: fsHeaders() })
      .then(function(d){ return d && d.fields ? deFireCampos(d.fields) : null; })
      ["catch"](function(){ return null; });
  }

  /* PATCH con updateMask escribe sin pisar lo que no viene, que es lo
     que hacia el upsert con merge-duplicates. */
  function fsEscribir(camino, datos){
    var campos = aFireCampos(datos), mask = [], k;
    for(k in campos) mask.push("updateMask.fieldPaths=" + encodeURIComponent(k));
    return pedir(fsBase() + "/" + camino + (mask.length ? "?" + mask.join("&") : ""), {
      method: "PATCH", headers: fsHeaders(), body: { fields: campos }
    });
  }

  /* Y agregar sin pisar: las colecciones que solo crecen -eventos,
     consentimientos- no tienen un documento por persona que
     actualizar, cada registro es un hecho nuevo con su fecha. */
  function fsAgregar(coleccion, datos){
    return pedir(fsBase() + "/" + coleccion, {
      method: "POST", headers: fsHeaders(), body: { fields: aFireCampos(datos) }
    });
  }

  function mio(){ return "usuarios/" + (ses ? ses.user_id : ""); }

  return {
    /* --------------------------------------------------- arranque */
    /* Los nombres de los parametros quedan genericos a proposito: las
       paginas llaman configure(a, b, c) y no tienen por que saber de
       que proveedor son. */
    configure: function(apiKey, projectId, googleClientId){
      cfg.apiKey = apiKey || "";
      cfg.projectId = projectId || "";
      cfg.googleClientId = googleClientId || "";
      if(cfg.apiKey && cfg.projectId) load();
      return !!(cfg.apiKey && cfg.projectId);
    },
    isOn: function(){ return !!(cfg.apiKey && cfg.projectId); },
    session: function(){ return ses; },

    /* Guardar avance NO pide cuenta. Nunca.

       Esto decia `!!ses`: con la nube encendida, marcar un curso
       pedia cuenta. Con el proyecto de Supabase borrado eso dejo el
       sitio sin poder marcar nada, y arreglarlo "mientras no haya
       nube" era tratar el sintoma: el dia que se enciende la nube
       vuelve el mismo problema, y ahora con diez mil visitas por mes
       de las que casi ninguna tiene cuenta.

       La cuenta existe para una sola cosa, y es la que dice el cartel
       de la cuenta desde el principio: que tu avance te siga a otra
       computadora. El avance se guarda siempre en este navegador, y
       si ademas hay sesion, se sincroniza. Pedir cuenta para marcar
       no protege nada: solo impide guardar.

       Queda como funcion y no como `true` suelto porque es la
       pregunta que hacen veintiocho lugares, y el dia que haya una
       razon de verdad para negarse, se contesta aca y en ningun otro
       lado. */
    puedeGuardar: function(){ return true; },

    /* --------------------------------------------------- entrar */

    /* El link del mail y el de Google vuelven a la misma URL de la que
       salieron. Abierta como archivo local no hay a donde volver:
       location.origin es la cadena "null". */
    canReturn: function(){
      return location.protocol === "http:" || location.protocol === "https:";
    },

    signUp: function(email, password){
      return authCall("accounts:signUp", {
        email: email, password: password, returnSecureToken: true
      }).then(function(d){ return guardarSesion(d, email); });
    },

    signIn: function(email, password){
      return authCall("accounts:signInWithPassword", {
        email: email, password: password, returnSecureToken: true
      }).then(function(d){ return guardarSesion(d, email); });
    },

    /* Google sin SDK. Se va a Google por el id_token y despues se lo
       canjea en signInWithIdp; el canje lo hace captureHash al
       volver.

       El nonce queda guardado para comprobar que el token que vuelve
       es el de este pedido y no uno pegado a mano en la barra. */
    signInWithGoogle: function(){
      if(!cfg.googleClientId){
        return Promise.reject(new Error(
          "falta el client id de Google en la configuración del sitio"));
      }
      var nonce = Math.random().toString(36).slice(2) + nowSec();
      set("snowpro-path/v1/nonce", nonce);

      /* Google vuelve SIEMPRE a la raiz, no a la pagina donde
         estabas.

         No es un detalle: Google exige que cada redirect_uri este
         cargada a mano en las credenciales, una por una. Volviendo a
         la pagina de origen habria que cargar treinta paginas por
         cada dominio -produccion, pruebas y local-, o sea noventa
         URLs, y cada ruta nueva seria una mas que agregar y que
         alguien se va a olvidar.

         Volviendo a la raiz son tres. La pagina donde estabas queda
         guardada aca y captureHash te devuelve ahi despues de
         canjear el token. */
      set("snowpro-path/v1/volver", location.pathname + location.search);
      var vuelve = location.origin + "/";
      location.href = "https://accounts.google.com/o/oauth2/v2/auth" +
        "?client_id=" + encodeURIComponent(cfg.googleClientId) +
        "&response_type=id_token" +
        "&scope=" + encodeURIComponent("openid email profile") +
        "&redirect_uri=" + encodeURIComponent(vuelve) +
        "&nonce=" + encodeURIComponent(nonce) +
        "&prompt=select_account";
      return Promise.resolve(null);
    },

    /* Entrar con un link en vez de contrasena. Pide tener activado
       "Email link" en el proyecto; si no lo esta, Firebase lo dice y
       el mensaje llega tal cual al panel. */
    sendLink: function(email, app){
      if(location.protocol !== "http:" && location.protocol !== "https:"){
        return Promise.reject(new Error(
          "abriste la página como archivo local y el link del mail no tiene a dónde " +
          "volver. Sube la página a internet o levántala en un servidor y entra desde ahí."));
      }
      set("snowpro-path/v1/mail-link", email || "");
      return authCall("accounts:sendOobCode", {
        requestType: "EMAIL_SIGNIN",
        email: email,
        continueUrl: location.origin + location.pathname,
        canHandleCodeInApp: true
      });
    },

    sendReset: function(email){
      return authCall("accounts:sendOobCode", {
        requestType: "PASSWORD_RESET",
        email: email,
        continueUrl: location.origin + location.pathname
      });
    },

    /* La contrasena nueva, con el codigo que vino en el link. */
    setPassword: function(password){
      var codigo = get("snowpro-path/v1/oob") || "";
      if(!codigo) return Promise.reject(new Error("el link no sirve, pedí uno nuevo"));
      return authCall("accounts:resetPassword", {
        oobCode: codigo, newPassword: password
      }).then(function(d){
        del("snowpro-path/v1/oob");
        /* Cambiar la contrasena no deja sesion: se entra con la
           nueva, que ademas confirma que quedo bien guardada. */
        return authCall("accounts:signInWithPassword", {
          email: d.email, password: password, returnSecureToken: true
        });
      }).then(function(d){ return guardarSesion(d); });
    },

    hashType: function(){ return lastType; },

    /* Lo que vuelve en la URL: el id_token de Google, o el codigo de
       un link de mail. Las dos cosas se limpian de la barra apenas se
       leen, porque un token en el historial es un token regalado. */
    captureHash: function(onError){
      var hash = location.hash || "", busq = location.search || "";
      var limpio = location.origin + location.pathname;

      var mTok = /[#&]id_token=([^&]+)/.exec(hash);
      if(mTok){
        var nonce = get("snowpro-path/v1/nonce") || "";
        del("snowpro-path/v1/nonce");
        history.replaceState(null, "", limpio);
        lastType = "google";
        return authCall("accounts:signInWithIdp", {
          postBody: "id_token=" + mTok[1] + "&providerId=google.com",
          requestUri: limpio,
          returnIdpCredential: true,
          returnSecureToken: true,
          /* Google firma el nonce adentro del token; Firebase lo
             comprueba si se lo pasamos. */
          nonce: nonce || undefined
        }).then(function(d){
          guardarSesion(d);
          /* Y de vuelta a donde estabas. Google siempre devuelve a la
             raiz -ver signInWithGoogle- asi que sin esto, entrar
             desde una ruta te dejaba en la portada. */
          var pagina = get("snowpro-path/v1/volver") || "";
          del("snowpro-path/v1/volver");
          if(pagina && pagina !== location.pathname){
            location.replace(pagina);
          }
          return ses;
        })["catch"](function(e){ if(onError) onError(e.message || String(e)); return null; });
      }

      var mErr = /[#&]error=([^&]+)/.exec(hash);
      if(mErr){
        history.replaceState(null, "", limpio);
        if(onError) onError(decodeURIComponent(mErr[1]).replace(/\+/g, " "));
        return Promise.resolve(null);
      }

      var mModo = /[?&]mode=([^&]+)/.exec(busq);
      var mCod  = /[?&]oobCode=([^&]+)/.exec(busq);
      if(mModo && mCod){
        var modo = mModo[1], codigo = mCod[1];
        history.replaceState(null, "", limpio);
        if(modo === "resetPassword"){
          /* Se guarda para setPassword: el panel pide la contrasena
             nueva en otra pantalla, asi que el codigo tiene que
             sobrevivir a ese paso. */
          set("snowpro-path/v1/oob", codigo);
          lastType = "recovery";
          return Promise.resolve(null);
        }
        if(modo === "signIn"){
          lastType = "magiclink";
          var mail = get("snowpro-path/v1/mail-link") || "";
          del("snowpro-path/v1/mail-link");
          return authCall("accounts:signInWithEmailLink", {
            oobCode: codigo, email: mail
          }).then(function(d){ return guardarSesion(d, mail); })
            ["catch"](function(e){ if(onError) onError(e.message || String(e)); return null; });
        }
      }
      return Promise.resolve(null);
    },

    signOut: function(){
      /* Firebase no tiene "cerrar sesion" del lado del servidor para
         un token que ya se emitio: se vence solo en una hora. Lo que
         se tira es el refresh, que es lo que la mantiene viva. */
      ses = null;
      save();
      del("snowpro-path/v1/oob");
      return Promise.resolve(true);
    },

    ready: function(){ return ensureFresh(); },

    /* --------------------------------------------------- datos

       Las tablas eran una fila por persona; en Firestore eso es un
       documento por persona, colgado del suyo. */
    getRow: function(table){
      return fsLeer(mio() + "/datos/" + table);
    },

    upsertRow: function(table, row){
      return fsEscribir(mio() + "/datos/" + table, row);
    },

    insertRow: function(table, row){
      row.fecha = row.fecha || new Date().toISOString();
      return fsAgregar(mio() + "/" + table, row);
    },

    /* --------------------------------------------------- perfil y uso

       Todo lo de abajo es best-effort: si falla, la app sigue andando.
       Perder un evento de uso no puede romperle la práctica a nadie, y
       reintentarlo tampoco vale la pena. */

    guardarPerfil: function(datos){
      if(!ses) return Promise.resolve(false);
      return this.ready()
        .then(function(){ return fsEscribir(mio(), datos); })
        .then(function(){ return true; })
        ["catch"](function(){ return false; });
    },

    leerPerfil: function(){
      if(!ses) return Promise.resolve(null);
      return this.ready()
        .then(function(){ return fsLeer(mio()); })
        ["catch"](function(){ return null; });
    },

    /* Cada sí y cada no queda con su fecha. */
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
        if(sid) return all()[sid] || null;
        /* Sin puntero de sesion pero con un unico perfil, ese es. No
           es adivinar: no hay otra opcion posible, y la alternativa
           es mostrarle la pagina vacia a alguien que tiene todo
           guardado adentro. Con dos o mas no se toca nada, porque ahi
           si habria que elegir por el.

           Pasaba de verdad: reclamarLocal() borraba la copia suelta
           al pasarla al perfil, y si despues se perdia el puntero
           -otro navegador, la clave borrada, un perfil que quedo sin
           activar- el avance quedaba adentro sin que lo leyera
           nadie. */
        var solo = list();
        if(solo.length === 1){
          setActive(solo[0].id);
          return solo[0];
        }
        return null;
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
        ["datachinchilla/v1/cursos",     "cursos"],
        /* Lo armado a mano antes de tener cuenta. Sin esto, quien
           armó una ruta y después se hizo el perfil la veía
           desaparecer de la portada y del armador: el perfil vacío
           gana sobre la clave suelta. */
        ["custom-path/v1/anon",          "custom"],
        ["custom-path/v1/guardadas",     "customs"]
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
