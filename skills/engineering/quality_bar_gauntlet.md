# Quality Bar Gauntlet

## Purpose

Use this workflow when NegritaOS must prove that a high-stakes artifact is
better than "good enough" by comparing it against a concrete reference. The
artifact can be code, a PR, dashboard, plot, PPTX, DOCX, PDF, research brief, or
model-review output.

This is a benchmarked evaluator loop, not a replacement for project rules. Load
the active project registry, skills, rules, rubrics, Brain gates, and domain
contracts first.

## Fit Criteria

Use this workflow when at least one condition is true:

- The user asks for `QG`, `quality gauntlet`, `gauntlet this`, or benchmarked
  comparison.
- A deliverable will be used by stakeholders, leadership, reviewers, or a PR
  gate.
- There is a real reference artifact to beat or match.
- The risk of self-approval is high.

Skip it for small edits, one-line fixes, routine formatting, or low-risk
answers where normal rules and tests are enough.

## Quality Bar Contract

The bar must be:

- Named: exact repo, URL, report, paper, deck, template, screenshot, benchmark,
  or test suite.
- Fetchable: readable, runnable, renderable, or inspectable by the agent.
- Comparable: the candidate and reference can be judged side by side.
- Relevant: same task class, audience, format, and constraints.

If no bar is supplied, propose two or three options and wait. Do not continue
with a vague benchmark.

## Roles

| Role | Responsibility |
|---|---|
| Lead | Defines the bar, budget, units, evidence, and stopping condition. |
| Builder | Improves one unit of the artifact. |
| Critic | Uses fresh context to inspect the actual output against the bar. |
| Smoother | Reviews the assembled artifact for consistency after unit-level work. |

The builder cannot be the only judge. The critic must use actual evidence:
rendered pages, screenshots, tests, diffs, query output, source documents, or
published references.

## Domain Evidence

| Domain | Minimum evidence |
|---|---|
| Code or PR | Diff, tests, coverage/CI status, lint/type/security checks, benchmark when applicable. |
| Dashboard or UI | Browser screenshot at matching viewport, interaction path, console/network status when available. |
| PPTX | Rendered slides, reference deck/template, speaker-note evidence, slide-flow audit. |
| DOCX or PDF | Template/source files, rendered pages or PDF-to-PNG QA, figure/table numbering, source traceability. |
| Plots or EDA | Source grain, filters, denominator, calculation, plot rendering, evidence boundary. |
| Research or TFM | Papers, datasets, method comparison, limitation check, citation/source audit. |

## Stopping Conditions

Stop when:

- the critic selects the candidate over the reference with evidence;
- the user stops the run;
- the declared budget or time limit is reached;
- the reference is unavailable;
- the artifact cannot be tested/rendered/read with available tools;
- NegritaOS Brain or project gates return `BLOCK`.

Never use a fixed number of rounds as proof of quality.

## Output Contract

Use `templates/quality_bar_contract.yaml` when a file artifact is useful. For
chat-only work, include the same fields in the response:

- reference and why it is valid;
- artifact and units reviewed;
- builder/critic separation method;
- exact evidence used;
- largest remaining gap;
- result: `PASS`, `PASS_WITH_WARNINGS`, `FAIL`, or `BLOCKED`;
- next action.

## Anti-Gaming Rules

- Do not weaken tests or expectations to win the comparison.
- Do not claim a reference was inspected if it was only described.
- Do not hide missing browser, data, CI, or rendering evidence.
- Do not use paid APIs, external publishing, or long-running loops without
  explicit approval.
- Do not over-optimize one section while breaking cross-document or
  cross-application flow.
