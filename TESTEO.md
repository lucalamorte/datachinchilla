# Guion de prueba de DataChinchilla

Para pasarle a un agente con navegador. Cada caso dice qué hacer y qué
tiene que pasar. Si algo no coincide, es un fallo: anotá el caso, lo
que esperabas y lo que viste.

**Sitio:** <https://datachinchilla.com>

---

## Antes de empezar

El sitio guarda todo en el navegador. Para probar como alguien que
entra por primera vez, abrí la consola (F12) y corré:

```js
localStorage.clear(); location.reload();
```

Hacelo antes de cualquier caso que diga "desde cero". Sin eso vas a
estar probando sobre datos viejos y los resultados no valen.

---

## 1. La portada, sin haber hecho nada

**Desde cero.** Abrí la portada.

Tiene que verse:

- El título "El camino completo para trabajar en tech"
- **Tres tarjetas y nada más**: "Empecemos por tu CV", "Ármala a mano",
  "O mira las 16 rutas"
- Abajo, "Práctica diaria" con dos tarjetas (Python y SQL)
- Más abajo, el catálogo de rutas
- Un globo de la chinchilla abajo a la derecha que dice "Hola, soy la
  chinchilla" y "Paso 1 de 9"

**Falla si:** el CV se pide dos veces en la misma pantalla (había un
banner duplicado abajo de las tarjetas; ya no tiene que estar).

---

## 2. El recorrido guiado, entero

Es el caso más importante. **Desde cero.**

Seguí el globo tocando siempre su botón, y anotá el número de paso que
muestra. Tienen que salir los nueve, en este orden y en estas páginas:

| Paso | Dice | Dónde estás |
|---|---|---|
| 1 de 9 | Hola, soy la chinchilla | portada |
| 2 de 9 | Primero, cuéntame de vos | portada |
| 3 de 9 | ¿A dónde vas? | cv |
| 4 de 9 | Ahora sí, tu experiencia | cv |
| 5 de 9 | Esto ya lo sabes | cv |
| 6 de 9 | Y esto es lo que falta | cv |
| 7 de 9 | Ahora, cuándo | una ruta |
| 8 de 9 | Tus días y tu rato | semana |
| 9 de 9 | Listo. Elige por dónde | portada |

En el paso 4 vas a tener que pegar un CV de verdad en el textarea para
poder seguir. Usá el de la sección 12.

Entre el paso 6 y el 7 el globo no aparece: tenés que tocar el botón
**"Guardarla y ver mi ruta"** de la página, que es el que guarda. El
globo del paso 6 solo confirma que lo leíste.

**Falla si:** el globo desaparece en alguna página y no vuelve. Es el
bug que más veces volvió. Si pasa, anotá en qué paso y en qué página.

**Falla si:** el globo aparece pegado a la esquina de arriba a la
izquierda, flotando sobre el contenido en vez de al lado de lo que hay
que tocar.

---

## 3. El popup de la cuenta se puede cerrar

En **cada una** de estas páginas: portada, `/cv`, `/practica`,
`/semana`, y una ruta cualquiera (`/dbt`).

Tocá "Entrar" arriba a la derecha y probá cerrarlo de tres formas:

1. La cruz de arriba a la derecha del recuadro
2. Un clic afuera del recuadro, sobre el fondo oscuro
3. La tecla Escape

**Las tres tienen que cerrarlo.** Un modal que no se puede cerrar deja
a quien lo abrió sin salida más que recargar la página.

Este bug estaba justo en las cuatro páginas principales, así que
probalas todas y no solo una.

---

## 4. El CV se lee y no se pierde

**Desde cero.** Andá a `/cv`.

1. Elegí el puesto **Data Engineer**
2. Pegá el CV de la sección 12 en el textarea
3. Esperá unos segundos

Tiene que aparecer:

- **"Esto ya lo tienes"** con chips de temas (SQL, Python, Pipelines...).
  Cada chip tiene una **cruz** para sacarlo.
- **"Tu ruta es Subir de nivel"** con un porcentaje de cobertura
- Un botón "Guardarla y ver mi ruta"

**Ahora la parte que importa:** recargá la página (F5).

El CV tiene que **seguir ahí**: el textarea con el texto y el resultado
abajo. Si la página abre en blanco y hay que subir el CV de nuevo, es
un fallo (pasaba hasta hace poco).

---

## 5. Los temas se pueden sacar

Seguí en `/cv` con el CV cargado.

1. Anotá el porcentaje que dice "Cubre el N% de lo que te falta"
2. Tocá la **cruz** de un chip, por ejemplo "Big data"
3. El chip desaparece y aparece abajo, tachado, bajo "Sacaste"
4. **El porcentaje tiene que cambiar** (la ruta se rehace sin ese tema)
5. Tocá el chip tachado: vuelve arriba y el porcentaje se recalcula

Recargá la página: **lo que sacaste tiene que seguir sacado.**

---

## 6. Sumar y sacar rutas de tu semana

Se puede hacer desde tres lugares y los tres tienen que coincidir.

**Desde una ruta:** andá a `/dbt`. Arriba, al lado de "Empezar por",
hay un botón que dice "Sumar a tu semana" o "Está en tu semana".
Tocalo. El texto cambia y aparece un cartel de la chinchilla abajo a la
izquierda.

