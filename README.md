# <picture><source media="(prefers-color-scheme: dark)" srcset=".github/assets/icon-dark.svg"><img src=".github/assets/icon-light.svg" width="36" height="36" alt=""></picture> rotulo

[![npm](https://img.shields.io/npm/v/@npmegar/rotulo)](https://www.npmjs.com/package/@npmegar/rotulo) [![PyPI](https://img.shields.io/pypi/v/rotulo)](https://pypi.org/project/rotulo/) [![license](https://img.shields.io/badge/license-OFL--1.1-blue)](LICENSE)

Monoline typeface generated from skeletons: strokes of lines and arcs expanded with a round pen.

![Rotulo Display and Rotulo Lectura specimen](.github/assets/specimen.png)

Every letter is a skeleton of straight lines and arcs drawn in code, never a hand-drawn outline. The
generator expands each skeleton with a round pen and writes TrueType and WOFF2 fonts. Weight is the
pen width, so the family is a variable font from 200 to 500. Floating details (dots, accents, the zero
slash, punctuation) are a second color layer. A reading cut, **Lectura**, adds weight, spacing and
letters that are hard to mirror.

## Install

```bash
npm install @npmegar/rotulo
pip install rotulo
```

| Package | What it is | Needs |
|---|---|---|
| `@npmegar/rotulo` | WOFF2 files and a stylesheet with the `@font-face` rules | A bundler that resolves CSS imports, or a plain `<link>` |
| `rotulo` | The generator: builds every font from the skeletons | Python 3.12 or later |

The TTF files are attached to each [GitHub release](https://github.com/GHEgar/rotulo/releases).

## Quick start

```css
@import '@npmegar/rotulo';

body {
    font-family: 'Rotulo', system-ui, sans-serif;
    font-weight: 200;
}

.reading {
    font-family: 'Rotulo Lectura', 'Rotulo', sans-serif;
}
```

```bash
python -m rotulo --out build --web build/web
```

## Fonts

| Family | File | Weight | Use |
|---|---|---|---|
| `Rotulo` | `Rotulo-Variable.woff2`, `Rotulo[wght].ttf` | 200 to 500 | Map labels, interface, titles |
| `Rotulo` | `Rotulo-Display.ttf` | 200, static and hinted | Renderers without variable fonts, such as GeoServer or PDF libraries |
| `Rotulo Lectura` | `Rotulo-Lectura.woff2`, `.ttf` | 500, static and hinted | Long reading |

## Color details

Dots, accents, the zero slash and punctuation sit on a color layer (COLR/CPAL). The body takes the text
color; the detail takes the palette color. Renderers without color fonts draw the whole letter in the
text color.

| Palette | Detail color | CSS |
|---|---|---|
| 0, light backgrounds | `#2f5d62` | default |
| 1, dark backgrounds | `#7fb7b5` | `font-palette: --rotulo-dark` |

Override the detail color with `@font-palette-values` and `override-colors: 0 <color>`.

## Reading forms

`ss01` switches four letters to the forms of Lectura: `l` with a tail, `q` with a crossed tail, a curved
flag on `1` and a straight `9`.

```css
.labels {
    font-feature-settings: 'ss01';
}
```

## Using the fonts outside the web

| Where | How |
|---|---|
| GeoServer | Copy `Rotulo-Display.ttf` into the font directory and name `Rotulo` in the SLD `font-family` |
| PDF | Embed `Rotulo-Display.ttf` or `Rotulo-Lectura.ttf` |

## Parameters

`Params` holds every design decision, in units of a 1000 em:

| Field | Default | What it controls |
|---|---|---|
| `weight` | 29 | Pen width |
| `x_height`, `cap_height` | 420, 700 | Body and capital heights |
| `ascender`, `descender` | 800, −260 | Shared by every letter with a tail |
| `corner` | 70 | Radius used to round every skeleton vertex |
| `gap` | 110 | Space between a stroke and a floating detail |
| `spacing`, `word_spacing` | 1.56, 1.0 | Side bearings and space width |
| `narrow_air` | 0.3 | Extra room around narrow letters such as `i`, `l`, `t` |

```python
from dataclasses import replace
from pathlib import Path

from rotulo import DISPLAY, build_font

print(build_font(replace(DISPLAY, weight=50), "Medium", 400, Path("build")))
```

## Known limitations

- Latin script: Spanish, Portuguese, French and Catalan, figures and common symbols.
- The variable font keeps overlapping strokes and is not hinted; use the static files at small sizes
  on Windows.
- Detail colors need COLR support. Safari, Chrome, Firefox and Windows render them; older renderers draw
  one color.

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check src tests && ruff format --check src tests
mypy
```

The tests build every font and check heights against the skeleton, kerning, color layers, `ss01`,
hinting and that the variable font interpolates every glyph.

## Contributing

Issues are welcome. Please open one before sending a pull request.

## License

OFL-1.1 © GHEgar
