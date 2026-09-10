# CLAIM.md — coordination point for concurrent agents

This file is a *claim register* so two AI sessions can work side by side
without clobbering each other. If you are an agent starting work in this
directory, read this file first, then update it with your scope.

## Current claims

- **Owner (opencode session, Sep 9 2026):** Everything, including
  monetization. Per an explicit user instruction ("do everything for me"),
  the earlier plan to reserve monetization for the hermes session is
  **superseded**. Scope: `termfx/`, `termfx.py`, `README*`, `LICENSE.md`,
  `CLAIM.md`, `.gitignore`, `products/` (build pipeline + manifest + license
  docs). Owns the engine, all 15 effects, the ars subtilior composer, the
  `pack` exporter, final pricing in `META`/`manifest.json`, and the
  ready-to-upload product bundle under `products/packed/`.
- **Other sessions (hermes et al.):** Please do **not** take ownership of
  monetization rails here (store, pricing, licenses, product bundle) without
  coordinating in this file — it is now claimed. Help with code/effects is
  welcome and should also be claimed here first.

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
- 2026-09-09: Monetization owned by this session (user override): `products/`
  pipeline, `LICENSE.md`, `README-SELL.md`, final prices, product bundle.
  The human-only step (creating a payment-processor account) is documented
  in `README-SELL.md`.