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
        "blurb": "A scrolling isorhythmic score plus the generative composer "
        "(termfx.py music) that writes its own motets to WAV.",
        "price": 6.99,
        "tags": ["music", "medieval", "generative"],
    },
    "sophia": {
        "title": "Sophia — Aeons of Light",
        "theme": "gnostic luminaries",
        "blurb": "A rotating aeon mandala of the pleroma, meditative sparks "
        "and pulsing rings of light.",
        "price": 2.99,
        "tags": ["meditative", "mandala"],
    },
    "deseret": {
        "title": "Deseret — Hive at Dawn",
        "theme": "the beehive",
        "blurb": "A honeycomb lattice glowing honey-gold over a slow sunrise.",
        "price": 2.99,
        "tags": ["pattern", "dawn"],
    },
    "maria": {
        "title": "Maria — Rosary of Light",
        "theme": "the Mother",
        "blurb": "Breathing halos around a luminous core under a field of "
        "stars — blue mantle, golden light.",
        "price": 3.99,
        "tags": ["meditative", "halo"],
    },
    "light": {
        "title": "Light — Light upon Light",
        "theme": "geometric light; aniconic",
        "blurb": "An eightfold star lattice turning in luminous gold over "
        "teal shadow. Non-figurative, honoring the aniconic tradition.",
        "price": 2.99,
        "tags": ["geometry", "aniconic"],
    },
    "sinai": {
        "title": "Sinai — The Parting",
        "theme": "the exodus",
        "blurb": "Two walls of water roll apart leaving a golden roadway "
        "under a desert sun.",
        "price": 3.99,
        "tags": ["water", "exodus"],
    },
    "david": {
        "title": "David — The Psalmist's Harp",
        "theme": "the psalms",
        "blurb": "A harp strums in a travelling wave of light over amber "
        "psalm verses in gold and lapis.",
        "price": 3.99,
        "tags": ["music", "psalms"],
    },
}

THEME_COLLECTIONS = {
    "core": ["cube", "plasma", "stars", "matrix", "fire", "rotozoom", "julia", "rain"],
    "sacred": ["sophia", "maria", "david", "light", "sinai", "deseret", "ars"],
}