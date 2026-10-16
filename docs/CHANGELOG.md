# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado con
[SemVer](https://semver.org/lang/es/).

## [No publicado]

### Cambiado

- Las colas descendentes (`g`, `j`, `p`, `q`, `y`) bajan lo mismo que suben las ascendentes sobre la
  altura x: descendente −415 en Display y −370 en Lectura. Corchetes, llaves, paréntesis, `|`, `/` y `_`
  conservan la profundidad de −180, en el nuevo `sign_descender`.
- Trazo un 15 % más grueso en toda la rampa: 46 en Display (peso 200), 86 en el peso 500 y en Lectura,
  y 122 en el peso 700.

## [0.2.0] - 2026-10-16

### Cambiado

- Proporciones y formas revisadas para que se lea menos infantil: altura x 425, ascendentes 840,
  descendentes −180, esquinas con radio 50, aperturas a 30° y espaciado 1.5.
- El peso de Display pasa de 29 a 40; el eje variable va de 40 (200) a 106 (700) y conserva 75 en 500.
- La `G` vuelve a llevar barra; la enroscada queda como `g_form="curl"`.
- Las fuentes son de un solo color; el detalle a color queda como `color_details=True`.
- El paquete npm se llama `rotulo`, sin scope; `@npmegar/rotulo` queda deprecado.

### Eliminado

- La paleta oscura automática de la hoja de estilos: sin capas de color ya no aplica.

## [0.1.1] - 2026-10-15

### Cambiado

- El detalle usa por defecto `#3d8a8f`, legible sobre fondo claro y oscuro; antes `#2f5d62` se perdía
  en fondos oscuros.
- La hoja de estilos activa la paleta oscura con `prefers-color-scheme: dark`, para `Rotulo` y
  `Rotulo Lectura` con un solo `--rotulo-dark`.

### Agregado

- Declaración de tipos en el paquete npm: `import '@npmegar/rotulo'` ya no pide un `declare module`.

### Eliminado

- `--rotulo-lectura-dark`: lo cubre `--rotulo-dark`.

## [0.1.0] - 2026-10-15

### Agregado

- Generador de la tipografía desde esqueletos de rectas y arcos, expandidos con un trazo redondo.
- Fuente variable de peso de 200 a 700, con un trazador de cápsulas de estructura fija.
- Estilos estáticos Display (peso 29) y Lectura (peso 75, más espacio y letras difíciles de reflejar),
  con hinting.
- Detalle a color con capas COLR y paletas para fondo claro y oscuro.
- Formas de lectura en `ss01`: `l` con cola, `q` con barra, `1` con bandera curva y `9` recto.
- Latín para español, portugués, francés y catalán, cifras, signos, comillas y kerning.
- Paquete npm `@npmegar/rotulo` con WOFF2 y las reglas `@font-face`.
