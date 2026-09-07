# Roadmap de DataChinchilla

Todo lo pedido, en un solo lado, para que no se pierda nada. La
numeración entre paréntesis es la del mensaje donde se pidió, para
poder buscarlo.

Estados: **abierto** · **en curso** · **hecho** · **a decidir**

---

## Roto ahora mismo

Lo que está mal en producción. Va primero, siempre.

| # | Qué | Estado |
|---|---|---|
| 1 | El onboarding ya no aparece | abierto |
| 8 | La agenda desapareció de la portada | abierto |
| 17 | Volver atrás desde el armador lleva a Data Engineer, no a la portada | abierto |
| 13 | Se pueden sumar bloques a "mi semana" sin cuenta; también guardar una ruta armada | abierto |

---

## Confianza: que se entienda que es gratis

Lo más importante del producto. Alguien tiene que poder llegar, mirar
diez segundos y saber que no se le va a cobrar nunca.

| # | Qué | Estado |
|---|---|---|
| 3 | Decir que es gratis sin que suene a las que dicen que son gratis y no lo son | abierto |
| 9 | FAQ, y lo que hace que una app se vea profesional | abierto |
| 7 | Sacar "Las bloqueadas todavía no existen. Escríbeme cuál te sirve" | abierto |
| 6 | Poner en cada ruta "¿Conoces algo gratis que debería estar acá?" | abierto |

Sobre el 3: no alcanza con escribir "gratis" más grande. Lo que
convence es que no haya ningún lugar donde pueda aparecer un precio:
sin plan, sin "pro", sin límite de nada, y decir de dónde sale el
material y por qué no cuesta.

---

## Interfaz: sacar ruido

| # | Qué | Estado |
|---|---|---|
| — | Unificar los cuatro "Practicar" de la portada | abierto |
| — | Sacar "Todas las rutas" y "Armar la mía" del pie | abierto |
| 5 | Reescribir "¿Ya sabes la mitad de esto?" | abierto |
| 22 | Ese bloque va al mismo lado que "Ármala a mano" de arriba: decidir si se queda | a decidir |
| 21 | Los bordes del catálogo parecen tarjetas seleccionadas. Definir jerarquía: qué lleva degradado, qué lleva borde, con qué intensidad | abierto |
| 24 | Estandarizar los espaciados entre secciones | abierto |
| 23 | Las huellas entre secciones: ocupan mucho y no se entiende la intención | a decidir |
| 11 | Barra de scroll propia | **hecho** |

---

## Navegación

| # | Qué | Estado |
|---|---|---|
| 20 | Menú hamburguesa: CV, a mano, rutas, práctica diaria, mi semana | abierto |
| 18 | La ruta armada a mano y la que sale del CV, ancladas juntas, cada una con su color y sus filtros | abierto |
| — | Flechitas para pasar de ejercicio en práctica sin entrar | abierto |

---

## El recorrido guiado

| # | Qué | Estado |
|---|---|---|
| 1 | No aparece más | abierto |
| — | Que explique dónde estás parado en cada página, no solo qué sigue | abierto |
| — | Poder volver al paso anterior, y que te devuelva a donde estabas | abierto |
| — | Que las acciones adelanten el paso | **hecho** |
| — | Que no se pueda avanzar sin hacer la acción | **hecho** |
| — | Que se pueda reabrir después de cerrarla | **hecho** |
| — | Que no se salga de la pantalla al scrollear | **hecho** |

---

## Contenido

| # | Qué | Estado |
|---|---|---|
| 2 | Desbloquear Airflow: hay que buscarle material gratis | abierto |
| 4 | Sumar Laws of UX (lawsofux.com, tiene versión en español) | abierto |
| — | Sección de lo que te dan gratis por ser estudiante | abierto |
| 14 | Que todo lo que agreguemos esté también en "armar ruta" | abierto |
| 15 | Evaluar el contenido: cuánto hay, qué falta, cuál es el mínimo para lanzar | abierto |
| 10 | Links rotos y de pago: revisar todos, no solo los cinco | en curso |

Sobre el 10: los cinco de LeetCode Premium ya se cambiaron por gratis
del mismo patrón. Falta pasar un verificador por **todos** los links
del sitio, que son cientos, y que quede corriendo solo.

---

## El motor

| # | Qué | Estado |
|---|---|---|
| 19 | Que subir el CV real dé exactamente "Subir de nivel". Iterar sin hardcodear | abierto |
| 19b | Evaluar si conviene IA para el análisis del CV, sin que nadie pague | a decidir |
| — | Preguntas de seguimiento cuando la evidencia del CV es ambigua | abierto |
| — | El motor no entiende negaciones: "no sé Docker" cuenta como saber Docker | abierto |

---

## Infraestructura

| # | Qué | Estado |
|---|---|---|
| 12 | Ambiente de pruebas | **hecho** — `pruebas.datachinchilla.pages.dev` |
| 13 | Pedir cuenta para guardar avance | **hecho** para cursos y práctica; falta semana y ruta armada |
| — | Rotar la clave `sb_secret_` de Supabase | abierto |
| — | Conectar `www.datachinchilla.com` | abierto |
| 16 | Pasar el sitio a inglés | abierto, al final |

Sobre el 16: conviene ir sacando los textos a un solo lugar a medida
que se toca cada página, así el día que se traduzca no hay que
recorrer veintiuna páginas buscando frases sueltas.

---

## Cómo se trabaja

- Todo va primero a la rama `pruebas`, se verifica en
  `pruebas.datachinchilla.pages.dev`, y recién ahí se mergea a `main`.
- `datachinchilla.com/version.txt` dice qué versión está publicada.
- Antes de publicar: `humo.py`, `cuentas.py` y `publicar.py` tienen
  que pasar.