**Desde el catálogo:** en la portada, bajá hasta las rutas. Cada
tarjeta tiene un botón "Sumar a mi semana" / "En tu semana". Buscá dbt:
tiene que reflejar lo que acabás de hacer.

**Desde la semana:** andá a `/semana`. Hay una lista "Qué entra en tu
semana" con las 15 rutas. dbt tiene que estar marcada igual.

Cambiá el estado desde cualquiera de los tres y verificá que los otros
dos lo muestren. **No hace falta tener CV cargado para esto.**

---

## 7. La semana se arma sola

En `/semana`, con al menos una ruta activa:

1. Elegí días (lunes, miércoles, viernes)
2. Elegí una franja (a la noche)
3. Movés las horas por semana

Abajo tiene que armarse la semana con bloques concretos: qué día, qué
curso y cuánto rato.

**Falla si:** un día se llena de muchos bloques chiquitos. El tope son
**dos bloques de estudio por día**, por más horas que pongas.

Volvé a la portada: la agenda tiene que aparecer con lo mismo.

---

## 8. La práctica y la racha

Andá a `/practica`.

- Hay dos bancos: **Blind 75** (Python) y **Consultas de entrevistas**
  (SQL)
- Los enunciados abren en LeetCode y StrataScratch, en su sitio
- Marcá **dos** problemas del mismo banco

Al marcar el segundo tiene que aparecer un cartel con la chinchilla en
un cohete: "El día está cerrado".

Volvé a la portada: en la fila de hoy de la agenda tiene que verse
"2/2".

La chinchilla con el café aparece con **los dos bancos** cerrados, no
con uno: son 2 de Python y 2 de SQL. Con uno solo no tiene que estar.
Y la fila de hoy solo muestra el contador si hoy es un día que
marcaste en tu semana; si hoy te toca libre, dice "Libre" y está
bien.

**Probá también los vacíos:** escribí algo sin sentido en el buscador
("zzzz"). Tiene que aparecer la chinchilla con una lupa y un texto que
diga qué hacer, no un renglón gris.

---

## 9. La chinchilla está en todos lados

No hay que hacer nada para que aparezcan. En cualquier página:

- Una **escarbando** al lado del texto de entrada, arriba
- **Huellas** entre sección y sección, donde haya al menos tres
  secciones a la vista. En `/practica` hay una sola, así que ahí no
  van, y en `/cv` los pasos que todavía no se abrieron no cuentan.
- Una que se **asoma** por el borde de arriba del pie, cada 7 segundos
- Una **huella chiquita** al lado del rótulo de cada bloque. En `/cv`
  los rótulos llevan número de paso en vez de huella.

Si tenés activado "reducir movimiento" en el sistema, la que se asoma
en el pie se queda quieta y visible en vez de aparecer cada 7
segundos. Es a propósito: sin su animación quedaría fuera de cuadro.

En el pie tiene que haber **una sola** chinchilla (la de la marca).
Si ves tres en el mismo renglón, es un fallo.

---

## 10. Los números coinciden

Entrá a estas rutas y comparen el título con el contador de arriba:

El catálogo dice "las 15 rutas" y el filtro "Todo 15": son las que se
pueden hacer. La grilla muestra 16 tarjetas porque hay una anunciada,
sin página.

| Ruta | Tiene que decir |
|---|---|
| `/dbt` | "Cuatro tramos, veintitrés pasos" y "0/23" arriba |
| `/subir-nivel` | "Cinco tramos, diecisiete cursos" y "0/17" |
| `/claude` | "Cinco tramos, dieciséis cursos" y "0/16" |
| `/llm-agentes` | "Cuatro credenciales, veintiocho pasos" y "0/28" |

**Falla si** el texto dice una cantidad y el contador otra.

---

## 11. Marcar un curso

En `/dbt`, tocá cualquier tarjeta de curso. Se abre una hoja con el
detalle. Tocá "Marcar como completado".

- El cartel de la chinchilla aparece **por encima** de la hoja, no
  detrás del velo gris
- El contador de arriba sube
- Cerrá la hoja: la tarjeta queda marcada

Recargá: **la marca tiene que seguir.**

---

## 12. El CV de prueba

Pegá esto tal cual donde el caso lo pida:

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

Con ese CV apuntando a **Data Engineer**, el sitio tiene que recomendar
**"Subir de nivel"**. Es la vara: si recomienda otra cosa o arma una
lista de cursos sueltos, es un fallo.

---

## 13. En el teléfono

Abrí el sitio en un teléfono, o achicá la ventana a 375px de ancho.

- Nada se sale para el costado (no tiene que haber scroll horizontal)
- El menú de arriba se lee
- Las tarjetas se apilan en una columna
- El globo de la chinchilla no tapa la pantalla entera
- La chinchilla del encabezado desaparece (a ese ancho estorba)

---

## 14. En claro y en oscuro

Tocá el botón de la luna arriba a la derecha, en varias páginas.

- Todo se lee en los dos temas
- **El pie se lee**: los links "Todas las rutas", "Armar la mía",
  "Invitame un café" y el nombre. Si se ven casi del color del fondo,
  es un fallo.
- Las chinchillas cambian de color según la ruta y se ven en ambos

---

## Qué anotar si algo falla

Para cada fallo:

1. El número del caso
2. Qué esperabas y qué viste
3. La URL exacta
4. Si hay algo en rojo en la consola (F12), copiá el mensaje

Los errores de consola valen mucho: casi todos los bugs de este sitio
aparecieron primero ahí.
