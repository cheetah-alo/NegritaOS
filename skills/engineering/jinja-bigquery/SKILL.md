---
name: engram-jinja-bigquery
description: >
  Jinja guardrails for rendering BigQuery GoogleSQL safely and deterministically.
  Trigger: Any Jinja template that emits SQL, dynamic CTEs, WHERE clauses,
  identifiers, or query variants for BigQuery.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Writing Jinja templates that render BigQuery SQL
- Refactoring dynamic SQL into template blocks or macros
- Building conditional CTEs, filters, projections, or UNION branches
- Reviewing whitespace-sensitive SQL rendering bugs

Read `references/official-docs.md` when you need the exact Jinja or BigQuery rule behind a guardrail.

---

## Required Jinja Environment

For SQL rendering, prefer:

- `undefined=StrictUndefined`
- `trim_blocks=True`
- `lstrip_blocks=True`
- `newline_sequence="\n"`
- `keep_trailing_newline=True` for deterministic rendered files
- `autoescape=False` for SQL text output

Rationale:
- `StrictUndefined` fails fast on missing variables instead of rendering broken SQL silently.
- `trim_blocks` and `lstrip_blocks` remove blank lines and indentation artifacts around block tags.
- `\n` keeps line endings stable across platforms.

---

## Core Rules

1. Render complete SQL tokens, not token fragments.
2. Parameterize values in BigQuery; do not use Jinja substitution for user-provided literals when query parameters can be used.
3. Treat dynamic identifiers separately from dynamic values.
4. Make whitespace deterministic around every conditional block.
5. Render full clauses or nothing; never leave dangling keywords, commas, or operators.

---

## SQL Safety Rules

### 1. Values vs identifiers

- Use BigQuery query parameters for values such as dates, strings, arrays, numbers, timestamps.
- Do not use query parameters for table names, dataset names, column names, or other identifiers because BigQuery does not support that.
- For dynamic identifiers, require an allowlist and quote them with backticks when needed.

### 2. Identifier rules

- If an identifier may contain reserved keywords or special characters, emit it as a quoted identifier using backticks.
- Do not concatenate partial identifier pieces across branches unless the full rendered value is validated first.
- Never pass raw user input directly into an identifier position.

### 3. Clause integrity

Render each unit as a syntactic whole:

- entire CTE
- entire JOIN clause
- entire predicate
- entire SELECT item
- entire ORDER BY item

Do not do this:

```jinja
WHERE
{% if include_filter %}
  col = @value
{% endif %}
```

Prefer this:

```jinja
{% if include_filter %}
WHERE col = @value
{% endif %}
```

Or compose predicates first, then join them.

---

## Whitespace Rules

### 1. Default posture

- Put block tags on their own lines when they control SQL structure.
- Use `trim_blocks=True` and `lstrip_blocks=True` so block lines disappear cleanly.
- Keep one SQL unit per line when possible.

### 2. Minus-sign control

Use `{%- ... %}` and `{% ... -%}` only when you need to remove a known unwanted newline or indentation boundary.

Rules:
- No spaces between the tag delimiter and `-`
- Use minus stripping sparingly; overuse makes SQL harder to read and can merge tokens unexpectedly
- Re-check the exact rendered output when adding `-`

### 3. Token separation

BigQuery separates tokens with whitespace or comments. Never let Jinja collapse two SQL tokens together.

Bad:

```jinja
SELECT * FROM table
{% if use_qualify -%}
QUALIFY row_num = 1
{%- endif %}
ORDER BY created_at
```

This can merge `tableQUALIFY` or `1ORDER` depending on placement.

Prefer explicit line boundaries:

```jinja
SELECT * FROM table
{% if use_qualify %}
QUALIFY row_num = 1
{% endif %}
ORDER BY created_at
```

### 4. Comma control

- Build comma-separated lists with `loop.last`, `join`, or precomputed lists
- Never leave trailing commas before `FROM`, `WHERE`, `GROUP BY`, or closing parentheses
- Never let an optional SELECT item control the comma of a neighboring mandatory item

Preferred:

```jinja
SELECT
{% for col in columns %}
  {{ col }}{% if not loop.last %},{% endif %}
{% endfor %}
```

---

## BigQuery-Specific Guardrails

### 1. Quote identifiers correctly

- Project, dataset, table, column, and field names must follow GoogleSQL identifier rules
- Reserved keywords must be backtick-quoted when used as identifiers
- Datasets cannot contain dashes; project IDs can in specific table-path positions

### 2. Keep literals out of string-built SQL when parameters work

Prefer:

```sql
WHERE event_date >= @start_date
```

Over:

```jinja
WHERE event_date >= DATE('{{ start_date }}')
```

### 3. Build repeated predicates from lists

For optional filters, accumulate predicates and join them with `AND` or `OR`. This is safer than toggling standalone `AND` lines.

### 4. Dry-run rendered SQL

Before merging:

- render the final SQL
- inspect the exact output
- run a BigQuery dry run if the environment supports it

---

## Recommended Composition Pattern

1. Validate and normalize template inputs before rendering.
2. Separate:
   - identifiers
   - parameter values
   - optional structural blocks
3. Precompute reusable lists:
   - select columns
   - predicates
   - joins
   - CTE fragments
4. Render with deterministic whitespace settings.
5. Review the final SQL, not just the template.

---

## Review Checklist

- [ ] `StrictUndefined` is enabled
- [ ] `trim_blocks` and `lstrip_blocks` are enabled
- [ ] Values use BigQuery parameters where possible
- [ ] Dynamic identifiers are allowlisted and safely quoted
- [ ] No dangling commas, `AND`, `OR`, or partial clauses
- [ ] No token merging caused by aggressive whitespace stripping
- [ ] Final rendered SQL was inspected
- [ ] BigQuery dry run or parser validation was executed when available
