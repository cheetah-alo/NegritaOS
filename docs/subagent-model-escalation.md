# Subagent Model Escalation

Negrita Brain selects the minimum justified Codex model tier for delegated
work in every registered project. The source of truth is
`core/orchestration/model_escalation_policy.yaml`; project registries do not
duplicate the policy.

## Available Subagents

| Agent | Model | Use |
|---|---|---|
| `luna-worker` | GPT-5.6 Luna, medium | Exploration, extraction, tests, metadata, mechanical validation, document QA |
| `luna-reviewer` | GPT-5.6 Luna, high | Focused code/SQL review, reproduction, reconciliation, approved-contract checks |
| `terra-reviewer` | GPT-5.6 Terra, high | Material ambiguity, semantics, lineage, multi-stage discrepancies, high-impact review |
| `sol-integrator` | GPT-5.6 Sol, high | Architecture, contract decisions, disputed results, production-candidate integration |
| `astra-reviewer` | GPT-6 Astra, high | Explicit Astra requests, exceptional cross-domain complexity, unresolved Sol investigations and disagreements |
| `gisel` | GPT-5.6 Luna, high | Evidence-based project-hours workbook creation and QA |
| `vera` | GPT-5.6 Terra, high | Evidence-bound ML, analytical-rule, and hybrid model governance cards |
| `pablo` | GPT-5.6 Luna, high | TepuFlow deployment operations; globally discoverable but scoped to `moneyflowlist` |
| `casilda` | GPT-5.6 Terra, high | TepuFlow functional QA; globally discoverable but scoped to `moneyflowlist` |
| `casilda-flows` | GPT-5.6 Terra, high | TepuFlow lifecycle adversarial QA; globally discoverable but scoped to `moneyflowlist` |

These TOML agents are global defaults and are materialized into every
NegritaOS adapter. Project-specific agents may have a canonical tier override.

## Astra And Cost Per Result

Use `@agent:Astra` or `@agent:Astral` for mode `ASTRA`, resolved globally to
`astra_review_agent`. The Codex native subagent is `astra-reviewer`; Claude's
native wrapper is `astra` and applies the protocol without claiming to run GPT-6.

```bash
python3 scripts/negrita_brain.py resolve --root "$PWD" --provider codex --action astra_review
```

For a different domain action, declare `--risk-signal exceptional_cross_domain_complexity`.
`sol_unresolved_debugging` and `sol_reviewer_disagreement` also select Astra.
Selection is direct: there is no obligation to try Luna, Terra and Sol first.
Ordinary production review still has Sol as its minimum; Astra is not mandatory
for every release. Model selection never substitutes for missing evidence.

Set worker models explicitly even when the parent uses Astra. An unconfigured
subagent may inherit its parent's model and reasoning effort. Confirm model/effort
availability in the runtime before spawning. A model can be available while a
new named profile still requires a fresh session for discovery. Never claim a
role is hot-loaded or substitute another model without saying so.

Compare actual task totals with `templates/model_comparison_record.yaml`: same
input hashes, acceptance contract and quality bar; include failures, retries,
subagents, elapsed time and usage receipts. Missing usage remains null and the
comparison stays `INSUFFICIENT_EVIDENCE`. A trial that did not achieve a validated
result is not a cheap successful result. Do not mix API USD and Codex credits.
No price table is hardcoded into routing; verify the applicable rate card for
each comparison. No benchmark has been run merely by installing this profile.

Suggested prompt:

```text
Use astra-reviewer for an independent review of builder session <id>.
Delegate inventory and mechanical checks to luna-worker explicitly.
Keep missing evidence as HOLD and report total usage when available.
```

