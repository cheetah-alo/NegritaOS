# ELAL rule and implementation traceability

Status: active control contract as of 2026-08-04.

## Purpose and canonical ledger

The ELAL rule system already has organized source material: governed taxonomy
PDFs, the technical rule DOCX, Markdown contracts, SQL/Python implementation,
backtests, Arik-review material, and decision decks. The missing control was a
single, reviewable route between them when a rule changes.

[`elal_rule_traceability.yaml`](elal_rule_traceability.yaml)
is the canonical traceability ledger. It connects each rule to its source
evidence, contract, implementation artifact, validation, decision state, and
deck/product impact. This document defines how to use the ledger; it does not
replace any business, outcome, or data contract.

## Source preservation

The PDF and DOCX source artifacts recorded in the ledger are immutable evidence.
Do not move, rename, save over, normalize, or regenerate them as part of
organization or implementation work. The ledger records their SHA-256 digests
and observed page counts so an audit can identify exactly what was reviewed.

The 2026-07-29 technical DOCX remains a historical baseline. Its historical
active-call scope is superseded only for the active EDA rail by
[`elal_fr_pr_call_contract.md`](elal_fr_pr_call_contract.md), version
`direct_metadata_v3`. Retaining the older document does not reactivate its
superseded source claim.

## Required traceability route

For every proposed or implemented change to an ELAL score, state, chip,
treatment, source rail, outcome rule, taxonomy, association/deduplication,
dashboard behavior, or rule-related deck claim, capture this route:

```text
source evidence -> governed contract -> implementation -> validation
                -> owner decision -> product/deck impact
```

Use a rule identifier already in `rule_registry` where it applies. Add a new
rule identifier before implementing a genuinely new rule; do not repurpose an
unrelated identifier to make a change appear historical.

## Append-only change protocol

1. Add a `PROPOSED` change record before implementation. It must identify the
   affected rule IDs, source evidence, contracts, implementation paths,
   intended validation, decision owner, policy effect, and deck/product impact.
2. Run the named validation and retain its result in a later record. A backtest,
   an observed signal, or an Arik-review comment is not by itself an approval.
3. Record the owner decision as `APPROVED`, `REJECTED`, or `DEFERRED`. Only an
   explicit approval can support a productive-policy claim.
4. When applied, append an `IMPLEMENTED` record that points to the proposal in
   `previous_change_id` and, if applicable, `supersedes`. Never edit or delete
   the earlier record to rewrite history.
5. If a prior record is wrong or withdrawn, append a corrective record with
   `supersedes`; preserve the original evidence and explain the correction.

The control protects decision sequence; it does not grant permission to change
a productive rule. Normal implementation and owner approval gates still apply.

## Non-negotiable current boundaries

- The active EDA call rail is `CALLS.calls_fric_prom_w_metadata` under
  `direct_metadata_v3`. `CALLS.ia_calls` is deprecated for this EDA. Never use
  a broad additive union or `FULL OUTER JOIN` to combine the rails.
- Outcome evidence must come from the governed flight-completion or refund
  source defined by `outcomes_contract.md`. Transcript language such as
  `resolved` or `acknowledged` is a signal, not a verified operational outcome.
- Tier controls treatment and priority, not the underlying pressure score;
  the severe chip is contextual and does not directly override colour or state.
- Same-date V9/V10 comparisons are a reclassification crosswalk, not proof of
  temporal recovery, flapping, or prior-day movement.
- `Seat Overbooking`, call-classification S3, and recovery S5 retain the state
  recorded in the ledger. They must not be presented as productive merely
  because they have a backtest or an audit finding.

## Deck and audit use

Every rule, audit, or Arik-response deck must cite the applicable ledger change
ID (or `BASELINE-2026-08-04-ELAL-RULES` if no later change applies) in its
speaker-note `[Evidence]` block. The note must also state whether the claim is
current baseline, active data contract, context-only, shadow candidate,
insufficient evidence, or deprecated.

This requirement is enforced by the ELAL Product Owner presentation skill. It
does not alter source PPTX files or make a candidate claim approved.

## Local validation

Run the ledger validator after every ledger change:

```bash
uv run python /Users/jackyb-cqi/repos/NegritaOS/.codex/skills/elal-rule-traceability/scripts/validate_rule_traceability.py
```

It verifies controlled states, unique identifiers, append-only chain links,
source/contract/implementation references, immutable PDF/DOCX digest format,
and required decision/impact fields. It validates the structure and repository
references; it does not certify business approval or execute SQL.

Run the focused regression test as well:

```bash
uv run python -m unittest discover \
  -s /Users/jackyb-cqi/repos/NegritaOS/.codex/skills/elal-rule-traceability/tests \
  -p 'test_elal_rule_traceability_contract.py'
```
