"""Effects registry. Each entry maps a CLI name to
``(render_callable, description)`` where
``render_callable(width, height, t) -> list[str]``."""

from . import cube, fire, julia, matrix, plasma, rain, rotozoom, stars

REGISTRY = {
    "cube": (cube.render, "spinning 3D wireframe cube"),
    "plasma": (plasma.render, "overlapping sine-wave plasma"),
    "stars": (stars.render, "warp-speed starfield"),
    "matrix": (matrix.render, "matrix-style code rain"),
    "fire": (fire.render, "rising flame"),
    "rotozoom": (rotozoom.render, "rotating and zooming sine tunnel"),
    "julia": (julia.render, "animated Julia-set fractal"),
    "rain": (rain.render, "slanted cyan rain streaks"),
}