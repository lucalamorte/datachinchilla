# DataChinchilla · Roadmap

> Documento vivo. Cada ítem dice **qué es**, **qué verifiqué** y **qué falta
> decidir**. Antes de escribir acá, se chequea contra lo que ya existe: la
> mitad de esta lista resultó estar a medias, no ausente.

Última revisión: 31 de agosto de 2026.

---

## P0 · Rompe la promesa del producto

### 1. Control por tema antes de marcar un nivel

Sin esto marcás todo como completado, bajás el certificado y la ruta no
significa nada.

**Estado verificado, y es peor de lo que parecía:**

| Ruta | Control por tema | Qué pasa hoy |
|---|---|---|
| SnowPro Core | Sí, existe `NODE_Q` con preguntas por hito | Funciona |
| Data Engineer | **No** | `requestMark()` marca directo, sin preguntar nada |
| CS50 | **No** | Ni siquiera tiene la función |

**Qué falta:** escribir el banco de preguntas por nivel para Data Engineer
(6 niveles) y CS50 (11 cursos), y portar el gate que ya funciona en SnowPro.
Es el mismo mecanismo, lo que falta es contenido.

**Y una corrección al gate que ya existe:** cada pregunta tiene que explicar
el concepto, se haya acertado o no. Acertar un multiple choice no prueba que
entendiste el tema. En el Data Interview Gym ya está resuelto con un banco de
conceptos aparte y una pestaña "El concepto" en la corrección. Ese patrón hay
que traerlo también acá.

**A decidir:** cuántas preguntas por nivel y cuántas hay que acertar para
habilitar la marca. En SnowPro el criterio actual es reintentable sin límite.

### 2. Los certificados quedaron mal

La tarjeta del certificado oficial que armé no sirve. **Sacarla.**

**Qué queda:** solo el certificado de completar la ruta, el mío.

**Qué pasa con la info oficial:** no desaparece, pero deja de ser una tarjeta
con forma de certificado. Se convierte en una aclaración de texto: quién lo
emite, qué cuesta, qué requisitos pide y el link. Los datos ya están
verificados contra las páginas oficiales.

| Ruta | Credencial | Precio | Requisito |
|---|---|---|---|
| SnowPro Core | Snowflake COF-C03 | USD 175 por intento | 6 meses de experiencia sugeridos |
| CS50 | CS50 Certificate | Gratis | 70% o más en cada entrega |
| Data Engineer | freeCodeCamp Relational Databases | Gratis | 5 proyectos, ~300 horas |

### 3. El tema claro es inusable

El oscuro está cuidado y el claro es una resta de contraste. Hoy es
inaceptable en las cuatro páginas de DataChinchilla.

**Ya hay una referencia que funciona:** la paleta clara del Data Interview
Gym, con fondo con temperatura, degradado suave, texto bien oscuro y
superficies que se despegan del fondo. Hay que portar ese criterio.

---

## P1 · Posicionamiento y crecimiento

### 4. Reposicionar: no es solo para empezar

Hoy la página le habla a quien arranca. Tiene que hablarle también al data
engineer con experiencia que quiere mejorar.

**La promesa nueva:** el lugar donde está **todo el contenido gratis de
internet**, ordenado. No un curso, un índice curado.

Toca los títulos, los leads y la descripción de las cuatro páginas.

### 5. Landing propia

Una página de entrada con el posicionamiento completo: para quién es, qué
resuelve, por qué está ordenado así, qué se llevan. Hoy la entrada es la
ruta de Data Engineer, que ya asume que sabés qué buscás.

### 6. Que los usuarios sumen contenido

Lo más importante del proyecto a mediano plazo. Si la comunidad no
retroalimenta el catálogo, se envejece solo.

**Hay que pensarlo.** Opciones sobre la mesa, de menos a más trabajo:

1. Un formulario que caiga en un mail o una planilla, y yo curo a mano.
2. Un issue template en un repo público de GitHub, con el catálogo versionado.
3. Envío desde la propia página, guardado en Supabase, con estado
   pendiente / aprobado y una vista de moderación.

