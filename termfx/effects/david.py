"""David: the psalmist's harp.

Harp strings strum in a traveling wave of light over a slowly scrolling
amber passage from the Psalms, rendered in gold and lapis.
"""

import math

from .. import color

PSALM = (
    "The LORD is my shepherd; I shall not want."
    " He maketh me to lie down in green pastures:"
    " he leadeth me beside the still waters. He restoreth my soul:"
    " he leadeth me in the paths of righteousness for his name's sake."
)

RAMP = " .:*oO@"
_state = {"scroll": 0.0}


def bead_pos(t, n):
    return (t * 1.4) % max(1, n)


def render(width, height, t):
    st = _state
    st["scroll"] = t * 1.6
    rows = []
    string_cols = max(6, min(40, width // 4))
    frame_height = max(2, height // 2)
    bead = bead_pos(t, string_cols)

    for y in range(frame_height):
        row = []
        depth_fade = 1.0 - (y / max(1, frame_height)) * 0.7
        for x in range(string_cols):
            energy = max(0.0, 1.0 - abs(x - bead) * 0.85)
            bright = energy * (0.30 + 0.70 * depth_fade)
            if bright > 0.15:
                r = int(255 * bright)
                g = int(210 * bright)
                b = int(120 * bright)
                row.append(color.ansi(r, g, b) + "|")
            else:
                row.append(color.ansi(46, 60, 110) + "|")
        rows.append("".join(row) + "".join([" "] * (width - string_cols)))

    while len(rows) < height:
        cols = (width - string_cols) - 8
        pos = max(0, int(st["scroll"] / 3) % (len(PSALM) + cols))
        verse = PSALM[pos:pos + cols]
        row = " " * 4 + verse.ljust(cols)
        row = row[:width].ljust(width)
        rows.append(color.ansi(230, 176, 90) + row)
    return rows[:height]