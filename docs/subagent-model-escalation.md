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

These TOML agents are global defaults and are materialized into every
NegritaOS adapter. Project-specific agents may have a canonical tier override.

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
Terra, or Sol. When the exact model is required, the work must be delegated to
the corresponding Codex custom agent.
