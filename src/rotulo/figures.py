import math

from rotulo.chars import DOTLESS_I, DOUBLE_PRIME, EN_DASH, PRIME
from rotulo.context import Context
from rotulo.skeleton import DEG, Stroke


def two_end(cx: float, cy: float, rx: float, ry: float) -> float:
    def f(deg: float) -> float:
        t = deg * DEG
        px, py = cx + rx * math.cos(t), cy + ry * math.sin(t)
        tx, ty = rx * math.sin(t), -ry * math.cos(t)
        return tx * (0 - py) - ty * (0 - px)

    prev = 150.0
    for step in range(1, 300):
        cur = 150.0 - step
        if math.copysign(1, f(cur)) != math.copysign(1, f(prev)):
            lo, hi = cur, prev
            for _ in range(40):
                mid = (lo + hi) / 2
                if math.copysign(1, f(mid)) == math.copysign(1, f(lo)):
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev = cur
    return -25.0


def add_figures(ctx: Context) -> None:
    p, pen, d = ctx.p, ctx.pen, ctx.define
    cap, xh, asc, desc, o, w, gap, dot_len, dv, fig = (
        ctx.cap,
        ctx.xh,
        ctx.asc,
        ctx.desc,
        ctx.o,
        ctx.w,
        ctx.gap,
        ctx.dot_len,
        ctx.dv,
        ctx.fig,
    )

    def zero_detail() -> list[Stroke]:
        if p.zero == "plain":
            return []
        if p.zero == "dot":
            return [ctx.dot(fig / 2, cap / 2 - dv / 2)]
        th = math.atan(1.6)
        c, s = math.cos(th), math.sin(th)
        re = 1 / math.sqrt((c / (fig / 2)) ** 2 + (s / (cap / 2)) ** 2)
        ln = max(12.0, re - w - gap)
        return [pen().m(fig / 2 - ln * c, cap / 2 - ln * s).l(fig / 2 + ln * c, cap / 2 + ln * s)]

    d("0", fig, "o", "o", [ctx.ring(fig / 2, cap / 2, fig / 2, cap / 2 + o)], zero_detail())
    if p.one_flag:
        d(
            "1",
            fig,
            "o",
            "o",
            [
                pen()
                .m(fig * 0.05, cap * 0.68)
                .c(fig * 0.3, cap * 0.76, fig * 0.5, cap * 0.86, fig * 0.6, cap)
                .l(fig * 0.6, 0)
            ],
        )
    else:
        d("1", fig, "o", "o", [pen().m(fig * 0.2, cap * 0.82).l(fig * 0.6, cap).l(fig * 0.6, 0)])
    end2 = two_end(fig / 2, cap - fig / 2, fig / 2, fig / 2 + o)
    d(
        "2",
        fig,
        "o",
        "o",
        [pen().a(fig / 2, cap - fig / 2, fig / 2, fig / 2 + o, 155, end2).l(0, 0).l(fig, 0)],
    )
    d(
        "3",
        fig,
        "o",
        "o",
        [
            pen()
            .a(fig / 2, cap * 0.76, fig * 0.45, cap * 0.24, 150, -90)
            .a(fig / 2, cap * 0.26, fig / 2, cap * 0.26, 90, -150)
        ],
    )
    d(
        "4",
        fig,
        "o",
        "o",
        [pen().m(fig * 0.72, 0).l(fig * 0.72, cap).l(0, cap * 0.3).l(fig * 0.72, cap * 0.3)],
    )
    d(
        "5",
        fig,
        "o",
        "o",
        [
            pen()
            .m(fig * 0.9, cap)
            .l(fig * 0.12, cap)
            .a(fig / 2, cap * 0.31, fig / 2, cap * 0.31 + o, 140, -145)
        ],
    )
    d(
        "6",
        fig,
        "o",
        "o",
        [
            pen()
            .m(fig * 0.8, cap)
            .c(fig * 0.38, cap * 0.98, 0, cap * 0.78, 0, cap * 0.31)
            .a(fig / 2, cap * 0.31, fig / 2, cap * 0.31 + o, 180, 540)
        ],
    )
    d("7", fig, "o", "o", [pen().m(0, cap).l(fig, cap).l(fig * 0.3, 0)])
    d(
        "8",
        fig,
        "o",
        "o",
        [
            ctx.ring(fig / 2, cap * 0.76, fig * 0.42, cap * 0.24),
            ctx.ring(fig / 2, cap * 0.26, fig / 2, cap * 0.26 + o),
        ],
    )
    if p.nine_straight:
        d(
            "9",
            fig,
            "o",
            "o",
            [
                ctx.ring(fig / 2, cap * 0.69, fig / 2, cap * 0.31 + o),
                pen().m(fig, cap * 0.69).l(fig, 0),
            ],
        )
    else:
        d(
            "9",
            fig,
            "o",
            "o",
            [pen().a(fig / 2, cap * 0.69, fig / 2, cap * 0.31 + o, -20, 340).l(fig * 0.22, 0)],
        )

    d(".", 0, "v", "v", [], [ctx.dot(0, 0)])
    d(",", 0, "v", "v", [], [pen().m(0, dot_len).l(-dot_len * 0.3, -dot_len * 0.8)])
    d(":", 0, "v", "v", [], [ctx.dot(0, 0), ctx.dot(0, xh - dv)])
    d(
        ";",
        0,
        "v",
        "v",
        [],
        [pen().m(0, dot_len).l(-dot_len * 0.3, -dot_len * 0.8), ctx.dot(0, xh - dv)],
    )
    d("-", xh * 0.4, "v", "v", [pen().m(0, xh * 0.48).l(xh * 0.4, xh * 0.48)])
    d(EN_DASH, xh * 0.8, "v", "v", [pen().m(0, xh * 0.48).l(xh * 0.8, xh * 0.48)])
    qw, qs = cap * 0.5, dv + w + gap

    def inv(x: float, y: float) -> tuple[float, float]:
        return qw - x, xh - y

    d(
        "?",
        qw,
        "o",
        "o",
        [pen().a(qw / 2, cap - qw / 2, qw / 2, qw / 2 + o, 160, -90).l(qw / 2, qs)],
        [ctx.dot(qw / 2, 0)],
    )
    d(
        "¿",
        qw,
        "o",
        "o",
        [pen(inv).a(qw / 2, cap - qw / 2, qw / 2, qw / 2 + o, 160, -90).l(qw / 2, qs)],
        [ctx.dot(qw / 2, xh - dv)],
    )
    d("!", 0, "o", "o", [pen().m(0, cap).l(0, qs)], [ctx.dot(0, 0)])
    d("¡", 0, "o", "o", [pen().m(0, xh - qs).l(0, xh - cap)], [ctx.dot(0, xh - dv)])
    dr = xh * 0.13
    d("°", dr * 2, "v", "v", [ctx.ring(dr, cap - dr, dr, dr)])
    d(PRIME, xh * 0.12, "v", "v", [pen().m(xh * 0.12, cap).l(0, cap - xh * 0.3)])
    d(
        DOUBLE_PRIME,
        xh * 0.32,
        "v",
        "v",
        [
            pen().m(xh * 0.12, cap).l(0, cap - xh * 0.3),
            pen().m(xh * 0.32, cap).l(xh * 0.2, cap - xh * 0.3),
        ],
    )
    d("'", 0, "v", "v", [pen().m(0, cap).l(0, cap - xh * 0.28)])
    d(
        '"',
        xh * 0.2,
        "v",
        "v",
        [
            pen().m(0, cap).l(0, cap - xh * 0.28),
            pen().m(xh * 0.2, cap).l(xh * 0.2, cap - xh * 0.28),
        ],
    )
    pw, pm, ph = xh * 0.24, (asc + desc) / 2, (asc - desc) / 2
    d("(", pw, "v", "v", [pen().a(pw * 2.4, pm, pw * 2.4, ph, 130, 230)])
    d(")", pw, "v", "v", [pen().a(-pw * 1.4, pm, pw * 2.4, ph, 50, -50)])
    d("/", xh * 0.5, "v", "v", [pen().m(0, desc * 0.5).l(xh * 0.5, asc)])


def add_accents(ctx: Context) -> None:
    g = ctx.glyphs

    def compose(ch: str, base: str, extra: list[Stroke]) -> None:
        b = g[base]
        ctx.define(ch, b.width, b.left, b.right, b.strokes, [*b.details, *extra], b.ax)

    for ch, base in (("á", "a"), ("é", "e"), ("ó", "o"), ("ú", "u")):
        compose(ch, base, [ctx.acute(g[base].ax, ctx.yt)])
    compose("í", DOTLESS_I, [ctx.acute(0, ctx.yt)])
    compose("ñ", "n", [ctx.tilde(g["n"].ax, ctx.yt)])
    compose("ü", "u", ctx.dieresis(g["u"].ax, ctx.yt))
    for ch, base in (("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U")):
        compose(ch, base, [ctx.acute(g[base].ax, ctx.yc)])
    compose("Ñ", "N", [ctx.tilde(g["N"].ax, ctx.yc)])
    compose("Ü", "U", ctx.dieresis(g["U"].ax, ctx.yc))
