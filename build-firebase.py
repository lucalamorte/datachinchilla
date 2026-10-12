# -*- coding: utf-8 -*-
u"""De Supabase a Firebase, sin cambiar las treinta paginas.

   El proyecto de Supabase se borro. Se cambia la capa que toca la
   red y nada mas: PathSync sigue exportando los mismos veintinueve
   nombres con los mismos contratos, asi que ninguna pagina cambia una
   linea de su JavaScript.

   QUE SE REEMPLAZA

     - La autenticacion, de GoTrue a Identity Toolkit (la API REST de
       Firebase Auth). Mail y contrasena, y Google.
     - Los datos, de tablas de Postgres a documentos de Firestore.

   QUE NO SE TOCA

     - store: los perfiles locales, que siempre fueron la fuente.
     - authUI: dibuja el panel llamando a signIn/signUp/etc, y esos
       nombres siguen existiendo.
     - cursos, ts, union: no tocan la red.

   SIN SDK, igual que antes. La libreria de Firebase pesa mas que
   todo este archivo para hacer lo que hacen cuatro fetch.

   GOOGLE SIN SDK es la unica parte que no es un fetch directo: se va
   a Google por el id_token y se lo canjea en accounts:signInWithIdp.
   Por eso hace falta un valor mas, el client id de OAuth, que
   Firebase crea solo al activar Google.

   EL MAPA DE DATOS. Las tablas eran una fila por persona; en
   Firestore eso es un documento por persona:

     usuarios                 ->  usuarios/<uid>
     <tabla> de getRow        ->  usuarios/<uid>/datos/<tabla>
     consentimientos, eventos ->  usuarios/<uid>/<coleccion>/<autoId>

   Las claves quedan vacias: hasta que haya proyecto, isOn() da false
   y el sitio funciona local, que es como esta hoy.

   Uso: python build-firebase.py
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "path-sync.js")

t = io.open(P, encoding="utf-8").read()
if u"identitytoolkit" in t:
    print(u"  ya estaba"); sys.exit(1)


# =========================================================== las entranas
A_INI = u"  function nowSec(){ return Math.floor(Date.now() / 1000); }"
A_FIN = u"  return {"
i, j = t.index(A_INI), t.index(A_FIN)

ENTRANAS = u'''  function nowSec(){ return Math.floor(Date.now() / 1000); }

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
    return pedir(TOKEN_API + "?key=" + encodeURIComponent(cfg.apiKey), {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: null,
      /* Este endpoint no acepta JSON. */
      _form: true
    }).then(function(d){ return d; })["catch"](function(){
      /* Se rehace a mano porque pedir() serializa JSON. */
      return fetch(TOKEN_API + "?key=" + encodeURIComponent(cfg.apiKey), {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "grant_type=refresh_token&refresh_token=" +
              encodeURIComponent(ses.refresh_token)
      }).then(function(r){ return r.json(); });
    }).then(function(d){
      if(!d || !d.id_token) throw new Error("la sesión venció, entra de nuevo");
      ses.access_token = d.id_token;
      ses.refresh_token = d.refresh_token || ses.refresh_token;
      ses.expires_at = nowSec() + (parseInt(d.expires_in, 10) || 3600);
      save();
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

'''
t = t[:i] + ENTRANAS + t[j:]


# ====================================================== los metodos publicos
B_INI = u"    /* --------------------------------------------------- arranque */"
B_FIN = u"    /* --------------------------------------------------- panel de acceso"
i, j = t.index(B_INI), t.index(B_FIN)

PUBLICOS = u'''    /* --------------------------------------------------- arranque */
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

    /* Guardar avance pide cuenta SI HAY NUBE. Un unico lugar que lo
       diga, para que no haya dos ideas distintas de que significa
       estar logueado repartidas por las paginas.

       Sin nube devuelve true: la cuenta existe para que tu avance te
       siga a otra computadora, y si no hay a donde sincronizar,
       pedirla no protege nada, solo impide guardar. */
    puedeGuardar: function(){ return !cfg.apiKey || !cfg.projectId || !!ses; },

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
      var vuelve = location.origin + location.pathname;
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
        }).then(function(d){ return guardarSesion(d); })
          ["catch"](function(e){ if(onError) onError(e.message || String(e)); return null; });
      }

      var mErr = /[#&]error=([^&]+)/.exec(hash);
      if(mErr){
        history.replaceState(null, "", limpio);
        if(onError) onError(decodeURIComponent(mErr[1]).replace(/\\+/g, " "));
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

'''
t = t[:i] + PUBLICOS + t[j:]


# ------------------------------------------------- la config y la cabecera
t = t.replace(u'  var cfg = { url: "", key: "" };',
              u'  var cfg = { apiKey: "", projectId: "", googleClientId: "" };', 1)

t = t.replace(
u'''   path-sync.js
   Capa de sesión y sincronización contra Supabase, compartida por
   las dos páginas del sitio. Acá vive una sola vez todo lo que
   toca la red: entrar por mail, refrescar el token, leer y escribir
   la fila de progreso.

   Sin claves cargadas, PathSync.isOn() devuelve false y ninguna
   página intenta nada: siguen funcionando con perfiles locales.

   La anon key es pública por diseño y viaja en el navegador.
   La service role NUNCA va acá.''',
u'''   path-sync.js
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
   protege los datos son las reglas de Firestore, no esconderla.''', 1)

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(u"path-sync.js: ahora habla Firebase, con la misma interfaz")
