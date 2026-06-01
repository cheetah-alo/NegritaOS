# `.codex` / `.claude` Alignment with NegritaOS — 2026-06-01

Status: **9/9 validator checks passing**. `.claude/` is now a symlink to `.codex/`.
Backup: `~/.negritaos/backups/2026-06-01_alignment/` (`codex.tgz`, `claude.tgz`,
`negritaos-memory.tgz`).

---

## 1. Problem we found

The repo carried **two near-duplicate agent-client stacks** (`.codex/`, `.claude/`)
inherited from a churn ML sibling repo. Neither was wired to the **NegritaOS metaagent
router** declared at `integrator.yaml`, so:

- Engineering rules (logging / error-handling / naming / data-contracts) were applied
  generically, bypassing NegritaOS mode routing (LP/AE/TD/MR/CR/EP/DQ/RT).
- Memory writes were ambiguous: the canonical memory home defined by
  `core/memory/memory_architecture.yaml` (`~/.negritaos/memory/projects/<id>/`) was
  empty, while `.codex/memory/sessions/` held an **orphan session for another
  project** (moneyflowlist UX-TRUST-001).
- `.codex/system.md` referenced churn-repo paths (`backend/app/`, `data_analytics/`,
  `mcp_server/`) that don't exist in NegritaOS.
- `.codex` drifted from `.claude` (4 extra rules, 3 different files). Any client
  switch silently changed agent behavior.
- No automated check existed for any of the above.

Reference diagnosis already in repo: `zsmash/revision_de_claude.md` (federation
principle: AE/RT/EP/LP/TD stay pure; MR/CR/DQ activate `.codex/core/` rules).

---

## 2. What changed (phase by phase)

### Phase A — Backup
- A1 — Tarballed `.codex/`, `.claude/`, and `~/.negritaos/memory/projects/negritaos/`
  to `~/.negritaos/backups/2026-06-01_alignment/`.

### Phase B — Single source of truth for client config
- B1–B3 — Copied `.claude/`-only assets (`prompts/`, `worktrees/`) into `.codex/`
  so `.codex/` became the superset.
- **B4 — Replaced `.claude/` with a relative symlink to `.codex/`** after explicit
  user confirmation (option A). Backup preserved.

### Phase C — Router rule + skill
- C1 — Created canonical [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md):
  8-mode table (LP/AE/TD/MR/CR/EP/DQ/RT), binding to `integrator.yaml`, output
  contracts, federation rules, conflict-resolution order
  (`priority: critical`, `enforcement: strict`).
- C1b — Adapter stub at [.codex/rules/negritaos-router.md](.codex/rules/negritaos-router.md)
  pointing to the canonical file.
- C2 — Skill [.codex/skills/negritaos-mode-router/SKILL.md](.codex/skills/negritaos-mode-router/SKILL.md):
  7-step session-entry procedure (detect project → classify mode → load agent
  block → merge adapter rules → enforce output contract → quality gate → memory
  hooks).
- C3 — Updated [.codex/instruction-manifest.yaml](.codex/instruction-manifest.yaml):
  `negritaos-router` is now the **first** rule loaded; `ai-behavior` depends on it.
- C4 — Added `depends_on: [negritaos-router]` and `see_also:` cross-references to
  `rules/global/global_rules.yaml` and the router rule in:
  - [.codex/rules/dev-logging.md](.codex/rules/dev-logging.md) (v1.0.2 → v1.0.3)
  - [.codex/rules/dev-error-handling.md](.codex/rules/dev-error-handling.md)
  - [.codex/rules/dev-naming-conventions.md](.codex/rules/dev-naming-conventions.md) (v1.0.2 → v1.0.3)

  Descriptions now state these rules load only for engineering modes MR/CR/DQ.

### Phase D — Project adapter + memory hygiene
- D1 — [.codex/project.yaml](.codex/project.yaml):
  `project_id: negritaos`,
  `memory_home: ~/.negritaos/memory/projects/negritaos`,
  references router rule + skill.
- D2 — [.codex/local-overrides.md](.codex/local-overrides.md): overrides the
  churn-path baseline in `.codex/system.md`; lists actual NegritaOS paths
  (`core/`, `business-layer/`, `intelligence-layer/`, `academic-layer/`,
  `strategic-layer/`, `technical-layr/`, `rules/`, `skills/`, `templates/`,
  `agents/`, `archetypes/`, `projects/`, `rubrics/`, `brands/`).
- D3 — Moved orphan moneyflowlist session out of `.codex/memory/sessions/` to
  `~/.negritaos/memory/projects/moneyflowlist/sessions/2026-05-08-session.md`.
- D4 — Seeded `~/.negritaos/memory/projects/negritaos/sessions/2026-06-01-codex-claude-alignment.md`.
- D5 — Updated `~/.negritaos/memory/projects/negritaos/index.md` with latest
  session + open threads.
- D6 — [scripts/validate_alignment.py](scripts/validate_alignment.py): 9 checks,
  exit 0/1, CI-ready.

### Phase E — Documentation
- E1 — This file.

---

## 3. Final state — validator

