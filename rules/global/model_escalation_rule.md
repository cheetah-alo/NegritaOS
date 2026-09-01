---
id: model-escalation
name: Model Escalation And Independent Review
domain: orchestration
enforcement: strict
priority: critical
description: >
  Routes delegated Codex work to the minimum justified Luna, Terra, or Sol
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

An agent cannot provide the final independent review of its own work. High
impact requires a separate Terra-or-higher reviewer; production candidates
require a separate Sol reviewer. The reviewer must try to falsify the
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
be a GPT-5.6 Luna, Terra, or Sol model. When exact model execution is required,
delegate through the corresponding Codex custom agent.

Contracts created before model routing must be refreshed with `resolve` before
commit. Every Git commit form, including `git -C`, `git -c`, absolute Git paths,
and command wrappers, is subject to the same commit gate.
