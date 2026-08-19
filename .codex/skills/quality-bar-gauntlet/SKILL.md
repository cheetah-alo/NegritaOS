---
name: quality-bar-gauntlet
description: >
  Runs a benchmark-driven quality loop with a separate builder and critic.
  Trigger: quality gauntlet, gauntlet this, compare against a reference,
  beat this benchmark, quality bar review, QG, or when a high-stakes code,
  dashboard, DOCX, PDF, PPTX, plot, research, or design deliverable needs
  evidence that it meets a real comparable bar.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, backend, frontend, data_analytics]
  auto_invoke:
    - "Run a quality gauntlet, benchmark comparison, or beat-this-reference loop"
    - "Use a named reference to judge code, dashboards, plots, PPTX, DOCX, PDF, or research deliverables"
    - "Create a separate builder and critic loop for high-stakes output"
---

# Quality Bar Gauntlet

Use this skill when the user asks for a benchmarked quality loop or when an
important artifact needs a real, comparable quality bar. This is a NegritaOS
adaptation of the gauntlet-loop evaluator pattern; apply NegritaOS routing,
Brain gates, evidence rules, and document-control policies first.

## Required Contract

Before writing or revising the artifact, define a quality bar that is:

- Named: a specific page, repo, paper, deck, DOCX, report, plot, benchmark, or
  test suite.
- Fetchable: the agent can read, run, render, screenshot, or inspect it.
- Comparable: the candidate and reference can be judged side by side.
- Evidence-backed: the pass/fail claim cites exact commands, renders, paths,
  screenshots, tests, or source documents.

If the user did not provide a bar, propose two or three candidate bars and stop
for selection. Do not invent a vague category such as "best in class".

## Execution Pattern

1. Resolve the active NegritaOS project, mode, profile, rules, and gates.
2. Load the domain skills for the artifact: PR/code, dashboard, plot, PPTX,
   DOCX/PDF, research, or model review.
3. Fill `templates/quality_bar_contract.yaml` or an equivalent compact note.
4. Split the artifact into judgeable units such as API contract, query logic,
   chart narrative, slide flow, document structure, visual polish, or tests.
5. Use a builder and a separate critic. The critic must inspect the actual
   output with fresh context and name the largest remaining gap.
6. Iterate only while there is actionable evidence and budget/time remains.
7. Run a smoothing pass across the assembled result so locally improved pieces
   still work together.
8. Report PASS, PASS_WITH_WARNINGS, FAIL, or BLOCKED with evidence.

## Domain Routing

| Work type | Required companion |
|---|---|
| Code, PR, refactor | `pull-request-risk-review`, `pr-review-deep`, `testing-coverage`, and project CI gates |
| Dashboard/UI | `analytical-dashboard-architecture`, frontend skills, Playwright/browser QA when runnable |
| PPTX/deck | `cqi-analytical-pptx`, `analytics-storytelling-deck`, render/screenshot QA |
| DOCX/PDF/report | `cqi-analytical-docx-pdf`, `document-control`, render-to-PNG QA |
| Plots/EDA | `evidence-first-plot-analysis`, `analytical-eda-governance`, source-quality gates |
| Research/TFM | `tfm-research-advisor`, `research-paper-findings`, current source verification |

## Hard Stops

- No self-approval: the same context that built the artifact cannot be the only
  judge.
- No hallucinated references: if the bar cannot be fetched or inspected, mark
  `BLOCKED_REFERENCE_UNAVAILABLE`.
- No hidden provider swaps, paid APIs, or long loops without user approval.
- No claim that data, CI, browser state, publication, or rendering passed unless
  that exact evidence exists.
- No fixed round count as proof of completion. Stop only when the bar is met,
  the user stops the run, or a blocker/budget limit is reached.
- Never weaken tests, ignore evidence gaps, or rewrite expectations just to
  declare a win.

## Output

Return a compact audit trail:

```yaml
quality_bar:
  reference: ""
  named: true
  fetchable: true
  comparable: true
artifact_under_review: ""
builder_units: []
critic_findings: []
evidence:
  commands: []
  rendered_outputs: []
  source_paths: []
result: PASS | PASS_WITH_WARNINGS | FAIL | BLOCKED
largest_remaining_gap: ""
next_action: ""
```

## Invocation Examples

```text
@agent:QG gauntlet this PR against the required CI, current dev branch, and the
project's own PR quality gates.
```

```text
@agent:QG audit this PPTX against the CQI reference deck. Render both to images,
compare slide flow, chart readability, evidence notes, and executive narrative.
```

```text
@agent:QG review this DOCX/PDF against the approved CQI report template and IBC
calibration report. Preserve source claims, APA figure/table style, and render QA.
```

## Resources

- Source provenance: `references/source-provenance.md`.
- Usage guide: `docs/quality-bar-gauntlet.md`.
- Contract template: `templates/quality_bar_contract.yaml`.
