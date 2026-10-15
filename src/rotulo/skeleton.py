import math
from collections.abc import Callable
from dataclasses import dataclass

Point = tuple[float, float]
Segment = tuple[str, tuple[Point, ...]]
Transform = Callable[[float, float], Point]

DEG = math.pi / 180


@dataclass(frozen=True)
class Fillet:
    a: Point
    b: Point
    c: Point
    rho: float
    u1: Point
    u2: Point
    k: float


def fillet(pv: Point, v: Point, nx: Point, radius: float) -> Fillet | None:
    l1 = math.hypot(v[0] - pv[0], v[1] - pv[1])
    l2 = math.hypot(nx[0] - v[0], nx[1] - v[1])
    if l1 < 0.5 or l2 < 0.5:
        return None
    u1 = ((v[0] - pv[0]) / l1, (v[1] - pv[1]) / l1)
    u2 = ((nx[0] - v[0]) / l2, (nx[1] - v[1]) / l2)
    phi = math.acos(max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1])))
    if radius <= 0 or phi < 0.02 or phi > 3.05:
        return None
    t = min(radius * math.tan(phi / 2), 0.45 * l1, 0.45 * l2)
    rho = t / math.tan(phi / 2)
    bx, by = u2[0] - u1[0], u2[1] - u1[1]
    bl = math.hypot(bx, by)
    cd = rho / math.cos(phi / 2)
    return Fillet(
        a=(v[0] - u1[0] * t, v[1] - u1[1] * t),
        b=(v[0] + u2[0] * t, v[1] + u2[1] * t),
        c=(v[0] + bx / bl * cd, v[1] + by / bl * cd),
        rho=rho,
        u1=u1,
        u2=u2,
        k=4 / 3 * math.tan(phi / 4) * rho,
    )


def extreme(f: Fillet, axis: int, sign: int) -> float:
    def wrap(x: float) -> float:
        return math.atan2(math.sin(x), math.cos(x))

    ta = math.atan2(f.a[1] - f.c[1], f.a[0] - f.c[0])
    dt = wrap(math.atan2(f.b[1] - f.c[1], f.b[0] - f.c[0]) - ta)
    if axis == 1:
        target = math.pi / 2 if sign > 0 else -math.pi / 2
    else:
        target = 0.0 if sign > 0 else math.pi
    dd = wrap(target - ta)
    if math.copysign(1, dd) == math.copysign(1, dt) and abs(dd) <= abs(dt):
        return f.c[axis] + sign * f.rho
    if sign > 0:
        return max(f.a[axis], f.b[axis])
    return min(f.a[axis], f.b[axis])


class Stroke:
    def __init__(self, radius: float, transform: Transform | None = None) -> None:
        self.radius = radius
        self.transform: Transform = transform or (lambda x, y: (x, y))
        self.segments: list[Segment] = []
        self.nodes: list[Point] = []
        self._pts: list[Point] = []
        self._cur: Point | None = None

    def _out(self, x: float, y: float) -> Point:
        return self.transform(x, y)

    def _flush(self) -> None:
        pts = self._pts
        n = len(pts)
        vs = [[p[0], p[1]] for p in pts]
        for i in range(1, n - 1):
            pv, v, nx = vs[i - 1], vs[i], vs[i + 1]
            for ax in (0, 1):
                if pv[ax] < v[ax] - 0.5 and nx[ax] < v[ax] - 0.5:
                    sign = 1
                elif pv[ax] > v[ax] + 0.5 and nx[ax] > v[ax] + 0.5:
                    sign = -1
                else:
                    continue
                goal = pts[i][ax]
                for _ in range(16):
                    f = fillet((pv[0], pv[1]), (v[0], v[1]), (nx[0], nx[1]), self.radius)
                    if f is None:
                        break
                    v[ax] += goal - extreme(f, ax, sign)
        for i in range(1, n):
            v = vs[i]
            f = None
            if i < n - 1:
                p, q = vs[i - 1], vs[i + 1]
                f = fillet((p[0], p[1]), (v[0], v[1]), (q[0], q[1]), self.radius)
            if f is None:
                self.segments.append(("L", (self._out(v[0], v[1]),)))
                continue
            c1 = (f.a[0] + f.u1[0] * f.k, f.a[1] + f.u1[1] * f.k)
            c2 = (f.b[0] - f.u2[0] * f.k, f.b[1] - f.u2[1] * f.k)
            self.segments.append(("L", (self._out(*f.a),)))
            self.segments.append(("C", (self._out(*c1), self._out(*c2), self._out(*f.b))))
        self._pts = [pts[-1]] if n else []

    def m(self, x: float, y: float) -> "Stroke":
        self._flush()
        self.segments.append(("M", (self._out(x, y),)))
        self._cur = (x, y)
        self._pts = [(x, y)]
        self.nodes.append(self._out(x, y))
        return self

    def l(self, x: float, y: float) -> "Stroke":  # noqa: E743
        if self._cur is None:
            return self.m(x, y)
        self._pts.append((x, y))
        self._cur = (x, y)
        self.nodes.append(self._out(x, y))
        return self

    def a(self, ox: float, oy: float, rx: float, ry: float, a0: float, a1: float) -> "Stroke":
        sx, sy = ox + rx * math.cos(a0 * DEG), oy + ry * math.sin(a0 * DEG)
        if self._cur is None:
            self.m(sx, sy)
        elif math.hypot(sx - self._cur[0], sy - self._cur[1]) > 0.5:
            self.l(sx, sy)
        self._flush()
        n = max(1, math.ceil(abs(a1 - a0) / 90))
        da = (a1 - a0) / n * DEG
        k = 4 / 3 * math.tan(da / 4)
        t = a0 * DEG
        for _ in range(n):
            t1 = t + da
            x0, y0 = ox + rx * math.cos(t), oy + ry * math.sin(t)
            x1, y1 = ox + rx * math.cos(t1), oy + ry * math.sin(t1)
            c1 = self._out(x0 - k * rx * math.sin(t), y0 + k * ry * math.cos(t))
            c2 = self._out(x1 + k * rx * math.sin(t1), y1 - k * ry * math.cos(t1))
            self.segments.append(("C", (c1, c2, self._out(x1, y1))))
            t = t1
        end = (ox + rx * math.cos(a1 * DEG), oy + ry * math.sin(a1 * DEG))
        self._cur = end
        self._pts = [end]
        self.nodes.append(self._out(*end))
        return self

    def c(self, x1: float, y1: float, x2: float, y2: float, x: float, y: float) -> "Stroke":
        self._flush()
        self.segments.append(("C", (self._out(x1, y1), self._out(x2, y2), self._out(x, y))))
        self._cur = (x, y)
        self._pts = [(x, y)]
        self.nodes.append(self._out(x, y))
        return self

    def finish(self) -> list[Segment]:
        self._flush()
        return self.segments
