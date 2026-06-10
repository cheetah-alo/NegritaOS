# Context Management Audit

**Date:** 2026-06-01  
**Scope:** `.codex/rules/` (22 files, 4177 lines) — all globally loaded via `instruction-manifest.yaml`.

---

## 1. File inventory

| File | Lines | Current role | Problem | Recommendation | Priority |
|------|-------|--------------|---------|----------------|----------|
| `ai-behavior.md` | 153 | Core meta-behavior | None — well-scoped | Keep, minor trim | Low |
| `negritaos-router.md` | 32 | Router stub | None | Keep as-is | None |
| `dev-coding-standards.md` | 167 | Core quality | Some verbose prose | Trim prose, keep rules | Low |
| `dev-security.md` | 206 | Core security | Acceptable length | Keep, minor trim | Low |
| `data-contracts.md` | 185 | Core data governance | Moderate verbosity | Trim examples | Low |
| `dev-learnings.md` | 297 | Meta-adaptive | Verbose meta-instructions | Trim, keep counter rules | Medium |
| `dev-logging.md` | 446 | Logging standard | Oversized, governance JSON spec is very long | Compress rule; create `dev-logging` skill for full spec | High |
| `dev-naming-conventions.md` | 443 | Naming standard | Oversized, many domain examples duplicated | Compress to bullet rules | High |
| `tests-unittest-standards.md` | 388 | Test standard | Oversized, examples covered by `create-unittest` skill | Compress; delegate detail to skill | High |
| `dev-error-handling.md` | 381 | Error handling | Oversized, domain code examples too long | Compress; delegate detail to `python-core` skill | High |
| `dev-python.md` | 357 | Python ML guidelines | Oversized, detail covered by `python-core` skill | Compress to mandatory rules | High |
| `dev-object-orientation.md` | 312 | OOP rules | Oversized for a global rule | Compress; detail belongs in `python-core` skill | Medium |
| `plotting-guidelines.md` | 308 | Plot standards | Advisory, task-specific (EDA only) | Move to `eda-reports` skill; remove from global | Medium |
| `dev-commit-hygiene.md` | 229 | Commit checklist | Detail covered by `commit-hygiene` skill | Compress; delegate checklist to skill | Medium |
| `data-sql-governance.md` | 118 | SQL governance | Task-specific (SQL work only) | Move to `data-analytics` skill; remove from global | Medium |
| `data-validation.md` | 75 | Validation rules | Task-specific | Move to `data-contracts` skill; remove from global | Medium |
| `notebooks.md` | 60 | Notebook governance | Task-specific | Move to `eda-reports` skill; remove from global | Low |
| `pipelines.md` | 5 | Pipeline rules | Too thin to be useful (3 bullets) | Expand with concrete rules | Medium |
| `ml-telemetry.md` | 5 | ML telemetry rules | Too thin to be useful (3 bullets) | Expand with concrete rules | Medium |
| `dev-tree-widgets.md` | 5 | Tree widget rules | Too thin to be useful (3 bullets) | Expand with concrete rules | Low |
| `dev-observables.md` | 5 | Observable rules | Too thin to be useful (3 bullets) | Expand with concrete rules | Low |
| `data-contracts-lite.md` | 0 | Data contracts summary | **EMPTY — no content** | Fill with compressed data-contracts summary | Critical |

---

## 2. Duplicate and overlapping areas

| Overlap | Files involved | Action |
|---------|---------------|--------|
| Naming rules appear in both `dev-naming-conventions.md` and `dev-coding-standards.md` | Both | Remove naming section from coding-standards |
| Error handling examples duplicated between `dev-error-handling.md` and `dev-python.md` | Both | Single source in compressed error-handling rule |
| Logging governance repeated in `dev-logging.md`, `dev-python.md`, and `dev-commit-hygiene.md` | All three | Compress each to a cross-reference |
| Testing standards overlap between `tests-unittest-standards.md` and `dev-python.md` §1 | Both | Remove from dev-python, defer to create-unittest skill |
| Commit checklist in `dev-commit-hygiene.md` duplicates `commit-hygiene` skill content | Both | Compress rule to header + pointer to skill |

