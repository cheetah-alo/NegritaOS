# Local Codex Adapter: negritaos (meta-repo)

This `.codex/` directory is a repo-local adapter for the NegritaOS meta-repository.
It is **not** the canonical memory store, but it **is** version-controlled here
(unlike sibling project adapters) because this repo is the source of truth for
the NegritaOS contract itself.

- Canonical memory: `~/.negritaos/memory/projects/negritaos`
- NegritaOS registry: `projects/negritaos.yaml`
- Preservation backup: `~/.negritaos/backups/2026-06-01_alignment`

## Repository path baseline (overrides `.codex/system.md`)

The `Repository Path Baseline` section of [.codex/system.md](system.md) lists
paths inherited from a churn-style sibling repo (`backend/app/`,
`frontend/src/`, `mcp_server/`, `data_analytics/`). Those paths do not exist
here. For the NegritaOS meta-repo, use:

- Core contracts: `core/`
- Agents (cognitive): `academic-layer/`, `intelligence-layer/`,
  `strategic-layer/`, `technical-layr/`, `business-layer/`
- Master registry: `integrator.yaml`
- Shared rules: `rules/`
- Shared skills: `skills/`
- Rubrics: `rubrics/`
- Templates: `templates/`
- Project registry: `projects/`
- Archetypes: `archetypes/`
- Operational scripts: `scripts/`
- Working notes / scratch: `zsmash/`
- Agent client adapters: `.codex/`, `.claude/` (the latter must be a
  symlink to `.codex/` once Phase B4 is executed).

## Rules

- Do not copy a full `.codex` from another project into this repo without
  going through the federation review.
- Do not store durable private memory inside `.codex/memory/`; write to
  `~/.negritaos/memory/projects/negritaos/`.
- Update project memory at session close. Use the `memory-protocol` skill.
- Engineering rules under `.codex/rules/dev-*.md` apply only to **MR / CR /
  DQ** modes per [rules/global/negritaos_router_rule.md](../rules/global/negritaos_router_rule.md).
- The `.claude/` folder must remain a symlink to `.codex/` once Phase B4 is
  executed; do not edit it as a separate copy.
