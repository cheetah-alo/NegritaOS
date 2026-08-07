# Negrita Brain Runtime And Memory v2

## Purpose

Negrita Brain resolves and enforces:

```text
project -> mode -> agent -> rules -> profiles -> skills
        -> artifact route -> quality gates -> runtime -> durable memory
```

It is the only supported writer for canonical project memory. Codex native
memory under `~/.codex/memories/` remains separate platform memory and is never
copied or synchronized.

## Sources Of Truth

- Package: `src/negrita_brain/`
- CLI: `scripts/negrita_brain.py`
- Claude bridge: `scripts/negrita_brain_hook.py`
- Policy: `core/orchestration/negrita_brain_policy.yaml`
- Project registry: `projects/<project_id>.yaml`
- Adapter: `<work-root>/.codex/project.yaml`

Registry `project.memory_home` is authoritative. An adapter `memory_home`, when
present, is a compatibility mirror checked for drift.

## Session Identity And Lifecycle

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  resolve --root "$PWD" --provider codex --action implementation
```

Codex uses `CODEX_THREAD_ID`; Claude hooks pass their `session_id`; CI and human
automation may pass `--session-key`. Only a SHA-256 key is stored:

```text
runtime/active/<provider>/<session_key_hash>.json
runtime/sessions/<session_id>/contract.json
```

If no v2 pointer exists, the loader falls back to the untouched v1
`runtime/active_session.json`. This lets sessions opened before Memory v2 close
normally without pointer reassignment or contract rehashing.

Gate and close the same provider task:

```bash
python3 scripts/negrita_brain.py gate \
  --root "$PWD" --provider codex --action write --path src/module.py
python3 scripts/negrita_brain.py close \
  --root "$PWD" --provider codex
```

After a durable handoff, add `--durable-ref sessions/example.md` to `close`.

V2 closure writes `state.json`, safe events, pointer state, and optional durable
references only. It ignores the legacy `--summary` compatibility argument. V1
fallback closure keeps its existing `summary.json` contract. Neither path
writes `index.md`.

## Durable Memory

```text
~/.negritaos/memory/projects/<project_id>/
├── index.md
├── observations.jsonl
├── sessions/
├── decisions/ledger.jsonl
├── tasks/
├── catalog/legacy_memory.jsonl
└── runtime/
    ├── active/
    └── sessions/
```

Persist only reusable information:

```bash
python3 scripts/negrita_brain.py memory remember \
  --root "$PWD" --provider codex --type discovery \
  --title "..." --summary "..." --learned "..."
```

Create one continuation handoff:

```bash
python3 scripts/negrita_brain.py memory handoff \
  --root "$PWD" --provider codex --title "..." --goal "..." \
  --accomplished "..." --next-step "..." --file "src/module.py"
```

`memory handoff` creates an immutable markdown session and updates only the
managed durable block in `index.md`, preserving unrelated curated text. Pass
its `durable_ref` to `close`. Ordinary session closure creates no durable
narrative.

## Migration And Recovery

Preview before applying:

```bash
python3 scripts/negrita_brain.py memory migrate --root "$PWD" --dry-run
python3 scripts/negrita_brain.py memory migrate --root "$PWD" --apply
```

The catalog records path, type, state, size, mtime, hash, authority, and project.
It is idempotent and never moves or rewrites source files.

An index containing the v1 `## Runtime Sessions` shape is reported as
`INDEX_RUNTIME_OWNED`. Rebuild is always explicit:

```bash
python3 scripts/negrita_brain.py memory rebuild-index --root "$PWD" --dry-run
python3 scripts/negrita_brain.py memory rebuild-index --root "$PWD" --apply
```

Apply refuses while any v1 session remains open and backs up the old index under
`legacy_import/index/` before replacement.

## Provider Permissions

Codex workspace-write needs the canonical memory root:

```bash
python3 scripts/negrita_brain.py configure codex --check
python3 scripts/negrita_brain.py configure codex --apply
```

Apply preserves the rest of `~/.codex/config.toml`, creates a backup, and adds:

```toml
[sandbox_workspace_write]
writable_roots = ["/Users/jackyb-cqi/.negritaos/memory"]
```

The change applies to new Codex tasks. A sandbox denial is emitted as
`PERMISSION_REQUIRED` with `MEMORY_WRITE_PERMISSION`, never as config resolution
failure.

## Decisions, Documents, And Safe Events

Decision transitions remain append-only under `decisions/ledger.jsonl` and may
project architecture/contract ADRs into `docs/decisions/`. New deliverables use
`documents/<slug>__updated_YYYYMMDD_HHMMSS.<ext>` and the document manifest.

Runtime events permit metadata only: ids, timestamps, status, provider, tool,
action, file path, decision ids, and durable references. Prompts, responses,
commands, file contents, tool outputs, transcripts, and secrets are prohibited.

## Installation And Validation

```bash
python3 scripts/negrita_brain.py install --root /path/to/project --dry-run
python3 scripts/negrita_brain.py doctor --root /path/to/project
python3 scripts/negrita_brain.py doctor --all
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_negrita_brain_coverage.py --fail-under 80
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root "$PWD"
python3 scripts/validate_alignment.py
git diff --check
```

The installer preserves local entrypoint content and unrelated hooks. It creates
durable/runtime directories but does not migrate memory or modify the Codex user
configuration automatically.
