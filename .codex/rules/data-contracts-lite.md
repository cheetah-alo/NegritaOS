---
id: data-contracts-lite
domain: data-governance
enforcement: advisory
priority: warning
depends_on: [data-contracts, data-validation]
version: 1.0.0
applyTo: [data, sql, python, pipelines]
---

# Data Contracts — Quick Reference

- Every dataset consumed by ML, analytics, or AutoML MUST have a JSON contract in `configs/contracts/*.json`.
- Contract columns are the single source of truth for BigQuery SQL, Python features, and AutoML inputs.
- Required fields per column: `type`, `description`, and at least one constraint (`minimum`, `maximum`, or `enum`).
- Versioning: MAJOR for breaking changes (rename/remove/type change); MINOR for additive changes; PATCH for doc fixes.
- Validate required columns before any feature engineering; raise `MissingColumnError` on failure.
- Record contract name + version + deviations in `governance_json["data_audit"]` on every training run.
- See `data-contracts.md` for full authoring rules and `data-contracts` skill for validation utilities.
