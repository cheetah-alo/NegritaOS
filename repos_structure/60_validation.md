# 60 — Validation

The validator lives at `scripts/validate_alignment.py` and exits 0 on success,
1 on failure. CI-ready.

## Checks performed (9 total)

1. `.claude` is a symlink to `.codex` (no drift).
2. `.codex/project.yaml` exists and references a known project in `projects/`.
3. `.codex/local-overrides.md` exists.
4. `negritaos-router` is the first rule in `.codex/instruction-manifest.yaml`.
5. Canonical router rule exists at `rules/global/negritaos_router_rule.md`
   (or at the global path declared in `project.yaml`).
6. Adapter stub exists at `.codex/rules/negritaos-router.md`.
7. Skill exists at `.codex/skills/negritaos-mode-router/SKILL.md`.
8. `.codex/memory/sessions/` contains no orphan sibling-repo sessions.
9. Memory home declared in `project.yaml` exists on disk.

## How to extend
- Add a new check function `check_<name>() -> tuple[bool, str]`.
- Append it to the `CHECKS` list.
- Keep each check side-effect-free and fast (< 100 ms).

## CI integration (suggested)
```yaml
# .github/workflows/negritaos-alignment.yml
name: negritaos-alignment
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/validate_alignment.py
```

## Pre-commit hook (suggested)
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: negritaos-alignment
      name: NegritaOS alignment
      entry: python3 scripts/validate_alignment.py
      language: system
      pass_filenames: false
```
