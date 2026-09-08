# Guion de prueba de DataChinchilla

Para pasárselo a un agente con navegador. Cada caso dice qué hacer y
qué tiene que pasar. Si algo no coincide, es un fallo: anota el caso,
lo que esperabas y lo que viste.

**Sitio:** <https://datachinchilla.com>

**Cómo saber qué versión estás probando:** abre
<https://datachinchilla.com/version.txt>. Devuelve el commit que está
publicado. Si reportas un fallo, incluí ese número: sin él no se sabe
si probaste lo de ahora o lo de ayer.

---

## Antes de empezar

El sitio guarda todo en el navegador. Para probar como alguien que
entra por primera vez, abre la consola (F12) y corre:

```js
localStorage.clear(); location.reload();
```

Hazlo antes de cualquier caso que diga **desde cero**. Sin eso vas a
estar probando sobre datos viejos y los resultados no valen.

También funciona agregar `?reset` a la dirección.

**Deja la consola abierta todo el tiempo.** Casi todos los fallos de
este sitio aparecieron primero como un error en rojo. Si ves uno,
cópialo aunque la página se vea bien.

---

## 1. La portada, sin haber hecho nada

**Desde cero.** Abre la portada.

Tiene que verse:

- El título "El camino completo para trabajar en tech"
- **Tres tarjetas y nada más**: "Empecemos por tu CV", "Ármala a mano",
  "O mira las 22 rutas"
- "Práctica diaria" con dos tarjetas (Python y SQL)
- El catálogo de rutas, con seis tarjetas y un botón para ver el resto
- Un globo de la chinchilla que dice "Hola, soy la chinchilla" y
  "Paso 1 de 9"

**No tiene que verse** el renglón de la agenda ni el bloque "Tu ruta":
quien no configuró nada no tiene agenda que mostrar.

---

## 2. El menú, en todas las páginas

Arriba a la derecha hay un botón de tres rayas. Ábrelo en la portada,
en `/cv`, en `/practica` y en una ruta cualquiera.

- Tiene ocho destinos: Inicio, Tu CV, Ármala a mano, Todas las rutas,
  Práctica diaria, Tu semana, Recursos, Preguntas
- **Marca dónde estás**: el destino de la página actual sale resaltado
- Cierra con Escape y con un clic afuera, no sólo con su botón

---

## 3. El recorrido guiado, entero

Es el caso más importante. **Desde cero.**

Sigue el globo tocando siempre su botón y anota el número de paso.
Tienen que salir los nueve, en este orden y en estas páginas:

| Paso | Dice | Dónde estás |
|---|---|---|
| 1 de 9 | Hola, soy la chinchilla | portada |
| 2 de 9 | Primero, cuéntame de ti | portada |
| 3 de 9 | ¿A dónde vas? | cv |
| 4 de 9 | Ahora sí, tu experiencia | cv |
| 5 de 9 | Esto ya lo sabes | cv |
| 6 de 9 | Y esto es lo que falta | cv |
| 7 de 9 | Ésta es tu ruta | una ruta |
| 8 de 9 | Acá se arma tu semana | semana |
| 9 de 9 | Listo, ésta es tu portada | portada |

En el paso 4 vas a tener que pegar un CV de verdad para poder seguir.
Usa el de la sección 14.

Entre el paso 6 y el 7 el globo no avanza solo: tienes que tocar
**"Guardarla y ver mi ruta"** en la página.

**Falla si:** el globo desaparece en alguna página y no vuelve. Es el
bug que más veces volvió. Anota en qué paso y en qué página.

**Falla si:** el globo aparece pegado a una esquina, flotando sobre el
contenido en vez de al lado de lo que hay que tocar.

### 3b. Salir del recorrido

- **No tiene que haber un botón "Saltear".** Si lo ves, es un fallo:
  se sacó a propósito, había dos salidas para lo mismo.
- La **cruz** de arriba a la derecha del globo tiene que **preguntar
  antes** de cerrar. Si cancelas, el globo sigue ahí.
- El botón **"Atrás"** vuelve al paso anterior, y si ese paso vive en
  otra página, te lleva a esa página.

### 3c. El botón de la interrogación

