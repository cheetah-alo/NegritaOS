---
id: load-context
mode_hint: AE   # Adapter / Environment bootstrap
loads:
  - README.md
  - .codex/project.yaml
  - .codex/system.md
  - .codex/instruction-manifest.yaml
  - rules/global/negritaos_router_rule.md
  - .codex/skills/AGENTS.md
---

# Load NegritaOS Context

Bootstrap the full repository context for a new session. Run this FIRST before
any non-trivial task in a NegritaOS-managed repo.

## Procedure

1. **Repository entry points**
   - Read `README.md` — architecture overview, skill/rule inventory, conflict-resolution order.
   - Note any project-specific overrides in `.codex/local-overrides.md`.

2. **Adapter resolution**
   - Read `.codex/project.yaml` → resolve symlink to `projects/<project>.yaml`.
   - Confirm `project_id` and `archetype`.
   - Resolve `negrita_registry` and confirm it matches the project id.
   - Resolve declared `skill_profiles`, `mode_map`, and `agents` before selecting a skill.
   - For the selected agent, load its `integrator.yaml` block, then its `rules`,
     `skills`, `rubrics`, `templates`, and `codex_skills` references.
   - Resolve profile skills through `skills/catalog.yaml`; do not infer availability
     from files copied into a sibling `.codex/skills/` directory.

3. **System contract**
   - Read `.codex/system.md` — operator-style contract for this repo.

4. **Instruction manifest**
   - Read `.codex/instruction-manifest.yaml`.
   - List `docs:` entries (always loaded) and `rules:` entries per mode.
   - Flag any rule with `version` drift or missing `depends_on` target.

5. **Active profile**
   - From `.codex/project.yaml`, identify `codex_profiles.default`.
   - Read the matching profile file under `.codex/profiles/`.

6. **Router**
   - Read `rules/global/negritaos_router_rule.md` (canonical).
   - Read `.codex/skills/AGENTS.md` and `.codex/skills/negritaos-mode-router/SKILL.md`.
   - Detect the current request mode using the trigger table + per-project `mode_map`.

7. **BigQuery analysis entry gate**
   - If the selected project/profile starts a new or migrated BigQuery analysis,
     load `bigquery-analysis-governance` before reading or writing analysis SQL.
   - Resolve the source-quality contract: grain, key, cardinality, event time,
     source capture time, BigQuery load time, latency SLA, freshness, and
     evidence path.
   - During Warn-first adoption, an incomplete contract is provisional and must
     be reported as `CONTRACT_INCOMPLETE`; it is never silently treated as
     validated.

8. **Validation**
   - Run `python3 scripts/validate_config_resolution.py`.
   - Run `python3 scripts/validate_alignment.py`.
   - For a declared source contract, run
     `python3 scripts/validate_source_quality_contract.py --contract <path>`.
   - If any check fails → halt and surface the failing item.

## Output contract

Single structured report:

```markdown
## NegritaOS Context Loaded

- Project: <project_id>
- Archetype: <archetype>
- Profile: <profile_id> (<file>)
- Mode (detected): <LP|AE|TD|MR|CR|EP|DQ|RT>
- Mode source: <mode_map override | global trigger | default>

## Rules auto-loaded for this mode
- <rule_id> v<version> — <path>
- ...

## Skills available
- <skill_name> — <trigger summary>

## Validation
- scripts/validate_config_resolution.py: <pass/fail + resolved chain>
- scripts/validate_alignment.py: <N/N checks passed>
- validate_source_quality_contract.py: <pass/fail or N/A>

## Ready
Next action awaiting: <user prompt summary or "idle">
```

## Stop conditions

- `README.md` missing → warn and continue without it.
- `.codex/project.yaml` symlink broken → halt.
- `instruction-manifest.yaml` references a missing rule file → halt.
- `validate_alignment.py` exit code ≠ 0 → halt and report failing check.
- `validate_config_resolution.py` exit code ≠ 0 → halt and report the broken
  project → registry → agent → asset reference.
