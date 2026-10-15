from pathlib import Path

from fontTools.ttLib import TTFont

from rotulo import DISPLAY, READING, build_context, build_font
from rotulo.build import glyph_name

SPANISH = "abcdefghijklmnñopqrstuvwxyzáéíóúüABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ0123456789¿?¡!.,:;"


EXTENDED = "àèìòùâêîôûãõçëïÿÀÈÌÒÙÂÊÎÔÛÃÕÇËÏ&@#%€$+=*_[]{}<>|~" + "".join(
    chr(c) for c in (0x2018, 0x2019, 0x201C, 0x201D, 0xAB, 0xBB, 0x2026, 0xB7, 0x2014)
)


def test_context_covers_spanish() -> None:
    ctx = build_context(DISPLAY)
    assert set(SPANISH) <= set(ctx.glyphs)


def test_context_covers_extended_latin_and_symbols() -> None:
    ctx = build_context(DISPLAY)
    assert set(EXTENDED) <= set(ctx.glyphs)


def test_font_metrics_follow_the_skeleton(tmp_path: Path) -> None:
    font = TTFont(build_font(DISPLAY, "Display", 200, tmp_path))
    glyf = font["glyf"]
    half = DISPLAY.weight / 2
    assert abs(glyf["b"].yMax - (DISPLAY.ascender + half)) <= 2
    assert abs(glyf["g"].yMin - (DISPLAY.descender - half)) <= 2
    assert abs(glyf["H"].yMax - (DISPLAY.cap_height + half)) <= 2
    assert abs(glyf["x"].yMax - (DISPLAY.x_height + half)) <= 2


def test_reading_font_has_kerning_and_alternates(tmp_path: Path) -> None:
    font = TTFont(build_font(READING, "Lectura", 500, tmp_path))
    tags = [r.FeatureTag for r in font["GPOS"].table.FeatureList.FeatureRecord]
    assert "kern" in tags
    assert font["glyf"][glyph_name("q")].xMax > font["glyf"][glyph_name("p")].xMax
    assert font["hmtx"]["i"][0] > 0
