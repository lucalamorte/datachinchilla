# Roadmap de DataChinchilla

Ordenado por esfuerzo contra impacto: arriba lo que cuesta poco y se
nota mucho. El número entre paréntesis es el del mensaje donde se
pidió.

Estados: **abierto** · **en curso** · **hecho** · **a decidir**

---

## 1. Cuesta poco y se nota mucho

| Qué | Por qué está acá | Estado |
|---|---|---|
| (17) El "volver" del armador va a Data Engineer | Un `href` hardcodeado. Navegación rota en la página que más se usa | **hecho** |
| (13) Pedir cuenta para guardar la ruta armada y para sumar bloques a la semana | El candado ya existe, falta usarlo en dos lugares más | **hecho** |
| (7) Sacar "Las bloqueadas todavía no existen" | Un borrado | **hecho** |
| (5, 22) Sacar la banda "¿Ya sabes la mitad de esto?" | Un borrado, y saca una acción duplicada | **hecho** |
| Sacar del pie "Todas las rutas" y "Armar la mía" | Un borrado | **hecho** |
| (3, 9, 4, 4.5) FAQ en su propia página, con la plata contestada de una | Una página nueva, y es lo que más frena a alguien que llega | **hecho** |
| (11) Barra de scroll propia | CSS | **hecho** |
| (12) Ambiente de pruebas | Ya estaba disponible en Cloudflare | **hecho** |
| Unificar los cuatro "Practicar" de la portada | Borrar tres, decidir cuál queda | abierto |
| (21) Los bordes del catálogo parecen "seleccionado" | CSS. Define la jerarquía visual de todo el sitio | abierto |
| (23) Las huellas entre secciones | Si se sacan, es un borrado. Ocupan mucho y no se entienden | abierto |
| (4) Sumar Laws of UX | Una entrada de contenido | abierto |

## 2. Cuesta poco y se nota

| Qué | Por qué acá | Estado |
|---|---|---|
| (24) Estandarizar espaciados entre secciones | CSS, pero hay que revisar 22 páginas | abierto |
| (6) "¿Conocés algo gratis que debería estar acá?" en cada ruta | Ya puesto en las 16 | **hecho** |
| (3) El pie sin borde en claro | CSS | **hecho** |
| Flechitas para pasar de ejercicio en práctica | Una fila de botones y dos funciones | abierto |
| (2) Desbloquear Airflow | Cuesta poco escribirla; lo que cuesta es encontrarle material gratis serio | abierto |

## 3. Cuesta medio, se nota mucho

| Qué | Por qué acá | Estado |
|---|---|---|
| (20) Menú hamburguesa: CV, a mano, rutas, práctica, semana | Toca 22 páginas | abierto |
| El recorrido: que explique dónde estás en cada página, y poder volver un paso | Rehacer el contenido de los nueve pasos | abierto |
| (18) La ruta armada a mano y la del CV, ancladas juntas | Toca la portada y el modelo de datos | abierto |
| (14) Que todo lo nuevo esté también en "armar ruta" | Hay que auditar qué falta | abierto |
| (1) El globo no aparece en incógnito | Sin causa todavía. Hay una red puesta para que falle mostrándose | en curso |
| Sección de lo que dan gratis por ser estudiante | Investigación de contenido | abierto |

## 4. Cuesta mucho

| Qué | Por qué acá | Estado |
|---|---|---|
| (10) Verificador de todos los links del sitio | Son cientos, y tiene que quedar corriendo solo | abierto |
| (15) Evaluar el contenido: cuánto hay, qué falta, mínimo para lanzar | Análisis de todo el catálogo | abierto |
| (19) Que el CV real dé exactamente "Subir de nivel", sin hardcodear | Iteración sobre el motor | abierto |
| (19b) Evaluar IA para leer el CV, sin que nadie pague | Decisión de arquitectura y de costo | a decidir |
| El motor no entiende negaciones: "no sé Docker" cuenta como saber | Requiere análisis de texto de verdad | abierto |
| Preguntas de seguimiento cuando el CV es ambiguo | Diseño nuevo | abierto |
| (16) Pasar el sitio a inglés | Al final. Conviene ir sacando textos a un solo lugar mientras tanto | abierto |

## 5. Fuera del sitio

| Qué | Estado |
|---|---|
| Rotar la clave `sb_secret_` de Supabase | abierto |
| Conectar `www.datachinchilla.com` | abierto |

---

## Cómo se trabaja

- Todo va primero a `pruebas`, se verifica en
  `pruebas.datachinchilla.pages.dev`, y recién ahí se mergea a `main`.
- `datachinchilla.com/version.txt` dice qué versión está publicada.
  Comparar contra el sha local antes de dar algo por desplegado: el
  sitio devuelve la portada para cualquier ruta que no existe, así que
  un 200 no prueba nada.
- Antes de publicar: `humo.py`, `cuentas.py` y `publicar.py`.