---

## 3. Largest context consumers

Ranked by line count (all globally loaded):

1. `dev-logging.md` — 446 lines (governance JSON spec dominates)
2. `dev-naming-conventions.md` — 443 lines (exhaustive domain examples)
3. `tests-unittest-standards.md` — 388 lines (many code blocks)
4. `dev-error-handling.md` — 381 lines (long code templates)
5. `dev-python.md` — 357 lines (partially redundant with skills)

**Estimated savings if top 5 compressed to ~80 lines each:** ~1600 lines / ~38% reduction.

---

## 4. Quick wins

| Win | Effort | Savings |
|-----|--------|---------|
| Fill `data-contracts-lite.md` | Minimal | Removes broken reference |
| Expand 4 stub files to useful content | Small | Removes token waste from near-empty globals |
| Remove long code templates from `dev-error-handling.md` | Medium | ~250 lines |
| Remove governance JSON spec from `dev-logging.md` (move to `dev-logging` skill) | Medium | ~200 lines |
| Remove domain examples from `dev-naming-conventions.md` | Medium | ~200 lines |
| Create `commit-push-pr.md` and `run-quality-checks.md` commands | Small | Improves workflow completeness |

---

## 5. Risks

| Risk | Mitigation |
|------|-----------|
| Compressing rules may remove context agents rely on for implicit defaults | Keep all mandatory rules; only remove verbose prose and duplicate examples |
| Removing a rule from always-loaded may cause agents to miss it | Add explicit trigger in skill metadata; update router routing table |
| `plotting-guidelines.md` and `data-sql-governance.md` are currently strict+critical despite being task-specific | Change `enforcement` to `advisory` and `priority` to `warning` before migrating |
| `data-contracts-lite.md` is referenced in `instruction-manifest.yaml` but is empty | Fill it immediately |

---

## 6. Proposed migration plan

### Phase 1 — Immediate (no risk)
1. Fill `data-contracts-lite.md`.
2. Expand 4 stub files.
3. Create `dev-logging` skill.
4. Create missing commands: `commit-push-pr.md`, `run-quality-checks.md`.
5. Fix `.codex/` path references in `system-audit.md`.

### Phase 2 — Compression (reduces global context ~40%)
6. Compress `dev-logging.md` (~446 → ~80 lines; full spec moves to skill).
7. Compress `dev-naming-conventions.md` (~443 → ~80 lines).
8. Compress `dev-error-handling.md` (~381 → ~60 lines).
9. Compress `dev-python.md` (~357 → ~50 lines).
10. Compress `tests-unittest-standards.md` (~388 → ~60 lines).

### Phase 3 — Migration (requires instruction-manifest.yaml updates)
11. Move `plotting-guidelines.md` content into `eda-reports` skill; set rule `enforcement: advisory`.
12. Move `data-sql-governance.md` content into `data-analytics` skill; set rule as stub pointer.
13. Move `notebooks.md` content into `eda-reports` skill; set rule as stub pointer.
14. Move `data-validation.md` content into `data-contracts` skill; set rule as stub pointer.

---

## 7. Files changed by initial implementation

| File | Action |
|------|--------|
| `docs/context-management-audit.md` | Created (this file) |
| `docs/context-management.md` | Created |
| `.codex/rules/data-contracts-lite.md` | Filled |
| `.codex/rules/pipelines.md` | Expanded |
| `.codex/rules/ml-telemetry.md` | Expanded |
| `.codex/rules/dev-tree-widgets.md` | Expanded |
| `.codex/rules/dev-observables.md` | Expanded |
| `.codex/skills/dev-logging/SKILL.md` | Created |
| `.codex/commands/commit-push-pr.md` | Created |
| `.codex/commands/run-quality-checks.md` | Created |
| `.codex/commands/system-audit.md` | Fixed path references |
| `.codex/rules/dev-logging.md` | Compressed |
| `.codex/rules/dev-naming-conventions.md` | Compressed |
| `.codex/rules/dev-error-handling.md` | Compressed |
| `.codex/rules/dev-python.md` | Compressed |
| `.codex/rules/tests-unittest-standards.md` | Compressed |
