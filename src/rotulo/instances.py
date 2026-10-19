from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import OverlapMode, instantiateVariableFont

from rotulo.build import FAMILY

MAP_WEIGHTS = {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700}


def _rename(font: TTFont, style: str, weight: int) -> None:
    name = font["name"]
    full = f"{FAMILY} {style}"
    ps = f"{FAMILY}-{style}"
    ribbi = style if style in ("Regular", "Bold") else "Regular"
    legacy = FAMILY if ribbi == style else full
    name.removeNames(platformID=1)
    for name_id in (16, 17, 25):
        name.removeNames(nameID=name_id)
    for name_id, value in ((1, legacy), (2, ribbi), (3, ps), (4, full), (6, ps)):
        name.setName(value, name_id, 3, 1, 0x409)
    if ribbi != style:
        name.setName(FAMILY, 16, 3, 1, 0x409)
        name.setName(style, 17, 3, 1, 0x409)
    font["OS/2"].usWeightClass = weight
    bold = style == "Bold"
    font["OS/2"].fsSelection = (font["OS/2"].fsSelection & ~0b1100001) | (0x20 if bold else 0x40)
    font["head"].macStyle = 1 if bold else 0


def build_instances(variable: Path, out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for style, weight in MAP_WEIGHTS.items():
        font = instantiateVariableFont(
            TTFont(str(variable)), {"wght": weight}, overlap=OverlapMode.REMOVE
        )
        _rename(font, style, weight)
        path = out / f"{FAMILY}-{style}.ttf"
        font.save(str(path))
        written.append(path)
    return written
