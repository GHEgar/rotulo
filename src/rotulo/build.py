from pathlib import Path
from typing import Any

from fontTools.colorLib.builder import ColorPaletteType, buildCOLR, buildCPAL
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder

from rotulo.glyphset import GlyphSet, build_context, collect, glyph_name
from rotulo.params import Params
from rotulo.spacing import kerning

FAMILY = "Rotulo"
VERSION = "0.2.0"
LICENSE = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
LICENSE_URL = "https://openfontlicense.org"
DETAIL_LIGHT = (0x3D / 255, 0x8A / 255, 0x8F / 255, 1.0)
DETAIL_DARK = (0x7F / 255, 0xB7 / 255, 0xB5 / 255, 1.0)

__all__ = ["build_context", "build_font", "font_builder", "glyph_name"]


def features(gs: GlyphSet) -> str:
    blocks = []
    rules = [
        f"    pos {gs.names[a]} {gs.names[b]} {v};"
        for (a, b), v in sorted(kerning(gs.ctx).items())
        if a in gs.names and b in gs.names
    ]
    if rules:
        blocks.append("feature kern {\n" + "\n".join(rules) + "\n} kern;")
    if gs.alternates:
        subs = "\n".join(f"    sub {base} by {alt};" for base, alt in gs.alternates.items())
        blocks.append(
            'feature ss01 {\n    featureNames { name "Lectura"; };\n' + subs + "\n} ss01;"
        )
    return "\n".join(blocks) + "\n"


def font_builder(params: Params, style: str, weight_class: int, gs: GlyphSet) -> Any:
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(gs.order)
    fb.setupCharacterMap(gs.cmap)
    fb.setupGlyf(gs.glyphs)
    glyf = fb.font["glyf"]
    fb.setupHorizontalMetrics({n: (gs.advances[n], getattr(glyf[n], "xMin", 0)) for n in gs.order})
    y_max = max(getattr(glyf[n], "yMax", 0) for n in gs.order)
    y_min = min(getattr(glyf[n], "yMin", 0) for n in gs.order)
    fb.setupHorizontalHeader(ascent=y_max, descent=y_min)
    ps = f"{FAMILY}-{style}"
    fb.setupNameTable(
        {
            "familyName": FAMILY,
            "styleName": style,
            "uniqueFontIdentifier": f"{ps};{VERSION}",
            "fullName": f"{FAMILY} {style}",
            "psName": ps,
            "version": f"Version {VERSION}",
            "licenseDescription": LICENSE,
            "licenseInfoURL": LICENSE_URL,
        }
    )
    fb.setupOS2(
        usWeightClass=weight_class,
        sTypoAscender=round(params.ascender),
        sTypoDescender=round(params.descender),
        sTypoLineGap=200,
        usWinAscent=y_max,
        usWinDescent=-y_min,
        sxHeight=round(params.x_height),
        sCapHeight=round(params.cap_height),
        fsType=0,
    )
    fb.setupPost()
    if gs.layers:
        fb.font["COLR"] = buildCOLR(gs.layers, version=0)
        fb.font["CPAL"] = buildCPAL(
            [[DETAIL_LIGHT], [DETAIL_DARK]],
            paletteTypes=[
                0,
                ColorPaletteType.USABLE_WITH_DARK_BACKGROUND,
            ],
        )
    addOpenTypeFeaturesFromString(fb.font, features(gs))
    return fb


def build_font(params: Params, style: str, weight_class: int, out: Path, hint: bool = True) -> Path:
    gs = collect(params)
    fb = font_builder(params, style, weight_class, gs)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{FAMILY}-{style}.ttf"
    fb.save(str(path))
    if hint:
        from ttfautohint import ttfautohint

        ttfautohint(in_file=str(path), out_file=str(path))
    return path
