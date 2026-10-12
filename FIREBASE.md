# Conectar el sitio a Firebase

El sitio funciona **sin nube**: todo lo que marcás vive en tu navegador.
La cuenta existe para una sola cosa — que tu avance te siga a otra
computadora — y mientras no haya proyecto, `PathSync.isOn()` devuelve
`false` y ninguna página intenta nada.

Esto es lo que hay que hacer para encenderla. Son tres valores al final.

---

## 1. El proyecto

En [console.firebase.google.com](https://console.firebase.google.com) →
**Agregar proyecto**. El nombre no importa; Google Analytics no hace
falta.

## 2. Las dos formas de entrar

**Authentication → Get started.**

| Método | Qué hay que hacer |
|---|---|
| **Email/Password** | Activarlo. Nada más. Anda en localhost y en producción sin configurar nada. |
| **Google** | Activarlo y elegir un mail de soporte. |

Después, **Authentication → Settings → Authorized domains**, agregar:

```
datachinchilla.com
pruebas.datachinchilla.pages.dev
```

`localhost` ya viene en la lista.

> **Esto es lo que falló en Supabase.** Si el dominio no está acá, el
> login de Google vuelve a `localhost` y da `ERR_CONNECTION_REFUSED`.

## 3. La base

**Firestore Database → Crear base de datos → modo producción**, región
la que te quede más cerca (`southamerica-east1` si estás en Argentina).

Modo producción quiere decir que nadie puede leer ni escribir hasta que
vos digas quién. Eso es el paso siguiente.

## 4. Las reglas

**Firestore → Rules**, pegar esto y publicar:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Cada quien, lo suyo y nada más. El id del documento es el uid
    // de Firebase, así que la regla es literalmente "sos vos".
    match /usuarios/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;

      match /{resto=**} {
        allow read, write: if request.auth != null && request.auth.uid == uid;
      }
    }
  }
}
```

**Esto no es opcional.** La `apiKey` es pública y viaja en el navegador
—así está diseñada—, así que lo único que separa los datos de una
persona de los de otra son estas reglas. Sin ellas, cualquiera con la
consola abierta lee todo.

## 5. Los tres valores

**Configuración del proyecto → Tus apps → Web (`</>`)**. Registrá la app
y copiá del snippet que te muestra:

- `apiKey`
- `projectId`

### El tercero: Google

Solo si querés ese botón. Va en **Google Cloud**, no en Firebase — pero
es el mismo proyecto:

```
https://console.cloud.google.com/apis/credentials?project=datachinchilla
```

En **ID de cliente de OAuth 2.0** vas a ver uno que dice **"Web client
(auto created by Google Service)"**. Ese lo creó Firebase solo cuando
activaste Google. Abrilo.

**Antes de copiar nada, agregale estas URLs**, porque Google rechaza
cualquier vuelta que no esté anotada a mano:

**Orígenes autorizados de JavaScript**
```
https://datachinchilla.com
https://pruebas.datachinchilla.pages.dev
http://localhost:8126
```

**URI de redireccionamiento autorizados**
```
https://datachinchilla.com/
https://pruebas.datachinchilla.pages.dev/
http://localhost:8126/
```

> **La barra final importa** y que sean solo tres también: el sitio
> vuelve siempre a la raíz y después te lleva solo a la página donde
> estabas. Si volviera a la página de origen habría que anotar las 30
> páginas por cada dominio — noventa URLs, y una más cada vez que se
> agrega una ruta.

Guardá, y recién ahí copiá el **ID de cliente**, que termina en
`.apps.googleusercontent.com`.

Los cambios en estas credenciales pueden tardar unos minutos en tomar
efecto. Si te dice `redirect_uri_mismatch`, es esto: esperá un rato o
revisá que la URL coincida **exacta**, barra incluida.

Con esos tres, en las 30 páginas:

```js
var CONFIG = {
  firebaseApiKey: "AIza...",
  firebaseProjectId: "datachinchilla-xxxx",
  googleClientId: "1234-abc.apps.googleusercontent.com"
};
```

No los pegues a mano treinta veces:

```bash
python build-claves.py AIza... datachinchilla-xxxx 1234-abc.apps.googleusercontent.com
```

---

## Cómo está armado

`path-sync.js` habla con Firebase por **REST, sin SDK**. La librería
pesa más que el archivo entero para hacer lo que hacen cuatro `fetch`.

| Lo que era en Supabase | Lo que es en Firebase |
|---|---|
| GoTrue (`/auth/v1/...`) | Identity Toolkit (`identitytoolkit.googleapis.com`) |
| Tabla `usuarios`, una fila por persona | Documento `usuarios/<uid>` |
| `getRow("x")` / `upsertRow("x", …)` | Documento `usuarios/<uid>/datos/x` |
| Tablas que solo crecen | Subcolecciones `usuarios/<uid>/eventos`, `…/consentimientos` |

**La interfaz de `PathSync` no cambió**: los mismos 29 nombres con los
mismos contratos. Por eso ninguna de las 30 páginas cambió una línea de
su JavaScript — solo los tres valores de arriba.

### Google sin SDK

Es la única parte que no es un `fetch` directo:

1. Se va a Google pidiendo un `id_token` (`response_type=id_token`), con
   un `nonce` que queda guardado.
2. Google vuelve con el token en el hash.
3. `captureHash()` lo canjea en `accounts:signInWithIdp` y limpia la
   barra de direcciones — un token en el historial es un token regalado.

### Si algo falla

Los errores de Firebase vienen en mayúsculas y en inglés
(`EMAIL_NOT_FOUND`, `INVALID_LOGIN_CREDENTIALS`). `path-sync.js` los
traduce antes de mostrarlos: nadie tiene que leer `WEAK_PASSWORD` cuando
lo que pasa es que la contraseña es corta.

Si ves **"esa forma de entrar no está activada en el proyecto"**, es el
paso 2.
