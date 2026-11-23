import math

from rotulo.chars import DOTLESS_I
from rotulo.sans.kit import Kit, Shape
from rotulo.skeleton import DEG, Stroke


def add_lowercase(k: Kit) -> None:
    s, h, x, asc, desc, ov, bw = k.s, k.h, k.x, k.asc, k.desc, k.ov, k.bw
    lo, hi = h - ov, x - h + ov
    nw = bw * 0.92

    def bowl() -> Stroke:
        return k.loop(0, lo, bw, hi)

    def arch(x0: float, wd: float) -> Stroke:
        r = wd / 2
        return (
            k.pen()
            .m(x0, x * 0.45)
            .a(x0 + r, x - h - r * 0.95, r, r * 0.95 + ov * 0.5, 180, 0)
            .l(x0 + wd, h)
        )

    k.put("o", lambda: ([bowl()], []))
    k.put("c", lambda: ([k.rarc(k.pen(), 0, lo, bw * 0.95, hi, k.ap, 360 - k.ap)], []))
    k.put(
        "e",
        lambda: (
            [
                k.pen().m(0, x / 2).l(bw, x / 2),
                k.rarc(k.pen().m(bw, x / 2), 0, lo, bw, hi, 0, 360 - s.aperture_e),
            ],
            [],
        ),
    )
    k.put("b", lambda: ([bowl(), k.stem(0, 0, asc)], []))
    k.put("p", lambda: ([bowl(), k.stem(0, desc, x)], []))
    k.put("q", lambda: ([bowl(), k.stem(bw, desc, x)], []))
    fb = x * 0.45
    fy = asc - h - fb * math.sin(40 * DEG)
    if s.d_form == "flick":
        k.put("d", lambda: ([bowl(), k.pen().a(bw + fb, fy, fb, fb, 140, 180).l(bw, h)], []))
    else:
        k.put("d", lambda: ([bowl(), k.stem(bw, 0, asc)], []))
    rr = bw * 0.42
    k.put(
        "g",
        lambda: (
            [
                bowl(),
                k.pen()
                .m(bw, x - h)
                .l(bw, desc + h + rr)
                .a(bw - rr, desc + h + rr, rr, rr, 0, -150),
            ],
            [],
        ),
    )
    k.put("n", lambda: ([k.stem(0, 0, x), arch(0, nw)], []))
    k.put("h", lambda: ([k.stem(0, 0, asc), arch(0, nw)], []))
    mw = nw * 0.82
    k.put("m", lambda: ([k.stem(0, 0, x), arch(0, mw), arch(mw, mw)], []))
    ur = nw / 2
    k.put(
        "u",
        lambda: (
            [
                k.stem(nw, 0, x),
                k.pen()
                .m(nw, x * 0.55)
                .a(ur, h + ur * 0.95, ur, ur * 0.95 + ov * 0.5, 0, -180)
                .l(0, x - h),
            ],
            [],
        ),
    )
    k.put("i", lambda: ([k.stem(0, 0, x)], [k.dot(0)]))
    k.put(DOTLESS_I, lambda: ([k.stem(0, 0, x)], []))
    k.put("l", lambda: ([k.stem(0, 0, asc)], []))
    rw = nw * 0.62
    k.put(
        "r",
        lambda: (
            [k.stem(0, 0, x), k.pen().m(0, x * 0.45).a(rw, x - h - rw, rw, rw + ov * 0.5, 180, 95)],
            [],
        ),
    )
    _add_bars(k, nw)
    _add_diagonals(k)
    _add_s_and_a(k, lo, hi)


