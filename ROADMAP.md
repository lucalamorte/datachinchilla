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
| Unificar los cuatro "Practicar" de la portada | Borrar tres, decidir cuál queda | **hecho** |
| (21) Los bordes del catálogo parecen "seleccionado" | CSS. Define la jerarquía visual de todo el sitio | **hecho** |
| (23) Las huellas entre secciones | Se sacaron: se leían como un indicador de carga | **hecho** |
| (4) Sumar Laws of UX | En `recursos.html`, que además aloja lo de estudiantes | **hecho** |

## 2. Cuesta poco y se nota

| Qué | Por qué acá | Estado |
|---|---|---|
| (24) Estandarizar espaciados entre secciones | Escala de dos distancias, con significado | **hecho** |
| (6) "¿Conocés algo gratis que debería estar acá?" en cada ruta | Ya puesto en las 16 | **hecho** |
| (3) El pie sin borde en claro | CSS | **hecho** |
| Flechitas para pasar de ejercicio en práctica | Con contador, y marcando el que está en pantalla | **hecho** |
| (2) Desbloquear Airflow | Ocho pasos: Astronomer Academy y los tutoriales de Apache | **hecho** |

## 3. Cuesta medio, se nota mucho

| Qué | Por qué acá | Estado |
|---|---|---|
| (20) Menú hamburguesa: CV, a mano, rutas, práctica, semana | Toca 22 páginas | **hecho** |
| El recorrido: que explique dónde estás en cada página, y poder volver un paso | Rehacer el contenido de los nueve pasos | **hecho** |
| (18) La ruta armada a mano y la del CV, ancladas juntas | Toca la portada y el modelo de datos | **hecho** |
| (14) Que todo lo nuevo esté también en "armar ruta" | El armador conocía tres rutas de diecisiete: 36 piezas de 263 | **hecho** |
| (1) El globo no aparece en incógnito | Sin causa todavía. Hay una red puesta para que falle mostrándose | en curso |
| Sección de lo que dan gratis por ser estudiante | Ya tiene página donde ir: `recursos.html` | abierto |
| Arquitectura y ML aplicado comparten color (#BE185D) | Los dos puntos del armador salen iguales. Es cambiarle el acento a una página | abierto |
| `recursos.html` y `preguntas.html` cargan el armador entero y `catalog.js` sin usarlos | Salieron de copiar `armar.html`. Son ~150 kB de código muerto por página. Podarlo bien pide análisis de alcance | abierto |

## 5. Lo del 7 de septiembre

| Qué | Por qué acá | Estado |
|---|---|---|
| (1) Agregar skills a mano, no sólo sacarlas | El espejo de la cruz, que no estaba | **hecho** |
| (2) El widget de la agenda en la landing | Estaba, pero siempre debajo del pliegue | **hecho** |
| (3) Sacar "Saltear": queda la cruz, y pregunta | Dos salidas para una acción | **hecho** |
| (4) El botón `?` fuera de la portada no hacía nada | Dejaba el recorrido en un paso de otra página | **hecho** |
| (6) Las preguntas de a una, y de tech y no de datos | Nunca tuvieron CSS, y eran de cuando el sitio eran tres rutas | **hecho** |
| (7) La frase de privacidad del CV, profesional | Verificado antes: el texto no sale del navegador | **hecho** |
| (8) Filtro "Resueltos" en la práctica | Faltaba el tercer estado | **hecho** |
| (5) Perfiles funcionales: tester y analista funcional | Dos rutas nuevas y dos puestos nuevos, cubiertos al 100% | **hecho** |
| (5) Credenciales cloud como ruta propia: AWS y Google | `nube.html`: AZ-900, DP-900, AWS CCP y Cloud Digital Leader | **hecho** |
| (5) PM: recursos, no ruta | Cuatro fuentes en `recursos.html`: Cagan, Shape Up, Lenny, Mind the Product | **hecho** |

| Web3 tenía 5 pasos que ningún puesto pedía | Entró el puesto Desarrollador Web3 | **hecho** |
| Faltaban tipos: Cloud Engineer y Big Data Engineer | Un aviso los pide por separado de Data Engineer | **hecho** |
| Cada puesto dice en qué se diferencia del de al lado | El resumen contaba qué hace, no cómo elegir entre dos parecidos | **hecho** |

## 4. Cuesta mucho

| Qué | Por qué acá | Estado |
|---|---|---|
| (10) Verificador de todos los links del sitio | `links.py`: 434 links, ninguno roto. 126 que se habían mudado, apuntados al lugar nuevo con `mudar.py` | **hecho** |
| (15) Evaluar el contenido: cuánto hay, qué falta, mínimo para lanzar | `contenido.py`: 1613 h, ningún tema pedido sin material | **hecho** |
| 41 pasos se parten en 10 bloques o más; CS50 llega a "parte 1 de 40" | El número además reiniciaba cada semana. Ya no se numera cuando el paso no entra en la semana | **hecho** |
| CS50 tiene cinco pasos de 50 a 60 horas | Partido por la estructura que publica Harvard: 29 semanas + 8 cursos enteros. De 41.8 h por paso a 12.4 | **hecho** |
| Data Engineer tiene pasos de 27 h; Games y Web, de 60 | Mismo caso que CS50. Su fuente no publica una estructura semanal, así que no hay de dónde sacarla | abierto |
| MLOps: 1 paso y 1 hora, y ML Engineer lo pide en nivel 4 | `mlops.html`: 13 pasos. ML Engineer pasó de 89% a 100% | **hecho** |
| Visualización: 3 pasos para lo que pide Data Analyst | `visualizacion.html`: 9 pasos. El tema pasó de 4 pasos a 13 | **hecho** |
| (19) Que el CV real dé exactamente "Subir de nivel", sin hardcodear | Iteración sobre el motor | abierto |
| (19b) Evaluar IA para leer el CV, sin que nadie pague | Decisión de arquitectura y de costo | a decidir |
| El motor no entiende negaciones: "no sé Docker" cuenta como saber | Resuelto en `cv.js`, con `motor.py` como red: 23 casos, la mitad trampas | **hecho** |
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
