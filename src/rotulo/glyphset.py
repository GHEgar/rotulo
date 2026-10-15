from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from fontTools.agl import UV2AGL
from fontTools.pens.ttGlyphPen import TTGlyphPen

from rotulo.accents import add_accents
from rotulo.chars import DOTLESS_I
from rotulo.context import Context
from rotulo.figures import add_figures
from rotulo.lowercase import add_lowercase
from rotulo.outline import tt_glyph
from rotulo.params import Params
from rotulo.skeleton import Stroke
from rotulo.spacing import placement, space_width
from rotulo.symbols import add_symbols
from rotulo.uppercase import add_uppercase

Draw = Callable[[Sequence[Stroke], float, float], Any]
FOREGROUND = 0xFFFF
READING_ALTERNATES = "lq19"


def glyph_name(ch: str) -> str:
    cp = ord(ch)
    return str(UV2AGL.get(cp, f"uni{cp:04X}"))


def build_context(params: Params) -> Context:
    ctx = Context(params)
    add_lowercase(ctx)
    add_uppercase(ctx)
    add_figures(ctx)
    add_symbols(ctx)
    add_accents(ctx)
    return ctx


def reading_forms(params: Params) -> Params:
    return replace(params, l_form="tail", q_bar=True, one_flag=True, nine_straight=True)


def notdef() -> Any:
    pen = TTGlyphPen(None)
    for (x0, y0), (x1, y1), inner in (((50, 0), (450, 700), False), ((100, 50), (400, 650), True)):
        pts = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
        if inner:
            pts.reverse()
        pen.moveTo(pts[0])
        for pt in pts[1:]:
            pen.lineTo(pt)
        pen.closePath()
    return pen.glyph()


@dataclass
class GlyphSet:
    ctx: Context
    names: dict[str, str] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)
    glyphs: dict[str, Any] = field(default_factory=dict)
    advances: dict[str, int] = field(default_factory=dict)
    layers: dict[str, list[tuple[str, int]]] = field(default_factory=dict)
    alternates: dict[str, str] = field(default_factory=dict)

    @property
    def cmap(self) -> dict[int, str]:
        return {32: "space", **{ord(ch): name for ch, name in self.names.items()}}

    def add(self, name: str, glyph: Any, advance: float) -> None:
        self.order.append(name)
        self.glyphs[name] = glyph
        self.advances[name] = round(advance)


def collect(params: Params, draw: Draw = tt_glyph, color: bool = True) -> GlyphSet:
    ctx = build_context(params)
    gs = GlyphSet(ctx)
    gs.add(".notdef", notdef(), 500)
    gs.add("space", TTGlyphPen(None).glyph(), space_width(ctx))
    extra: list[tuple[str, Any, float]] = []
    for ch, g in ctx.glyphs.items():
        if ch == DOTLESS_I:
            continue
        name = glyph_name(ch)
        gs.names[ch] = name
        place = placement(ctx, ch, g)
        gs.add(name, draw([*g.strokes, *g.details], params.weight, place.dx), place.advance)
        if not color or not g.details:
            continue
        layers = []
        if g.strokes:
            extra.append((f"{name}.body", draw(g.strokes, params.weight, place.dx), place.advance))
            layers.append((f"{name}.body", FOREGROUND))
        extra.append((f"{name}.detail", draw(g.details, params.weight, place.dx), place.advance))
        layers.append((f"{name}.detail", 0))
        gs.layers[name] = layers
    alt = reading_forms(params)
    if alt != params:
        actx = build_context(alt)
        for ch in READING_ALTERNATES:
            ag = actx.glyphs[ch]
            place = placement(actx, ch, ag)
            name = f"{glyph_name(ch)}.ss01"
            extra.append(
                (name, draw([*ag.strokes, *ag.details], params.weight, place.dx), place.advance)
            )
            gs.alternates[glyph_name(ch)] = name
    for name, glyph, advance in extra:
        gs.add(name, glyph, advance)
    return gs
