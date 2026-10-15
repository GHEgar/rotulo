import unicodedata
from dataclasses import dataclass

from rotulo.context import Context, Glyph

KERN: dict[str, float] = {
    "AV": -0.1,
    "VA": -0.1,
    "AT": -0.08,
    "TA": -0.08,
    "AY": -0.08,
    "YA": -0.08,
    "LT": -0.12,
    "LV": -0.1,
    "LY": -0.1,
    "Ta": -0.1,
    "Te": -0.1,
    "To": -0.1,
    "Tu": -0.06,
    "Tr": -0.06,
    "Ty": -0.06,
    "Va": -0.06,
    "Ve": -0.06,
    "Vo": -0.06,
    "Ya": -0.08,
    "Yo": -0.08,
    "F.": -0.1,
    "P.": -0.1,
    "T.": -0.1,
    "V.": -0.1,
    "r.": -0.06,
    "v.": -0.05,
    "y.": -0.05,
    "r,": -0.06,
}
DESCENDER_J = ("g", "j", "p", "q", "y")


@dataclass(frozen=True)
class Placement:
    dx: float
    advance: float


def side_bearing(ctx: Context, side: str) -> float:
    unit = ctx.xh * 0.14 * ctx.p.spacing
    return {"h": unit, "o": unit * 0.62, "v": unit * 0.18}[side]


def narrow_air(ctx: Context, ch: str, glyph: Glyph) -> float:
    if not ch.isalpha():
        return 0.0
    return max(0.0, 1 - glyph.width / (ctx.xh * 0.5)) * ctx.xh * ctx.p.narrow_air * 0.5


def placement(ctx: Context, ch: str, glyph: Glyph) -> Placement:
    air = narrow_air(ctx, ch, glyph)
    dx = side_bearing(ctx, glyph.left) + air + ctx.w / 2
    advance = dx + glyph.width + ctx.w / 2 + side_bearing(ctx, glyph.right) + air
    return Placement(dx, advance)


def space_width(ctx: Context) -> float:
    return ctx.xh * 0.5 * ctx.p.spacing * ctx.p.word_spacing


def _base(ch: str) -> str:
    return unicodedata.normalize("NFD", ch)[0]


def kerning(ctx: Context) -> dict[tuple[str, str], int]:
    chars = list(ctx.glyphs)
    pairs: dict[tuple[str, str], int] = {}
    for a in chars:
        for b in chars:
            value = KERN.get(_base(a) + _base(b))
            if value:
                pairs[(a, b)] = round(value * ctx.cap)
    for a in DESCENDER_J:
        pairs[(a, "j")] = round(ctx.xh * 0.15)
    return pairs
