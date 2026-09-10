"""Animated Julia-set fractal.

Escape-time iteration with a rotating complex constant, colored by iteration
count. The iteration budget scales with the terminal size to keep the frame
rate usable on large windows.
"""

import math

from .. import color

CHARS = color.RAMP10


def render(width, height, t):
    c = complex(0.7885 * math.cos(t * 0.6), 0.7885 * math.sin(t * 0.6))
    max_iter = max(10, min(30, int(150000 / (width * height))))
    span = max(width, height) * 0.5
    out = []

    for y in range(height):
        im = (y - height / 2) / span * 1.2
        row = []
        for x in range(width):
            re = (x - width / 2) / span * 1.8
            z = complex(re, im)
            it = 0
            abs_sq = re * re + im * im
            while it < max_iter and abs_sq <= 4.0:
                z = z * z + c
                abs_sq = z.real * z.real + z.imag * z.imag
                it += 1
            if it >= max_iter:
                row.append(color.ansi(0, 0, 0) + " ")
            else:
                v = it / max_iter
                hue = (v * 3 + t * 0.1) % 1.0
                idx = int(v * (len(CHARS) - 1))
                r, g, b = color.hsv_to_rgb(
                    hue * 360, 0.85, 0.35 + 0.65 * v
                )
                row.append(color.ansi(r, g, b) + CHARS[idx])
        out.append("".join(row))
    return out