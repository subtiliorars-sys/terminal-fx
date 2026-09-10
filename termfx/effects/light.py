"""Light: an eightfold star lattice, light upon light.

Non-figurative — as befits Islamic art — an interlaced geometric lattice
rotates slowly and breathes in luminous gold over teal shadow. The eye is
drawn along the lines of the pattern rather than to any image, keeping
faith with the aniconic tradition.
"""

import math

from .. import color

RAMP = " .:*oO@"


def render(width, height, t):
    cxs, cys = (width - 1) / 2, (height - 1) / 2
    maxr = max(1.0, math.hypot(cxs, cys))
    ca, sa = math.cos(t * 0.12), math.sin(t * 0.12)
    out = []

    for y in range(height):
        row = []
        for x in range(width):
            dx, dy = x - cxs, y - cys
            u = (dx * ca - dy * sa) * 0.16
            v = (dx * sa + dy * ca) * 0.16
            line = 1.0 - max(abs(math.sin(math.pi * u)), abs(math.sin(math.pi * v)))
            r = math.hypot(dx, dy) / maxr
            bloom = 0.5 + 0.5 * math.sin(r * 3.0 - t * 0.7)
            radial = math.exp(-1.6 * r)
            val = min(1.0, line * bloom * 0.9 + 0.35 * radial)

            idx = int(val * (len(RAMP) - 1))
            gold = min(255, int(230 * val + 30))
            green = min(255, int(150 * val + 70))
            blue = int(60 + 90 * (1 - val))
            row.append(color.ansi(gold, green, blue) + RAMP[idx])
        out.append("".join(row))
    return out