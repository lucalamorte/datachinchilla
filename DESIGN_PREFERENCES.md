# Preferencias de diseño y construcción

Guía para armar cualquier app con el criterio que venimos usando. Cada regla salió
de un error concreto, no de una teoría. Cuando una regla no aplique, ignorala con
criterio, pero sabé qué estás pagando.

Idioma: la conversación va en español, el código y los comentarios en inglés.

---

## 1. Proceso

- **Reusar antes de reescribir.** Antes de crear un componente, buscar si ya existe
  uno que haga lo mismo. La mayoría de los bugs largos de este proyecto fueron una
  misma regla escrita en dos lugares que se fueron separando sin que nadie lo viera.
- **Una sola fuente de verdad por regla.** Si una decisión se toma en dos archivos,
  ya está rota, solo falta que alguien lo note.
- **Verificar contra la base real, no contra los tests.** Un motor puede pasar 30
  tests unitarios y estar escribiendo contra una tabla que rechaza todo.
- **Probar antes de avanzar.** No pasar al ítem siguiente sin ver el anterior
  funcionando.
- **Preguntar antes de construir algo grande.** Pedir referencia o ejemplo antes de
  armar una visualización, un rediseño o cualquier cosa cara en tiempo.
- **La spec es guía, no dictado.** Si la instrucción teórica choca con lo que la app
  necesita en la práctica, gana la práctica, y hay que decir qué se apartó y por qué.

### Antes de cerrar cualquier cambio

```bash
npx tsc --noEmit -p tsconfig.json    # 0 errores
npx next lint                         # 0 errores
npx vitest run                        # todo verde
npx next build                        # exit 0
```

Nunca desactivar `ignoreBuildErrors`. Cortar código muerto y que el compilador avise
es más barato que descubrirlo en producción.

---

## 2. Íconos: SVG inline, nunca emojis

Los emojis cambian según el sistema operativo, no heredan color y no se pueden
alinear. Todos los íconos van como SVG escrito a mano en el componente.

```tsx
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
     className="flex-shrink-0">
  <path d="M5 12h14M13 5l7 7-7 7" />
</svg>
```

Reglas fijas:

| Propiedad | Valor | Motivo |
|---|---|---|
| `viewBox` | siempre `0 0 24 24` | todos los íconos escalan igual |
| `fill` | `none` (salvo íconos sólidos tipo llama o estrella) | trazo, no mancha |
| `stroke` | `currentColor` | hereda el color del texto, un solo lugar donde cambiarlo |
| `strokeWidth` | `2.2` a `2.5` | menos se ve anémico, más se ve tosco |
| `strokeLinecap` / `strokeLinejoin` | `round` | sin puntas duras |
| `width` / `height` | `10` a `16` inline, `26` en estados vacíos | proporcional al texto |
| `className` | `flex-shrink-0` | nunca se deforma dentro de un flex |

Los íconos que se repiten se declaran como componentes chicos al final del archivo,
bajo un separador, con `size` y `className` como props:

```tsx
function FlameIcon({ size = 16, className = '' }: { size?: number; className?: string }) { … }
```

Para gráficos generativos o decorativos, Canvas antes que un `path` gigante escrito
a mano.

---

## 3. Color y tema

Todo color vive como variable CSS en `:root`, nunca hardcodeado en un componente.

```css
:root {
  --color-surface:        #FFFFFF;
  --color-surface-muted:  #F9FAFB;
  --color-text-secondary: #6B7280;
  --color-divider:        #E5E7EB;
}
```

- **Los dos temas se diseñan, no se invierten.** El oscuro redefine solo los tokens,
  y los componentes se estilan por token, jamás dentro del media query.
- Ningún color puede tener su única definición adentro de un bloque de tema.
- El acento se gasta en un solo lugar por pantalla. Todo lo que lo rodea va callado.
- Color semántico (bien, alerta, crítico) es un eje aparte del acento y no cuenta
  como acento.

---

## 4. Jerarquía de acciones

