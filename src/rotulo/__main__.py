import argparse
from pathlib import Path

from rotulo.build import build_font
from rotulo.params import DISPLAY, READING
from rotulo.variable import build_variable


def main() -> None:
    parser = argparse.ArgumentParser(prog="rotulo", description="Build the Rotulo fonts.")
    parser.add_argument("--out", type=Path, default=Path("build"))
    parser.add_argument("--no-variable", action="store_true", help="skip the variable font")
    args = parser.parse_args()
    for params, style, weight_class in ((DISPLAY, "Display", 200), (READING, "Lectura", 500)):
        print(build_font(params, style, weight_class, args.out))
    if not args.no_variable:
        print(build_variable(args.out))


if __name__ == "__main__":
    main()
