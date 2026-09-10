"""Matrix-style code rain.

Every column holds a persistent stream that falls continuously. Column
speed varies to give the classic depth illusion. Cells are deterministic
functions of position and time, so the stream is smooth and never regenerates
random data per frame.
"""

import random

from .. import color

ALPHABET = "0123456789ABCDEF"
_LEN = 0.65

_state = {}


def render(width, height, t):
    st = _state
    if st.get("shape") != (width, height) or not st.get("cols"):
        rng = random.Random(5678)
        cols = []
        for x in range(width):
            stream_len = max(4, int(height * _LEN))
            cols.append(
                (
                    x,
                    rng.uniform(-stream_len, -1),
                    rng.uniform(2.2, 6.5),
                    stream_len,
                )
            )
        st["cols"] = cols
        st["shape"] = (width, height)

    rows = [[" "] * width for _ in range(height)]
    for x, base, speed, stream_len in st["cols"]:
        head = int(base + t * speed)
        head_max = head
        start_k = 0
        if head < 0:
            start_k = -head
        for k in range(start_k, stream_len):
            y = head - k
            if y >= height:
                break
            if y < 0:
                continue
            fade = k / stream_len
            bright = int(255 * (1 - fade))
            if k == 0:
                r, g, b = 255, 255, 255
            else:
                r, g, b = 0, bright, int(bright * 0.55)
            ch = ALPHABET[(x * 7 + y * 13 + int(t * 9)) % len(ALPHABET)]
            rows[y][x] = color.ansi(r, g, b) + ch

    return ["".join(row) for row in rows]