Una pantalla pide **una** cosa. El resto acompaña.

### Primaria

Una sola por pantalla. Gradiente, sombra del color del gradiente, `rounded-2xl`.

```tsx
style={{
  background: 'linear-gradient(135deg, #60A5FA, #A78BFA)',
  boxShadow: '0 8px 24px rgba(96,165,250,0.35)',
}}
```

Dos filas cuando lleva a algún lado: el verbo arriba en mayúsculas chicas, el destino
abajo. **Un botón siempre dice adónde te lleva.** Apretar no puede ser la forma de
enterarse.

### Secundaria

Nunca texto subrayado. El subrayado es cómo un documento apunta a otro documento, no
cómo una app ofrece una acción, y al lado de una primaria rellena se lee como algo sin
terminar.

Componente único (`QuietButton`): área de click real, borde `rounded-xl`, texto en
`--color-text-secondary`, y el color aparece recién en el hover. `hover:-translate-y-px`
para que responda.

**Excepción:** un link adentro de una oración sí va subrayado. Un botón incrustado en
un párrafo queda peor que el subrayado que reemplaza.

### Deshabilitado

Tiene que diferenciarse en **más que la opacidad del texto**. Si el activo y el
inactivo comparten fondo y borde, el activo se lee como muerto.

- Activo: superficie con contraste, borde visible, hover.
- Deshabilitado: fondo apagado, borde apenas visible, sin hover, `cursor-not-allowed`,
  y un `title` que explique por qué.

### Pills y toggles

Relleno sólido cuando están prendidos, contorno limpio cuando no. Dos matices del
mismo tinte no se distinguen. Ícono opcional en vez del punto de color cuando el
filtro tiene un significado que merece dibujo (por ejemplo, ojo tachado para
"desactivados").

---

## 5. Layout

- El alto de un banner o un header es finito. **Nunca agregar una fila.** Si algo
  nuevo tiene que aparecer, entra en una línea que ya existe o desplaza algo.
- Espaciado con `flex` o `grid` y `gap`, nunca con márgenes por elemento que se
  colapsan o se duplican.
- Contenido ancho (tablas, código, diagramas) scrollea adentro de su propio contenedor
  con `overflow-x: auto`. El body nunca scrollea de costado.
- Unidades relativas, `max-width: 100%` en imágenes.

---

## 6. Tipografía y números

- `font-variant-numeric: tabular-nums` (o `tabular-nums` de Tailwind) en todo número
  que pueda cambiar o alinearse en columna. Sin eso, un contador vibra al actualizarse.
- Jerarquía real de tamaños: etiqueta de `10px` en mayúsculas con `tracking-wide`,
  cuerpo de `12` a `14`, mensaje central de `16` a `18` en `font-extrabold`.
- Los indicadores secundarios van en una sola línea, no en tres pills apiladas.

### Nombres largos

Los nombres de entidades (mazos, archivos, workspaces) se **desplazan**, no se cortan.
Elementos importados comparten prefijos largos, así que la cola que corta la elipsis
suele ser justo lo que distingue uno de otro.

`MarqueeText`: se mueve solo si desborda, pausa en cada extremo para que se pueda leer,
ciclo de 7 segundos, y se queda quieto con `prefers-reduced-motion`.

---

## 7. Movimiento

- Sirve para algo o no está. Nada de animación de adorno.
- `prefers-reduced-motion` siempre respetado.
- Transiciones cortas (`duration-150`) para hover y foco.
- Un momento orquestado pega más que cinco efectos sueltos.

---

## 8. Copy

Reglas duras:

- **Tuteo siempre, voseo nunca.** Aplica también a los prompts del sistema, porque el
  modelo copia el registro que recibe.
- **La frase "la IA" está prohibida** en toda la app.
- Sin raya larga.
- Sin construcción "desde X hasta Y".
- No repetir la misma palabra cerca.
- Voz activa.

Criterios:

