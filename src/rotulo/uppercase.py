import math

from rotulo.context import Context
from rotulo.lowercase import s_curve
from rotulo.skeleton import DEG


def add_uppercase(ctx: Context) -> None:
    p, pen, d = ctx.p, ctx.pen, ctx.define
    cap, o, hr, hs, sh = ctx.cap, ctx.o, ctx.hr, ctx.hs, ctx.sharp
    ap = p.aperture

    aw = cap * 0.86
    d(
        "A",
        aw,
        "v",
        "v",
        [
            pen().m(0, 0).l(aw / 2, cap).l(aw, 0),
            pen().m(aw * 0.15, cap * 0.3).l(aw * 0.85, cap * 0.3),
        ],
    )
    xb1, xb2 = cap * 0.3, cap * 0.32
    d(
        "B",
        xb2 + cap * 0.27,
        "h",
        "o",
        [
            pen()
            .m(0, cap / 2)
            .l(0, cap)
            .l(xb1, cap)
            .a(xb1, cap * 0.75, cap * 0.24, cap / 4, 90, -90)
            .l(0, cap / 2),
            pen()
            .m(0, cap / 2)
            .l(0, 0)
            .l(xb2, 0)
            .a(xb2, cap / 4, cap * 0.27, cap / 4, -90, 90)
            .l(0, cap / 2),
        ],
    )
    cw = cap * 0.9
    d(
        "C",
        cw / 2 * (1 + math.cos(ap * DEG)),
        "o",
        "v",
        [pen().a(cw / 2, cap / 2, cw / 2, cap / 2 + o, ap, 360 - ap)],
        ax=cw / 2,
    )
    dw = cap * 0.82
    drx = dw * 0.6
    d(
        "D",
        dw,
        "h",
        "o",
        [
            pen()
            .m(0, cap / 2)
            .l(0, cap)
            .l(dw - drx, cap)
            .a(dw - drx, cap / 2, drx, cap / 2, 90, -90)
            .l(0, 0)
            .l(0, cap / 2)
        ],
    )
    ew = cap * 0.6
    d(
        "E",
        ew,
        "h",
        "v",
        [pen().m(ew, cap).l(0, cap).l(0, 0).l(ew, 0), pen().m(0, cap / 2).l(ew * 0.7, cap / 2)],
    )
    d(
        "F",
        ew,
        "h",
        "v",
        [pen().m(ew, cap).l(0, cap).l(0, 0), pen().m(0, cap / 2).l(ew * 0.7, cap / 2)],
    )
    gw = cap * 0.92
    lo, hi = 10.0, (cap / 2 + o) * 0.49
    for _ in range(40):
        r = (lo + hi) / 2
        if ctx.bar_fillet(gw / 2, cap / 2, gw / 2, cap / 2 + o, cap / 2, r, -1).c[0] > gw * 0.6:
            lo = r
        else:
            hi = r
    gr = (lo + hi) / 2
    gf = ctx.bar_fillet(gw / 2, cap / 2, gw / 2, cap / 2 + o, cap / 2, gr, -1)
    gx = gf.c[0] + gr
    top = cap + o
    d(
        "G",
        gx,
        "o",
        "o",
        [
            pen()
            .m(gx, top - cap * p.lift_g)
            .c(
                gx - (gx - gw / 2) * 0.2,
                top - cap * p.lift_g * 0.35,
                gw / 2 + (gx - gw / 2) * 0.55,
                top,
                gw / 2,
                top,
            )
            .a(gw / 2, cap / 2, gw / 2, cap / 2 + o, 90, 360 + gf.th)
            .a(gf.c[0], gf.c[1], gr, gr, gf.phi, 90)
        ],
        ax=gw / 2,
    )
    hw = cap * 0.72
    d(
        "H",
        hw,
        "h",
        "h",
        [pen().m(0, cap).l(0, 0), pen().m(hw, cap).l(hw, 0), pen().m(0, cap / 2).l(hw, cap / 2)],
    )
    d("I", 0, "h", "h", [pen().m(0, cap).l(0, 0)])
    jw = max(cap * 0.45, hr * p.tail_j * 1.75)
    d("J", jw, "v", "h", [ctx.soft_tail(jw, cap, hr * p.tail_j, hs, bottom=0)])
    kw = cap * 0.68
    d("K", kw, "h", "v", [pen().m(0, cap).l(0, 0), pen().m(kw, cap).l(0, cap * 0.47).l(kw, 0)])
    d("L", cap * 0.56, "h", "v", [pen().m(0, cap).l(0, 0).l(cap * 0.56, 0)])
    vw = cap * 0.84
    d("M", vw, "h", "h", [pen(sharp=sh).m(0, 0).l(0, cap).l(vw / 2, 0).l(vw, cap).l(vw, 0)])
    nw = cap * 0.74
    d("N", nw, "h", "h", [pen(sharp=sh).m(0, 0).l(0, cap).l(nw, 0).l(nw, cap)])
    d("O", cap, "o", "o", [ctx.ring(cap / 2, cap / 2, cap / 2, cap / 2 + o)])
    qa = -48 * DEG
    d(
        "Q",
        cap,
        "o",
        "o",
        [
            ctx.ring(cap / 2, cap / 2, cap / 2, cap / 2 + o),
            pen()
            .m(cap / 2 * (1 + math.cos(qa)), cap / 2 + (cap / 2 + o) * math.sin(qa))
            .l(cap * 1.04, -cap * 0.07),
        ],
    )
    xp, pr = cap * 0.3, cap * 0.27
    d(
        "P",
        xp + pr,
        "h",
        "o",
        [pen().m(0, 0).l(0, cap).l(xp, cap).a(xp, cap - pr, pr, pr, 90, -90).l(0, cap - 2 * pr)],
    )
    d(
        "R",
        xp + pr,
        "h",
        "v",
        [
            pen().m(0, 0).l(0, cap).l(xp, cap).a(xp, cap - pr, pr, pr, 90, -90).l(0, cap - 2 * pr),
            pen().m(xp * 0.6, cap - 2 * pr).l(xp, cap - 2 * pr).a(xp, 0, pr, cap - 2 * pr, 90, 0),
        ],
    )
    d("S", cap * 0.62, "o", "o", [s_curve(ctx, cap * 0.62, cap)])
    tw = cap * 0.66
    d("T", tw, "v", "v", [pen().m(0, cap).l(tw, cap), pen().m(tw / 2, cap).l(tw / 2, 0)])
    uw = cap * 0.74
    d(
        "U",
        uw,
        "h",
        "h",
        [pen().m(0, cap).l(0, uw / 2).a(uw / 2, uw / 2, uw / 2, uw / 2 + o, 180, 360).l(uw, cap)],
    )
    d("V", vw, "v", "v", [pen(sharp=sh).m(0, cap).l(vw / 2, 0).l(vw, cap)])
    d(
        "W",
        vw * 2,
        "v",
        "v",
        [pen(sharp=sh).m(0, cap).l(vw / 2, 0).l(vw, cap).l(vw * 1.5, 0).l(vw * 2, cap)],
    )
    xw = cap * 0.78
    xs = (ctx.w + ctx.xh * 0.06) / 2
    d(
        "X",
        xw,
        "v",
        "v",
        [
            pen().m(0, cap).l(xw / 2 - xs, cap / 2).l(0, 0),
            pen().m(xw, cap).l(xw / 2 + xs, cap / 2).l(xw, 0),
        ],
    )
    yw = cap * 0.8
    d(
        "Y",
        yw,
        "v",
        "v",
        [
            pen().m(0, cap).l(yw / 2, cap * 0.45).l(yw, cap),
            pen().m(yw / 2, cap * 0.45).l(yw / 2, 0),
        ],
    )
    zw = cap * 0.66
    d("Z", zw, "o", "o", [pen().m(0, cap).l(zw, cap).l(0, 0).l(zw, 0)])
