import math
from collections.abc import Sequence

from rotulo.skeleton import Point, Stroke

Cubic = tuple[Point, Point, Point, Point]
Contour = list[Cubic]

KAPPA = 4 / 3 * math.tan(math.pi / 8)


def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: Point, b: Point, s: float = 1.0) -> Point:
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def _unit(v: Point) -> Point:
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n) if n > 1e-9 else (1.0, 0.0)


def _normal(t: Point) -> Point:
    return (-t[1], t[0])


def _split(c: Cubic) -> tuple[Cubic, Cubic]:
    p0, p1, p2, p3 = c

    def mid(a: Point, b: Point) -> Point:
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    a, b, e = mid(p0, p1), mid(p1, p2), mid(p2, p3)
    f, g = mid(a, b), mid(b, e)
    h = mid(f, g)
    return (p0, a, f, h), (h, g, e, p3)


def _tangents(c: Cubic) -> tuple[Point, Point]:
    p0, p1, p2, p3 = c
    start = _sub(p1, p0) if math.hypot(*_sub(p1, p0)) > 1e-6 else _sub(p2, p0)
    end = _sub(p3, p2) if math.hypot(*_sub(p3, p2)) > 1e-6 else _sub(p3, p1)
    return _unit(start), _unit(end)


def _offset(c: Cubic, h: float) -> Cubic:
    p0, p1, p2, p3 = c
    t0, t3 = _tangents(c)
    turn = math.acos(max(-1.0, min(1.0, t0[0] * t3[0] + t0[1] * t3[1])))
    chord = math.hypot(*_sub(p3, p0))
    if turn > 1e-3 and chord > 1e-6:
        radius = chord / (2 * math.sin(turn / 2))
        cross = t0[0] * t3[1] - t0[1] * t3[0]
        if (cross > 0) == (h > 0):
            h = math.copysign(min(abs(h), radius * 0.95), h)
    q0 = _add(p0, _normal(t0), h)
    q3 = _add(p3, _normal(t3), h)
    scale = math.hypot(*_sub(q3, q0)) / chord if chord > 1e-6 else 1.0
    return q0, _add(q0, _sub(p1, p0), scale), _add(q3, _sub(p2, p3), scale), q3


def _cap(center: Point, tangent: Point, h: float) -> list[Cubic]:
    n = _normal(tangent)
    left, tip, right = _add(center, n, h), _add(center, tangent, h), _add(center, n, -h)
    k = KAPPA * h
    return [
        (left, _add(left, tangent, k), _add(tip, n, k), tip),
        (tip, _add(tip, n, -k), _add(right, tangent, k), right),
    ]


def _piece(c: Cubic, h: float) -> Contour:
    t0, t3 = _tangents(c)
    left = _offset(c, h)
    right = _offset(c, -h)
    back: Cubic = (right[3], right[2], right[1], right[0])
    return [left, *_cap(c[3], t3, h), back, *_cap(c[0], (-t0[0], -t0[1]), h)]


def _cubics(stroke: Stroke, dx: float) -> list[Cubic]:
    out: list[Cubic] = []
    cur: Point | None = None
    for kind, pts in stroke.finish():
        moved = [(x + dx, y) for x, y in pts]
        if kind == "M":
            cur = moved[0]
            continue
        assert cur is not None
        if kind == "L":
            end = moved[0]
            d = _sub(end, cur)
            out.append((cur, _add(cur, d, 1 / 3), _add(cur, d, 2 / 3), end))
        else:
            c1, c2, end = moved
            out.extend(_split((cur, c1, c2, end)))
        cur = moved[-1]
    return out


def capsules(strokes: Sequence[Stroke], weight: float, dx: float) -> list[Contour]:
    h = weight / 2
    return [_piece(c, h) for stroke in strokes for c in _cubics(stroke, dx)]
