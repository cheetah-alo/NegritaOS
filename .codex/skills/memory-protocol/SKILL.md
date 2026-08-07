---
name: local-memory-protocol
description: >
  Canonical project memory discipline through Negrita Brain.
  Trigger: Recall requests, durable discoveries, decisions, bugfixes,
  preferences, session handoff, or recovery after compaction.
license: Apache-2.0
metadata:
  author: negritaos
  version: "3.0"
---

## Authority

Negrita Brain is the only project-memory writer. Canonical project memory remains
under `~/.negritaos/memory/projects/<project_id>/`; it is not copied into the
repository or `~/.codex/memories/`.

Never write `index.md`, `sessions/`, `observations.jsonl`, `decisions/`, or
`tasks/` directly. Use `scripts/negrita_brain.py memory ...`.

## Durable And Runtime Planes

- Durable: `index.md`, `sessions/`, `observations.jsonl`, `decisions/`, `tasks/`.
- Runtime metadata: `runtime/sessions/` and provider-scoped pointers under
  `runtime/active/`.
- Legacy: preserved and cataloged; never moved, renamed, or rewritten implicitly.

Runtime closure is not a handoff. `close` records technical state only and never
regenerates the durable index.

## Read And Recall

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  memory status --root "$PWD" --provider codex
```

Then read the canonical `index.md`, the latest relevant file under `sessions/`,
and search `observations.jsonl`, `decisions/`, and `tasks/` by task keywords.

## Persist By Relevance

Use `memory remember` only for reusable facts: architecture, bug causes,
constraints, decisions, preferences, discoveries, or governance changes.

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  memory remember --root "$PWD" --provider codex \
  --type discovery --title "..." --summary "..." --learned "..." \
  --tag "..." --file "path/to/file"
```

Use `memory handoff` when another task or agent must continue. Include goal,
discoveries, accomplished work, decisions, blockers, ordered next steps, and
relevant files. Pass the returned `durable_ref` to `close`.

Do not persist ordinary exploration, raw chat, prompts, responses, tool output,
file contents, secrets, or duplicated summaries.

## Permission Failure

`PERMISSION_REQUIRED` / `MEMORY_WRITE_PERMISSION` means the canonical path is
valid but the provider sandbox cannot write it. Retry with elevated permission
or run `configure codex --apply` and start a new Codex task. Never relabel this
condition as configuration-resolution failure.
