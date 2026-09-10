"""Export any registered effect as a standalone, self-contained Python file.

``python3 termfx.py pack maria`` writes ``maria.py`` — a single executable
with no dependency on this repository (stdlib only), ready to be given away
or sold on its own.
"""

import importlib
import pathlib
import re
import textwrap

from .effects import META, REGISTRY


def standalone_source(name):
    if name not in REGISTRY:
        raise KeyError(f"unknown effect '{name}'")
    effect_text = _read_module(f"termfx.effects.{name}")
    color_text = _read_module("termfx.color")

    effect_text = effect_text.replace("from .. import color", "")
    effect_text = re.sub(r"(?<![\w.])color\.", "", effect_text)

    meta = META.get(name, {})
    title = meta.get("title", name.capitalize())
    header = textwrap.dedent(
        f"""\
        #!/usr/bin/env python3
        # {title}  —  a TermFX effect, exported as a standalone piece.
        # Single file, standard library only.  python3 {name}.py
        #
        # Ctrl+C to exit; the terminal is restored afterwards.

        import os
        import re as _re
        import signal as _signal
        import sys as _sys
        import time as _time

        """
    )
    runtime = textwrap.dedent(
        """\

        def _terminal_size():
            try:
                return os.get_terminal_size()
            except OSError:
                return os.terminal_size((80, 24))

        def _run():
            _pid = None
            try:
                _pid = _signal.signal(_signal.SIGWINCH, lambda *_: None)
            except (AttributeError, ValueError):
                pass
            size = _terminal_size()
            width, height = max(20, size.columns), max(10, size.lines - 1)
            _sys.stdout.write("\\033[2J\\033[?25l")
            _sys.stdout.flush()
            start = last = _time.monotonic()
            next_frame = start
            try:
                while True:
                    now = _time.monotonic()
                    t = now - start
                    rows = render(width, height, t)
                    _sys.stdout.write("\\033[H" + "\\n".join(rows) + "\\033[0m")
                    _sys.stdout.flush()
                    next_frame += 1.0 / 30.0
                    delay = next_frame - now
                    if delay > 0:
                        _time.sleep(delay)
                    last = now
                    try:
                        try:
                            size = _terminal_size()
                            width, height = max(20, size.columns), max(10, size.lines - 1)
                        except OSError:
                            pass
                    except Exception:
                        pass
            except KeyboardInterrupt:
                pass
            finally:
                _sys.stdout.write("\\033[2J\\033[H\\033[?25h\\033[0m")
                _sys.stdout.flush()

        if __name__ == "__main__":
            _run()
        """
    )
    return header + color_text + "\n\n# ---- effect ----\n" + effect_text + runtime


def _read_module(module_name):
    module = importlib.import_module(module_name)
    return pathlib.Path(module.__file__).read_text()