Arriba a la derecha hay un botón `?`. Pruébalo en **`/practica`**, que
no es la portada:

- **Desde cero**, te lleva a la portada y abre el recorrido en el paso
  2, saltando el saludo.
- **Con un CV ya cargado**, te lleva a `/cv`, que es donde el recorrido
  está de verdad, y el globo aparece ahí.

**Falla si:** no pasa nada al tocarlo, o si te deja en una página sin
globo. Ese era el bug: el botón era decorativo fuera de la portada.

---

## 4. El popup de la cuenta se puede cerrar

En **cada una** de estas páginas: portada, `/cv`, `/practica`,
`/semana` y una ruta cualquiera (`/dbt`).

Toca "Entrar" y prueba cerrarlo de tres formas:

1. La cruz del recuadro
2. Un clic afuera, sobre el fondo oscuro
3. La tecla Escape

**Las tres tienen que cerrarlo.**

---

## 5. El CV, paso por paso

**Desde cero.** Anda a `/cv`.

La página tiene **cinco pasos numerados**: El puesto, Tu experiencia,
Tus skills, Para afinar, Tu ruta.

### 5a. Los trece puestos

En el paso 1 hay **trece** puestos. Cada uno tiene tres cosas: el
nombre, qué hace, y **debajo de una línea, en qué se diferencia**.

| | |
|---|---|
| Data Engineer | Data Analyst |
| Data Scientist | ML Engineer |
| AI Engineer | Big Data Engineer |
| Cloud Engineer | Desarrollador Full Stack |
| Desarrollador Frontend | Desarrollador Backend |
| Desarrollador Web3 | QA / Tester |
| Analista funcional | |

**Falla si** alguno no tiene la línea de diferencia.

### 5b. El CV se lee y no se pierde

Elige **Data Engineer** y pega el CV de la sección 14.

Tiene que aparecer, en el paso 3, chips con los temas que reconoció,
cada uno con una **cruz** para sacarlo. Y en el paso 5, la ruta.

**Ahora lo que importa:** recarga la página (F5). El CV tiene que
**seguir ahí**, con el textarea lleno y el resultado abajo.

### 5c. Sacar y agregar temas

En el paso 3:

1. Anota el porcentaje que dice "Cubre el N%"
2. Toca la **cruz** de un chip. Desaparece y aparece abajo, bajo
   "Sacaste". **El porcentaje tiene que cambiar.**
3. Toca el chip tachado: vuelve arriba y el porcentaje se recalcula
4. Toca **"Agregar una que sepas"**. Se abre un panel con los temas
   que todavía no tienes. Elige uno: aparece arriba como chip, con
   **borde punteado** (es tuyo, no salió del CV), y el panel ya no lo
   ofrece.

Recarga: **lo que sacaste sigue sacado y lo que agregaste sigue
agregado.**

### 5d. Las preguntas, de a una

El paso 4 tiene **cinco** preguntas y muestra **una sola por vez**:

1. ¿Programas?
2. ¿Construiste algo que se vea en pantalla?
3. ¿Y del otro lado: APIs, servidores, bases?
4. ¿Trabajaste con datos para que otro decida?
5. ¿Nube e infraestructura?

- Arriba dice "1 de 5" y hay cinco puntos para saltar a cualquiera
- Al **contestar**, pasa sola a la siguiente
- Las flechas "Anterior" y "Siguiente" funcionan
- La opción elegida queda marcada con el color de acento

**Falla si** salen las cinco juntas, o si el título y la ayuda de la
pregunta aparecen pegados en el mismo renglón.

### 5e. La frase de privacidad

Abajo del paso 2 tiene que decir que **tu CV no se envía a ningún
servidor**, que se procesa en el navegador y que no se comparte.

**Falla si** dice "se lee acá, en tu navegador": era la redacción vieja.

---

## 6. Que cada puesto reciba su ruta

Este es el caso que más bugs encontró. **Desde cero para cada uno.**

En `/cv`, elige el puesto, pega el CV, y comprueba la ruta.

