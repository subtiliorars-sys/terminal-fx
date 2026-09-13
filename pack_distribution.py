#!/usr/bin/env python3
"""Build distribution archives for TermFX digital products.

Creates individual zip packages and a full Sacred Collection bundle in dist/
ready for upload to Gumroad, itch.io, Lemon Squeezy, or direct delivery.
"""

import json
import os
import shutil
import zipfile
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_DIR = BASE_DIR / "products"
PACKED_DIR = PRODUCTS_DIR / "packed"
DIST_DIR = BASE_DIR / "dist"
MANIFEST_FILE = PRODUCTS_DIR / "manifest.json"
LICENSE_FILE = BASE_DIR / "LICENSE.md"

README_TEMPLATE = """========================================================================
TermFX: {title}
========================================================================

Theme: {theme}
Summary: {blurb}

REQUIREMENTS:
- Python 3.9 or higher (standard library only - zero dependencies to install!)
- Any modern terminal emulator (supporting ANSI colors / 256 colors / truecolor)
- Works on Linux, macOS, and Windows (WSL, Windows Terminal, PowerShell)

HOW TO RUN:
1. Open your terminal.
2. Run with Python:
     python3 {filename}

CONTROLS:
- Ctrl+C or 'q' to exit.
- Terminal automatically restores cleanly upon exit.
- Resizes dynamically when you adjust your terminal window.

ARTISTIC BACKGROUND:
{artistic_note}

LICENSE & USAGE:
Please see LICENSE.md included in this package.
Original work by subtiliorars / OmniTender Systems.
Thank you for supporting independent digital craft!
========================================================================
"""

SACRED_BUNDLE_README = """========================================================================
TermFX: The Sacred Collection — Complete Digital Edition
========================================================================

Thank you for purchasing the complete TermFX Sacred Collection.

This bundle contains all seven thematic visual meditations inspired by sacred
geometry, musical heritage, and historical texts, plus the generative Ars
Subtilior musical motet (audio + code) and the bonus Starfield visualizer.

INCLUDED PIECES:
1. ars.py        — Ars Subtilior: isorhythmic scrolling score
2. sophia.py     — Sophia: rotating aeon mandala of the pleroma
3. maria.py      — Maria: rosary of light around the Mother
4. david.py      — David: travelling wave psalmist's harp in amber & lapis
5. light.py      — Light: eightfold star lattice (non-figurative aniconic geometry)
6. sinai.py      — Sinai: golden roadway between parted waves
7. deseret.py    — Deseret: honeycomb beehive glowing at sunrise
8. stars.py      — Starfield: warp-speed particle horizon (bonus)
9. ars-subtilior.wav — 44.1kHz 16-bit PCM master of generative isorhythmic motet

REQUIREMENTS:
- Python 3.9 or newer (standard library only — NO external pip dependencies)
- Any terminal emulator with ANSI/truecolor support

HOW TO RUN:
Simply run any piece directly with Python 3:
    python3 ars.py
    python3 maria.py
    python3 light.py

CONTROLS:
- Press Ctrl+C or 'q' to cleanly stop any effect and restore terminal screen.
- Window resize is handled dynamically in real time.

ARTISTIC FRAMING:
The themed pieces (ars, sophia, maria, david, light, sinai, deseret) are
original artistic interpretations inspired by centuries of religious and musical
heritage — not religious artifacts, and not affiliated with or endorsed by any
church or institution. 'light' is deliberately non-figurative in keeping with
the aniconic tradition of Islamic art.

LICENSE:
See LICENSE.md included in this directory.
Created by subtiliorars / OmniTender Systems.
========================================================================
"""

def get_artistic_note(item_id: str) -> str:
    notes = {
        "ars": "Ars Subtilior ('The Subtle Art') honors the intricate polyphony and complex notation of late 14th-century southern France and northern Italy. Features an isorhythmic scrolling visual score.",
        "sophia": "Sophia ('Aeons of Light') draws upon ancient gnostic meditative geometry, depicting concentric spheres of light pulsing across the celestial pleroma.",
        "maria": "Maria ('Rosary of Light') weaves a sapphire-and-gold halo field around a luminous center, inspired by timeless Marian iconography.",
        "david": "David ('The Psalmist's Harp') visualizes harmonic strings rippling across amber psalm verses in gold and deep lapis lazuli.",
        "light": "Light ('Light upon Light') is an eightfold star geometric lattice in luminous gold over deep teal shadow. Non-figurative, honoring the Islamic aniconic tradition.",
        "sinai": "Sinai ('The Parting') evokes the dramatic biblical crossing, parting radiant waves along a glowing desert highway under dawn skies.",
        "deseret": "Deseret ('Hive at Dawn') draws from the industrious pioneer beehive motif, rendering golden hexagonal lattices that pulse with sunrise warmth.",
        "stars": "A high-speed particle simulation testing terminal throughput with 3D projection."
    }
    return notes.get(item_id, "An original terminal art piece.")

def build_dist():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    with open(LICENSE_FILE, "r", encoding="utf-8") as f:
        license_text = f.read()

    print(f"Building packages in {DIST_DIR}...")
    manifest_items = manifest.get("items", [])
    built_packages = []

    # 1. Build individual product archives
    for item in manifest_items:
        item_id = item["id"]
        rel_file = item["file"]
        src_path = PRODUCTS_DIR / rel_file

        # Skip extra audio if it's already an upload_as_extra
        if item.get("upload_as_extra"):
            continue

        if not src_path.exists():
            print(f"WARNING: Source file missing: {src_path}")
            continue

        zip_name = f"termfx-{item_id}.zip"
        zip_path = DIST_DIR / zip_name

        readme_content = README_TEMPLATE.format(
            title=item["title"],
            theme=item.get("theme", ""),
            blurb=item.get("blurb", ""),
            filename=src_path.name,
            artistic_note=get_artistic_note(item_id),
        )

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(src_path, arcname=src_path.name)
            zf.writestr("README.txt", readme_content)
            zf.writestr("LICENSE.md", license_text)

            # If this is 'ars', bundle the bonus audio file
            if item_id == "ars":
                wav_path = PACKED_DIR / "ars-subtilior.wav"
                if wav_path.exists():
                    zf.write(wav_path, arcname="ars-subtilior.wav")

        size_kb = zip_path.stat().st_size / 1024
        print(f"  -> Created {zip_name} ({size_kb:.1f} KB)")
        built_packages.append((zip_name, zip_path))

    # 2. Build complete Sacred Collection Bundle
    bundle_name = "termfx-sacred-collection-bundle.zip"
    bundle_path = DIST_DIR / bundle_name

    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.txt", SACRED_BUNDLE_README)
        zf.writestr("LICENSE.md", license_text)

        # Include all packed python scripts & wav
        for py_file in PACKED_DIR.glob("*.py"):
            zf.write(py_file, arcname=py_file.name)
        for wav_file in PACKED_DIR.glob("*.wav"):
            zf.write(wav_file, arcname=wav_file.name)

    bundle_size_mb = bundle_path.stat().st_size / (1024 * 1024)
    print(f"  -> Created {bundle_name} ({bundle_size_mb:.2f} MB)")
    built_packages.append((bundle_name, bundle_path))

    # 3. Generate SHA256 checksums
    checksum_file = DIST_DIR / "SHA256SUMS.txt"
    with open(checksum_file, "w", encoding="utf-8") as cs_out:
        for fname, fpath in built_packages:
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            cs_out.write(f"{sha}  {fname}\n")
    print(f"Wrote checksums to {checksum_file.name}")
    print("Done!")

if __name__ == "__main__":
    build_dist()
