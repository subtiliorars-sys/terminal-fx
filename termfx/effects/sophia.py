"""Sophia: an aeon mandala of the pleroma.

A rotating star-lattice mandala ringed by pulsing lights, with fleeting
sparks — a meditation on the Gnostic vision of the fullness of light and
the divine spark in every soul.
"""

import math

from .. import color

RAMP = " .:*oO@"


def render(width, height, t):
    cxs, cys = (width - 1) / 2, (height - 1) / 2
    maxr = max(1.0, math.hypot(cxs, cys))
    out = []

    for y in range(height):
        row = []
        for x in range(width):
            dx = x - cxs
            dy = y - cys
            r = math.hypot(dx, dy) / maxr
            angle = math.atan2(dy, dx)

            petals = 0.5 + 0.5 * math.sin(6 * angle - t * 0.7 + r * 6)
            rings = 0.5 + 0.5 * math.sin(r * 9 - t * 1.1)
            core = math.exp(-8.0 * r)
            val = 0.18 + 0.5 * petals * rings + 0.45 * core

            spark = (
                math.sin(x * 12.9898 + y * 78.233 + t * 5.0)
                > 0.992
            )
            v = min(1.0, max(0.0, val))
            if spark:
                row.append(color.ansi(255, 255, 250) + "+")
                continue
            idx = int(v * (len(RAMP) - 1))
            r_gold = int(255 * (0.35 + 0.65 * v))
            g_gold = int(214 * (0.30 + 0.70 * v))
            b_gold = int(120 * v + 40)
            row.append(color.ansi(r_gold, g_gold, b_gold) + RAMP[idx])
        out.append("".join(row))
    return out