# Agent entry point — <PROJECT_NAME>

This repo is governed by **NegritaOS**.

## Session start (mandatory, run in order)
1. Read `.codex/project.yaml` → confirm `project_id` and `memory_home`.
2. Load `.codex/rules/negritaos-router.md` (stub). It redirects to the canonical
   router rule at:
   - `rules/global/negritaos_router_rule.md` (if NegritaOS is vendored in this repo), OR
   - `~/.negritaos/rules/global/negritaos_router_rule.md` (global install).
3. Run the `negritaos-mode-router` skill:
   `.codex/skills/negritaos-mode-router/SKILL.md`
4. Then load the rules listed in `.codex/instruction-manifest.yaml` in order.

## Memory
- Project memory home: see `memory_home` in `.codex/project.yaml`
  (canonical: `~/.negritaos/memory/projects/<project_id>/`).
- Do NOT write session logs into `.codex/memory/` — that path is adapter scratch
  only and is gitignored.

## Local overrides
- See `.codex/local-overrides.md` for repo-specific paths and lexicon. These
  override anything in `.codex/system.md` that came from a sibling-repo baseline.

## Project metadata
- Project ID: `<PROJECT_ID>`
- Archetype: `<archetype-name from /archetypes/>` (e.g. `data-platform`, `eda-analytics`, `ml-automl`, `product-app`)
- Primary stack: `<python|node|mixed>`
- Brand: `<cqi|moneyflow|viu|none>`

## Operational modes most used in this repo
- `<mode-code>` — `<short reason>`
- `<mode-code>` — `<short reason>`