La 2 tiene una ventaja fuerte: el catálogo ya se genera con
`build-catalog.py`, así que versionarlo en GitHub hace que sumar contenido
sea un pull request. Cuesta poco y da trazabilidad.

**A decidir:** cuál de las tres, y si el que sugiere queda acreditado en el
catálogo.

### 7. Comunidad

**Recomendación:** empezar por **Discord**, y sumar Reddit solo si hay
volumen.

El motivo es que Discord sirve para un grupo chico y activo desde el día uno,
mientras que un subreddit vacío se ve muerto y cuesta mucho arrancarlo. Un
servidor con tres canales alcanza: sugerencias de contenido, dudas de las
rutas, y quién aprobó qué certificación.

LinkedIn ya es el canal natural para llegar, porque es donde está la
audiencia de datos en español.

---

## P2 · Alcance

### 8. Inglés

Traducir las cuatro páginas. **Regla que se define ahora:** los simulacros y
el repaso activo van en el idioma de la página. Página en español, preguntas
en español. Página en inglés, preguntas en inglés.

Esto obliga a que el banco de preguntas tenga las dos versiones desde el
diseño, no como un parche. Aplica igual al Data Interview Gym.

### 9. Ruta de Data Science y AI

**Por qué está bloqueada, verificado:** los cinco links de CognitiveClass que
pasaste **nunca se guardaron**. Aparecen mencionados en la descripción de la
tarjeta, en prosa, pero no hay ni una URL en el código. Está bloqueada
porque no existe la página ni el material cargado.

**Qué falta:** que me vuelvas a pasar los cinco links, y armo la ruta con su
mapa igual que las otras.

### 10. Armar la ruta desde tu CV — HECHO (3 de septiembre de 2026)

Está en `cv.html`. Pegas el CV o lo sueltas como PDF, eliges uno de
los cinco puestos, y sale la lista corta de lo que te falta.

**Cómo quedaron las tres decisiones que este ítem planteaba:**

1. **Qué pasa con el archivo.** Nunca sale del navegador. El PDF se lee
   con pdf.js del lado del cliente y el texto se cruza contra
   `temas.js` ahí mismo. No hay subida, no hay servidor, no hay nada
   que guardar ni que borrar, así que tampoco hace falta pedir
   consentimiento. La página lo dice y propone comprobarlo cortando
   internet.
2. **Quién detecta los huecos.** El cuestionario, en la versión de
   reglas: se cuentan señales distintas por tema (un CV que dice
   "SQL, Postgres, BigQuery" dice más que uno que dice "SQL"), y hay
   una tabla de implicaciones para no ofrecerle el curso de
   principiantes a alguien con oficio. Cuesta cero y no inventa.
3. **Contra qué se compara.** Acá estaba el trabajo real y ahora
   existe: `build-temas.py` define quince temas, sus señales de CV y
   cinco puestos con cuánto pide cada uno de cada tema. Los puestos
   son los mismos del gimnasio de entrevistas a propósito.

**Lo que el trabajo dejó a la vista:** MLOps no tiene un solo paso en
todo el catálogo, y ML Engineer lo pide como su día a día. La página
lo dice en vez de esconderlo ("tenemos el 83% del temario"), pero es un
hueco de contenido real. Visualización tiene tres pasos para algo que
Data Analyst pide al máximo.

---

### 11. El análisis del CV con IA (el paso pago)

Lo de arriba arma el path gratis y sin backend. Esto es la otra mitad:
un análisis de verdad del CV, que es lo que se puede cobrar.

**Qué haría que no hace el motor de reglas:** leer la experiencia y no
las palabras. El motor ve "Airflow" y marca pipelines; no puede ver que
alguien orquestó tres DAGs de juguete y otro sostiene doscientos. Un
modelo sí puede decir qué falta *contar mejor*, qué hueco te van a
buscar en la entrevista y cómo se lee tu CV para el puesto que
quieres.

