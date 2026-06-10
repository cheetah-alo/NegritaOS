---
id: plotting-guidelines
domain: ml-eda
enforcement: advisory
depends_on: [coding-standards, naming-guidelines, dev-python]
provides: [plot-standards, business-focused-visuals, premodel-evaluation-plots]
description: >
  Standards for business-quality plots during EDA and pre-model decision phases.
  Full spec in skills/plotting-guidelines/SKILL.md.
version: 1.1.0
applyTo: [plotting, eda, visualization]
priority: warning
see_also: skills/plotting-guidelines/SKILL.md
---

# Plotting Guidelines — Quick Reference

Full specification: load the `plotting-guidelines` skill.

## Non-negotiable rules (enforced here)

- Every plot MUST have an explicit X-axis label, Y-axis label (with units), and title.
- Title pattern: `<Metric> by <Dimension> — N={n:,} | <Period>`. Embed sample size and KPI.
- Subtitle: required when calculation method or feature derivation is non-obvious.
- Business-facing analytical plots MUST state population/filter, denominator, support threshold, and KPI window.
- If a plot compares against a baseline, the overall/base rate MUST be visible for every KPI being compared.
- Labels must include nominal support (`n`) whenever rates, percentages, lifts, or ranks are shown.
- Do not put more than two subplots in a single output. Split dense plots into multiple named outputs.
- Legend default: `loc="upper center", bbox_to_anchor=(0.5, 0.97)` — top-center, below subtitle, no overlap.
- Long legends (> 4 items): `loc="lower center", bbox_to_anchor=(0.5, -0.18), ncols=2|3` — below axes, centered, no Y-axis overlap.
- Never use `loc="best"` on dense charts.
- Always call `fig.tight_layout()` or set explicit `subplots_adjust` margins.
- Color palette: seaborn `colorblind` or `cividis`/`viridis` — never default matplotlib cycle.
- Plots must answer a named business or pre-model question; decorative plots are forbidden.
- Future-looking outcomes such as `leads_to_*` must be described as temporal association within the window, not causal impact.
- Extraction coverage states must be separated: `processed but no signal` is not the same as `not processed`.
- Generated plot runs should maintain an artifact manifest or registry with source function, input, output path, denominator, filters, metrics, support threshold, and split dimensions.

## See skill for

- Full title/subtitle code patterns with N, KPI, feature calculation embedding
- Axis tick formatters (human scale: K/M, date formats)
- `plot_time_series()` reference helper function
- Agile evidence-contract then visual-contract workflow
- Processed-vs-missing signal guardrails
- PR review checklist (9 items)
- Forbidden patterns list
