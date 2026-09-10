"""Warp-speed starfield.

Stars persist across frames and fly toward the viewer along the z axis,
accelerating outward as they approach the screen. Each star's position is
derived purely from its birth time and speed, so motion is smooth and
independent of the frame rate.
"""

import math
import random

from .. import color

CHARS = ".:*+"
_LIFE = 3.0
_Z_NEAR = 0.12

_state = {}


def _respawn(rng, t):
    u = rng.uniform(-0.9, 0.9)
    v = rng.uniform(-0.9, 0.9)
    while math.hypot(u, v) > 0.95:
        u = rng.uniform(-0.9, 0.9)
        v = rng.uniform(-0.9, 0.9)
    return [u, v, t, rng.uniform(0.35, 1.0)]


def render(width, height, t):
    st = _state
    if st.get("shape") != (width, height) or not st.get("stars"):
        count = min(160, max(48, (width * height) // 6))
        rng = random.Random(1234)
        st["shape"] = (width, height)
        root = t if t else 0.0
        st["stars"] = [_respawn(rng, root - rng.uniform(0, _LIFE)) for _ in range(count)]

    rows = [[" "] * width for _ in range(height)]
    half_w, half_h = width / 2, height / 2

    for star in st["stars"]:
        progress = (t - star[2]) / _LIFE * star[3]
        if progress >= 1.0:
            star[2] = t
            star[3] = random.uniform(0.35, 1.0)
            continue
        radial = (1 - _Z_NEAR) * progress / (1 - _Z_NEAR * progress)
        px = int(half_w + star[0] * radial * (width * 0.49))
        py = int(half_h + star[1] * radial * (height * 0.49))
        if 0 <= px < width and 0 <= py < height:
            bright = int(255 * radial)
            char = CHARS[min(len(CHARS) - 1, int(radial * len(CHARS)))]
            rows[py][px] = color.ansi(bright, bright, min(255, int(bright * 1.4))) + char

    return ["".join(row) for row in rows]