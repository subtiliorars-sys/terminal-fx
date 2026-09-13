#!/usr/bin/env python3
# Maria — Rosary of Light  —  a TermFX effect, exported as a standalone piece.
# Single file, standard library only.  python3 maria.py
#
# Ctrl+C to exit; the terminal is restored afterwards.

import os
import re as _re
import signal as _signal
import sys as _sys
import time as _time

"""Color helpers: palettes, truecolor detection, and ANSI escapes."""

import os

_TRUE_COLOR = os.environ.get("COLORTERM", "") in ("truecolor", "24bit")


def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def ansi256(r, g, b):
    """Nearest 256-color escape for a truecolor triple.

    Uses the standard 6x6x6 color cube for saturated colors and the
    grayscale ramp for near-neutral ones.
    """
    def cube(v):
        v = max(0, min(255, v))
        if v == 0:
            return 0
        if v < 48:
            return 1
        if v < 115:
            return 2
        if v < 155:
            return 3
        if v < 195:
            return 4
        if v < 235:
            return 5
        return 6

    r_, g_, b_ = cube(r), cube(g), cube(b)
    if r_ == g_ == b_:
        gray = 232 + round(max(r, g, b) / 255 * 23)
        return f"\033[38;5;{gray}m"
    return f"\033[38;5;{16 + 36 * r_ + 6 * g_ + b_}m"


def ansi(r, g, b):
    """Truecolor escape when supported, else the closest 256-color one."""
    if _TRUE_COLOR:
        return fg(r, g, b)
    return ansi256(r, g, b)


def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB. h: 0-360, s/v: 0-1. Returns (r, g, b) 0-255."""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (round((r + m) * 255), round((g + m) * 255), round((b + m) * 255))


FIRE_RAMP = [
    (0, 0, 0),
    (24, 0, 0),
    (52, 4, 0),
    (84, 12, 0),
    (120, 26, 0),
    (160, 46, 0),
    (200, 76, 0),
    (235, 122, 0),
    (255, 178, 20),
    (255, 224, 96),
    (255, 250, 160),
    (255, 255, 235),
]

FIRE_CHARS = " .:*oO@%#"
RAMP10 = " .:-=+*#%@"

# ---- effect ----
"""Maria: a rosary of light around the Mother.

Concentric halos breathe around a luminous core over deep midnight blue,
adrift with the stars of heaven. Blue for the mantle, gold for the light.
"""

import math



RAMP = " .:*oO@"


def render(width, height, t):
    cxs, cys = (width - 1) / 2, (height - 1) / 2
    maxr = max(1.0, math.hypot(cxs, cys))
    out = []

    for y in range(height):
        row = []
        for x in range(width):
            r = math.hypot(x - cxs, y - cys) / maxr
            breath = 0.5 + 0.5 * math.sin(t * 0.9)
            halo = abs(math.sin(r * math.pi * 4 - t * 0.35))
            glow = math.exp(-3.2 * r)
            ring = math.exp(-((r - (0.45 + 0.06 * breath)) ** 2) / (2 * 0.012))
            val = 0.10 + 0.5 * glow + 0.6 * halo * ring

            star = math.sin(x * 3.7 + y * 9.1 + t * 4.0) > 0.995
            v = min(1.0, max(0.0, val))
            if star:
                row.append(ansi(235, 245, 255) + "+")
                continue
            idx = int(v * (len(RAMP) - 1))
            r_ = int(70 * v + 255 * ring)
            g_ = int(90 * v + 205 * ring)
            b_ = int(150 + 100 * v)
            row.append(ansi(r_, g_, b_) + RAMP[idx])
        out.append("".join(row))
    return out
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
    _sys.stdout.write("\033[2J\033[?25l")
    _sys.stdout.flush()
    start = last = _time.monotonic()
    next_frame = start
    try:
        while True:
            now = _time.monotonic()
            t = now - start
            rows = render(width, height, t)
            _sys.stdout.write("\033[H" + "\n".join(rows) + "\033[0m")
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
        _sys.stdout.write("\033[2J\033[H\033[?25h\033[0m")
        _sys.stdout.flush()

if __name__ == "__main__":
    _run()
