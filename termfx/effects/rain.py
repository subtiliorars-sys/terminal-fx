"""Slanted cyan rain streaks.

Drops fall diagonally, wrapping from bottom to top so the rain never stops.
Each streak uses a bright head and a dim slanted body.
"""

import random

from .. import color

_state = {}


def render(width, height, t):
    st = _state
    if st.get("shape") != (width, height) or not st.get("drops"):
        rng = random.Random(2468)
        count = max(8, width // 3)
        st["drops"] = [
            (rng.randint(0, width - 1), rng.uniform(0, 6.28), rng.uniform(5, 11))
            for _ in range(count)
        ]
        st["shape"] = (width, height)

    rows = [[" "] * width for _ in range(height)]
    slant = 0.22
    for col, phase, speed in st["drops"]:
        head = (t * speed + phase) % (height + 6)
        for k in range(5):
            y = int(head) - k
            if 0 <= y < height:
                x = (col - int(y * slant)) % width
                if k == 0:
                    rows[y][x] = color.ansi(210, 255, 255) + "'"
                else:
                    rows[y][x] = color.ansi(40, 90, 200) + "`"

    return ["".join(row) for row in rows]