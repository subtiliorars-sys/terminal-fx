# TermFX — a terminal effects showcase

A zero-dependency, pure-stdlib Python playground of live terminal visuals.
Truecolor when available, 256-color fallback, resizes live on terminal
resize, and never needs `pip install`. Python 3.9+.

Includes two special tools: a **generative isorhythmic composer** that writes
real WAV files (`termfx.py music`) and a **packager** that exports any effect
as a standalone single-file piece (`termfx.py pack <effect>`).

## Quick start

```bash
./termfx.py                 # menu mode: cycles through all effects
./termfx.py maria           # run one effect by name
./termfx.py --list          # list effects and keys
```

Controls (menu mode, in a real terminal):

| Key | Action            |
| --- | ----------------- |
| `n` | jump to next effect |
| `p` | jump to previous effect |
| `q` | quit               |

Flags:

| Flag            | Meaning                                        |
| --------------- | ---------------------------------------------- |
| `--fps N`       | target frame rate (default `30`)               |
| `--seconds S`   | auto-exit after `S` seconds (handy for tests)  |
| `--menu-secs S` | seconds per effect in menu mode (default `7`)  |

Exit anytime with `Ctrl+C`; the terminal is always restored.

## Effects

| Name       | Description                                        |
| ---------- | -------------------------------------------------- |
| `cube`     | spinning 3D wireframe cube, z-buffered depth shading |
| `plasma`   | overlapping sine waves, HSV palette cycling        |
| `stars`    | warp-speed starfield (stars fly toward the viewer) |
| `matrix`   | matrix-style code rain                             |
| `fire`     | rising flame with a hot palette                    |
| `rotozoom` | rotating and zooming sine tunnel                   |
| `julia`    | animated Julia-set fractal                          |
| `rain`     | slanted cyan rain streaks                          |

### The sacred collection

Thematic pieces, each an original artistic interpretation in the spirit of the
tradition it honors:

| Name       | Title / theme                              |
| ---------- | ------------------------------------------ |
| `ars`      | Ars Subtilior — an isorhythmic score       |
| `sophia`   | Aeon mandala of the pleroma (gnostic)      |
| `maria`    | Rosary of light around the Mother          |
| `david`    | The psalmist's harp, psalms in amber       |
| `light`    | Eightfold star lattice — light upon light  |
| `sinai`    | The parting of the sea                     |
| `deseret`  | Honeycomb beehive at dawn                  |

These are artistic works *inspired by* religious heritage, not religious
artifacts, and are not affiliated with or endorsed by any church or
institution. `light` deliberately uses non-figurative geometry and light —
no human depiction — in keeping with the aniconic tradition of Islamic art.

## Generating music (ars subtilior)

```bash
./termfx.py music                         # ~38s piece -> ars-subtilior-<seed>.wav
./termfx.py music --bpm 96 --measures 24  # longer, faster
./termfx.py music --play                  # auto-play if a player is installed
./termfx.py music --out ~/Music/hymn.wav  # explicit path
```

Pure-stdlib synthesis (no numpy/audio deps): a three-voice Dorian motet with
isorhythmic talea/color, hockets, and a low tenor — 16-bit PCM WAV at 44.1 kHz.

## Packaging a standalone piece

```bash
./termfx.py pack maria --out ~/Pieces/maria.py
python3 ~/Pieces/maria.py
```

Exports the effect plus a minimal runtime into one self-contained executable
file (stdlib only) — ready to share or sell as a digital artifact.

## Selling the collection

```bash
./termfx.py products        # build products/packed/ + manifest.json
```

Final prices live in `termfx/effects/META` (mirrored to `manifest.json`).
`README-SELL.md` is the store-setup runbook (Lemon Squeezy, Gumroad, or
itch.io) and the `LICENSE.md` buyer license is written. The only step that
needs a human is creating the payment-processor account — everything else is
ready to upload.

## Adding an effect

1. Create `termfx/effects/<name>.py` exposing
   `render(width, height, t) -> list[str]` where `t` is seconds since start.
   Each string must be exactly `width` characters per row.
2. Register it in `termfx/effects/__init__.py` under `REGISTRY` (and `META`
   for title/theme/pricing hints).
3. It appears in `--list`, the menu cycle, and can be packed.

## Color fallback

`termfx/color.py` writes truecolor escapes when `COLORTERM=truecolor` (or
`24bit`) is set, otherwise it maps each color to the closest 256-color cube
entry so effects degrade gracefully on older terminals.

## Notes

- Pure standard library. No dependencies, no network, no build step.
- Per-effect state persists across frames (stars, drops, flame buffer) so
  animations are smooth and do not regenerate random data each frame.
- Keyboard keys only register when stdin is a real TTY; piped runs behave
  exactly like before.

See `CLAIM.md` for the concurrent-agent coordination file if you are an AI
session working in this repository.