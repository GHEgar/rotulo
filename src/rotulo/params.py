from dataclasses import dataclass, replace
from typing import Literal

Dot = Literal["round", "line", "slant"]
AForm = Literal["tail", "single", "double"]
LForm = Literal["straight", "tail"]
ZeroForm = Literal["slash", "dot", "plain"]


@dataclass(frozen=True)
class Params:
    weight: float = 29
    x_height: float = 420
    cap_height: float = 700
    ascender: float = 800
    descender: float = -260
    width: float = 1.0
    aperture: float = 70
    gap: float = 110
    spacing: float = 1.56
    word_spacing: float = 1.0
    corner: float = 70
    overshoot: float = 0
    bar: float = 0.5
    tail: float = 1.15
    tail_close: float = 160
    tail_j: float = 1.5
    lift: float = 0.08
    lift_g: float = 0.16
    narrow_air: float = 0.3
    dot: Dot = "line"
    a_form: AForm = "tail"
    l_form: LForm = "straight"
    zero: ZeroForm = "slash"
    q_bar: bool = False
    one_flag: bool = False
    nine_straight: bool = False


DISPLAY = Params()
READING = replace(
    DISPLAY,
    weight=75,
    x_height=470,
    spacing=1.8,
    word_spacing=1.6,
    l_form="tail",
    q_bar=True,
    one_flag=True,
    nine_straight=True,
)
