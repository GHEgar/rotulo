from pathlib import Path

from fontTools.agl import UV2AGL
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

from rotulo.chars import DOTLESS_I
from rotulo.context import Context
from rotulo.figures import add_accents, add_figures
from rotulo.lowercase import add_lowercase
from rotulo.outline import outline
from rotulo.params import Params
from rotulo.spacing import kerning, placement, space_width
from rotulo.uppercase import add_uppercase

FAMILY = "Rotulo"
LICENSE = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
LICENSE_URL = "https://openfontlicense.org"


def glyph_name(ch: str) -> str:
    cp = ord(ch)
    return str(UV2AGL.get(cp, f"uni{cp:04X}"))


def build_context(params: Params) -> Context:
    ctx = Context(params)
    add_lowercase(ctx)
    add_uppercase(ctx)
    add_figures(ctx)
    add_accents(ctx)
    return ctx


def _notdef() -> object:
    pen = TTGlyphPen(None)
    for box in (((50, 0), (450, 700)), ((100, 50), (400, 650))):
        (x0, y0), (x1, y1) = box
        pts = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
        if box[0] == (100, 50):
            pts.reverse()
        pen.moveTo(pts[0])
        for pt in pts[1:]:
            pen.lineTo(pt)
        pen.closePath()
    return pen.glyph()


def build_font(params: Params, style: str, weight_class: int, out: Path) -> Path:
    ctx = build_context(params)
    chars = [ch for ch in ctx.glyphs if ch != DOTLESS_I]
    names = {ch: glyph_name(ch) for ch in chars}
    order = [".notdef", "space", *names.values()]
    glyphs: dict[str, object] = {".notdef": _notdef(), "space": TTGlyphPen(None).glyph()}
    advances: dict[str, int] = {".notdef": 500, "space": round(space_width(ctx))}
    for ch in chars:
        g = ctx.glyphs[ch]
        place = placement(ctx, ch, g)
        pen = TTGlyphPen(None)
        outline(g, params.weight, place.dx).draw(Cu2QuPen(pen, 1.0, reverse_direction=False))
        glyphs[names[ch]] = pen.glyph()
        advances[names[ch]] = round(place.advance)

    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({32: "space", **{ord(ch): names[ch] for ch in chars}})
    fb.setupGlyf(glyphs)
    glyf = fb.font["glyf"]
    fb.setupHorizontalMetrics({n: (advances[n], getattr(glyf[n], "xMin", 0)) for n in order})
    y_max = max(getattr(glyf[n], "yMax", 0) for n in order)
    y_min = min(getattr(glyf[n], "yMin", 0) for n in order)
    fb.setupHorizontalHeader(ascent=y_max, descent=y_min)
    ps = f"{FAMILY}-{style}"
    fb.setupNameTable(
        {
            "familyName": FAMILY,
            "styleName": style,
            "uniqueFontIdentifier": f"{ps};0.1.0",
            "fullName": f"{FAMILY} {style}",
            "psName": ps,
            "version": "Version 0.100",
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
    pairs = kerning(ctx)
    if pairs:
        rules = "\n".join(
            f"    pos {names[a]} {names[b]} {v};"
            for (a, b), v in sorted(pairs.items())
            if a in names and b in names
        )
        addOpenTypeFeaturesFromString(fb.font, f"feature kern {{\n{rules}\n}} kern;\n")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{ps}.ttf"
    fb.save(str(path))
    return path
