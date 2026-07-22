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
- `skills/engineering/` contains native NegritaOS agent skills.
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

## Distribution Procedure

1. Add or update the project registry and declare profiles.
2. Run `scripts/validate_skill_catalog.py`.
3. Run `scripts/materialize_project_skills.py <repo> --dry-run`.
4. Review local overrides and backup requirements.
5. Run `scripts/migrate_sibling_to_canonical.sh <repo>` only after the
   project's worktree is approved for adapter mutation.
6. Validate with `scripts/validate_alignment.py --sibling <repo>`.

The materializer links only canonical `.codex/skills` directories selected by
profile. It preserves local overrides by creating timestamped backups before
replacing a real directory. Raw Engram/Nate directories are never linked.

## Quality Gates

- Catalog IDs and canonical paths are unique and resolvable.
- Every active skill has matching directory/name frontmatter.
- Profiles reference known skills only.
- Physical source names are absent from frontend contracts and helpers.
- Provider adapter tests and logical contract tests exist for data-backed apps.
- API, documentation, E2E, coverage, and PR-base evidence are reported.
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
