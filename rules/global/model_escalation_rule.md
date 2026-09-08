---
id: model-escalation
name: Model Escalation And Independent Review
domain: orchestration
enforcement: strict
priority: critical
description: >
  Routes delegated Codex work to the minimum justified Luna, Terra, Sol, or Astra
  tier and requires separate falsification-oriented review for high-impact work.
version: 1.0.0
applyTo: [repo, agents, prompts, claude, codex]
canonical_location: core/orchestration/model_escalation_policy.yaml
adapter_stubs:
  - .codex/rules/model-escalation.md
---

# Model Escalation And Independent Review

Before delegating work, use the `model_route` returned by Negrita Brain. The
default is `gpt-5.6-luna` with medium reasoning. Escalation is based on the
declared task class, material risk signals, change impact, and review role. Do
not select a larger model merely because it is available.

Use Luna medium for bounded exploration, extraction, straightforward tests,
metadata inspection, mechanical validation, document QA, and comparisons with
explicit acceptance criteria. Use Luna high for focused review, read-only SQL,
bounded reproduction, reconciliation, limited-scope reasoning, compliance, and
approved-contract validation.

Escalate to Terra for material semantics, meaningful data-writing impact,
stateful V10 behavior, multi-stage reasoning, unresolved Luna ambiguity,
multiple plausible explanations, contract divergence, live/local evidence
conflict, new assumptions, or material reviewer disagreement. Escalate to Sol
for architecture, score/segmentation/evidence contract decisions, conflicting
cross-domain evidence, unresolved Terra debugging, high-impact irreversible
work, production-candidate final integration, disputed PASS/HOLD/FAIL, or
Terra-level disagreement.

Use Astra (`gpt-6-astra`, high) directly for an explicit Astra review request or
`exceptional_cross_domain_complexity`. Escalate unresolved Sol debugging and
Sol-level reviewer disagreements to Astra. Prior attempts with other models
are not required. At the highest tier, unresolved disagreement remains HOLD
for human resolution; it never becomes approval merely because no larger
model is available.

Give supporting subagents explicit model/effort settings. Selecting Astra for
the parent must not implicitly move mechanical tasks to Astra. Before spawning,
check that the runtime advertises the selected model/effort. If unavailable,
report BLOCKED_MODEL_ROUTING rather than silently switching models. Configuration
validation alone does not prove runtime availability.

Evaluate total cost per validated result, including failed attempts, retries
and every subagent. Use `templates/model_comparison_record.yaml`. Compare the
same acceptance contract and input evidence; missing usage is unknown, not zero.
Keep Codex credits and API USD separate. Token pricing alone cannot determine
which model is cheaper for a completed task. Benchmarks do not authorize paid
calls, automatic changes to routing, or relaxing quality gates.

An agent cannot provide the final independent review of its own work. High
impact requires a separate Terra-or-higher reviewer; production candidates
require a separate Sol-or-higher reviewer. The reviewer must try to falsify the
implementation. A different alias in the same provider task is not independent.
The review PASS is bound to a SHA-256 worktree fingerprint and required evidence
categories. `commit` remains blocked if the review is absent, too weak, open,
or stale. Evidence must resolve to a SHA-256-bound JSON receipt for the exact
reviewed worktree; a model-authored PASS string is not evidence. Agreement never
overrides missing evidence.

Material risk signals raise both the model tier and the minimum change impact.
Agents cannot keep `standard` impact when a declared signal requires `high` or
`production_candidate` review.

Missing required data, skipped gates, failed validation, unverified lineage,
or unresolved material ambiguity remains `HOLD`. A larger model never replaces
evidence or required user authorization. Once a semantic or architectural
decision is recorded, bounded implementation may return to Luna.

Claude and CI apply the same tier and evidence semantics but must not claim to
be a GPT-5.6 Luna, Terra, Sol, or GPT-6 Astra model. When exact model execution is required,
delegate through the corresponding Codex custom agent.

Contracts created before model routing must be refreshed with `resolve` before
commit. Every Git commit form, including `git -C`, `git -c`, absolute Git paths,
and command wrappers, is subject to the same commit gate.
