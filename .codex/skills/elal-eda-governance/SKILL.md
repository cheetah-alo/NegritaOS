---
name: elal-eda-governance
description: >
  Opt-in ELAL EDA semantics for raw operational severity, IA call taxonomy
  proxies, BLOCKED_DATA/BLOCKED_NO_SUPPORT states, and third-subtitle evidence.
  Use only for governed ELAL passenger-journey EDA packages.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, data_analytics]
  auto_invoke: false
---

# ELAL EDA Governance

Apply only when the project or analysis explicitly selects the
`elal-eda-governance` profile. Keep these semantics out of HOT, IBC, PostgreSQL,
and generic EDA contracts.

Required distinctions:

- raw operational severity is separate from score-derived state;
- `IA_CALL_TAXONOMY_PROXY` is a proxy and is not confirmed denied boarding;
- `BLOCKED_NO_SUPPORT` means no defensible intersection, not zero prevalence;
- `BLOCKED_DATA` means the required source/window is unavailable;
- a valid zero remains distinct from both blocked states;
- canonical plots expose snapshot, window, grain, denominator, and source in
  the third subtitle, not footer metadata.
