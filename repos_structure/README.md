# `repos_structure/` — NegritaOS repo baseline

Reference template for **what every NegritaOS-managed repo must contain** so that
Claude Code, Codex CLI, and VS Code Copilot all load the same governance,
memory, and routing rules.

Updated iteratively. Source of truth for the bootstrap script
`scripts/bootstrap_negritaos_repo.sh` (TBD).

---

## TL;DR — minimum set

```
<repo>/
├── AGENTS.md                 ← entry pointer (both clients read it)
├── .codex/                   ← single source of truth
│   ├── system.md
│   ├── instruction-manifest.yaml
│   ├── project.yaml
│   ├── local-overrides.md
│   ├── rules/
│   │   ├── negritaos-router.md           (stub → canonical)
│   │   └── ...adapter rules
│   └── skills/
│       └── negritaos-mode-router/SKILL.md
├── .claude  → .codex          ← symlink, NOT a folder
└── scripts/validate_alignment.py
```

Per-file templates and explanations live in this folder:

| File | Purpose |
|---|---|
| [00_overview.md](00_overview.md) | High-level model: federation, modes, why these files |
| [10_AGENTS.md.template](10_AGENTS.md.template) | Drop-in for repo-root `AGENTS.md` |
| [20_codex_project.yaml.template](20_codex_project.yaml.template) | `.codex/project.yaml` |
| [21_codex_local-overrides.md.template](21_codex_local-overrides.md.template) | `.codex/local-overrides.md` |
| [22_codex_instruction-manifest.yaml.template](22_codex_instruction-manifest.yaml.template) | `.codex/instruction-manifest.yaml` |
| [23_codex_rules_negritaos-router.md.template](23_codex_rules_negritaos-router.md.template) | `.codex/rules/negritaos-router.md` stub |
| [24_codex_skills_negritaos-mode-router_SKILL.md.template](24_codex_skills_negritaos-mode-router_SKILL.md.template) | Mode-router skill |
| [30_canonical_router_rule.md.reference](30_canonical_router_rule.md.reference) | The canonical rule (lives in NegritaOS or `~/.negritaos/rules/global/`) |
| [40_memory_layout.md](40_memory_layout.md) | Where memory goes per project |
| [50_bootstrap_checklist.md](50_bootstrap_checklist.md) | Per-repo bootstrap steps |
| [60_validation.md](60_validation.md) | What the validator checks; how to extend |
| [70_client_loading.md](70_client_loading.md) | How Claude / Codex / Copilot discover these files |
| [99_changelog.md](99_changelog.md) | Iterative updates to this baseline |