def _add_bars(k: Kit, nw: float) -> None:
    s, h, x, asc, desc, ov, bw = k.s, k.h, k.x, k.asc, k.desc, k.ov, k.bw
    tr = nw * 0.38
    tx = tr * 0.9
    top = x + (asc - x) * s.t_height
    if s.t_form == "hook":

        def t() -> Shape:
            return (
                [
                    k.pen()
                    .m(tx, top - h)
                    .l(tx, h + tr)
                    .a(tx + tr, h + tr, tr, tr + ov * 0.5, 180, 285),
                    k.pen().m(0, x - h).l(tx * 2.1 + h, x - h),
                ],
                [],
            )

        k.put("t", t, ax=tx)
    else:
        k.put("t", lambda: ([k.stem(tx, 0, top), k.pen().m(0, x - h).l(tx * 2, x - h)], []))
    fr = nw * 0.4
    k.put(
        "f",
        lambda: (
            [
                k.pen()
                .m(tx, h)
                .l(tx, asc - h - fr)
                .a(tx + fr, asc - h - fr, fr, fr + ov * 0.5, 180, 75),
                k.pen().m(0, x - h).l(tx * 2.1 + h, x - h),
            ],
            [],
        ),
        ax=tx,
    )
    jr = bw * 0.3
    k.put(
        "j",
        lambda: (
            [k.pen().m(0, x - h).l(0, desc + h + jr).a(-jr, desc + h + jr, jr, jr, 0, -150)],
            [k.dot(0)],
        ),
        width=0,
    )


def _add_diagonals(k: Kit) -> None:
    h, x, desc, bw = k.h, k.x, k.desc, k.bw
    yw = bw * 1.02
    slope = yw / 2 / x
    xd = yw / 2 - slope * (-desc)
    k.put("v", lambda: ([k.pen().m(0, x - h).l(yw / 2, h).l(yw, x - h)], []))
    k.put(
        "y",
        lambda: (
            [k.pen().m(yw, x - h).l(xd, desc + h), k.pen().m(0, x - h).l(yw / 2, h * 0.6)],
            [],
        ),
    )
    ww = bw * 1.5
    k.put(
        "w",
        lambda: (
            [k.pen().m(0, x - h).l(ww * 0.25, h).l(ww * 0.5, x - h).l(ww * 0.75, h).l(ww, x - h)],
            [],
        ),
    )
    xw = bw * 0.95
    k.put("x", lambda: ([k.diag(0, x, xw, 0), k.diag(xw, x, 0, 0)], []))
    kw = bw * 0.85
    kb = (h * 0.4, x * 0.3)
    leg = (kb[0] + (kw - kb[0]) * 0.38, kb[1] + (x - kb[1]) * 0.38)
    k.put(
        "k",
        lambda: (
            [
                k.stem(0, 0, k.asc),
                k.diag(kw, x, kb[0], kb[1], True, False),
                k.diag(leg[0], leg[1], kw * 1.02, 0, False, True),
            ],
            [],
        ),
    )
    zw = bw * 0.9
    k.put("z", lambda: ([k.pen().m(0, x - h).l(zw, x - h).l(0, h).l(zw, h)], []))


def _add_s_and_a(k: Kit, lo: float, hi: float) -> None:
    s, h, x, ov, bw = k.s, k.h, k.x, k.ov, k.bw
    sr = bw * 0.47
    ryu = (x - h + ov - x / 2) / 2
    ryl = (x / 2 - h + ov) / 2
    k.put(
        "s",
        lambda: (
            [
                k.pen()
                .a(sr, x / 2 + ryu, sr * 0.92, ryu, 30, 270)
                .a(sr, x / 2 - ryl, sr, ryl, 90, -150)
            ],
            [],
        ),
    )
    if s.a_form == "double":
        ra = bw * 0.47
        ab = x * 0.56

        def a() -> Shape:
            return (
                [
                    k.pen()
                    .m(bw, h)
                    .l(bw, x - h - ra * 0.8)
                    .a(bw / 2, x - h - ra * 0.8, bw / 2, ra * 0.8 + ov * 0.5, 0, 155),
                    k.pen()
                    .m(bw, ab)
                    .l(ra, ab)
                    .a(ra, (ab + lo) / 2, ra, (ab - lo) / 2, 90, 270)
                    .l(bw, lo),
                ],
                [],
            )

        k.put("a", a)
    elif s.a_form == "tail":
        lr = bw * 0.24
        k.put(
            "a",
            lambda: (
                [
                    k.loop(0, lo, bw, hi),
                    k.pen()
                    .m(bw, x - h)
                    .l(bw, h + lr)
                    .a(bw + lr, h + lr, lr, lr + ov * 0.5, 180, 270),
                ],
                [],
            ),
            ax=bw / 2,
        )
    else:
        k.put("a", lambda: ([k.loop(0, lo, bw, hi), k.stem(bw, 0, x)], []), ax=bw / 2)
