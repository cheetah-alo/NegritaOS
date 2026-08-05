# Jinja + BigQuery Official Notes

Use this reference when you need the exact source behind a Jinja or BigQuery rendering rule.

## Jinja

### Whitespace control

Official docs:
- https://jinja.palletsprojects.com/en/stable/templates/#whitespace-control

Relevant points:
- Jinja preserves most whitespace unless configured otherwise.
- `trim_blocks` removes the first newline after a block tag.
- `lstrip_blocks` strips leading spaces and tabs before a block.
- `-` can strip whitespace manually on blocks, comments, and variables.
- There must be no whitespace between the tag delimiter and `-`.

### Environment settings and undefined behavior

Official docs:
- https://jinja.palletsprojects.com/en/stable/api/

Relevant points:
- `StrictUndefined` fails on print, iteration, boolean tests, and comparisons.
- `newline_sequence` should be one of `\r`, `\n`, or `\r\n`.
- `keep_trailing_newline` preserves the trailing newline in rendered output.
- `trim_blocks` and `lstrip_blocks` are environment-level controls.

## BigQuery GoogleSQL

### Lexical structure, tokens, identifiers, and whitespace

Official docs:
- https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical

Relevant points:
- GoogleSQL statements are made of tokens.
- Tokens can be separated by comments or whitespace such as spaces, tabs, or newlines.
- Reserved keywords used as identifiers must be enclosed in backticks.
- Quoted identifiers use backticks.
- Table, column, and field naming rules differ in important ways.

### Parameterized queries

Official docs:
- https://cloud.google.com/bigquery/docs/parameterized-queries

Relevant points:
- Query parameters protect value positions against SQL injection.
- Parameters are supported only in GoogleSQL.
- Parameters cannot substitute identifiers such as table names, column names, or dataset names.
- Named and positional parameters cannot be mixed in one query.

## Derived Guardrails

These are the practical consequences for Jinja + BigQuery:

1. Use Jinja for structure, not for unsafe value interpolation.
2. Use BigQuery parameters for values.
3. Use allowlisted quoted identifiers for dynamic object names.
4. Treat whitespace stripping as a correctness concern, not just formatting.
5. Validate the fully rendered SQL because template correctness is not enough.
