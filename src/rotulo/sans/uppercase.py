from rotulo.sans.kit import Kit, Shape
from rotulo.skeleton import Stroke


def add_uppercase(k: Kit) -> None:
    h, c, ov, cw, w = k.h, k.cap, k.ov, k.cw, k.w
    lo, hi = h - ov, c - h + ov
    ow = (c * 0.98 - w) * cw

    def ring() -> Stroke:
        return k.loop(0, lo, ow, hi)

    k.put("O", lambda: ([ring()], []))
    k.put("Q", lambda: ([ring(), k.diag(ow * 0.62, c * 0.24, ow * 1.02, 0, False, True)], []))
    ac = k.ap * 0.9
    k.put("C", lambda: ([k.rarc(k.pen(), 0, lo, ow * 0.93, hi, ac, 360 - ac)], []))
    gy = c * 0.45
    k.put(
        "G",
        lambda: (
            [k.rarc(k.pen(), 0, lo, ow * 0.95, hi, ac, 360).l(ow * 0.95, gy).l(ow * 0.55, gy)],
            [],
        ),
    )
    k.put("I", lambda: ([k.stem(0, 0, c)], []))
    tw = c * 0.62 * cw
    k.put("T", lambda: ([k.pen().m(0, c - h).l(tw, c - h), k.stem(tw / 2, 0, c - h)], []))
    ew = c * 0.5 * cw
    k.put(
        "E",
        lambda: (
            [
                k.pen().m(ew, c - h).l(0, c - h).l(0, h).l(ew, h),
                k.pen().m(0, c * 0.5).l(ew * 0.9, c * 0.5),
            ],
            [],
        ),
    )
    k.put(
        "F",
        lambda: (
            [
                k.pen().m(ew, c - h).l(0, c - h).l(0, h),
                k.pen().m(0, c * 0.5).l(ew * 0.88, c * 0.5),
            ],
            [],
        ),
    )
    k.put("L", lambda: ([k.pen().m(0, c - h).l(0, h).l(ew * 0.95, h)], []))
    hw = c * 0.66 * cw
    k.put(
        "H",
        lambda: ([k.stem(0, 0, c), k.stem(hw, 0, c), k.pen().m(0, c * 0.5).l(hw, c * 0.5)], []),
    )
    _add_bowls(k)
    _add_diagonals(k)
    _add_curves(k)


def _add_bowls(k: Kit) -> None:
    h, c, cw, w = k.h, k.cap, k.cw, k.w
    pw = c * 0.32 * cw
    pr = (c - w) * 0.27
    py = c - h - pr

    def bowl() -> Stroke:
        return k.pen().m(0, c - h).l(pw, c - h).a(pw, py, pr, pr, 90, -90).l(0, py - pr)

    k.put("P", lambda: ([k.stem(0, 0, c - h), bowl()], []))
    k.put(
        "R",
        lambda: (
            [k.stem(0, 0, c - h), bowl(), k.pen().m(pw * 0.9, py - pr).l(pw + pr * 1.05, h)],
            [],
        ),
    )
    ym = c * 0.53
    r1 = (c - h - ym) / 2
    r2 = (ym - h) / 2
    b1, b2 = c * 0.26 * cw, c * 0.3 * cw
    k.put(
        "B",
        lambda: (
            [
                k.stem(0, 0, c),
                k.pen().m(0, c - h).l(b1, c - h).a(b1, ym + r1, r1, r1, 90, -90).l(0, ym),
                k.pen().m(0, ym).l(b2, ym).a(b2, h + r2, r2, r2, 90, -90).l(0, h),
            ],
            [],
        ),
    )
    dx, dr = c * 0.3 * cw, c * 0.32
    k.put(
        "D",
        lambda: (
            [
                k.stem(0, 0, c),
                k.rarc(k.pen().m(0, c - h).l(dx, c - h), dx - dr, h, dx + dr, c - h, 90, -90).l(
                    0, h
                ),
            ],
            [],
        ),
    )


def _add_diagonals(k: Kit) -> None:
    h, c, cw = k.h, k.cap, k.cw
    kw = c * 0.6 * cw
    kb = (h * 0.4, c * 0.32)
    leg = (kb[0] + (kw - kb[0]) * 0.36, kb[1] + (c - kb[1]) * 0.36)
    k.put(
        "K",
        lambda: (
            [
                k.stem(0, 0, c),
                k.diag(kw, c, kb[0], kb[1], True, False),
                k.diag(leg[0], leg[1], kw * 1.03, 0, False, True),
            ],
            [],
        ),
    )
    aw, ab = c * 0.78 * cw, c * 0.27
    k.put(
        "A",
        lambda: (
            [
                k.pen().m(0, h).l(aw / 2, c - h).l(aw, h),
                k.pen().m(aw * 0.18, ab).l(aw * 0.82, ab),
            ],
            [],
        ),
    )
    vw = c * 0.74 * cw
    k.put("V", lambda: ([k.pen().m(0, c - h).l(vw / 2, h).l(vw, c - h)], []))
    ww = c * 1.08 * cw

    def w_shape() -> Shape:
        pen = k.pen().m(0, c - h)
        for i, y in ((1, h), (2, c - h), (3, h), (4, c - h)):
            pen.l(ww * i / 4, y)
        return [pen], []

    k.put("W", w_shape)
    xw = c * 0.68 * cw
    k.put("X", lambda: ([k.diag(0, c, xw, 0), k.diag(xw, c, 0, 0)], []))
    mw = c * 0.78 * cw
    mv = c * k.s.m_vertex + h
    k.put(
        "M",
        lambda: ([k.pen().m(0, h).l(0, c - h).l(mw / 2, mv).l(mw, c - h).l(mw, h)], []),
    )
    nw = c * 0.66 * cw
    k.put("N", lambda: ([k.pen().m(0, h).l(0, c - h).l(nw, h).l(nw, c - h)], []))
    yw = c * 0.72 * cw
    k.put(
        "Y",
        lambda: (
            [
                k.pen().m(0, c - h).l(yw / 2, c * 0.44).l(yw, c - h),
                k.stem(yw / 2, 0, c * 0.44),
            ],
            [],
        ),
    )
    zw = c * 0.62 * cw
    k.put("Z", lambda: ([k.pen().m(0, c - h).l(zw, c - h).l(0, h).l(zw, h)], []))


def _add_curves(k: Kit) -> None:
    h, c, cw, ov = k.h, k.cap, k.cw, k.ov
    ur = c * 0.31 * cw
    k.put(
        "U",
        lambda: (
            [
                k.pen()
                .m(0, c - h)
                .l(0, h + ur)
                .a(ur, h + ur, ur, ur + ov * 0.5, 180, 360)
                .l(2 * ur, c - h)
            ],
            [],
        ),
    )
    jw = c * 0.42 * cw
    jr = jw * 0.5
    k.put(
        "J",
        lambda: (
            [k.pen().m(jw, c - h).l(jw, h + jr).a(jw - jr, h + jr, jr, jr + ov * 0.5, 0, -165)],
            [],
        ),
    )
    sr = c * 0.29 * cw
    ru = (c - h + ov - c / 2) / 2
    rl = (c / 2 - h + ov) / 2
    k.put(
        "S",
        lambda: (
            [k.pen().a(sr, c / 2 + ru, sr * 0.93, ru, 28, 270).a(sr, c / 2 - rl, sr, rl, 90, -148)],
            [],
        ),
    )
