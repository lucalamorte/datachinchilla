# Cómo probarlo

## Levantar el sitio

```bash
cd "C:\Users\Luca\Desktop\snowflake path" && python -m http.server 5500
```

Y abrir <http://localhost:5500>

Hace falta un servidor: abriendo el HTML con doble clic, el navegador
bloquea los `.js` compartidos y no anda nada.

## Empezar de cero

La guía y tu ruta viven en el navegador. Para probar como si fueras
alguien nuevo, en la consola del navegador (F12):

```js
localStorage.clear(); location.reload();
```

## El recorrido, de punta a punta

La chinchilla aparece abajo y te lleva por siete pasos. Cada uno
resalta lo que hay que tocar.

| # | Dónde | Qué pasa |
|---|-------|----------|
| 1 | Portada | Se presenta. La agenda todavía no aparece. |
| 2 | Portada | Resalta la invitación y te manda al CV. |
| 3 | `cv.html` | Elegir el puesto. |
| 4 | `cv.html` | Cargar el CV (PDF o pegado). |
| 5 | Tu ruta | Resalta el paso a la semana. |
| 6 | `semana.html` | Días, franja y horas. |
| 7 | Portada | Elegís por dónde arrancar. |

Se puede saltear con la cruz o con "Saltear", y volver a verla desde
el panel de cuenta (arriba a la derecha).

## Qué vale la pena mirar

**Con un CV de alguien con oficio** (Airflow, dbt, Snowflake, SQL
avanzado, Python, AWS) el motor tiene que recomendar **Subir de
nivel**, no armar una mezcla. Esa es la vara.

**Con un CV de analista** (SQL, Power BI, algo de Python) ninguna ruta
calza y arma una a medida, diciéndolo.

**Sin CV**: el link de "cuatro preguntas" da un resultado parecido.

**La práctica**: marcar dos problemas prende la racha sola. Los 139
tienen link directo al enunciado.

**La semana**: subir las horas no puede llenar un día de tarjetas.
El tope es dos bloques de estudio por día.

**Los temas del CV**: cada uno tiene una cruz. Sacar uno rehace la
ruta sin él, y queda abajo para devolverlo. Sobrevive a recargar.

## Los scripts

Se corren desde esta carpeta, con `python <nombre>`.

| Script | Para qué |
|--------|----------|
| `humo.py` | Abre las 20 páginas y avisa si alguna no se pinta |
| `tuteo.py` | Busca voseo. Con `--arreglar` lo corrige |
| `sellar.py` | Actualiza el `?v=` de los `.js` y `.css` |
| `dedup-css.py` | Encuentra reglas CSS repetidas |
| `build-brand.py` | Regenera las cabeceras (llama a `sellar.py`) |
| `build-pasos.py` | `pasos.js` desde los NODES de cada ruta |
| `build-temas.py` | `temas.js`: temas, puestos y qué paso enseña qué |
| `build-problemas.py` | `problemas.js`: Blind 75 y las consultas |
| `build-festejo.py` | Engancha el festejo al marcar un curso |
| `build-claude.py` | `claude.html` desde `ai-fundamentos.html` |
| `build-dbt-mas.py` | Los 8 cursos de dbt Learn que faltaban |
| `build-activar.py` | El botón de sumar la ruta a tu semana |
| `cuentas.py` | Avisa si una ruta dice una cantidad y tiene otra |

Después de tocar cualquier `.js` o `.css` compartido: `python sellar.py`.
Si no, el navegador sirve la versión vieja.

## La chinchilla

Aparece en los dos extremos: cuando no hay nada y cuando algo sale bien.

| Dónde | Qué hace |
|-------|----------|
| Leyendo un PDF, armando la ruta | Escarba, con el texto rotando |
| Búsqueda del catálogo sin resultados | Busca con la lupa |
| `practica.html` sin coincidencias | Busca con la lupa |
| `practica.html` con todo hecho | Festeja |
| `mi-ruta.html` sin ruta armada | Escarba, con el botón para armarla |
| Marcar un curso | Festeja, en una esquina |
| Cada 5 cursos, o la ruta entera | En cohete |
| Cerrar el día de práctica | En cohete, con los días seguidos |
| Un día libre de la agenda | Durmiendo |
| Con la práctica del día hecha | Con el café |
| Al volver otro día | Saludando |

El cartel del festejo dura tres segundos y medio y se va solo. No tapa
nada y no hay que cerrarlo. Con `prefers-reduced-motion` no aparece:
es movimiento sin información nueva.

Para verlo sin esperar, desde la consola:

```js
Chin.festejar("cohete", "Probando", "Así se ve.");
```

## Las rutas activas

Una ruta entra en tu semana o no entra, y se puede tocar desde tres
lados, sin pasar por el CV:

- **el catálogo**, con el botón de cada tarjeta
- **la ruta misma**, con el botón del encabezado
- **tu semana**, con la lista de las quince

Pueden estar varias a la vez: el tiempo se reparte entre ellas.
Sacar una no borra tu avance, solo deja de ocupar tiempo.

## Lo que falta

- MLOps no tiene ningún curso, y ML Engineer lo pide como su día a día.
- Nada está deployado.
- La key de Supabase que se filtró sigue sin rotar.
