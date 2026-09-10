"""Ars subtilior: an isorhythmic score scrolling across the screen.

Three voice bands (triplum, motetus, tenor) repeat their own rhythm pattern
(*talea*) against a slowly-rotating pitch sequence (*color*). Because every
voice's phrase length differs, the patterns sheer against one another — the
visual signature of late-medieval isorhythm.
"""

import math

from .. import color

UNIT = 0.15

RAMP = " .:*oO@"

BANDS = [
    ("triplum", [2, 4, 2, 4, 2, 4], (255, 198, 70)),
    ("motetus", [3, 3, 6, 3, 3, 6], (214, 78, 74)),
    ("tenor", [12, 12, 12, 12], (78, 128, 255)),
]

_state = {}


def _on_table(rhythm):
    period = sum(rhythm)
    on = [False] * period
    cursor = 0
    for dur in rhythm:
        for _ in range(dur):
            on[cursor] = True
            cursor += 1
    return on


def render(width, height, t):
    st = _state
    if st.get("shape") != (width, height):
        st["shape"] = (width, height)
        st["tables"] = [(_on_table(r), sum(r)) for _, r, _ in BANDS]

    rows = [[" "] * width for _ in range(height)]
    band_h = max(1, height // len(BANDS))

    for band_index, (name, rhythm, palette) in enumerate(BANDS):
        on, period = st["tables"][band_index]
        y0 = band_index * band_h
        y1 = min(height, y0 + band_h)

        for y in range(y0, y1):
            band_frac = (y - y0) / (band_h - 1) if band_h > 1 else 0.5
            depth = 0.4 + 0.6 * (1 - band_frac)
            row = rows[y]
            for x in range(width):
                time_here = t - (width - 1 - x) * UNIT
                idx = int(time_here / UNIT) % period
                if not on[idx]:
                    continue
                age = idx / period
                glow = math.exp(-3.0 * age)
                r, g, b = palette
                rr = int(r * glow * depth)
                gg = int(g * glow * depth)
                bb = int(b * glow * depth)
                char = RAMP[int(glow * (len(RAMP) - 1))]
                row[x] = color.ansi(rr, gg, bb) + char

    for band_index in range(1, len(BANDS)):
        y = band_index * band_h - 1
        if 0 <= y < height:
            rows[y] = [color.ansi(90, 84, 60) + "=" for _ in range(width)]

    return ["".join(row) for row in rows]