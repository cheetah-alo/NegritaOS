---
name: cqisense-design
description: Use this skill to generate well-branded interfaces, slides and assets for CQISense. Contains essential design guidelines, colors, type (Poppins / Noto Sans / IBM Plex Mono), fonts, domain tokens, assets, and reusable presentation patterns. Use for production or throwaway prototypes/mocks/presentations.
user-invocable: true
---

Read the `readme.md` file within this skill to understand the brand, product, domain model, and visual system.

Key files to explore first:
- `readme.md` — brand context, content rules, visual foundations, domain model
- `styles.css` — global entry point; `@import` this to get all tokens and fonts
- `tokens/domain.css` — the CQISense-specific semantic tokens (Repair, Risk, Archetypes, etc.)
- `templates/hot-orange-deck/HotOrangeDeck.dc.html` — 10-slide ADHD-friendly presentation of the Hot Orange model

If creating **visual artifacts** (slides, mocks, throwaway prototypes, etc.):
- Copy `styles.css` and the `tokens/` folder (or link them relatively) so all CSS custom properties are available.
- Copy `assets/cqisense-mark.svg` and `assets/cqisense-logo.svg` for the logo.
- The cobalt brand (`#1A43F5`) + cool gray palette, Poppins headings, Noto Sans body text, and IBM Plex Mono for all numbers are non-negotiable.
- Follow the Reading Rule: Brand/UI = cobalt (`--brand`), Repair = teal (`--repair`), Risk = pink (`--risk`), Operational = green (`--operational`), priority/heat = `--heat` (used sparingly, never as a surface).
- For slides: one idea per slide, finding first, visible evidence, readable typography, and minimal body text.
- For components: reference the primitives in `components/core/` and `components/domain/` — never re-implement Button or ArchetypeBadge.

If working on **production code**:
- `styles.css` is the single consumer entry point — link it and use the CSS custom properties.
- The compiled bundle `_ds_bundle.js` exposes all components under `window.CQISenseDesignSystem_73301e`.
- The domain model (archetypes A–F + D2, mechanisms, rules R1–R9, scores) is documented in `readme.md` and encoded in `tokens/domain.css` and `components/domain/`.
- All metrics must use `font-family: var(--font-mono)` + `font-variant-numeric: tabular-nums`.

If the user invokes this skill without other guidance, ask what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts OR production code, depending on the need.
