from typing import Any

import pathops

from rotulo.context import Glyph
from rotulo.skeleton import Stroke


def _skeleton_path(stroke: Stroke, dx: float) -> Any:
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


def outline(glyph: Glyph, weight: float, dx: float) -> Any:
    result = pathops.Path()
    for stroke in [*glyph.strokes, *glyph.details]:
        path = _skeleton_path(stroke, dx)
        path.stroke(weight, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
        path.convertConicsToQuads()
        result.addPath(path)
    result.simplify(fix_winding=True, keep_starting_points=False, clockwise=True)
    return result
