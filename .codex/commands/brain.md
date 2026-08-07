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

Never write canonical memory directly. A permission failure requires elevation
or `configure codex --apply`, followed by a new Codex task.
