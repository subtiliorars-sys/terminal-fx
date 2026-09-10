"""Command-line entry point for TermFX."""

import argparse
import sys

from .effects import REGISTRY
from .engine import Engine


def build_parser():
    parser = argparse.ArgumentParser(
        prog="termfx",
        description="A zero-dependency terminal effects showcase.",
    )
    parser.add_argument("effect", nargs="?", help="effect name, or omit for menu mode")
    parser.add_argument("--list", action="store_true", help="list effects and exit")
    parser.add_argument("--fps", type=float, default=30.0, help="target frame rate")
    parser.add_argument(
        "--seconds", type=float, default=None, help="auto-exit after N seconds"
    )
    parser.add_argument(
        "--menu-secs", type=float, default=7.0, help="seconds per effect in menu mode"
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.list:
        for name, (_, description) in REGISTRY.items():
            print(f"{name:10s} {description}")
        return 0

    if args.effect and args.effect not in REGISTRY:
        print(f"unknown effect '{args.effect}'", file=sys.stderr)
        print("available: " + ", ".join(REGISTRY), file=sys.stderr)
        return 2

    if args.fps <= 0:
        print("--fps must be positive", file=sys.stderr)
        return 2

    engine = Engine(fps=args.fps)
    engine.start()
    try:
        if args.effect:
            render, _ = REGISTRY[args.effect]
            engine.frame_loop(render, args.effect, duration=args.seconds)
        else:
            engine.menu_cycle(REGISTRY, per_effect=args.menu_secs, total_duration=args.seconds)
    except KeyboardInterrupt:
        pass
    finally:
        engine.cleanup()

    print("Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())