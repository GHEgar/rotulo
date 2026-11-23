from dataclasses import dataclass, replace
from typing import Literal

Dot = Literal["round", "line", "slant"]
AForm = Literal["tail", "single", "double"]
LForm = Literal["straight", "tail"]
ZeroForm = Literal["slash", "dot", "plain"]
GForm = Literal["bar", "curl"]
SansA = Literal["tail", "single", "double"]
SansD = Literal["flick", "straight"]
SansT = Literal["hook", "straight"]


@dataclass(frozen=True)
class Sans:
    width: float = 0.8
    cap_width: float = 0.99
    aperture_e: float = 50
    stadium: bool = True
    a_form: SansA = "double"
    d_form: SansD = "straight"
    t_form: SansT = "hook"
    t_height: float = 1.0
    m_vertex: float = 0.5
    optical: float = 0.5


@dataclass(frozen=True)
class Params:
    weight: float = 46
    x_height: float = 425
    cap_height: float = 700
    ascender: float = 840
    descender: float = -415
    sign_descender: float = -180
    width: float = 1.0
    aperture: float = 30
    gap: float = 110
    spacing: float = 1.5
    word_spacing: float = 1.0
    corner: float = 50
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
    g_form: GForm = "bar"
    color_details: bool = False
    q_bar: bool = False
    one_flag: bool = False
    nine_straight: bool = False
    sans: Sans | None = None


DISPLAY = Params()
READING = replace(
    DISPLAY,
    weight=86,
    x_height=470,
    descender=-370,
    spacing=1.8,
    word_spacing=1.6,
    l_form="tail",
    q_bar=True,
    one_flag=True,
    nine_straight=True,
)
SANS = replace(
    DISPLAY,
    weight=90,
    x_height=500,
    cap_height=700,
    ascender=700,
    descender=-200,
    spacing=1.0,
    narrow_air=0,
    overshoot=0,
    aperture=50,
    corner=0,
    dot="round",
    sans=Sans(),
)
