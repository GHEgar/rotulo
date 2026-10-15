import math

from rotulo.chars import DOTLESS_I
from rotulo.context import Context
from rotulo.skeleton import DEG, Stroke, Transform


def s_curve(ctx: Context, sw: float, ht: float, transform: Transform | None = None) -> Stroke:
    return (
        ctx.pen(transform)
        .a(sw / 2, ht * 0.77, sw * 0.44, ht * 0.23, 25, 270)
        .a(sw / 2, ht * 0.27, sw / 2, ht * 0.27, 90, -155)
    )


def add_lowercase(ctx: Context) -> None:
    p, pen, d = ctx.p, ctx.pen, ctx.define
    xh, asc, desc, bowl, nw, h2, ry, o = (
        ctx.xh,
        ctx.asc,
        ctx.desc,
        ctx.bowl,
        ctx.nw,
        ctx.h2,
        ctx.ry,
        ctx.o,
    )
    hr, hs, hx, lr, sh = ctx.hr, ctx.hs, ctx.hx, ctx.lr, ctx.sharp

    d("o", bowl, "o", "o", [ctx.ring(bowl / 2, xh / 2, bowl / 2, ry)])
    d(
        "b",
        bowl,
        "h",
        "o",
        [pen().m(0, asc).l(0, xh / 2).a(bowl / 2, xh / 2, bowl / 2, ry, 180, 540)],
    )
    fb = xh * 0.45
    fy = asc - fb * math.sin(40 * DEG)
    d(
        "d",
        bowl + fb * (1 + math.cos(140 * DEG)),
        "o",
        "v",
        [
            pen()
            .a(bowl + fb, fy, fb, fb, 140, 180)
            .l(bowl, xh / 2)
            .a(bowl / 2, xh / 2, bowl / 2, ry, 0, -360)
        ],
        ax=bowl / 2,
    )
    d(
        "p",
        bowl,
        "h",
        "o",
        [pen().m(0, desc).l(0, xh / 2).a(bowl / 2, xh / 2, bowl / 2, ry, 180, -180)],
    )
    if p.q_bar:
        d(
            "q",
            bowl + xh * 0.2,
            "o",
            "v",
            [
                pen().m(bowl, desc).l(bowl, xh / 2).a(bowl / 2, xh / 2, bowl / 2, ry, 0, 360),
                pen().m(bowl - xh * 0.2, desc * 0.5).l(bowl + xh * 0.2, desc * 0.5),
            ],
            ax=bowl / 2,
        )
    else:
        d(
            "q",
            bowl,
            "o",
            "h",
            [pen().m(bowl, desc).l(bowl, xh / 2).a(bowl / 2, xh / 2, bowl / 2, ry, 0, 360)],
        )
    ap = p.aperture
    d(
        "c",
        bowl / 2 * (1 + math.cos(ap * DEG)),
        "o",
        "v",
        [pen().a(bowl / 2, xh / 2, bowl / 2, ry, ap, 360 - ap)],
        ax=bowl / 2,
    )
    ef = max(min(p.corner, xh * 0.2), 1)
    ef_ = ctx.bar_fillet(bowl / 2, xh / 2, bowl / 2, ry, xh / 2, ef, 1)
    right = ef_.c[0] + ef
    d(
        "e",
        bowl,
        "o",
        "o",
        [
            pen()
            .m(0, xh / 2)
            .l(ef_.c[0], xh / 2)
            .a(ef_.c[0], ef_.c[1], ef, ef, -90, ef_.phi)
            .a(bowl / 2, xh / 2, bowl / 2, ry, ef_.th, 270)
            .c(
                bowl / 2 + (right - bowl / 2) * 0.55,
                xh / 2 - ry,
                right - (right - bowl / 2) * 0.2,
                xh / 2 - ry + xh * p.lift * 0.35,
                right,
                xh / 2 - ry + xh * p.lift,
            )
        ],
    )
    if p.a_form == "tail":
        d(
            "a",
            bowl + lr,
            "o",
            "o",
            [
                pen()
                .a(bowl / 2, xh / 2, bowl / 2, ry, 360, 0)
                .l(bowl, lr)
                .a(bowl + lr, lr, lr, lr, 180, 270)
            ],
            ax=bowl / 2,
        )
    elif p.a_form == "single":
        d(
            "a",
            bowl,
            "o",
            "h",
            [pen().m(bowl, 0).l(bowl, xh / 2).a(bowl / 2, xh / 2, bowl / 2, ry, 0, 360)],
        )
    else:
        ht, by = xh * 0.3, xh * 0.27
        d(
            "a",
            bowl,
            "o",
            "h",
            [
                pen().a(bowl / 2, xh - ht, bowl / 2, ht + o, 160, 0).l(bowl, 0),
                pen()
                .m(bowl, 2 * by)
                .l(bowl / 2, 2 * by)
                .a(bowl / 2, by, bowl / 2, by, 90, 270)
                .l(bowl, 0),
            ],
        )

    def arch(x0: float, wd: float) -> Stroke:
        return (
            pen()
            .m(x0, xh - wd / 2)
            .a(x0 + wd / 2, xh - wd / 2, wd / 2, wd / 2 + o, 180, 0)
            .l(x0 + wd, 0)
        )

    def arch_full(wd: float) -> Stroke:
        return (
            pen()
            .m(0, 0)
            .l(0, xh - wd / 2)
            .a(wd / 2, xh - wd / 2, wd / 2, wd / 2 + o, 180, 0)
            .l(wd, 0)
        )

    d("n", nw, "h", "h", [arch_full(nw)])
    d("h", nw, "h", "h", [pen().m(0, asc).l(0, 0), arch(0, nw)])
    md, mh = 28 * DEG, h2 * 0.55
    m1 = (h2 + h2 * math.cos(md), xh - h2 + (h2 + o) * math.sin(md))
    m2 = (nw + h2 - h2 * math.cos(md), m1[1])
    mv = m1[1] - 0.75 * mh * math.cos(md)
    d(
        "m",
        nw * 2,
        "h",
        "h",
        [
            pen()
            .m(0, 0)
            .l(0, xh - h2)
            .a(h2, xh - h2, h2, h2 + o, 180, 28)
            .c(
                m1[0] + math.sin(md) * mh,
                m1[1] - math.cos(md) * mh,
                m2[0] - math.sin(md) * mh,
                m2[1] - math.cos(md) * mh,
                m2[0],
                m2[1],
            )
            .a(nw + h2, xh - h2, h2, h2 + o, 152, 0)
            .l(2 * nw, 0),
            pen().m(nw, 0).l(nw, mv),
        ],
    )
    d("u", nw, "h", "h", [pen().m(0, xh).l(0, h2).a(h2, h2, h2, h2 + o, 180, 360).l(nw, xh)])
    ra = 65
    d(
        "r",
        h2 + h2 * math.cos(ra * DEG),
        "h",
        "v",
        [pen().m(0, 0).l(0, xh - h2).a(h2, xh - h2, h2, h2 + o, 180, ra)],
        ax=0,
    )
    d(DOTLESS_I, 0, "h", "h", [pen().m(0, xh).l(0, 0)])
    d("i", 0, "h", "h", [pen().m(0, xh).l(0, 0)], [ctx.dot(0, ctx.yt)])
    hxj = hr * p.tail_j
    jx = hxj * 1.1
    d("j", jx, "v", "h", [ctx.soft_tail(jx, xh, hxj, hs)], [ctx.dot(jx, ctx.yt)], ax=jx)
    if p.l_form == "tail":
        d("l", lr, "h", "o", [pen().m(0, asc).l(0, lr).a(lr, lr, lr, lr, 180, 270)], ax=0)
    else:
        d("l", 0, "h", "h", [pen().m(0, asc).l(0, 0)])
    tx = xh * 0.2
    tyb = min(ctx.cap * p.bar, xh)
    d("t", tx * 2, "o", "o", [pen().m(tx, asc).l(tx, 0), pen().m(0, tyb).l(tx * 2, tyb)])
    d(
        "f",
        max(tx * 2, tx + hx * (1 + math.cos((180 - hs) * DEG))),
        "o",
        "o",
        [
            pen().m(tx, 0).l(tx, asc - hr).a(tx + hx, asc - hr, hx, hr, 180, 180 - hs),
            pen().m(0, tyb).l(tx * 2, tyb),
        ],
    )
    k = nw * 0.85
    d("k", k, "h", "v", [pen().m(0, asc).l(0, 0), pen().m(k, xh).l(0, xh * 0.45).l(k, 0)])
    v = bowl * 0.95
    d("v", v, "v", "v", [pen(sharp=sh).m(0, xh).l(v / 2, 0).l(v, xh)])
    d(
        "w",
        v * 2,
        "v",
        "v",
        [pen(sharp=sh).m(0, xh).l(v / 2, 0).l(v, xh).l(v * 1.5, 0).l(v * 2, xh)],
    )
    xl = bowl * 0.9
    xs = (ctx.w + xh * 0.06) / 2
    d(
        "x",
        xl,
        "v",
        "v",
        [
            pen(sharp=sh).m(0, xh).l(xl / 2 - xs, xh / 2).l(0, 0),
            pen(sharp=sh).m(xl, xh).l(xl / 2 + xs, xh / 2).l(xl, 0),
        ],
    )
    d(
        "y",
        v,
        "v",
        "v",
        [
            pen(sharp=sh).m(0, xh).l(v / 2, 0),
            pen().m(v, xh).l(v - v / 2 * (xh - desc) / xh, desc),
        ],
    )
    z = bowl * 0.85
    d("z", z, "o", "o", [pen(sharp=sh).m(0, xh).l(z, xh).l(0, 0).l(z, 0)])
    d("s", bowl * 0.82, "o", "o", [s_curve(ctx, bowl * 0.82, xh)])
    d(
        "g",
        bowl,
        "o",
        "h",
        [
            ctx.soft_tail(
                bowl,
                xh / 2,
                bowl / (1 - 0.8 * math.cos(hs * DEG)),
                hs,
                pen().a(bowl / 2, xh / 2, bowl / 2, ry, 360, 0),
            )
        ],
    )
