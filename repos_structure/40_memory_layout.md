# 40 — Memory layout per project

## Canonical layout (under `$HOME`)

```
~/.negritaos/
├── rules/global/                  ← shared router rule (optional symlink)
├── backups/<YYYY-MM-DD_label>/    ← preservation tarballs
└── memory/
    └── projects/
        ├── negritaos/
        │   ├── index.md
        │   ├── sessions/
        │   │   └── YYYY-MM-DD-<slug>.md
        │   ├── decisions/         ← ADR-style files (optional)
        │   ├── learnings/         ← cross-session learnings (optional)
        │   └── ontology/          ← domain terms (optional)
        ├── moneyflowlist/
        │   └── sessions/...
        └── <project_id>/
            └── sessions/...
```

## Per project_id — minimum files

- `index.md` — pinned summary + open threads + pointer to latest session
- `sessions/YYYY-MM-DD-<slug>.md` — one file per work session

## Repo-local `.codex/memory/`
- Reserved as **adapter scratch only**.
- Must be `.gitignore`d.
- MUST NOT contain sessions for other projects (validator enforces this).

## Write rules (enforced by `negritaos-mode-router` Step 7)
- Sessions always write to `<memory_home>/sessions/`.
- Cross-cutting learnings → `<memory_home>/learnings/<topic>.md`.
- Decisions → `<memory_home>/decisions/YYYY-MM-DD-<slug>.md`.
- Never write personal data, secrets, or raw datasets to memory.
