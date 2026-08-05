---
name: jinja-bigquery
description: >
  Guardrails for rendering BigQuery GoogleSQL from Jinja templates safely and
  deterministically. Trigger when writing, reviewing, or refactoring Jinja SQL
  templates, dynamic CTEs, optional predicates, identifier routing, or query
  variants for BigQuery.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, data_analytics, backend]
  auto_invoke:
    - "Writing or reviewing Jinja templates that render BigQuery SQL"
    - "Refactoring dynamic SQL into Jinja template blocks or macros"
    - "Building optional CTEs, filters, projections, joins, or UNION branches for BigQuery"
    - "Reviewing whitespace-sensitive SQL rendering bugs"
---

# Jinja BigQuery

Apply the native guidance in:

`skills/engineering/jinja-bigquery/SKILL.md`

Use this wrapper whenever a NegritaOS-managed project renders BigQuery
GoogleSQL through Jinja. Pair it with:

- `data-source-adapters` for provider routing and physical object boundaries;
- `bigquery-analysis-governance` for SELECT-only, dry-run, cost, and source
  quality gates;
- `data-contracts` when rendered queries feed logical contracts.

## Critical Rules

1. Use Jinja for SQL structure, not unsafe value interpolation.
2. Use BigQuery query parameters for values.
3. Use allowlisted and quoted identifiers for dynamic object names.
4. Render complete SQL units: clauses, predicates, CTEs, SELECT items, joins,
   and UNION branches.
5. Use deterministic whitespace settings and inspect the final rendered SQL.
6. Run a BigQuery dry run or parser validation when the environment supports it.

## Commands

```bash
python3 scripts/validate_config_resolution.py
python3 scripts/validate_skill_catalog.py
python3 scripts/validate_registry_paths.py --root /Users/jackyb-cqi/repos/NegritaOS
```

## Resources

- `skills/engineering/jinja-bigquery/references/official-docs.md`
