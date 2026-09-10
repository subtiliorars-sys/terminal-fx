"""Rising flame: a heat buffer propagates upward with diffusion and cooling.

The bottom rows are re-ignited every frame. Thanks to in-place bottom-up
updates the flame reads the freshly-updated row below, so heat naturally
rises and flickers.
"""

import random

from .. import color

_DECAY = 0.045

_state = {}


def render(width, height, t):
    st = _state
    if st.get("shape") != (width, height):
        st["shape"] = (width, height)
        st["buf"] = [[0.0] * width for _ in range(height)]

    buf = st["buf"]
    bottom = height - 1
    for x in range(width):
        v = random.random()
        if random.random() < 0.5:
            v *= random.random()
        buf[bottom][x] = v
        buf[bottom - 1][x] = v * random.uniform(0.55, 1.0)

    for y in range(height - 2, -1, -1):
        row = buf[y]
        below = buf[y + 1]
        for x in range(width):
            left = below[(x - 1) % width]
            mid = below[x]
            right = below[(x + 1) % width]
            hot = (left + mid + right) / 3.0 - _DECAY
            row[x] = hot if hot > 0.0 else 0.0

    ramp = color.FIRE_RAMP
    ramp_chars = color.FIRE_CHARS
    out = []
    for y in range(height):
        row = []
        bufrow = buf[y]
        for x in range(width):
            v = bufrow[x]
            idx = int(v * (len(ramp) - 1))
            idx = max(0, min(len(ramp) - 1, idx))
            char_idx = int(v * (len(ramp_chars) - 1))
            char_idx = max(0, min(len(ramp_chars) - 1, char_idx))
            r, g, b = ramp[idx]
            row.append(color.ansi(r, g, b) + ramp_chars[char_idx])
        out.append("".join(row))
    return out