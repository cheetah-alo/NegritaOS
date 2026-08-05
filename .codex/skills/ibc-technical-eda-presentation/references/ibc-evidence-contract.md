# IBC Evidence Contract

## Required Fields

Every analytical claim in an IBC deck must be traceable to:

- source table or output artifact;
- observation window or snapshot;
- grain;
- population;
- denominator;
- association or bridge rule;
- deduplication rule;
- evidence state;
- limitation;
- allowed conclusion.

## Join Evidence

For joins between `issues_on_subs`, `trap_events`, and
`ibc_asset_status_daily`, record:

- join key candidate;
- normalization applied;
- time/as-of rule;
- expected cardinality;
- observed fanout;
- null rates in join fields;
- unmatched/residual count;
- duplicate handling;
- privacy/export limits;
- source-owner approval status.

## Prohibited Claims

- Do not call a join canonical because field names look similar.
- Do not call a dataset ML-ready from match rate alone.
- Do not use trap `id` as the exact duplicate definition.
- Do not collapse UP and DOWN trap events unless the analysis explicitly
  validates an aggregation grain.
- Do not export raw serials, IPs, addresses, subscriptions, customer identifiers,
  message text, or root values when hashes/counts are sufficient.
