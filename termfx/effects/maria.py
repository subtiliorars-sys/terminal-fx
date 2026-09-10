"""Maria: a rosary of light around the Mother.

Concentric halos breathe around a luminous core over deep midnight blue,
adrift with the stars of heaven. Blue for the mantle, gold for the light.
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
            r = math.hypot(x - cxs, y - cys) / maxr
            breath = 0.5 + 0.5 * math.sin(t * 0.9)
            halo = abs(math.sin(r * math.pi * 4 - t * 0.35))
            glow = math.exp(-3.2 * r)
            ring = math.exp(-((r - (0.45 + 0.06 * breath)) ** 2) / (2 * 0.012))
            val = 0.10 + 0.5 * glow + 0.6 * halo * ring

            star = math.sin(x * 3.7 + y * 9.1 + t * 4.0) > 0.995
            v = min(1.0, max(0.0, val))
            if star:
                row.append(color.ansi(235, 245, 255) + "+")
                continue
            idx = int(v * (len(RAMP) - 1))
            r_ = int(70 * v + 255 * ring)
            g_ = int(90 * v + 205 * ring)
            b_ = int(150 + 100 * v)
            row.append(color.ansi(r_, g_, b_) + RAMP[idx])
        out.append("".join(row))
    return out