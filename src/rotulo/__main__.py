import argparse
from pathlib import Path

from rotulo.build import build_font
from rotulo.params import DISPLAY, READING


def main() -> None:
    parser = argparse.ArgumentParser(prog="rotulo", description="Build the Rotulo fonts.")
    parser.add_argument("--out", type=Path, default=Path("build"))
    args = parser.parse_args()
    for params, style, weight_class in ((DISPLAY, "Display", 200), (READING, "Lectura", 500)):
        print(build_font(params, style, weight_class, args.out))


if __name__ == "__main__":
    main()
