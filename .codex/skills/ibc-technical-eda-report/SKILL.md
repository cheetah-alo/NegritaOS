---
name: ibc-technical-eda-report
description: Use when creating, updating, auditing, or exporting IBC Fiber Network technical EDA DOCX/PDF reports, evidence packs, data-quality reports, source-readiness reports, join-readiness memos, trap/issue analysis reports, or ML-readiness documentation. Applies IBC source guardrails and calibrates report format against the IBC PON variables primer v5 when the user asks to keep the current IBC report style.
---

# IBC Technical EDA Report

## Purpose

Create IBC Fiber Network technical EDA reports that use CQI DOCX/PDF formatting
while preserving IBC-specific evidence boundaries: no premature joins, no
client-grain overclaim, no ML-readiness claim without gates.

This skill layers on `cqi-analytical-docx-pdf` and
`evidence-first-plot-analysis` when reports include analytical visuals.

## Required Context

Before creating or updating an IBC technical EDA DOCX/PDF, load:

1. `/Users/jackyb-cqi/repos/ibc_fiber_network/.codex/project.yaml`
2. `/Users/jackyb-cqi/repos/NegritaOS/projects/ibc_fiber_network.yaml`
3. IBC project memory index, when available from the local memory home declared
   by the registry.
4. `src/fiber_network_ml/config/tenants/ibc.yaml` when fields, source contracts,
   joins, or source semantics are discussed.
5. Relevant analysis README, YAML config, manifest, SQL, and output summaries.
6. `cqi-analytical-docx-pdf` and its IBC PON primer calibration reference when
   the user asks for the existing IBC report format.
7. `evidence-first-plot-analysis` for every plot, chart, EDA figure, or model
   diagnostic included in the report.

## Visual Calibration

When the user says to keep the IBC report format, use this reference:

`/Users/jackyb-cqi/repos/ibc_fiber_network/team-lead-qaqc/tenants/ibc/generated_outputs/ibc_pon_variables_primer/ibc_pon_variables_primer.v5.pdf`

That means:

- Start from CQI Word template, not blank DOCX.
- Preserve document control, index, cover/header/footer style.
- Use APA-style tables and figures.
- Add interpretation blocks for figures and analytical visuals.
- Separate observation, interpretation, and evidence boundary for every plot.
- End with traceability and next actions.
- Render to PDF and inspect every page.

## IBC Source Positions

Use these current positions unless newer owner-approved evidence supersedes
them:

- `trap_events`: analyze as isolated source for intensity, counts, recurrence,
  trend, lifecycle candidates, duplicate/id reuse/null/timestamp quality, and
  technical hotspots. Do not use it as direct customer-impact truth.
- `issues_on_subs`: current operational analysis rail for severity/category,
  lifecycle/resolution, scope, topology signals, location/exposure aggregates,
  and source-composition review.
- `issues_enrichment`: future expected table from Ale. Do not treat as available
  until received, profiled, and contract-reviewed.
- `ibc_asset_status_daily`: enrichment/source context, but joins require grain,
  time/as-of, cardinality, fanout, null, coverage, and owner approval.
- Cisco: out of initial scope unless the user explicitly opens a Cisco-specific
  track with contract and parser rules.

## IBC Guardrails

Do not claim:

- an approved `issues` to `traps` row-level join;
- `root` as an approved join to enrichment/location;
- client/customer as universal grain;
- `id` as unique event key;
- ML readiness from EDA alone;
- affected customers for OLT/PON/uplink/infrastructure alerts.

Use these states when communicating evidence:

- `OBSERVED`
- `CANDIDATE`
- `REVIEW`
- `HOLD_JOIN_FANOUT`
- `HOLD_CONTRACT_INCOMPLETE`
- `HOLD_ROOT_PARSE_NO_MATCH`
- `ML_HOLD_JOIN_KEY_UNRESOLVED`
- `NOT_MATERIALIZED`
- `N/D`

## Required Report Sections For IBC EDA

1. TLDR / executive decision.
2. Source scope and exclusions.
3. Current owner input and what changed.
4. Methodology and windows.
5. Evidence by source.
6. Allowed conclusions.
7. What is explicitly not concluded.
8. Operational implications.
9. Risks and FODA/SWOT when project decision support is requested.
10. Next actions with owner, dependency, acceptance criteria.
11. Traceability appendix: source paths, run IDs, scripts, render QA.

## Tables To Prefer

- Source scope matrix.
- Evidence status matrix.
- Analysis technique inventory.
- Field-family/composition matrix.
- Risk register.
- Next-action table with owner and acceptance criteria.

## QA Checklist

Before delivery:

- Confirm `trap_events` remains isolated unless a join has passed gates.
- Confirm `issues_on_subs` is operational/review, not ML-ready.
- Confirm `issues_enrichment` is future/pending if not yet received.
- Confirm Cisco is excluded unless explicitly in scope.
- Confirm no PII/raw serial/IP/subscription/address/message content is exposed.
- Confirm PDF/DOCX visual format follows `ibc_pon_variables_primer.v5.pdf` when
  requested.
- Render all pages and fix any layout defect before final response.
