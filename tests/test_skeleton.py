from rotulo.skeleton import Point, Stroke


def _bezier_points(segments: list[tuple[str, tuple[Point, ...]]]) -> list[Point]:
    out: list[Point] = []
    cur: Point = (0.0, 0.0)
    for kind, pts in segments:
        if kind in ("M", "L"):
            cur = pts[0]
            out.append(cur)
            continue
        c1, c2, end = pts
        for i in range(1, 21):
            t = i / 20
            u = 1 - t
            out.append(
                (
                    u**3 * cur[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * end[0],
                    u**3 * cur[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * end[1],
                )
            )
        cur = end
    return out


def test_rounded_corner_still_reaches_the_line() -> None:
    stroke = Stroke(70).m(0, 0).l(0, 700).l(500, 0)
    top = max(y for _, y in _bezier_points(stroke.finish()))
    assert abs(top - 700) < 1


def test_straight_polyline_without_radius_keeps_vertices() -> None:
    segments = Stroke(0).m(0, 0).l(100, 0).l(100, 100).finish()
    assert [kind for kind, _ in segments] == ["M", "L", "L"]


def test_finish_is_idempotent() -> None:
    stroke = Stroke(50).m(0, 0).l(0, 100).l(100, 100)
    first = list(stroke.finish())
    assert stroke.finish() == first