- **Nunca mostrar el vocabulario del motor.** Si el scheduler dice `due`, el usuario no
  tiene por qué leer "vence". Traducir jerga técnica a lo que la persona necesita hacer.
- **Un número que no pide hacer nada no merece espacio.** Si aparece al lado de una
  acción, compite con ella.
- Un control dice exactamente qué pasa. Si el botón dice "Publicar", el aviso después
  dice "Publicado".
- Nada de afirmaciones sin respaldo ("dos minutos por día alcanzan") ni frases genéricas
  que ya no aplican al producto.
- Los errores explican qué pasó y cómo salir. Sin disculpas ni vaguedad.
- Paridad de idiomas y concordancia de singular y plural, testeada.

---

## 9. Estados

Toda pantalla necesita cuatro, y ninguno es opcional:

1. **Cargando:** sin saltos de layout.
2. **Vacío:** decir qué pasa, ofrecer una salida. El vacío de "todavía no hay nada"
   dice algo distinto del vacío de "ya lo hiciste todo".
3. **Error:** visible. **Nunca `.catch(() => {})` en algo que el usuario espera que se
   guarde.** Un error tragado escondió 62 días de escrituras rechazadas en este
   proyecto. Telemetría es la única excepción: un evento fallido no puede romper la
   sesión.
4. **Lleno:** el caso normal.

Las funciones que guardan devuelven si guardaron:

```ts
Promise<{ saved: boolean; saveError?: string }>
```

Y la pantalla muestra un aviso cuando `saved` es `false`.

---

## 10. Filtros y listas

- **Multi-select con OR adentro de un eje.** Tildar Libro A y Libro B muestra los dos.
- **Estado ortogonal como toggle aparte con AND.** "Desactivados" no es una categoría,
  es un cruce: se combina con el filtro actual en vez de reemplazarlo.
- Un filtro que siempre devuelve vacío no es libertad, es una trampa. Si dos ejes no se
  pueden cruzar por cómo están los datos, mantenerlos excluyentes y dejar el motivo
  escrito en el código.
- Contadores al lado de cada filtro, intersectados con lo que ya está seleccionado.
- La selección persiste en `localStorage` con claves centralizadas en un solo módulo,
  nunca strings sueltos por archivo.

---

## 11. Reglas de decisión

Toda regla que decide qué ve el usuario vive en una **función pura**, fuera de React y
fuera del cliente de base de datos, con tests.

```ts
export function decideBanner(input: BannerInput): BannerDecision
```

Es lo que se rompe en silencio cuando alguien la edita seis meses después. Si está
mezclada con JSX, no hay forma de testear la prioridad sin montar media app.

---

## 12. Datos y límites

- Todo `select` sin límite tiene tope de filas por defecto. Paginar explícitamente.
- Consultar solo las columnas que se usan, así una migración pendiente no rompe la
  pantalla entera.
- Agregar en la base, no en el navegador. Un contador se resuelve con una vista, no
  trayendo cada fila.
- Los límites de subida se declaran una vez y se comparten entre cliente y servidor.
  Verificar el techo real de la plataforma, no el que uno supone.
- Nunca asumir que una respuesta es JSON. Un error de infraestructura contesta HTML, y
  parsearlo muestra un error de sintaxis en vez de la causa real.

---

## 13. Checklist antes de shippear

- [ ] ¿Reusé un componente existente en vez de escribir otro?
- [ ] ¿La regla vive en un solo lugar?
- [ ] ¿Los dos temas están diseñados?
- [ ] ¿El deshabilitado se distingue en más que la opacidad del texto?
- [ ] ¿El botón dice adónde lleva?
- [ ] ¿Agregué una fila a un contenedor que no tenía alto de sobra?
- [ ] ¿Hay jerga del motor en pantalla?
- [ ] ¿Barrido de voseo sobre el diff?
- [ ] ¿Los números usan `tabular-nums`?
- [ ] ¿Los cuatro estados existen?
- [ ] ¿Algún error se traga en silencio?
- [ ] ¿tsc, lint, tests y build en verde?
