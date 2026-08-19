# Quality Bar Gauntlet

## Purpose

Quality Bar Gauntlet is the NegritaOS workflow for high-stakes work that must
be judged against a real benchmark instead of the same agent's opinion. It uses
a lead, a builder, a separate critic, and a final smoothing pass.

Use it when you want the output to meet or beat a named reference: a repo, PR
standard, test suite, dashboard, deck, DOCX/PDF template, plot, paper, or report.

## How To Invoke

In Codex:

```text
@agent:QG gauntlet this against <reference>.
```

In Claude:

```text
QG: gauntlet this against <reference>.
```

If Claude supports `/loop` and agent teams in the active project, it can use
them as an execution convenience. The NegritaOS contract remains the same:
separate builder and critic, actual artifact inspection, and evidence-backed
result.

If no reference is supplied, the agent proposes two or three candidate bars and
waits for selection. It must not continue with a vague benchmark such as
"best-in-class" or "professional quality".

## Required Reference Bar

The reference must be:

- Named: exact URL, repo, deck, report, template, paper, screenshot, benchmark,
  or test suite.
- Fetchable: the agent can read, run, render, screenshot, or inspect it.
- Comparable: the candidate and reference can be judged side by side.
- Relevant: same audience, format, domain, and constraints.

## Code And PR Usage

Use QG when a PR, refactor, or new module is high-risk or when you want more
than normal review.

```text
@agent:QG review this PR against the current dev branch, required CI checks,
the PR quality toolchain, and the project's existing implementation patterns.
```

Minimum evidence:

- `git diff` or PR diff inspected.
- tests and coverage status reported.
- lint/type/security checks reported when available.
- architecture/risk gaps passed to `code_review_agent`,
  `pull_request_reviewer_agent`, or `software_architect_agent`.
- no self-approval by the builder.

Use the PR-specific reviewer first when the task is a merge gate:

```text
@agent:PRR review PR #<number>. Then run @agent:QG if it needs benchmarked
comparison or an independent critic loop.
```

## Dashboard And UI Usage

```text
@agent:QG audit this dashboard against <reference dashboard URL>. Compare the
same desktop and mobile viewports, interaction flow, chart readability, loading
states, and evidence boundaries.
```

Minimum evidence:

- screenshots from matching viewport sizes;
- browser or Playwright results when runnable;
- console/network status when available;
- connected flow checks, not isolated static screenshots.

## PPTX Usage

```text
@agent:QG audit this PPTX against the CQI reference deck. Check slide flow,
one-message-per-slide discipline, chart readability, evidence notes, template
alignment, and executive narrative.
```

Minimum evidence:

- source PPTX path and reference deck path;
- rendered slide images or equivalent visual QA;
- speaker-note evidence audit when notes exist;
- `cqi-analytical-pptx` and `analytics-storytelling-deck` loaded;
- pass/warn/fail result with the largest remaining gap.

## DOCX And PDF Usage

```text
@agent:QG audit this DOCX/PDF against the approved CQI report template and the
selected calibration report. Check structure, tone, figure/table treatment,
source traceability, render quality, and evidence limits.
```

Minimum evidence:

- user-selected output/storage path for new deliverables;
- source document and reference paths;
- DOCX/PDF render or page inspection;
- figure/table numbering and text-reference consistency;
- `document-control` and `cqi-analytical-docx-pdf` loaded;
- SHA-256/provenance recorded when producing a deliverable.

## Plot And EDA Usage

```text
@agent:QG compare these plots against <reference plot/report>. Judge axis
clarity, denominator, grain, annotation, business readability, and whether the
text overclaims what the plot proves.
```

Minimum evidence:

- plotted data grain, filters, denominator, and time window;
- actual image/render inspected;
- source-quality status for governed analyses;
- plot claim separated into observation, interpretation, and boundary.

## Output Status

The result must be one of:

- `PASS`: the critic selects the candidate over the bar with evidence.
- `PASS_WITH_WARNINGS`: usable, but with explicitly bounded gaps.
- `FAIL`: the candidate does not meet the bar.
- `BLOCKED`: missing reference, tools, permissions, data, Brain gate, or
  required evidence.

## Maintenance

The canonical skill is
`.codex/skills/quality-bar-gauntlet/SKILL.md`.

The native agent guidance is
`skills/engineering/quality_bar_gauntlet.md`.

The reusable contract template is
`templates/quality_bar_contract.yaml`.

When the workflow changes, update all three files and refresh
`skills/catalog.yaml`, `.codex/skills/AGENTS.md`, `.codex/skills/README.md`,
`integrator.yaml`, and `core/orchestration/metaagent_router.yaml`.
