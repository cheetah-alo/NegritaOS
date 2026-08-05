---
name: elal-rule-traceability
description: Enforces the canonical append-only ELAL rule, implementation, decision, and deck traceability control.
---

# ELAL Rule Traceability

Use this skill for every ELAL change or claim involving a rule, source rail,
outcome, score, state, chip, treatment, taxonomy, association/deduplication,
implementation, or rule-related deck.

The canonical control lives in NegritaOS:

- `projects/elal_rule_traceability.yaml` — append-only ledger.
- `projects/elal_rule_traceability.md` — operating contract.
- `scripts/validate_rule_traceability.py` — structural and immutable-source
  integrity validator.

The recorded sources live in the external `proj_data_analytics` repository.
They are evidence, not files to copy into or out of NegritaOS. Resolve every
source, contract, and implementation path relative to `source_repository.root`
in the ledger.

## Non-bypass gate

Before applying or presenting a rule-related ELAL change:

1. Read `projects/proj_data_analytics.yaml` and the ledger.
2. Identify each affected `rule_registry` identifier and current state.
3. Add a `PROPOSED` record before implementation, including source, contract,
   implementation, validation, owner decision, policy effect, and deck/product
   impact.
4. Keep `CALLS.calls_fric_prom_w_metadata` and deprecated `CALLS.ia_calls`
   separate. A broad additive union or `FULL OUTER JOIN` is prohibited.
5. Do not call a backtest, candidate, or Arik-review observation productive or
   approved without the owner decision recorded in a later append-only entry.
6. Run the validator and its focused regression test after every ledger change.

For a deck, cite the applicable ledger change ID and controlled rule state in
the speaker-note evidence block. If no later record applies, cite
`BASELINE-2026-08-04-ELAL-RULES`.
