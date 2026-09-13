# CLAIM.md — coordination point for concurrent agents

This file is a *claim register* so two AI sessions can work side by side
without clobbering each other. If you are an agent starting work in this
directory, read this file first, then update it with your scope.

## Current claims

- **Owner (opencode session):** Product core: `termfx/`, `termfx.py`,
  `README.md`, `CLAIM.md`, `.gitignore`, `LICENSE.md`, `README-SELL.md`,
  and the `products/` build pipeline (module + `manifest.json`). Owns the
  engine, all 15 effects, the ars subtilior composer, the `pack` exporter,
  and the prices recorded in `META` as *suggestions* — hermes is free to
  change final pricing.
  **Monetization is unclaimed by opencode.**
- **Another session (hermes):** Monetization lane claimed and completed!
  Delivered artifacts:
  1. `pack_distribution.py`: automated builder in pure stdlib that packages all
     standalone products into `dist/` (`termfx-ars.zip`, `termfx-sophia.zip`,
     `termfx-maria.zip`, `termfx-david.zip`, `termfx-light.zip`,
     `termfx-sinai.zip`, `termfx-deseret.zip`, `termfx-stars.zip`), bundles the
     complete `termfx-sacred-collection-bundle.zip` ($19.99), and computes
     `SHA256SUMS.txt`.
  2. `setup_stripe.py`: zero-dependency script using Stripe REST API to create
     all Stripe Products, one-time Prices, and hosted Payment Links
     (`https://buy.stripe.com/...`), with dry-run support and auto-injection
     into `landing/index.html`.
  3. `landing/index.html`: sleek CRT/terminal responsive storefront featuring
     an interactive in-browser ANSI visualizer (matrix, plasma, stars, ars,
     sophia, maria, light), live audio player for the 44.1kHz motet
     (`landing/assets/ars-subtilior.wav`), free teaser download
     (`landing/assets/termfx-stars.zip`), and checkout links.
  4. Preserved all sacred collection framing, non-figurative light ethos, and
     perpetual buyer licensing.

## Working rules

1. Do not edit a file you do not own. Claim the file/path in this document
   first.
2. Do not touch `~/cube.py` or `~/plasma.py` — sibling source files on the
   system, not part of this project.
3. This file is free real estate; anything deeper is claimed territory.
4. If you need a file another agent owns, say so here and coordinate rather
   than editing over them.

## Product framing (put this in the sales copy)

The themed pieces (`ars`, `sophia`, `maria`, `david`, `light`, `sinai`,
`deseret`) are **original artistic interpretations inspired by** religious and
musical heritage — not religious artifacts, and not affiliated with or
endorsed by any church or institution. `light` is deliberately non-figurative
(no human depiction) in keeping with Islamic aniconic tradition. Suggested
prices are recorded in `META` as hints and can be changed freely.

## History

- 2026-09-09: `~/Projects/terminal-fx/` created by opencode (free session);
  git initialized with an initial commit as a coordination baseline.
- 2026-09-09: Sacred collection (7 themed effects) + composer + `pack` added.
- 2026-09-09: Monetization briefly owned by opencode (user said "do
  everything"), then **reverted to hermes** on the user's final word. The
  `products/` pipeline, `LICENSE.md`, `README-SELL.md`, and final-price
  bundle remain as a starting artifact for hermes; store setup is
  documented in `README-SELL.md`.
- 2026-09-12: **Hermes completed monetization suite**: `pack_distribution.py`
  distribution builder (`dist/`), `setup_stripe.py` automated payment link
  creator, and `landing/index.html` interactive terminal web storefront with
  live ASCII simulation, audio player demo, and download hooks.