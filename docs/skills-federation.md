# NegritaOS Federated Skills

## Purpose

This document defines how reusable skills from Engram and Nate become
available to current and future NegritaOS projects without copying a full
`.codex` tree or coupling every project to one database provider.

## Audience And Scope

Maintainers of NegritaOS, project adapter owners, software architects, code
reviewers, and agents adding or consuming skills. This covers canonical skill
registration, project profiles, source provenance, adapter distribution, and
validation. It does not change a sibling repository by itself.

## Sources And Source Of Truth

- `skills/skills_engram/` is an Engram reference bundle.
- `skills/skill_nate/` is a Nate reference bundle.
- `.codex/skills/` contains activable IDE skills.
- `skills/engineering/` and `skills/academic/` contain native NegritaOS agent skills.
- `skills/catalog.yaml` is the machine-readable federation catalog.
- `projects/<project>.yaml` declares project profiles and data-source facts.

Raw source bundles remain reference-only. Adapted skills must have valid
frontmatter, a matching directory/name, declared scope, declared dependencies,
and explicit side-effect policy.

## Project Contract

Projects may declare:

```yaml
skill_profiles:
  - analytical-dashboard
  - fastapi-nextjs
  - data-source-bigquery

integration_branch: dev_ml

data_source:
  provider: bigquery
  dialect: google_standard_sql
  source_of_truth: governed_remote_source
  access: read_only
```

Use `data-source-postgresql` and `dialect: postgresql` for a PostgreSQL
project. The provider changes the adapter implementation, not the logical API
contract consumed by the frontend. The integration branch is project-owned;
`dev_ml` is an ELAL declaration, not a global database or Git assumption.

## Analysis Profiles And BigQuery Entry Gate

Use `analytical-eda` for provider-neutral exploratory analysis governance and
`data-source-bigquery` when the analysis reads BigQuery. The latter activates
`bigquery-analysis-governance`; it does not make BigQuery table names or
physical columns part of a frontend or public API contract.

Every new or migrated BigQuery analysis must begin with a source-quality
preflight. Declare the logical grain, unique or composite key, expected
cardinality, join relationships, `event_time`, `source_capture_time`, and
`bq_loaded_at`. Validate duplicates, fan-out, null timestamps, timezone
consistency, temporal coverage, ingestion latency, freshness, and the
source-specific latency SLA. Ingestion latency is
`bq_loaded_at - source_capture_time`; freshness is
`now - max(bq_loaded_at)`. `event_time` is never a silent fallback for source
capture time.

The reusable contract template is
[`templates/bigquery_analysis_source_contract.yaml`](../templates/bigquery_analysis_source_contract.yaml).
Physical-to-logical column mapping belongs in the source adapter or analysis
manifest. Evidence must be retained in the run manifest under
`source_quality`, including row and distinct-key counts, duplicate/fan-out
results, timestamp null rates, latency percentiles, freshness, SLA, query
hashes, status, and limitations.

The first adoption phase is `warn_first`: an analysis may execute with an
incomplete preflight, but its result is `CONTRACT_INCOMPLETE`/provisional and
cannot be described as validated or `production-ready`. If reliable source
capture time is unavailable, record `NOT_APPLICABLE` with the proxy, owner, and
limitation. Never fabricate latency and never silently substitute `event_time`.

Run the standalone validator when a contract or evidence manifest is ready:

```bash
python3 scripts/validate_source_quality_contract.py \
  --contract templates/bigquery_analysis_source_contract.yaml
```

`elal-eda-governance` is opt-in. It preserves ELAL-specific semantics such as
raw operational severity, `IA_CALL_TAXONOMY_PROXY`, `BLOCKED_NO_SUPPORT`,
`BLOCKED_DATA`, zero-vs-no-support separation, and the third-subtitle rule.
These rules are not activated for HOT, IBC, PostgreSQL, file, API, or academic
projects unless their registry explicitly selects that profile.

## Project Impact And Rollout

The first rollout changes only NegritaOS. Adapter workspaces are inspected in
dry-run mode and are not modified automatically.

