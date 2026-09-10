"""Sinai: the parting of the sea.

Two walls of water roll apart to leave a dry roadway — golden sand under a
desert sun, blue waves capped with white. A quiet animation of the exodus
across Yam Suf.
"""

import math

from .. import color

RAMP = " .:*oO@"


def render(width, height, t):
    out = []
    cys = height - 1
    for y in range(height):
        ny = y / height if height else 0.0
        row = []
        for x in range(width):
            nx = x / width - 0.5
            gap = (0.16 + 0.30 * ny) * width + 0.5 * math.sin(t * 0.9)
            half = width / 2
            in_sea_left = x < half - gap
            in_sea_right = x > half + gap

            if not in_sea_left and not in_sea_right:
                wave = x % 3 == int(t * 2) % 3
                depth = (1 - ny) * 0.9
                r = int(222 * (0.4 + 0.6 * (1 - ny)))
                g = int(182 * (0.3 + 0.7 * (1 - ny)))
                b = int(110 * (1 - ny))
                char = "." if not wave else "+"
                row.append(color.ansi(r, g, b) + char)
                continue

            depth = 0.35 + 0.65 * ny
            wave = math.sin(x * 1.7 + t * 3.0 + y * 0.6) * depth
            crest = wave > 0.75
            r = int(24 + 90 * depth)
            g = int(70 + 130 * depth)
            b = int(160 + 90 * depth)
            char = "~" if not crest else "@"
            row.append(color.ansi(r, g, b) + char)
        out.append("".join(row))
    return out