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