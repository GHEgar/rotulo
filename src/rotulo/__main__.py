import argparse
from pathlib import Path

from rotulo.build import build_font
from rotulo.instances import build_instances
from rotulo.params import DISPLAY, READING
from rotulo.variable import build_variable
from rotulo.web import to_woff2


def main() -> None:
    parser = argparse.ArgumentParser(prog="rotulo", description="Build the Rotulo fonts.")
    parser.add_argument("--out", type=Path, default=Path("build"))
    parser.add_argument("--no-variable", action="store_true", help="skip the variable font")
    parser.add_argument("--web", type=Path, help="also write WOFF2 files into this directory")
    parser.add_argument(
        "--map", type=Path, help="also write static map weights for glyph PBFs here"
    )
    args = parser.parse_args()
    for params, style, weight_class in ((DISPLAY, "Display", 200), (READING, "Lectura", 500)):
        print(build_font(params, style, weight_class, args.out))
    if not args.no_variable:
        variable = build_variable(args.out)
        print(variable)
        if args.map:
            for path in build_instances(variable, args.map):
                print(path)
    if args.web:
        for path in to_woff2(args.out, args.web):
            print(path)


if __name__ == "__main__":
    main()
