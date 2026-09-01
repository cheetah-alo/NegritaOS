---
id: brain
mode_hint: LP
loads:
  - .codex/project.yaml
  - .codex/skills/local-memory-protocol/SKILL.md
---

# Negrita Brain

Route `/brain <operation>` to the canonical CLI. The provider is `codex` in
Codex and `claude` in Claude.

## Operations

- `/brain status`: run `negrita_brain.py memory status` and report project,
  active contract, durable paths, counts, and warnings.
- `/brain remember`: collect type, title, summary, learned, tags, and files;
  invoke `memory remember` once.
- `/brain handoff`: synthesize the persistent handoff contract and invoke
  `memory handoff` once; return its `durable_ref`.
- `/brain doctor`: run `negrita_brain.py doctor --root "$PWD"` and distinguish
  FAIL, WARN, permission, legacy-index, and open-session conditions.
- `/brain migrate`: run `memory migrate --dry-run` unless the user explicitly
  requests `--apply`.
- `/brain legacy-sessions`: list Memory v1 session IDs and closure state without
  reading narrative content.
- `/brain authorize-legacy-close`: require the user to name the exact v1
  session, authorized-by value, and reason; create a backup before closing it.
- `/brain model-route`: resolve the task with `--delegation-class`, repeated
  `--risk-signal`, `--change-impact`, and `--review-role` as applicable; report
  tier, model, reasoning effort, reasons, and independent-review requirements.
  An independent PASS must close with `--status PASS` and one SHA-256-bound JSON
  receipt using
  `--evidence-ref category=(repo|memory):path@sha256:<64_hex>` per required
  category. Before commit, `gate --action commit` must revalidate every receipt
  and return the matching review session and current worktree fingerprint.

Never write canonical memory directly. A permission failure requires elevation
or `configure codex --apply`, followed by a new Codex task.
