from rotulo.chars import DOTLESS_I
from rotulo.context import Context
from rotulo.skeleton import Stroke


def add_accents(ctx: Context) -> None:
    g, xh, pen, sh = ctx.glyphs, ctx.xh, ctx.pen, ctx.sharp

    def compose(ch: str, base: str, extra: list[Stroke]) -> None:
        b = g[base]
        ctx.define(ch, b.width, b.left, b.right, b.strokes, [*b.details, *extra], b.ax)

    def grave(x: float, y: float) -> Stroke:
        return pen().m(x + xh * 0.06, y).l(x - xh * 0.08, y + xh * 0.18)

    def circumflex(x: float, y: float) -> Stroke:
        return pen(sharp=sh).m(x - xh * 0.12, y).l(x, y + xh * 0.16).l(x + xh * 0.12, y)

    def cedilla(x: float) -> Stroke:
        y0, r = -(ctx.w + ctx.gap * 0.5), xh * 0.08
        return pen().m(x, y0).a(x, y0 - r, r, r, 90, -150)

    marks = {
        "acute": ctx.acute,
        "grave": grave,
        "circumflex": circumflex,
    }
    lower = {"a": "a", "e": "e", "i": DOTLESS_I, "o": "o", "u": "u"}
    upper = {"A": "A", "E": "E", "I": "I", "O": "O", "U": "U"}
    table = {
        "acute": ("áéíóú", "ÁÉÍÓÚ"),
        "grave": ("àèìòù", "ÀÈÌÒÙ"),
        "circumflex": ("âêîôû", "ÂÊÎÔÛ"),
    }
    for mark, (low, up) in table.items():
        draw = marks[mark]
        for ch, base in zip(low, lower.values(), strict=True):
            compose(ch, base, [draw(0 if base == DOTLESS_I else g[base].ax, ctx.yt)])
        for ch, base in zip(up, upper.values(), strict=True):
            compose(ch, base, [draw(g[base].ax, ctx.yc)])
    for ch, base in (("ñ", "n"), ("ã", "a"), ("õ", "o")):
        compose(ch, base, [ctx.tilde(g[base].ax, ctx.yt)])
    for ch, base in (("Ñ", "N"), ("Ã", "A"), ("Õ", "O")):
        compose(ch, base, [ctx.tilde(g[base].ax, ctx.yc)])
    for ch, base in (("ü", "u"), ("ë", "e"), ("ï", DOTLESS_I), ("ÿ", "y")):
        compose(ch, base, ctx.dieresis(0 if base == DOTLESS_I else g[base].ax, ctx.yt))
    for ch, base in (("Ü", "U"), ("Ë", "E"), ("Ï", "I")):
        compose(ch, base, ctx.dieresis(g[base].ax, ctx.yc))
    compose("ç", "c", [cedilla(g["c"].ax)])
    compose("Ç", "C", [cedilla(g["C"].ax)])