Official references, checked 2026-09-08:
[Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
[subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Codex pricing](https://learn.chatgpt.com/docs/pricing).
The canonical policy and this guide are owned by NegritaOS maintainers and must
be updated together when routing, availability or evidence requirements change.

They are also linked into `~/.codex/agents/` so new Codex sessions can discover
the same roles outside a particular adapter. Run:

```bash
python3 scripts/sync_codex_custom_agents.py --user-home --all-projects --write
python3 scripts/validate_codex_custom_agents.py --user-home --all-projects
```

Agent discovery occurs when a Codex session starts. A session opened before a
profile was added must be restarted; changing files cannot retrofit the role
catalog already attached to an active session.

## Resolve Before Delegating

Default bounded work:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve \
  --root "$PWD" --provider codex --action implementation \
  --delegation-class repository_exploration
```

Material semantic risk:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve \
  --root "$PWD" --provider codex --action code_review \
  --risk-signal semantic_contract_change --change-impact high
```

Independent production-candidate review:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve \
  --root "$PWD" --provider codex --action pull_request_review \
  --change-impact production_candidate \
  --review-role independent_reviewer \
  --review-of-session NBS-<project>-<builder-session>
```

The independent-review command must run in a different Codex task/session from
the builder. Negrita Brain compares provider-native task identities, so changing
only `--session-key` does not create an independent reviewer. Resolution seals a
SHA-256 fingerprint of HEAD-relative tracked changes plus untracked content.

The reviewer closes the review with hashed, machine-readable evidence receipts.
Each receipt must use schema version 1, name its category and reviewed worktree
fingerprint, and record either a passing command with exit code 0 or an approved
`NOT_APPLICABLE` reason. Receipts live under canonical project memory or a
Git-ignored repository path; a free-form claim is rejected.

Example PASS receipt:

```json
{
  "schema_version": 1,
  "category": "applicable_tests",
  "status": "PASS",
  "subject_worktree_sha256": "<reviewed_worktree_sha256>",
  "completed_at": "2026-09-01T18:00:00+02:00",
  "command": "python3 -m unittest discover -s tests",
  "exit_code": 0
}
```

Close the review using the receipt path and its SHA-256:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py close \
  --root "$PWD" --provider codex --status PASS \
  --evidence-ref \
  'applicable_tests=memory:runtime/sessions/<review-session>/evidence/tests.json@sha256:<64_hex>'
```

`applicable_tests` cannot be `NOT_APPLICABLE`. Categories whose names explicitly
say "when applicable" may use `NOT_APPLICABLE`, but their receipt must include a
specific `reason` and `authorized_by`. If a receipt, its hash, or the worktree
changes, the PASS becomes invalid. The builder's `gate --action commit` remains
`BLOCK` until a separate, sufficiently ranked Codex reviewer closes PASS over
the current fingerprint.

Sessions created before this policy are never grandfathered into a commit.
Re-run `resolve` in the original builder task to create a current contract;
Brain returns a specific refresh reason instead of crashing on legacy fields.

## Invocation In Codex

After reading `model_route`, ask Codex directly:

```text
Spawn luna-worker to inventory the repository and return exact paths only.
Spawn luna-reviewer to review this SQL read-only against the approved contract.
Spawn terra-reviewer as an independent reviewer of builder session <id>.
Spawn sol-integrator for the final production-candidate integration review.
```

Do not ask a larger model to compensate for missing data, skipped tests,
unverified lineage, failed validation, or missing user authorization. Those
conditions remain `HOLD`.

Material signals automatically raise review impact. For example,
`semantic_contract_change` implies `high`, while
`production_candidate_final_review` implies `production_candidate`; leaving
`--change-impact` at its default cannot bypass the independent-review gate.

## Claude Boundary

Claude loads the same rule and must follow its evidence and escalation
semantics. On every user prompt, the hook closes the prior prompt contract and
creates a prompt-specific contract using only safe action/risk labels; prompt
text is neither logged nor persisted. Claude cannot claim to be GPT-5.6 Luna,
Terra, Sol, or GPT-6 Astra. When the exact model is required, the work must be delegated to
the corresponding Codex custom agent.
