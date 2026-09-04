# Progreso en la nube, sobre tu proyecto de Supabase

La página funciona sin esto. Los perfiles locales con PIN siguen andando igual.
Esta guía agrega la opción de entrar con tu mail y que el avance te siga a
cualquier computadora.

Todo vive en **una sola tabla** del proyecto que ya tenés. No toca nada de lo que
haya adentro.

---

## 1. Crear la tabla

Abre el **SQL Editor** de tu proyecto y corre el archivo `supabase_snowpath.sql`
completo. Crea `public.snowpath_progress` con Row Level Security activa: cada
persona solo puede leer y escribir su propia fila.

Para confirmar que quedó bien, corre esto y fíjate en que `relrowsecurity` diga `true`:

```sql
select relname, relrowsecurity from pg_class where relname = 'snowpath_progress';
```

## 1 bis. Marcar de dónde viene cada cuenta

Corre también `supabase_snowpath_02_origen.sql`. Agrega tres columnas a la misma
tabla y deja escrito, por cada persona, si la cuenta nació entrando al path o si
ya existía en el proyecto por tu otra app.

Eso es lo que va a permitir separar las dos poblaciones el día que quieras mover
el path a un proyecto propio. Al final de ese archivo están las consultas listas
para ese momento.

El origen queda guardado en dos lugares a propósito: en la fila de progreso y en
la metadata de la cuenta (`raw_user_meta_data->>'app'`). Si alguien borra su
progreso, el rastro del origen sobrevive.

## 1 ter. Sumar la ruta de Data Engineer

Corré `supabase_snowpath_03_de.sql`. Agrega una columna `de` a la misma tabla,
donde la ruta de Data Engineer guarda sus hitos y sus días de práctica.

Las dos rutas comparten **una sola fila por persona**: el path de SnowPro escribe
en `done`, `quiz` y `done_at`, y la ruta de Data Engineer en `de`. Con un solo
login, las dos te siguen a cualquier computadora.

## 1 quater. Sumar el armador y el gimnasio

Corré `supabase_snowpath_04_custom.sql` y después `supabase_snowpath_05_gym.sql`.
El primero agrega la columna `custom`, donde vive la ruta que arma cada persona.
El segundo agrega `gym`, donde el Data Interview Gym guarda qué practicó y qué
falló.

Con esto quedan cinco columnas de avance en **una sola fila por persona**:
`done` y `quiz` para SnowPro, `de` para Data Engineer, `custom` para la ruta a
medida y `gym` para el gimnasio. El gimnasio hoy se ve como una app aparte, pero
comparte la fila desde el principio para que fusionarlos después no obligue a
migrar datos de nadie.

## 2. Habilitar el login por mail

En **Authentication → Providers → Email**, deja activado *Email* y encendé
*Magic Link*. No hace falta contraseña: la persona recibe un link y entra.

## 3. Autorizar la URL de la página

En **Authentication → URL Configuration**:

- **Site URL**: la dirección donde publiques la página.
- **Redirect URLs**: agrega esa misma dirección.

Sin este paso, el link del mail rebota. Si vas a probar en tu máquina antes de
publicar, agrega también la dirección local que uses.

## 4. Pegar las dos claves en las dos páginas

Arriba de todo del `<script>` de **cada página** está el bloque `CONFIG`. Van los
mismos dos valores en `index.html` y en `data-engineer.html`, porque son el mismo
proyecto y la misma fila:

```js
supabaseUrl: "https://TU-PROYECTO.supabase.co",
supabaseKey: "eyJhbGciOi...",   // la clave anon public, no la service role
```

Las dos salen de **Project Settings → API**. La `anon` es pública por diseño y
viaja en el navegador de cualquiera que entre: es la que corresponde acá. La
**service role nunca va en una página**, porque saltea todas las políticas de
seguridad.

Con esas dos líneas cargadas, aparece el botón de entrar con mail. Vacías, las
páginas se comportan exactamente como hoy, con perfiles locales.

En **Redirect URLs** hay que autorizar las dos direcciones, la de `index.html` y la
de `data-engineer.html`, porque el link del mail vuelve a la página desde donde
lo pediste.

### Un detalle de arquitectura

Todo lo que toca la red vive en `path-sync.js`, un archivo aparte que cargan las
dos páginas. Es a propósito: un cliente de autenticación duplicado en dos lugares
se separa con el primer cambio. Ese archivo tiene que viajar junto a los `.html`.

---

## Qué comparte con tu otro proyecto

Estás reusando un proyecto, así que conviene tenerlo presente:

- **Los usuarios son los mismos.** Quien entre al path aparece en `auth.users`,
  igual que los de tu otra app. Cada app lee sus propias tablas, así que no se
  cruzan los datos, pero sí la lista de cuentas.
- **Los usuarios activos suman al mismo plan.** El plan gratuito cuenta MAU por
  proyecto. Una página pública puede traer registros de gente que entra una vez.
- **La cuota es compartida.** El avance pesa bytes, pero la cuenta de MAU y los
  mails de login salen del mismo lugar.

Si en algún momento eso molesta, mover el path a su propio proyecto es cambiar
las dos líneas de `CONFIG` y correr el SQL en el proyecto nuevo.

---

## Cómo resuelve los conflictos

Si estudiaste en dos computadoras sin conectar:

- **Los hitos se suman.** Un hito marcado en cualquiera de las dos queda marcado.
  Nunca se pierde avance por sincronizar.
- **La fecha de finalización** se queda con la más vieja, que es cuando de verdad
  terminaste.
- **La lista de preguntas falladas** se queda con la del lado que tocaste más
  recientemente. Es una ayuda de estudio, no avance: perder una entrada no cuesta
  nada, y mantener las dos listas unidas haría que una pregunta ya dominada
  reapareciera para siempre.
