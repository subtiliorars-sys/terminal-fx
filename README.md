# TermFX — a terminal effects showcase

A zero-dependency, pure-stdlib Python playground of live terminal visuals.
Truecolor when available, 256-color fallback, resizes live on terminal
resize, and never needs `pip install`. Python 3.9+.

## Quick start

```bash
./termfx.py                 # menu mode: cycles through all effects
./termfx.py plasma          # run one effect by name
./termfx.py --list          # list available effects
```

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

Everything runs on `os.get_terminal_size()`; an 80x24 fallback is used when
no TTY is present. Resizing the window re-fits the effect on the next frame.

## Adding an effect

1. Create `termfx/effects/<name>.py` exposing
   `render(width, height, t) -> list[str]` where `t` is seconds since start.
   Each string must be exactly `width` characters per row.
2. Register it in `termfx/effects/__init__.py` under `REGISTRY` with a short
   description.
3. It appears in `--list` and the menu cycle automatically.

## Color fallback

`termfx/color.py` writes truecolor escapes when `COLORTERM=truecolor` (or
`24bit`) is set, otherwise it maps each color to the closest 256-color cube
entry so effects degrade gracefully on older terminals.

## Notes

- Pure standard library. No dependencies, no network, no build step.
- Per-effect state persists across frames (stars, drops, flame buffer) so
  animations are smooth and do not regenerate random data each frame.

See `CLAIM.md` for the concurrent-agent coordination file if you are an AI
session working in this repository.