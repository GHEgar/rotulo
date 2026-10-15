from collections.abc import Sequence
from typing import Any

import pathops
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

from rotulo.skeleton import Stroke


def skeleton_path(stroke: Stroke, dx: float) -> Any:
    path = pathops.Path()
    pen = path.getPen()
    open_contour = False
    for kind, pts in stroke.finish():
        moved = [(x + dx, y) for x, y in pts]
        if kind == "M":
            if open_contour:
                pen.endPath()
            pen.moveTo(moved[0])
            open_contour = True
        elif kind == "L":
            pen.lineTo(moved[0])
        else:
            pen.curveTo(*moved)
    if open_contour:
        pen.endPath()
    return path


def outline(strokes: Sequence[Stroke], weight: float, dx: float) -> Any:
    result = pathops.Path()
    for stroke in strokes:
        path = skeleton_path(stroke, dx)
        path.stroke(weight, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
        path.convertConicsToQuads()
        result.addPath(path)
    result.simplify(fix_winding=True, keep_starting_points=False, clockwise=True)
    return result


def tt_glyph(strokes: Sequence[Stroke], weight: float, dx: float) -> Any:
    pen = TTGlyphPen(None)
    outline(strokes, weight, dx).draw(Cu2QuPen(pen, 1.0, reverse_direction=False))
    return pen.glyph()
