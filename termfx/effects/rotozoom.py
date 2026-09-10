"""Rotating and zooming sine tunnel (rotozoomer)."""

import math

from .. import color

CHARS = color.RAMP10


def render(width, height, t):
    cxs, cys = (width - 1) / 2, (height - 1) / 2
    ang = t * 0.6
    zoom = (1.0 + 0.35 * math.sin(t * 0.7)) * 0.35
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    out = []

    for y in range(height):
        row = []
        for x in range(width):
            u = (x - cxs) * zoom
            v = (y - cys) * zoom
            xr = u * cos_a - v * sin_a
            yr = u * sin_a + v * cos_a
            p = math.sin(xr) + math.sin(yr)
            val = (p + 2) / 4.0
            idx = int(val * (len(CHARS) - 1))
            hue = (val * 2.5 + t * 0.15) % 1.0
            r, g, b = color.hsv_to_rgb(hue * 360, 0.75, 1.0)
            row.append(color.ansi(r, g, b) + CHARS[idx])
        out.append("".join(row))
    return out