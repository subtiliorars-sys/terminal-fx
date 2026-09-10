"""Deseret: a honeycomb beehive at dawn.

The beehive — the enduring symbol of industriousness — glows honey-gold
over a sunrise gathering. A hex lattice pulses gently while the dawn
gradient rises along the horizon.
"""

import math

from .. import color

RAMP = " .:*oO@"


def render(width, height, t):
    out = []
    for y in range(height):
        row = []
        ny = y / height
        for x in range(width):
            gx = x * 0.5
            gy = y * 0.35
            edge = max(
                abs(math.sin(math.pi * (gx + gy * 0.5))),
                abs(math.sin(math.pi * (gx - gy * 0.5))),
            )
            pulse = 0.5 + 0.5 * math.sin(t * 0.8 - gx)
            darkness = 0.55 + 0.45 * (1 - ny)
            val = (1 - edge) * pulse * darkness

            dawn = max(0.0, 1.0 - abs(ny - 0.82) * 5.0)
            v = min(1.0, val + 0.25 * dawn)
            if v < 0.02:
                row.append(color.ansi(24, 26, 40) + " ")
                continue
            idx = int(v * (len(RAMP) - 1))
            r = int(255 * v + 90 * dawn)
            g = int(170 * v + 60 * dawn)
            b = int(70 * (1 - v) + 40 * dawn)
            row.append(color.ansi(r, g, b) + RAMP[idx])
        out.append("".join(row))
    return out