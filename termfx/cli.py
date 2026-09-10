"""Command-line entry point for TermFX.

Sub-commands:
    termfx.py                  menu mode (cycles all effects)
    termfx.py <effect>         run one effect by name
    termfx.py --list           list effects
    termfx.py music            compose an isorhythmic WAV (ars subtilior)
    termfx.py pack <effect>    export an effect as a standalone single file
"""

import argparse
import os
import sys

from . import bundle, composer, products
from .effects import REGISTRY
from .engine import Engine


def build_parser():
    parser = argparse.ArgumentParser(
        prog="termfx",
        description="TermFX  —  a zero-dependency terminal effects showcase "
        "with themed collections.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="effect name, 'music', or 'pack' (omit for menu mode)",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="effect name for 'pack'; unused otherwise",
    )
    parser.add_argument("--list", action="store_true", help="list effects and exit")
    parser.add_argument("--fps", type=float, default=30.0, help="target frame rate")
    parser.add_argument(
        "--seconds", type=float, default=None, help="auto-exit after N seconds"
    )
    parser.add_argument(
        "--menu-secs", type=float, default=7.0, help="seconds per effect in menu mode"
    )
    music = parser.add_argument_group("music (ars subtilior composer)")
    music.add_argument("--bpm", type=float, default=88.0, help="tempo (quarter notes/min)")
    music.add_argument("--measures", type=int, default=16, help="number of measures")
    music.add_argument("--out", default=None, help="output path for music/pack")
    music.add_argument("--play", action="store_true", help="try to play the result")
    music.add_argument("--seed", type=int, default=None, help="RNG seed")
    return parser


def _list_effects():
    from .effects import META

    for name, (_, description) in REGISTRY.items():
        title = META.get(name, {}).get("title")
        tag = f"[{title}] " if title else ""
        print(f"{name:10s} {tag}{description}")
    print("\nrun:  termfx.py              menu mode (n=next, p=prev, q=quit)")
    print("      termfx.py music        compose an isorhythmic WAV")
    print("      termfx.py pack <fx>    export one effect as a standalone file")
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.list:
        return _list_effects()

    command = args.command or "menu"
    if command == "pack":
        if not args.target:
            print("pack needs an effect name, e.g.  termfx.py pack maria", file=sys.stderr)
            return 2
        out = args.out or f"{args.target}.py"
        src = bundle.standalone_source(args.target)
        with open(out, "w") as fh:
            fh.write(src)
        os.chmod(out, 0o755)
        print(f"packed {args.target} -> {out}  (python3 {out})")
        return 0

    if command == "music":
        return composer.main(
            bpm=args.bpm,
            measures=args.measures,
            out=args.out,
            play=args.play,
            seed=args.seed,
        )

    if command == "products":
        return products.main(seed=args.seed)

    if command not in REGISTRY and command != "menu":
        print(f"unknown effect '{command}'", file=sys.stderr)
        print("available: " + ", ".join(REGISTRY), file=sys.stderr)
        return 2

    if args.fps <= 0:
        print("--fps must be positive", file=sys.stderr)
        return 2

    engine = Engine(fps=args.fps)
    engine.start()
    try:
        if command != "menu":
            render, _ = REGISTRY[command]
            engine.frame_loop(render, command, duration=args.seconds)
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