"""Spinning 3D wireframe cube with z-buffered depth shading."""

import math

from .. import color


def _rotate(v, ax, ay, az):
    x, y, z = v
    cy, sy = math.cos(ax), math.sin(ax)
    y, z = y * cy - z * sy, y * sy + z * cy
    cx, sx = math.cos(ay), math.sin(ay)
    x, z = x * cx + z * sx, -x * sx + z * cx
    cz, sz = math.cos(az), math.sin(az)
    x, y = x * cz - y * sz, x * sz + y * cz
    return x, y, z


def render(width, height, t):
    ax, ay, az = t * 0.7, t * 1.1, t * 0.5
    s = 1.0
    vertices = [
        (-s, -s, -s), ( s, -s, -s), ( s,  s, -s), (-s,  s, -s),
        (-s, -s,  s), ( s, -s,  s), ( s,  s,  s), (-s,  s,  s),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    distance = 3.0
    projected = []
    for v in vertices:
        rx, ry, rz = _rotate(v, ax, ay, az)
        factor = max(0.01, distance / (rz + distance + 0.01))
        projected.append((rx * factor, ry * factor, rz))

    xs = [p[0] for p in projected]
    ys = [p[1] for p in projected]
    extent = max(max(abs(x) for x in xs), max(abs(y) for y in ys), 1e-3)
    target = min(width, height) * 0.72
    scale = target / (2 * extent)

    for i, (px, py, rz) in enumerate(projected):
        sx = px * scale + width / 2
        sy = height / 2 - py * scale
        projected[i] = (sx, sy, rz)

    edge_depths = []
    for i, j in edges:
        avg_z = (projected[i][2] + projected[j][2]) / 2
        edge_depths.append((avg_z, i, j))
    edge_depths.sort(key=lambda item: item[0])

    buffer = [[" "] * width for _ in range(height)]
    zbuf = [[-999.0] * width for _ in range(height)]
    chars = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    corner = s * math.sqrt(3)

    for avg_z, i, j in edge_depths:
        x0, y0, z0 = projected[i]
        x1, y1, z1 = projected[j]

        x0i, y0i = int(round(x0)), int(round(y0))
        x1i, y1i = int(round(x1)), int(round(y1))
        dx = abs(x1i - x0i)
        dy = -abs(y1i - y0i)
        sx = -1 if x0i > x1i else 1
        sy = -1 if y0i > y1i else 1
        err = dx + dy
        steps = dx - dy
        cx, cy = x0i, y0i
        step = 0

        while True:
            if 0 <= cx < width and 0 <= cy < height:
                tt = step / steps if steps else 1.0
                z = z0 + (z1 - z0) * tt
                if z > zbuf[cy][cx]:
                    zbuf[cy][cx] = z
                    norm = max(0.0, min(1.0, (z + corner) / (2 * corner)))
                    char_idx = int(norm * (len(chars) - 1))
                    b = 255
                    r = int(255 * norm)
                    g = int(255 * (1 - norm))
                    buffer[cy][cx] = color.ansi(r, g, b) + chars[char_idx]
            if cx == x1i and cy == y1i:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                cx += sx
            if e2 <= dx:
                err += dx
                cy += sy
            step += 1

    return ["".join(row) for row in buffer]