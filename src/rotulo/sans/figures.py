import math

from rotulo.sans.kit import Kit
from rotulo.skeleton import DEG


def add_figures(k: Kit) -> None:
    h, c, ov, w, gap = k.h, k.cap, k.ov, k.w, k.ctx.gap
    fw = c * 0.6 * k.cw - w
    lo, hi = h - ov, c - h + ov
    cx = fw / 2
    th = 72 * DEG
    inner = min(fw / 2, c / 2) - w - gap * 0.4
    sl = max(12.0, inner / math.cos(th) * 0.5)
    sl = min(sl, c / 2 - w - gap * 0.4 - h)
    zero = (
        k.pen()
        .m(cx - sl * math.cos(th), c / 2 - sl * math.sin(th))
        .l(cx + sl * math.cos(th), c / 2 + sl * math.sin(th))
    )

    k.put("0", lambda: ([k.loop(0, lo, fw, hi)], [zero]), width=fw)
    k.put(
        "1",
        lambda: ([k.pen().m(fw * 0.2, c * 0.8).l(fw * 0.62, c - h).l(fw * 0.62, h)], []),
        width=fw,
    )
    r2 = fw / 2
    k.put(
        "2",
        lambda: (
            [k.pen().a(cx, c - h - r2, r2, r2 + ov * 0.5, 160, -35).l(0, h).l(fw, h)],
            [],
        ),
        width=fw,
    )
    ym = c * 0.54
    ru, rl = (c - h - ym) / 2, (ym - h) / 2
    k.put(
        "3",
        lambda: (
            [
                k.pen()
                .a(cx, ym + ru, fw * 0.45, ru + ov * 0.5, 150, -90)
                .a(cx, h + rl, fw / 2, rl + ov * 0.5, 90, -150)
            ],
            [],
        ),
        width=fw,
    )
    k.put(
        "4",
        lambda: (
            [
                k.pen().m(fw * 0.72, c - h).l(0, c * 0.3).l(fw, c * 0.3),
                k.stem(fw * 0.72, 0, c),
            ],
            [],
        ),
        width=fw,
    )
    r5 = (c * 0.6 - h) / 2
    k.put(
        "5",
        lambda: (
            [
                k.pen()
                .m(fw * 0.9, c - h)
                .l(fw * 0.1, c - h)
                .l(fw * 0.04, c * 0.56)
                .a(cx, h + r5, fw / 2, r5 + ov * 0.5, 140, -150)
            ],
            [],
        ),
        width=fw,
    )
    top = c * 0.62
    k.put(
        "6",
        lambda: (
            [
                k.loop(0, lo, fw, top),
                k.pen()
                .m(0, top / 2)
                .l(0, c - h - r2)
                .a(cx, c - h - r2, r2, r2 + ov * 0.5, 180, 40),
            ],
            [],
        ),
        width=fw,
    )
    k.put("7", lambda: ([k.pen().m(0, c - h).l(fw, c - h).l(fw * 0.32, h)], []), width=fw)
    k.put(
        "8",
        lambda: ([k.loop(fw * 0.05, ym, fw * 0.95, hi, False), k.loop(0, lo, fw, ym, False)], []),
        width=fw,
    )
    bottom = c - top
    k.put(
        "9",
        lambda: (
            [
                k.loop(0, bottom, fw, hi),
                k.pen()
                .m(fw, (bottom + c) / 2)
                .l(fw, h + r2)
                .a(cx, h + r2, r2, r2 + ov * 0.5, 0, -140),
            ],
            [],
        ),
        width=fw,
    )