| Puesto | Pega esto | Tiene que recomendar |
|---|---|---|
| Cloud Engineer | `Sysadmin 4 anios. Linux, bash, algo de Python. Nunca use la nube ni contenedores.` | **Credenciales de nube** |
| QA / Tester | `Soporte 3 anios. Reporto bugs, escribo casos de prueba. Algo de SQL. No tengo experiencia en automatizacion.` | **Testing y QA** |
| Desarrollador Web3 | `Desarrollador React y Node. Nunca toque un contrato inteligente ni blockchain.` | **Web3** |
| Analista funcional | `Administrativo. Excel. No conozco Scrum ni BPMN ni SQL.` | **Analista funcional** |
| Data Analyst | `Analista de negocio. Excel y SQL en Postgres. No manejo ninguna herramienta de visualizacion ni tableros.` | **Visualización y BI** |
| ML Engineer | `Data scientist. Python, scikit-learn, entreno modelos. Estadistica y experimentos A/B. No puse ninguno en produccion.` | **MLOps** |

**Falla si** un puesto recibe la ruta de otro. Pasó: un sysadmin
recibía la ruta de testing porque esa ruta estaba etiquetada de más.

---

## 7. Las negaciones

El motor tiene que entender lo que **no** sabes. **Desde cero**, en
`/cv`, con el puesto Data Engineer, pega:

```
Analista con 4 anos. SQL en Snowflake y Postgres, stored procedures.
Modelado dimensional con dbt. Power BI para los tableros. Python con
pandas.

Lo que me falta: no tengo experiencia en Spark ni en Kubernetes.
Ganas de aprender machine learning en produccion.
```

En "Esto ya lo sabes" tienen que estar SQL, Modelado, Python,
Visualización. **No tienen que estar** Big data, Nube ni Machine
learning: el CV dice explícitamente que no los tiene.

**Falla si** aparece cualquiera de esos tres. Es el bug de las
negaciones: antes "no tengo experiencia en Spark" contaba igual que
"cinco años con Spark".

**Y la trampa al revés:** pega `No solo Python, tambien R.` Python
**sí** tiene que aparecer: "no solo" no es una negación.

---

## 8. Sumar y sacar rutas de tu semana

Se puede desde tres lugares y los tres tienen que coincidir.

- **Desde una ruta:** en `/dbt`, arriba, "Sumar a tu semana"
- **Desde el catálogo:** en la portada, cada tarjeta tiene su botón
- **Desde la semana:** en `/semana`, la lista con las 22 rutas

Cambia el estado desde cualquiera y verifica que los otros dos lo
muestren. **No hace falta tener CV cargado.**

---

## 9. La semana y la agenda

En `/semana`, con al menos una ruta activa: elige días, franja y
horas. Abajo se arma la semana con bloques concretos.

**Falla si** un día se llena de bloques chiquitos: el tope son **dos
bloques de estudio por día**.

### 9a. Todo esto, sin entrar con tu mail

Este es el caso que hay que hacer **primero**, y el que se saltó tres
veces: hacer el recorrido entero **sin cuenta**, en una ventana de
incógnito.

Antes, el último botón del CV -"Guardar mi ruta"- avisaba que hacía
falta una cuenta y volvía sin guardar nada. Sin rutas activas no hay
plan, sin plan no hay agenda, y la portada quedaba **igual que la de
alguien que nunca entró**. El widget de la agenda estaba puesto desde
hacía rato: lo que no existía era el plan.

**Falla si** después de guardar la ruta sin cuenta, la portada no
tiene agenda, o si el botón abre el cartel de la cuenta.

**Falla si** en `/semana` sumar o sacar una ruta pide cuenta.

La cuenta sigue haciendo falta para **marcar cursos y ejercicios**.
Eso es a propósito y no es un fallo.

Ahora vuelve a la portada. Tiene que verse, **sin scrollear**:

- Un renglón en el hero que dice **"Hoy: N horas"** con lo que toca, y
  un enlace "Ver la agenda"
- Más abajo, la agenda de los siete días, **antes** del bloque "Tu
  ruta"

**Falla si** hay que bajar dos pantallas para encontrar la agenda.

### 9b. Los bloques dicen algo útil

Mira los nombres de los bloques.

