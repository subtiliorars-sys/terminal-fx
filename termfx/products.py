"""Build the ready-to-sell product bundle under ``products/``.

Outputs ``products/packed/`` (one standalone single-file executable per
product, plus a sample composition) and ``products/manifest.json`` — the
catalog a store can be populated from directly.

Run:    python3 termfx.py products
"""

import json
import pathlib
import time

from . import bundle, composer
from .effects import META, REGISTRY

ROOT = pathlib.Path("products")
PACKED = ROOT / "packed"
MANIFEST = ROOT / "manifest.json"

# ids in REGISTRY that are sold as standalone products.
# "stars" is the free teaser — pay-what-you-want or a free lead magnet.
SELL_SET = [
    "ars",
    "sophia",
    "maria",
    "david",
    "light",
    "sinai",
    "deseret",
]

FREE_TEASER = "stars"


def _catalog():
    items = []
    for effect_id in SELL_SET:
        meta = META[effect_id]
        items.append(
            {
                "id": effect_id,
                "title": meta["title"],
                "theme": meta["theme"],
                "blurb": meta["blurb"],
                "price": meta["price"],
                "file": f"packed/{effect_id}.py",
                "free": False,
                "tags": meta["tags"],
            }
        )
    teaser = META.get(FREE_TEASER) or {
        "title": "Starfield — a free teaser",
        "theme": "space",
        "blurb": "The warp-speed starfield, free: a taste of the collection.",
        "tags": ["free", "space"],
    }
    items.append(
        {
            "id": FREE_TEASER,
            "title": teaser["title"],
            "theme": teaser["theme"],
            "blurb": teaser["blurb"],
            "price": 0,
            "file": f"packed/{FREE_TEASER}.py",
            "free": True,
            "tags": teaser["tags"],
        }
    )
    items.append(
        {
            "id": "ars-music-demo",
            "title": "Ars Subtilior — demo motet (audio)",
            "theme": "medieval music",
            "blurb": "A ~40s isorhythmic motet generated with the ars "
            "composer; bundled bonus for the Ars Subtilior product.",
            "price": 0,
            "file": "packed/ars-subtilior.wav",
            "free": True,
            "upload_as_extra": "ars",
            "tags": ["music", "audio"],
        }
    )
    return items


def build(seed=None):
    items = _catalog()
    PACKED.mkdir(parents=True, exist_ok=True)
    for item in items:
        target = PACKED / item["id"]
        file_path = PACKED / pathlib.Path(item["file"]).name
        if item["id"] == "ars-music-demo":
            events, total_units, unit = composer.compose(
                measures=16, bpm=88, seed=seed
            )
            samples = composer.synthesize(events, total_units, unit)
            composer.write_wav(str(file_path), samples)
        elif item["id"] == FREE_TEASER or item["id"] in REGISTRY:
            src = bundle.standalone_source(item["id"])
            file_path.write_text(src)
            file_path.chmod(0o755)
        item["bytes"] = file_path.stat().st_size

    manifest = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "license": "See LICENSE.md. One-time purchase; run for personal or "
        "commercial use; do not redistribute the standalones.",
        "items": items,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    total = sum(i["bytes"] for i in items)
    print(f"products ready in {ROOT}/  ({len(items)} items, {total} bytes)")
    print(f"catalog -> {MANIFEST}")
    return 0


def main(seed=None):
    return build(seed=seed)