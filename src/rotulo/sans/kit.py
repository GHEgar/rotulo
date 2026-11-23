import itertools
import math
from collections.abc import Callable

from rotulo.context import Context
from rotulo.outline import outline
from rotulo.params import Sans
from rotulo.skeleton import Stroke

Shape = tuple[list[Stroke], list[Stroke]]


class Kit:
    def __init__(self, ctx: Context, sans: Sans) -> None:
        self.ctx = ctx
        self.s = sans
        self.w = ctx.w
        self.h = ctx.w / 2
        self.x = ctx.xh
        self.cap = ctx.cap
        self.asc = ctx.asc
        self.desc = ctx.desc
        self.ov = ctx.o
        self.ap = ctx.p.aperture
        self.bw = ctx.xh * sans.width - ctx.w
        self.cw = sans.cap_width
        self.shift = 0.0

    def pen(self) -> Stroke:
        dx = self.shift
        return Stroke(0, lambda x, y: (x - dx, y))

    def rarc(
        self,
        pen: Stroke,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        a0: float,
        a1: float,
        stadium: bool | None = None,
    ) -> Stroke:
        cx, rx = (x0 + x1) / 2, (x1 - x0) / 2
        if stadium is None:
            stadium = self.s.stadium and (y1 - y0) > (x1 - x0) * 1.05
        if not stadium:
            return pen.a(cx, (y0 + y1) / 2, rx, (y1 - y0) / 2, a0, a1)
        yt, yb = y1 - rx, y0 + rx
        up = a1 > a0
        step = 180 if up else -180
        cuts = [a0]
        k = math.floor(a0 / 180) * 180 + (180 if up else 0)
        if not up and k == a0:
            k -= 180
        while (k - a1) * step < 0:
            if k != a0:
                cuts.append(k)
            k += step
        cuts.append(a1)
        for a, b in itertools.pairwise(cuts):
            mid = ((a + b) / 2) % 360
            pen.a(cx, yt if mid < 180 else yb, rx, rx, a, b)
        return pen

    def loop(
        self, x0: float, y0: float, x1: float, y1: float, stadium: bool | None = None
    ) -> Stroke:
        if stadium is None:
            stadium = self.s.stadium and (y1 - y0) > (x1 - x0) * 1.05
        pen = self.rarc(self.pen(), x0, y0, x1, y1, 0, 360, stadium)
        if stadium:
            pen.l(x1, y1 - (x1 - x0) / 2)
        return pen

    def stem(self, x: float, y0: float, y1: float) -> Stroke:
        return self.pen().m(x, y0 + self.h).l(x, y1 - self.h)

    def diag(
        self, ax: float, ay: float, bx: float, by: float, end_a: bool = True, end_b: bool = True
    ) -> Stroke:
        ln = math.hypot(bx - ax, by - ay)
        dx, dy = (bx - ax) / ln, (by - ay) / ln
        k = self.h / max(abs(dy), 0.2)
        sa, sb = (k if end_a else 0.0), (k if end_b else 0.0)
        return self.pen().m(ax + dx * sa, ay + dy * sa).l(bx - dx * sb, by - dy * sb)

    def dot(self, x: float) -> Stroke:
        y = max(self.cap - self.h, self.x + self.w * 0.9 + self.h)
        return self.pen().m(x, y).l(x + 0.01, y)

    def put(
        self,
        ch: str,
        draw: Callable[[], Shape],
        ax: float | None = None,
        width: float | None = None,
    ) -> None:
        self.shift = 0.0
        if width is None:
            strokes, details = draw()
            x0, _, x1, _ = outline([*strokes, *details], self.w, 0).bounds
            self.shift = x0 + self.h
            width = x1 - x0 - self.w
        strokes, details = draw()
        center = None if ax is None else ax - self.shift
        self.ctx.define(ch, width, "h", "h", strokes, details, center)
        self.shift = 0.0