- Un paso que **entra en la semana** se numera: "parte 1 de 3",
  "parte 2 de 3", y se cierra
- Un paso que **no entra** no lleva número: dice el tamaño, por
  ejemplo "50 horas en total"

**Falla si** ves "parte 1 de 40", o si el mismo bloque dice "parte 1"
semana tras semana. El número no avanzaba entre semanas.

---

## 10. La práctica

Anda a `/practica`.

- Dos bancos: **Blind 75** (Python, 75 problemas) y **Consultas de
  entrevistas** (SQL, 64)
- Los enunciados abren en LeetCode y StrataScratch
- Hay **tres filtros** con su número: "Por hacer", "Resueltos",
  "Todos"

### 10a. De fácil a difícil, y punto

Mira el **primer** ejercicio que ofrece cada banco, en la portada y en
`/practica`, con la cuenta recién empezada.

- Blind 75 tiene que empezar por uno **fácil**
- Avanzando con las flechas, primero salen los **18 fáciles**, después
  los **51 medios**, y al final los **6 difíciles**
- Dentro de la misma dificultad va primero el más resuelto

**Falla si** aparece un medio primero y un difícil cuarto. La portada
recorría la lista en el orden del archivo, que arranca 128 medio, 1
fácil, 3 medio: no era al azar, pero se veía igual que al azar, y es
peor, porque parece que hay un criterio.

**Falla si** marcas "Lo resolví" y se tilda otro. La lista que se
pinta y la que usa el botón tienen que ser la misma.

**Marcar pide cuenta.** Sin haber entrado, tocar el tilde no marca
nada: tiene que aparecer el cartel de la cuenta.

Con cuenta, marca dos del mismo banco: aparece "El día está cerrado".

Toca **"Resueltos"**: salen sólo los que marcaste, y el número del
filtro coincide.

**Los vacíos:** busca "zzzz". Tiene que aparecer la chinchilla con una
lupa y un texto que diga qué hacer, no un renglón gris.

---

## 11. Los números coinciden

Compara el título de cada ruta con el contador de arriba.

| Ruta | Tiene que decir |
|---|---|
| `/cs50` | "Cuatro tramos, treinta y siete pasos" y "0/37" |
| `/dbt` | "Cuatro tramos, veintitrés pasos" y "0/23" |
| `/testing` | "Cuatro tramos, trece pasos" y "0/13" |
| `/mlops` | "Cuatro tramos, trece pasos" y "0/13" |
| `/nube` | "Cuatro tramos, nueve pasos" y "0/9" |
| `/visualizacion` | "Tres tramos, nueve pasos" y "0/9" |
| `/funcional` | "Cuatro tramos, diez pasos" y "0/10" |

**Falla si** el texto dice una cantidad y el contador otra.

Y al terminar una ruta, el botón grande dice **"Los N pasos"** con el
número de esa ruta. **Falla si** dice "Las quince partes": ése era el
número de Full Stack Open, heredado por copiar la página.

---

## 12. CS50, semana por semana

Anda a `/cs50`. Tiene **37 pasos**, no once cursos.

- Los primeros son **"CS50x · Semana 0 · Scratch"**, "Semana 1 · C",
  "Semana 2 · Arrays"… hasta "Semana 10" y el proyecto final
- Después las nueve semanas de Python y las siete de bases de datos
- Al final, ocho cursos enteros: Scratch, R, AI, Web, Cybersecurity,
  Games, Business y Law

**Falla si** algún paso dice sólo "CS50x" sin semana: eran los pasos
de sesenta horas que no se podían repartir en una agenda.

---

## 13. Marcar un curso

En `/dbt`, toca cualquier tarjeta. Se abre una hoja con el detalle.
Toca "Marcar como completado".

- El cartel de la chinchilla aparece **por encima** de la hoja
- El contador de arriba sube
- Cierra la hoja: la tarjeta queda marcada

Recarga: **la marca tiene que seguir.**

---

## 14. El CV de prueba

Pega esto tal cual donde el caso lo pida:

