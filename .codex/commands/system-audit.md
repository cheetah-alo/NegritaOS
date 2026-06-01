---
id: system-audit
mode_hint: CR   # Code Review / Hardening
loads:
  - rules/global/negritaos_router_rule.md
  - .codex/instruction-manifest.yaml
  - rules/dev-coding-standards.md
  - rules/dev-error-handling.md
  - rules/dev-logging.md
  - rules/dev-security.md
  - rules/tests-unittest-standards.md
  - rules/data-contracts.md
  - rules/data-validation.md
---

# System Audit & Hardening

Audit the full system for **build, runtime, architecture, validation, integration,
config, performance, security, test, and maintainability** risks. Harden it with
**minimal necessary changes**.

## Procedure

### Phase 1 — Inventory (read-only)

- Map the active project from `.codex/project.yaml` → `projects/<project>.yaml`.
- List entry points, services, pipelines, dataset contracts, tests, CI jobs.
- Identify the active profile and mode (NegritaOS router).

### Phase 2 — Audit matrix

For each dimension, classify findings as `Critical / High / Medium / Low / Info`:

| Dimension       | Probes                                                                 |
|-----------------|------------------------------------------------------------------------|
| Build           | uv lock drift, broken imports, missing deps in `pyproject.toml`        |
| Runtime         | unhandled exceptions, infinite loops, blocking I/O, GPU/memory leaks   |
| Architecture    | layer violations, circular imports, files >1700 lines, god-classes    |
| Validation      | missing schema/contract checks, leakage risk, weak input validation    |
| Integration     | SQL/BigQuery contract drift, broken pipeline phases, MCP tool mismatch |
| Config          | hardcoded paths, missing env vars, `.env.example` drift                |
| Performance     | N+1 queries, missing partitions/clusters, unbounded scans              |
| Security        | secrets in code/logs, PII in fixtures, missing gitleaks, CVE pins      |
| Test            | coverage <80% prod / unittest+pytest parity / behavior-named tests     |
| Maintainability | dead code, duplicated logic, naming violations, missing docstrings     |

### Phase 3 — Harden (minimal diffs)

- Propose ONE smallest change per `Critical` and `High` finding.
- For `Medium`/`Low` → list as backlog with rationale, do not edit unless asked.
- Every fix must comply with `.codex/rules/dev-commit-hygiene.md`
  (per-commit checklist + trailer).

### Phase 4 — Report

```markdown
## System Health
overall_status: green | amber | red
confidence: NN%

## Findings by Severity
- Critical: N
- High:     N
- Medium:   N
- Low:      N
- Info:     N

## Fixes Applied (this run)
- <file>:<line> — what, why, rule_id

## Remaining Risks
- <id> — severity — owner_suggestion — effort

## Next Steps
1. ...
2. ...

## Task Log (append-only)
| When (UTC) | What | How | Lessons learned |
|------------|------|-----|------------------|
| ...        | ...  | ... | ...              |
```

## Stop conditions

- Any `Critical` finding touching security/PII → halt edits, escalate.
- Coverage would drop below tier floor.
- Schema contract change without version bump.
