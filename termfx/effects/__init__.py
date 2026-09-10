"""Effects registry and collection metadata.

Each ``REGISTRY`` entry maps a CLI name to ``(render_callable, description)``
where ``render_callable(width, height, t) -> list[str]``.

``META`` carries per-effect product metadata for the monetization track
(pricing is the monetization session's call — these are suggestions only).
"""

from . import ars, cube, david, deseret, fire, julia, light, maria, matrix
from . import plasma, rain, rotozoom, sinai, sophia, stars

REGISTRY = {
    "cube": (cube.render, "spinning 3D wireframe cube"),
    "plasma": (plasma.render, "overlapping sine-wave plasma"),
    "stars": (stars.render, "warp-speed starfield"),
    "matrix": (matrix.render, "matrix-style code rain"),
    "fire": (fire.render, "rising flame"),
    "rotozoom": (rotozoom.render, "rotating and zooming sine tunnel"),
    "julia": (julia.render, "animated Julia-set fractal"),
    "rain": (rain.render, "slanted cyan rain streaks"),
    "ars": (ars.render, "isorhythmic score — the subtle art"),
    "sophia": (sophia.render, "aeon mandala of the pleroma"),
    "deseret": (deseret.render, "honeycomb beehive at dawn"),
    "maria": (maria.render, "rosary of light around the Mother"),
    "light": (light.render, "eightfold star lattice, light upon light"),
    "sinai": (sinai.render, "the parting of the sea"),
    "david": (david.render, "the psalmist's harp"),
}

META = {
    "ars": {
        "title": "Ars Subtilior — The Subtle Art",
        "theme": "medieval music",
        "hint": "poetic; ships with the generative composer (termfx.py music)",
        "suggested": 4.99,
    },
    "sophia": {
        "title": "Sophia — Aeons of Light",
        "theme": "gnostic luminaries",
        "hint": "meditative mandala, sparks and rings",
        "suggested": 2.99,
    },
    "deseret": {
        "title": "Deseret — Hive at Dawn",
        "theme": "the beehive",
        "hint": "honeycomb lattice with sunrise",
        "suggested": 2.99,
    },
    "maria": {
        "title": "Maria — Rosary of Light",
        "theme": "the Mother",
        "hint": "breathing halos under a field of stars",
        "suggested": 3.99,
    },
    "light": {
        "title": "Light — Light upon Light",
        "theme": "geometric light; aniconic",
        "hint": "eightfold lattice, no figuration",
        "suggested": 2.99,
    },
    "sinai": {
        "title": "Sinai — The Parting",
        "theme": "the exodus",
        "hint": "opening sea with a golden way",
        "suggested": 3.99,
    },
    "david": {
        "title": "David — The Psalmist's Harp",
        "theme": "the psalms",
        "hint": "strumming harp over psalm verse",
        "suggested": 3.99,
    },
}

THEME_COLLECTIONS = {
    "core": ["cube", "plasma", "stars", "matrix", "fire", "rotozoom", "julia", "rain"],
    "sacred": ["sophia", "maria", "david", "light", "sinai", "deseret", "ars"],
}