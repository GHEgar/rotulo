import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

from rotulo.params import Params
from rotulo.skeleton import DEG, Point, Stroke, Transform

Side = Literal["h", "o", "v"]


@dataclass
class Glyph:
    width: float
    left: Side
    right: Side
    strokes: list[Stroke]
    details: list[Stroke]
    ax: float


@dataclass(frozen=True)
class BarFillet:
    th: float
    c: Point
    phi: float


@dataclass
class Context:
    p: Params
    glyphs: dict[str, Glyph] = field(default_factory=dict)

    def __post_init__(self) -> None:
        p = self.p
        self.xh = p.x_height
        self.cap = p.cap_height
        self.asc = p.ascender
        self.desc = p.descender
        self.w = p.weight
        self.o = self.xh * p.overshoot / 100
        self.gap = p.gap
        self.bowl = self.xh * p.width * 0.96
        self.nw = self.bowl * 0.9
        self.h2 = self.nw / 2
        self.ry = self.xh / 2 + self.o
        self.yt = self.xh + self.w + self.gap
        self.yc = self.cap + self.w + self.gap
        self.dot_len = self.xh * 0.1 + self.w * 0.3
        self.dv = (
            0.0 if p.dot == "round" else self.dot_len if p.dot == "line" else self.dot_len * 0.7
        )
        self.hr = self.xh * 0.3
        self.hs = p.tail_close
        self.hx = self.hr * p.tail
        self.lr = self.xh * 0.2
        self.sharp = 0.35
        self.fig = self.cap * 0.58

    def pen(self, transform: Transform | None = None, sharp: float = 1.0) -> Stroke:
        return Stroke(self.p.corner * sharp, transform)

    def define(
        self,
        ch: str,
        width: float,
        left: Side,
        right: Side,
        strokes: Sequence[Stroke],
        details: Sequence[Stroke] = (),
        ax: float | None = None,
    ) -> None:
        self.glyphs[ch] = Glyph(
            width, left, right, list(strokes), list(details), width / 2 if ax is None else ax
        )

    def ring(
        self, cx: float, cy: float, rx: float, ry: float, transform: Transform | None = None
    ) -> Stroke:
        return self.pen(transform).a(cx, cy, rx, ry, 90, 450)

    def dot(self, x: float, y: float, transform: Transform | None = None) -> Stroke:
        s = self.pen(transform)
        if self.p.dot == "round":
            return s.m(x, y).l(x + 0.01, y)
        if self.p.dot == "line":
            return s.m(x, y).l(x, y + self.dot_len)
        return s.m(x - self.dot_len * 0.35, y).l(x + self.dot_len * 0.35, y + self.dot_len * 0.7)

    def acute(self, x: float, y: float) -> Stroke:
        return self.pen().m(x - self.xh * 0.06, y).l(x + self.xh * 0.08, y + self.xh * 0.18)

    def dieresis(self, x: float, y: float) -> list[Stroke]:
        return [self.dot(x - self.xh * 0.15, y), self.dot(x + self.xh * 0.15, y)]

    def tilde(self, x: float, y: float) -> Stroke:
        t, a = self.xh * 0.2, self.xh * 0.06
        return (
            self.pen().a(x - t / 2, y + a, t / 2, a, 180, 0).a(x + t / 2, y + a, t / 2, a, 180, 360)
        )

    def soft_tail(
        self,
        x: float,
        top: float,
        wx: float,
        sweep: float,
        base: Stroke | None = None,
        bottom: float | None = None,
    ) -> Stroke:
        bot = self.desc if bottom is None else bottom
        hr = self.hr
        ys = bot + hr * 1.6
        s = base if base is not None else self.pen().m(x, top)
        return (
            s.l(x, ys)
            .c(x, ys - (ys - bot) * 0.55, x - wx * 0.45, bot, x - wx, bot)
            .a(x - wx, bot + hr, wx * 0.8, hr, -90, -sweep)
        )

    def bar_fillet(
        self, cx: float, cy: float, rx: float, ry: float, bar_y: float, r: float, side: int
    ) -> BarFillet:
        def at(th: float) -> tuple[Point, Point]:
            nx, ny = math.cos(th) / rx, math.sin(th) / ry
            nl = math.hypot(nx, ny)
            e = (cx + rx * math.cos(th), cy + ry * math.sin(th))
            return e, (e[0] - r * nx / nl, e[1] - r * ny / nl)

        def f(th: float) -> float:
            return at(th)[1][1] - (bar_y + side * r)

        lo, hi = (0.0, math.pi / 2) if side > 0 else (-math.pi / 2, 0.0)
        for _ in range(50):
            mid = (lo + hi) / 2
            if math.copysign(1, f(mid)) == math.copysign(1, f(lo)):
                lo = mid
            else:
                hi = mid
        th = (lo + hi) / 2
        e, c = at(th)
        return BarFillet(th / DEG, c, math.atan2(e[1] - c[1], e[0] - c[0]) / DEG)
