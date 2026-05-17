# Skill: SQL / BigQuery Review

**Type:** Domain — Engineering
**Applicable agents:** code_review_agent

## Purpose
Reviews SQL queries and BigQuery scripts for correctness, cost efficiency,
maintainability, and production readiness.

## Review Checklist

### Correctness (P0/P1)
- [ ] JOIN logic is correct: no fan-out or data duplication due to incorrect join type
- [ ] NULL handling is explicit where nulls are expected in join keys or filter conditions
- [ ] Date/timestamp filters use the correct column (partition column vs. event column)
- [ ] Aggregation grain is consistent with the intended output

### BigQuery Cost Awareness (P1)
- [ ] `SELECT *` is not used on large tables — columns are explicitly listed
- [ ] Partition pruning is applied: WHERE clause uses the partition column
- [ ] No unnecessary CROSS JOINs or unfiltered scans on large tables
- [ ] Approximate functions used where exactness is not required (`APPROX_COUNT_DISTINCT`)
- [ ] Subqueries that could be CTEs are refactored for readability (P2)

### Reproducibility and Auditability (P1)
- [ ] Queries reference versioned table names or snapshots, not live tables where stability matters
- [ ] Date parameters are configurable, not hardcoded as literals
- [ ] Query has a comment block: purpose, author, last modified date, dependencies

### Maintainability (P2)
- [ ] CTEs used to break down complex logic into named steps
- [ ] Column aliases are descriptive, not `col1`, `a`, `tmp`
- [ ] No deeply nested subqueries (max 2 levels — refactor to CTEs beyond this)
- [ ] Consistent formatting: keywords uppercase, column names lowercase

### Data Quality Checks (P2)
- [ ] Assertions or quality checks at key transformation steps
- [ ] Deduplication logic is explicit where source data may have duplicates

## Output Format (per issue)
```
[SEVERITY] Query: [name or description]
Line/CTE: [reference]
Issue: [what is wrong]
Risk: [cost / correctness / maintainability]
Fix: [specific recommendation with example if needed]
```
