"""Overlapping sine-wave plasma with HSV palette cycling."""

import math

from .. import color

CHARS = color.RAMP10


def render(width, height, t):
    out = []
    for y in range(height):
        row = []
        ny = y / height
        for x in range(width):
            nx = x / width
            v1 = math.sin(nx * 10 + t)
            v2 = math.sin(ny * 8 + t * 0.7)
            v3 = math.sin((nx + ny) * 6 + t * 1.3)
            v4 = math.sin(math.hypot(nx - 0.5, ny - 0.5) * 14 + t * 0.5)
            value = (v1 + v2 + v3 + v4) / 4.0
            value = (value + 1) / 2.0
            idx = int(value * (len(CHARS) - 1))
            r, g, b = color.hsv_to_rgb(value * 360, 0.8, 0.9)
            row.append(color.ansi(r, g, b) + CHARS[idx])
        out.append("".join(row))
    return out