import math

from rotulo.chars import (
    ELLIPSIS,
    EM_DASH,
    LEFT_DOUBLE,
    LEFT_GUILLEMET,
    LEFT_SINGLE,
    MIDDLE_DOT,
    RIGHT_DOUBLE,
    RIGHT_GUILLEMET,
    RIGHT_SINGLE,
)
from rotulo.context import Context
from rotulo.lowercase import s_curve
from rotulo.skeleton import DEG, Stroke


def add_symbols(ctx: Context) -> None:
    p, pen, d, sh = ctx.p, ctx.pen, ctx.define, ctx.sharp
    cap, xh, asc, desc, o, dot_len, dv = (
        ctx.cap,
        ctx.xh,
        ctx.asc,
        ctx.desc,
        ctx.o,
        ctx.dot_len,
        ctx.dv,
    )

    amp = cap * 0.62
    d(
        "&",
        amp,
        "o",
        "v",
        [
            pen()
            .m(amp, 0)
            .l(amp * 0.25, cap * 0.64)
            .a(amp * 0.42, cap * 0.78, amp * 0.22, cap * 0.22, 220, -50)
            .l(amp * 0.14, cap * 0.48)
            .a(amp * 0.36, cap * 0.27, amp * 0.34, cap * 0.27, 130, 375)
            .l(amp * 0.92, cap * 0.42)
        ],
    )
    atw, atc = cap * 0.9, cap * 0.32
    atr = atw * 0.2
    atrh = atr * 0.5
    d(
        "@",
        atw,
        "o",
        "o",
        [
            ctx.ring(atw / 2, atc, atr, atr),
            pen()
            .m(atw / 2 + atr, atc + atr)
            .l(atw / 2 + atr, atc - atr * 0.5)
            .a(atw / 2 + atr + atrh, atc - atr * 0.5, atrh, atrh, 180, 270)
            .a(atw / 2, atc, atw / 2, cap * 0.5, -20, 300),
        ],
    )
    hw = cap * 0.62
    d(
        "#",
        hw,
        "v",
        "v",
        [
            pen().m(hw * 0.3, 0).l(hw * 0.3, cap),
            pen().m(hw * 0.7, 0).l(hw * 0.7, cap),
            pen().m(0, cap * 0.33).l(hw, cap * 0.33),
            pen().m(0, cap * 0.67).l(hw, cap * 0.67),
        ],
    )
    pcw = cap * 0.7
    d(
        "%",
        pcw,
        "o",
        "o",
        [
            ctx.ring(pcw * 0.2, cap * 0.8, pcw * 0.2, cap * 0.2),
            ctx.ring(pcw * 0.8, cap * 0.2, pcw * 0.2, cap * 0.2),
            pen(sharp=sh).m(pcw * 0.9, cap).l(pcw * 0.1, 0),
        ],
    )
    euw, ap = cap * 0.72, p.aperture
    d(
        "€",
        euw,
        "o",
        "v",
        [
            pen().a(euw * 0.55, cap / 2, euw * 0.45, cap / 2 + o, ap, 360 - ap),
            pen().m(0, cap * 0.58).l(euw * 0.6, cap * 0.58),
            pen().m(0, cap * 0.42).l(euw * 0.6, cap * 0.42),
        ],
    )
    dlw = cap * 0.62
    d(
        "$",
        dlw,
        "o",
        "o",
        [s_curve(ctx, dlw, cap), pen().m(dlw / 2, cap * 1.1).l(dlw / 2, -cap * 0.1)],
    )
    mw, mcy = xh * 0.8, xh * 0.5
    d(
        "+",
        mw,
        "o",
        "o",
        [pen().m(0, mcy).l(mw, mcy), pen().m(mw / 2, mcy - mw / 2).l(mw / 2, mcy + mw / 2)],
    )
    d(
        "=",
        mw,
        "o",
        "o",
        [
            pen().m(0, mcy + xh * 0.12).l(mw, mcy + xh * 0.12),
            pen().m(0, mcy - xh * 0.12).l(mw, mcy - xh * 0.12),
        ],
    )
    asr = xh * 0.2
    asy = cap - asr

    def spoke(a: float) -> Stroke:
        t = (a + 90) * DEG
        return (
            pen()
            .m(asr + asr * math.cos(t), asy + asr * math.sin(t))
            .l(asr - asr * math.cos(t), asy - asr * math.sin(t))
        )

    d("*", asr * 2, "o", "o", [spoke(0), spoke(60), spoke(120)])
    d("_", xh * 0.7, "v", "v", [pen().m(0, desc * 0.45).l(xh * 0.7, desc * 0.45)])
    bw = xh * 0.22
    d("[", bw, "h", "v", [pen().m(bw, asc).l(0, asc).l(0, desc).l(bw, desc)])
    d("]", bw, "v", "h", [pen().m(0, asc).l(bw, asc).l(bw, desc).l(0, desc)])
    cbw, cpm, cph = xh * 0.3, (asc + desc) / 2, (asc - desc) / 2

    def brace(inner: float, outer: float, tip: float) -> Stroke:
        return (
            pen()
            .m(outer, asc)
            .l(inner, asc)
            .l(inner, cpm + cph * 0.12)
            .l(tip, cpm)
            .l(inner, cpm - cph * 0.12)
            .l(inner, desc)
            .l(outer, desc)
        )

    d("{", cbw, "v", "v", [brace(cbw * 0.4, cbw, 0)])
    d("}", cbw, "v", "v", [brace(cbw * 0.6, 0, cbw)])
    ltw, lth = xh * 0.6, xh * 0.3
    d("<", ltw, "v", "v", [pen(sharp=sh).m(ltw, mcy + lth).l(0, mcy).l(ltw, mcy - lth)])
    d(">", ltw, "v", "v", [pen(sharp=sh).m(0, mcy + lth).l(ltw, mcy).l(0, mcy - lth)])
    d("|", 0, "h", "h", [pen().m(0, asc).l(0, desc)])
    tlw, tla = xh * 0.6, xh * 0.09
    d(
        "~",
        tlw,
        "o",
        "o",
        [pen().a(tlw / 4, mcy, tlw / 4, tla, 180, 0).a(tlw * 3 / 4, mcy, tlw / 4, tla, 180, 360)],
    )

    def quote_open(x: float) -> Stroke:
        return pen().m(x, cap).l(x + dot_len * 0.3, cap - dot_len * 1.8)

    def quote_close(x: float) -> Stroke:
        return pen().m(x + dot_len * 0.3, cap).l(x, cap - dot_len * 1.8)

    qw, qg = dot_len * 0.3, xh * 0.16
    d(LEFT_SINGLE, qw, "v", "v", [], [quote_open(0)])
    d(RIGHT_SINGLE, qw, "v", "v", [], [quote_close(0)])
    d(LEFT_DOUBLE, qw + qg, "v", "v", [], [quote_open(0), quote_open(qg)])
    d(RIGHT_DOUBLE, qw + qg, "v", "v", [], [quote_close(0), quote_close(qg)])
    gw, gh, gs = xh * 0.25, xh * 0.2, xh * 0.2

    def chevron(x: float, left: bool) -> Stroke:
        s = pen(sharp=sh)
        if left:
            return s.m(x + gw, mcy + gh).l(x, mcy).l(x + gw, mcy - gh)
        return s.m(x, mcy + gh).l(x + gw, mcy).l(x, mcy - gh)

    d(LEFT_GUILLEMET, gw + gs, "v", "v", [chevron(0, True), chevron(gs, True)])
    d(RIGHT_GUILLEMET, gw + gs, "v", "v", [chevron(0, False), chevron(gs, False)])
    d(
        ELLIPSIS,
        xh * 0.5,
        "v",
        "v",
        [],
        [ctx.dot(0, 0), ctx.dot(xh * 0.25, 0), ctx.dot(xh * 0.5, 0)],
    )
    d(MIDDLE_DOT, 0, "v", "v", [], [ctx.dot(0, xh / 2 - dv / 2)])
    d(EM_DASH, xh * 1.6, "v", "v", [pen().m(0, xh * 0.48).l(xh * 1.6, xh * 0.48)])