**Cómo:** Edge Function de Supabase con la key del lado del servidor.
La key nunca puede estar en la página.

**A decidir antes:**

- **Qué pasa con el archivo, otra vez.** Acá sí viaja. Eso cambia
  todo lo del punto 1 de arriba: hay que decir qué se manda, qué se
  guarda, por cuánto tiempo, y pedir consentimiento explícito.
- **Cuánto sale y quién paga.** Cada análisis cuesta plata desde el
  primer usuario anónimo. O se cobra, o se limita por cuenta, o las
  dos cosas.
- **Validar antes de construir.** Conviene saber si alguien lo pagaría
  antes de escribir la Edge Function.

**Dependencia:** el path gratis tiene que estar andando y con gente
usándolo. Sin eso no hay a quién cobrarle.

---

### 10b. Notas viejas de este ítem, por si sirven


Subís el CV, elegís el puesto al que apuntás, y la página arma una ruta con
lo que te falta en vez de darte el catálogo entero.

**Por qué vale la pena:** hoy el sitio ordena contenido, pero sigue siendo el
usuario el que decide qué necesita. Esto lo invierte. Y encaja con lo que ya
existe: el cross-listing permite que un mismo curso viva en varias rutas, así
que una ruta armada a medida es una selección sobre lo que ya está cargado,
no material nuevo.

**Lo que ya está y sirve de base:**

- Los cursos con su duración real, su emisor y qué credencial dejan.
- El Data Interview Gym tiene cuatro roles definidos con sus temas, que es
  media definición de "posición a la que apuntás".
- Las tablas de usuarios y eventos de Supabase, para guardar el resultado.

**A decidir antes de escribir una línea:**

1. **Qué pasa con el archivo.** Un CV tiene nombre, teléfono, mail y a veces
   dirección, de una persona que no soy yo. Lo más limpio es procesarlo en el
   navegador y no subirlo nunca; si tiene que ir a un servidor, hay que
   decir qué se guarda, por cuánto tiempo y cómo se borra, y pedir
   consentimiento explícito y separado del de marketing.
2. **Quién detecta los huecos.** Un modelo de lenguaje leyendo el CV es lo
   directo, y tiene costo por uso y riesgo de inventar. La alternativa es un
   cuestionario de veinte preguntas que da un resultado parecido, cuesta
   cero y no pide subir nada. Conviene probar la segunda primero.
3. **Contra qué se compara.** Hace falta una definición de cada puesto: qué
   temas pide y con qué profundidad. Eso hoy no existe escrito en ningún
   lado, y es el trabajo de fondo. Sin eso, cualquiera de las dos opciones
   devuelve algo genérico.

**Dependencia real:** el punto 3 es el que manda. Definir los puestos es lo
que hace que esto sirva; el resto es interfaz.

---

## Pendientes de infraestructura

- **Supabase.** Correr los cuatro SQL, activar el magic link, autorizar las
  URLs de redirect y pasarme la URL del proyecto y la anon key. Hasta
  entonces el login por mail y la sincronización están escritos y sin probar
  contra un servidor real.
- **Recordatorios por mail.** Depende de lo anterior más un proveedor de correo.
- **Study Guide del C03.** Hace falta para recuperar los pesos por dominio.

---

## Fuera de este roadmap

**Data Interview Gym** va aparte por ahora, en su propia carpeta y con su
propio spec. Se fusiona más adelante. Lo único que ya comparte es el
criterio del tema claro, que salió bien ahí primero.

---

## Cosas que revisé y estaban bien

No todo lo que parecía roto lo estaba. Queda anotado para no volver a
revisarlo:

- **CS50 no está vacío.** Tiene sus once cursos en orden, en cuatro actos,
  con su mapa y sus enlaces. Si viste otra cosa, decime en qué pantalla.
- **DataExpert no está caído.** El bootcamp con certificado cerró el 31 de
  julio de 2026, pero todos los links del sitio apuntan al handbook de
  GitHub, que sigue vivo y gratis.
- **Los links de los certificados responden.** Los cuatro dan 200.
