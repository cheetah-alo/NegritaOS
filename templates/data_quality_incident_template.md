# Data Quality Incident Report

> **TL;DR:** [What broke, what is affected, severity, and required action]

---

## Incident Metadata
- **Incident ID:** DQ-[YYYY-MM-DD]-[sequence]
- **Reported by:** [name / system]
- **Detected at:** [YYYY-MM-DD HH:MM UTC]
- **Severity:** P[1/2/3/4] — [Critical / High / Medium / Low]
- **Status:** [OPEN / IN PROGRESS / RESOLVED]

---

## Affected Scope

| Layer | Resource | Impact |
|-------|----------|--------|
| Table | [schema.table_name] | [Rows affected, period] |
| Pipeline | [pipeline name] | [Step failing] |
| KPI / Dashboard | [KPI name] | [Metric affected] |
| Model | [model name] | [Whether predictions are impacted] |

**Affected period:** [YYYY-MM-DD — YYYY-MM-DD] or [ONGOING]

---

## Evidence

Reproducible evidence (query or observation):

```sql
-- [Description of what this query shows]
SELECT ...
```

**Observation:** [What the evidence shows, stated factually]

---

## Root Cause

**Status:** [CONFIRMED / SUSPECTED / UNKNOWN]

**Description:**
[What caused the issue. If unknown, state the leading hypothesis and what is needed to confirm it.]

**Contributing factors:**
- [factor 1]
- [factor 2]

---

## Business Impact

| Impact Area | Description | Estimated Magnitude |
|-------------|-------------|---------------------|
| [KPI / Decision / Model] | [How it is affected] | [Quantified or bounded] |

---

## Resolution Criteria

The incident is resolved when:
1. [Measurable criterion 1]
2. [Measurable criterion 2]

---

## Escalation Path

| Role | Name / Team | Action Required | SLA |
|------|-------------|----------------|-----|
| Data Engineering | [team] | Fix pipeline / table | [time] |
| Data Owner | [name] | Confirm business impact | [time] |
| ML Team | [team] | Assess model impact | [time] |

---

## Resolution Log

| Timestamp | Action Taken | By Whom |
|-----------|-------------|---------|
| | | |

---

*NegritaOS — data_quality_sentinel_agent | v1.0*
