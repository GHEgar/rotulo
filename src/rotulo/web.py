from pathlib import Path

from fontTools.ttLib import TTFont

WEB_NAMES = {
    "Rotulo-Variable.ttf": "Rotulo-Variable.woff2",
    "Rotulo-Display.ttf": "Rotulo-Display.woff2",
    "Rotulo-Lectura.ttf": "Rotulo-Lectura.woff2",
    "RotuloSans-Variable.ttf": "RotuloSans-Variable.woff2",
    "RotuloSans-Medium.ttf": "RotuloSans-Medium.woff2",
}


def to_woff2(fonts: Path, out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for source, target in WEB_NAMES.items():
        path = fonts / source
        if not path.exists():
            continue
        font = TTFont(str(path))
        font.flavor = "woff2"
        font.save(str(out / target))
        written.append(out / target)
    return written