| Project | Status | Treatment |
|---|---|---|
| `proj_data_analytics` | `migration_required` | Pilot registry now declares `analytical-eda`, BigQuery, and `warn_first`; apply first to new analyses and `p_elal_eda`. |
| `elal_journey_dashboard` | `ready` | BigQuery preflight applies to analysis/EDA modes; frontend remains provider-blind. |
| `ibc_fiber_network` | `migration_required` | Registry declares the profile and source; inventory grain, latency, and coverage evidence remain prerequisites for readiness claims. |
| `hot_onedrive_workspace` | `conditional` | Activate only when a real BigQuery analysis starts; evidence review alone is unaffected. |
| PostgreSQL, files, API, and academic projects | `ready` | BigQuery rules are not loaded; use the provider-neutral contracts and the relevant adapter profile. |

Before resolving a configuration-sensitive analysis, follow this order:

```text
project.yaml
-> project registry
-> skill_profiles/data_source
-> mode_map/agents
-> integrator
-> rules/skills/rubrics
-> source-quality preflight
-> analysis
```

If canonical resolution fails, return `BLOCKED_CONFIG_RESOLUTION` and do not
plan changes from the sibling's visible files alone. Use
`validate_config_resolution.py --project-yaml <adapter>/.codex/project.yaml`
for a read-only sibling dry-run. Full alignment reports unresolved external
adapter conditions without mutating those worktrees.

## Distribution Procedure

1. Add or update the project registry and declare profiles.
2. Run `scripts/validate_skill_catalog.py`.
3. Run `scripts/materialize_project_skills.py <repo> --dry-run`.
4. Review local overrides and backup requirements.
5. Run `scripts/migrate_sibling_to_canonical.sh <repo>` only after the
   project's worktree is approved for adapter mutation.
6. Validate with `scripts/validate_alignment.py --sibling <repo>`.

Before answering a configuration-sensitive request, resolve the active chain
with `scripts/validate_config_resolution.py`. This checks
`.codex/project.yaml` → project registry → profiles and `mode_map` → agent
block in `integrator.yaml` → rules, skills, rubrics, templates, and Codex
wrappers. A skill is not considered available merely because a folder is
visible in the current environment.

The materializer links only canonical `.codex/skills` directories selected by
profile. It preserves local overrides by creating timestamped backups before
replacing a real directory. Raw Engram/Nate directories are never linked.

### Direct activation contract

Codex and Claude discover a skill through the canonical adapter entrypoint:

```text
.codex/skills/<skill-id>/SKILL.md
```

`.claude/skills/` is a compatibility view of the same directory. A native
source such as `skills/engineering/<name>/SKILL.md` is not itself a portable
adapter entrypoint, even when it is a valid skill document. The catalog and
materializer must expose the canonical ID as the folder name; physical source
symlinks must not rename it. A skill is not available to an adapter until this
direct `SKILL.md` path exists and resolves successfully.

## Quality Gates

- Catalog IDs and canonical paths are unique and resolvable.
- Every active skill has matching directory/name frontmatter.
- Profiles reference known skills only.
- Physical source names are absent from frontend contracts and helpers.
- Provider adapter tests and logical contract tests exist for data-backed apps.
- API, documentation, E2E, coverage, and PR-base evidence are reported.
- New and migrated BigQuery analyses carry source-quality evidence before they
  can be called validated or production-ready.
- Generated images, frames, coverage, tmp, outputs, credentials, and local
  settings remain outside committed source.

## Ownership And Updates

The NegritaOS maintainers own `skills/catalog.yaml`, canonical wrappers,
profile definitions, and adapter scripts. A skill source update requires a
catalog review, frontmatter validation, documentation alignment, and the
NegritaOS validation suite. Project owners own their registry profiles and
provider facts.

## Limitations

Visual generation and video workflows remain opt-in because they may call
external APIs, require local binaries, or create large artifacts. BigQuery and
PostgreSQL performance rules remain provider-specific implementation guidance;
the shared contract only governs boundaries and logical behavior.
