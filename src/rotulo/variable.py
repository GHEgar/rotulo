from dataclasses import replace
from pathlib import Path
from typing import Any

from fontTools.cu2qu import curves_to_quadratic
from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, SourceDescriptor
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import flagOverlapSimple
from fontTools.varLib import build

from rotulo.build import FAMILY, font_builder
from rotulo.capsule import Contour, capsules
from rotulo.glyphset import GlyphSet, collect
from rotulo.params import DISPLAY, Params

AXIS_MIN, AXIS_MAX = 200, 500
MAX_ERROR = 1.0


def _quadratic(masters: list[list[Contour]]) -> list[Any]:
    pens = [TTGlyphPen(None) for _ in masters]
    for contours in zip(*masters, strict=True):
        starts = [contour[0][0] for contour in contours]
        for pen, start in zip(pens, starts, strict=True):
            pen.moveTo(start)
        last = len(contours[0]) - 1
        for i, cubics in enumerate(zip(*contours, strict=True)):
            splines = curves_to_quadratic(list(cubics), [MAX_ERROR] * len(cubics))
            for pen, spline, start in zip(pens, splines, starts, strict=True):
                points = list(spline[1:])
                if i == last:
                    points[-1] = start
                pen.qCurveTo(*points)
        for pen in pens:
            pen.closePath()
    glyphs = [pen.glyph() for pen in pens]
    for glyph in glyphs:
        if glyph.numberOfContours > 0:
            glyph.flags[0] |= flagOverlapSimple
    return glyphs


def _compatible(sets: list[GlyphSet]) -> None:
    for name in sets[0].order:
        outlines = [gs.glyphs[name] for gs in sets]
        if not isinstance(outlines[0], list):
            continue
        for gs, glyph in zip(sets, _quadratic(outlines), strict=True):
            gs.glyphs[name] = glyph


def build_variable(out: Path, light: Params = DISPLAY, heavy_weight: float = 75) -> Path:
    masters = [light, replace(light, weight=heavy_weight)]
    sets = [collect(p, draw=capsules) for p in masters]
    _compatible(sets)
    doc = DesignSpaceDocument()
    doc.addAxis(
        AxisDescriptor(
            tag="wght",
            name="Weight",
            minimum=AXIS_MIN,
            default=AXIS_MIN,
            maximum=AXIS_MAX,
            map=[(AXIS_MIN, light.weight), (AXIS_MAX, heavy_weight)],
        )
    )
    for params, gs, style in zip(masters, sets, ("Display", "Heavy"), strict=True):
        source = SourceDescriptor()
        source.font = font_builder(params, style, 200, gs).font
        source.location = {"Weight": params.weight}
        source.styleName = style
        doc.addSource(source)
    font, _, _ = build(doc)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{FAMILY}[wght].ttf"
    font.save(str(path))
    return path