```
$ python3 scripts/validate_alignment.py
[OK]   .claude -> .codex symlink in place
[OK]   .codex/project.yaml -> projects/negritaos.yaml
[OK]   .codex/local-overrides.md present
[OK]   negritaos-router registered in instruction-manifest.yaml
[OK]   rules/global/negritaos_router_rule.md present
[OK]   .codex/rules/negritaos-router.md adapter stub present
[OK]   .codex/skills/negritaos-mode-router/SKILL.md present
[OK]   .codex/memory/sessions/ contains no orphan sibling-repo sessions
[OK]   memory_home present: /Users/jackyb-cqi/.negritaos/memory/projects/negritaos

9/9 checks passed.
```

---

## 4. What changed and why — matrix

| Change | Why | File |
|---|---|---|
| Canonical router rule | Bind `integrator.yaml` to every session | [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md) |
| Adapter stub | Allow `.codex` clients to load the canonical rule via manifest | [.codex/rules/negritaos-router.md](.codex/rules/negritaos-router.md) |
| Mode-router skill | Make 7-step procedure invokable per session | [.codex/skills/negritaos-mode-router/SKILL.md](.codex/skills/negritaos-mode-router/SKILL.md) |
| Manifest first-load | Force router before any other rule | [.codex/instruction-manifest.yaml](.codex/instruction-manifest.yaml) |
| `depends_on: negritaos-router` in dev-* | Engineering rules defer to NegritaOS governance | [.codex/rules/dev-logging.md](.codex/rules/dev-logging.md), [.codex/rules/dev-error-handling.md](.codex/rules/dev-error-handling.md), [.codex/rules/dev-naming-conventions.md](.codex/rules/dev-naming-conventions.md) |
| `project.yaml` | Identifies the project to the client + pins memory home | [.codex/project.yaml](.codex/project.yaml) |
| `local-overrides.md` | Neutralizes churn-path baseline from `.codex/system.md` | [.codex/local-overrides.md](.codex/local-overrides.md) |
| Symlink `.claude -> .codex` | Eliminate drift between two clients | `.claude` |
| Move moneyflowlist session | Repo memory must contain only this project's sessions | `~/.negritaos/memory/projects/moneyflowlist/sessions/2026-05-08-session.md` |
| Seed NegritaOS session + update index | Canonical memory home was empty | `~/.negritaos/memory/projects/negritaos/{sessions/,index.md}` |
| Validator | Detect regression of any of the above | [scripts/validate_alignment.py](scripts/validate_alignment.py) |

---

## 5. Reproduce locally

```bash
# from repo root
python3 scripts/validate_alignment.py    # expect 9/9

# verify .claude is the symlink
ls -la .claude                            # -> .codex

# inspect canonical router rule
sed -n '1,40p' rules/global/negritaos_router_rule.md

# inspect adapter stub
cat .codex/rules/negritaos-router.md

# project identity + memory home
cat .codex/project.yaml

# canonical memory home
ls ~/.negritaos/memory/projects/negritaos/sessions/
```

To restore from backup if needed:

```bash
cd ~/.negritaos/backups/2026-06-01_alignment/
# tarballs: codex.tgz, claude.tgz, negritaos-memory.tgz
```

---

## 6. Federation contract (re-stated for posterity)

Per [zsmash/revision_de_claude.md](zsmash/revision_de_claude.md) and the new
router rule:

- **Pure NegritaOS modes** (LP, AE, TD, EP, RT) → rely only on
  `rules/global/`, `rules/<mode>/`, `skills/<scope>/`. They do **not** load
  `.codex/rules/dev-*`.
- **Engineering modes** (MR, CR, DQ) → first load NegritaOS rules, then
  activate `.codex/rules/dev-*` and `.codex/skills/engineering/` as supporting
  craft layer. The router rule is `depends_on` for all of them, so NegritaOS
  rules always win on conflict.

Conflict resolution order (router rule §Conflict Resolution):
1. `rules/global/` (NegritaOS canonical)
2. `rules/<mode>/`
3. `.codex/rules/negritaos-router.md` (adapter)
4. `.codex/rules/*` (craft adapters)
5. `.codex/local-overrides.md`

---

## 7. Follow-ups (open)

- Wire `scripts/validate_alignment.py` into a pre-commit hook or CI job.
- Add equivalent `depends_on: negritaos-router` to remaining
  `.codex/rules/dev-*.md`, `ml-*.md`, and `data-*.md` files (only the 3
  highest-traffic ones were updated today).
- Document `core/memory/memory_architecture.yaml` write-paths in the
  `negritaos-mode-router` skill (currently only references them).
- Confirm Claude Desktop client follows the `.claude -> .codex` symlink on
  this machine. If it does not, switch to the rsync alternative (option B)
  via a `scripts/sync_claude_from_codex.sh` script.
- Decide whether `.codex/memory/` should remain `.gitignore`d (currently yes
  for sessions; only structural files tracked).

---

## 8. Session record

- Canonical session log: `~/.negritaos/memory/projects/negritaos/sessions/2026-06-01-codex-claude-alignment.md`
- Project index updated: `~/.negritaos/memory/projects/negritaos/index.md`
- Backup: `~/.negritaos/backups/2026-06-01_alignment/`
