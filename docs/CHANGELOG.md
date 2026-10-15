# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado con
[SemVer](https://semver.org/lang/es/).

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