```
Data Engineer con 4 anos de experiencia.

Diseno y mantengo pipelines en Apache Airflow, con DAGs que corren a
diario para el area comercial y de producto.

Modelo el warehouse en dbt sobre Snowflake: capas staging, intermediate
y marts, con tests, documentacion y snapshots.

SQL avanzado: window functions, CTEs recursivas y optimizacion de
queries pesadas sobre tablas de miles de millones de filas.

Python para ETL, con pandas y pyspark.

AWS a diario: S3, Glue, Lambda y Redshift. Spark para los volumenes
que no entran en una maquina.

Git, CI/CD con GitHub Actions, Docker.
```

Con ese CV apuntando a **Data Engineer**, tiene que recomendar
**"Subir de nivel"**. Es la vara: si recomienda otra cosa o arma una
lista de cursos sueltos, es un fallo.

### 14b. El CV que no es de datos

**Desde cero**, en `/cv`, puesto **Desarrollador Full Stack**.

**Alguien que empieza:**

```
Estudiante de sistemas. Hice algo de programacion en la facultad, con
Java y un poco de algoritmos y estructura de datos. Manejo Git basico.
Arme dos paginas con HTML y CSS para practicar. Nunca trabaje de esto
y quiero dedicarme al desarrollo web.
```

Tiene que recomendar **"Full Stack Open"**.

**Alguien que ya trabaja de esto:**

```
Desarrollador con 3 anos de experiencia. Hago interfaces en React con
JavaScript y algo de TypeScript. Consumo APIs REST y armo formularios y
tablas. Uso HTML y CSS a diario, y Git para todo. Toque Node con
Express para un par de endpoints simples. No hice tests nunca.
```

Acá **no** tiene que recomendar una ruta entera: la respuesta correcta
es una lista corta con lo que le falta.

**Falla si** en cualquiera de los dos aparece una ruta de datos
—SnowPro Core, dbt, Big Data— como recomendación principal.

---

## 15. La ruta armada a mano

Anda a `/armar`.

- El catálogo tiene **343 niveles de las 22 rutas**, y los filtros de
  arriba listan las 22
- El texto dice "22 rutas" y el número de niveles, no un número viejo

Arma una ruta con cuatro niveles de rutas distintas y ponle nombre.
**Guardarla pide cuenta.**

Con cuenta, guárdala y vuelve a la portada: tiene que aparecer
**anclada al lado de la del CV**, con su propio color, sus niveles y
sus horas. Al tocarla, se abre en el armador.

En el catálogo de la portada, el filtro **"Tuyas"** tiene que
mostrarla.

---

## 16. Que nada prometa lo que no da

Esto es de leer, no de tocar. Abre `/airflow`, `/fullstack` y
`/testing`.

- **Ninguna** puede decir que sus cursos dejan "insignia de Anthropic":
  sólo la ruta de Claude da eso
- El botón "Ir al sitio de X" tiene que **llevar a X**. Fíjate en el
  texto y después en dónde caés.
- El pie de cada una dice qué es gratis y **dónde empieza a costar**.
  En `/nube` tiene que decir que los exámenes se pagan; en `/testing`,
  que el examen de ISTQB se paga y el sílabo no.

**Falla si** el botón dice un sitio y te lleva a otro. Un link que
miente es peor que uno roto, porque no se nota.

---

## 17. En el teléfono

Abre el sitio en un teléfono, o achica la ventana a 375px.

- Nada se sale para el costado
- Las tarjetas se apilan en una columna
- El globo de la chinchilla no tapa la pantalla entera
- El menú de tres rayas abre y se lee

---

## 18. En claro y en oscuro

Toca el botón de la luna en varias páginas.

- Todo se lee en los dos temas
- **El pie se lee**: "Recursos", "Preguntas frecuentes", "Invitame un
  café" y el nombre. Si se ven casi del color del fondo, es un fallo.
- En una ruta armada a mano anclada en la portada, su color se ve en
  los dos temas
- Las chinchillas cambian de color según la ruta y se ven en ambos

---

## Qué anotar si algo falla

1. El número del caso
2. Qué esperabas y qué viste
3. La URL exacta
4. **El commit** de `/version.txt`
5. Si hay algo en rojo en la consola (F12), copia el mensaje

Los errores de consola valen mucho: casi todos los bugs de este sitio
aparecieron primero ahí.
