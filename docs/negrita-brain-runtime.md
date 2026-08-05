# Negrita Brain Runtime

## Purpose

Negrita Brain turns NegritaOS configuration into an executable session contract:

```text
project -> mode -> agent -> rules -> profile closure -> skills
        -> artifact route -> quality gates -> memory
```

The kernel is provider-neutral. Codex uses `AGENTS.md`, explicit CLI preflight,
CI, and an optional pre-commit hook. Claude imports the same `AGENTS.md` through
`CLAUDE.md` and is enforced by shared lifecycle hooks.

## Source Of Truth

- Package: `src/negrita_brain/`
- CLI: `scripts/negrita_brain.py`
- Claude bridge: `scripts/negrita_brain_hook.py`
- Runtime policy: `core/orchestration/negrita_brain_policy.yaml`
- Profile catalog: `skills/catalog.yaml`
- Project registry: `projects/<project_id>.yaml`
- Project adapter: `<work-root>/.codex/project.yaml`

## Session Lifecycle

Resolve before substantive work:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  resolve --root "$PWD" --provider codex --action implementation
```

The immutable contract is written under:

```text
~/.negritaos/memory/projects/<project_id>/runtime/sessions/<session_id>/contract.json
```

It contains project identity, provider, Git branch/HEAD, actions, modes, agents,
rules, parent-first profile closure, de-duplicated skills, document route,
quality gates, warnings, state, and SHA-256.

Gate mutations and commits:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  gate --root "$PWD" --action write --path src/module.py
```

Close substantive sessions:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py \
  close --root "$PWD" --summary "Implemented and validated contract routing"
```

`close` writes a summary, appends a safe event, closes the active pointer, and
refreshes the project memory index. An incomplete or closed contract cannot
authorize code-repository mutations.

## Profile Inheritance

Profiles use `extends`. Resolution is parent-first, stable, de-duplicated, and
fails on unknown parents or cycles.

The document chain is:

```text
document-delivery
  -> analytical-deck-delivery
    -> cqi-analytical-pptx
      -> elal-analytical-deck | ibc-technical-eda-presentation
```

`document-delivery` is a catalog default, so `docs-alignment` and
`document-control` apply to every registered project even when a project does
not declare a presentation profile.

## Decision Ledger

```bash
python3 scripts/negrita_brain.py decision propose \
  --root "$PWD" --kind architecture --title "..." --summary "..."
python3 scripts/negrita_brain.py decision accept \
  --root "$PWD" NBD-... --accepted-by owner --acceptance-ref commit:abc123
python3 scripts/negrita_brain.py decision supersede \
  --root "$PWD" NBD-... --kind contract --title "..." --summary "..."
```

Transitions append to `decisions/ledger.jsonl`. Architecture and contract
candidates in Git repositories also create a versioned ADR under
`docs/decisions/`. Corrections append `SUPERSEDED`; history is never rewritten.

Commits may carry these trailers:

```text
Negrita-Contract: <session_id>
Negrita-Decision: <decision_id>
Negrita-Gates: tests,coverage,alignment
```

## Safe Events

`event` stores metadata only: event/session ids, time, kind, status, provider,
tool, action, file path, and decision ids. Prompts, responses, file contents,
tool outputs, commands, and secrets are discarded.

## Documents And Evidence

New deliverables use:

```text
documents/<slug>__updated_YYYYMMDD_HHMMSS.<ext>
documents/document_manifest.jsonl
```

`catalog-legacy` inventories historical deliverables by path, size, mtime, type,
and hash when safely local. It never moves, renames, or overwrites evidence. It
does not hash OneDrive CloudStorage files, avoiding placeholder downloads.

## Installation And Audit

Dry-run first:

```bash
python3 scripts/negrita_brain.py install --root /path/to/project --dry-run
python3 scripts/negrita_brain.py doctor --root /path/to/project
python3 scripts/negrita_brain.py doctor --all
```

Installation preserves local text outside managed blocks and backs up changed
files under `~/.negritaos/backups/<project_id>/<timestamp>/`. Existing `.codex`
content and unrelated hooks are retained. Re-running the installer is a no-op.

## Validation

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_negrita_brain_coverage.py --fail-under 80
python3 scripts/validate_skill_catalog.py --project projects/negritaos.yaml
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root "$PWD"
python3 scripts/validate_alignment.py
python3 scripts/audit_document_control.py /path/to/project
git diff --check
```

## Ownership And Update Trigger

Update this contract when CLI interfaces, policy states, hook events, profile
inheritance, memory layout, or document routing changes. Runtime policy and code
must change together in one pull request.
