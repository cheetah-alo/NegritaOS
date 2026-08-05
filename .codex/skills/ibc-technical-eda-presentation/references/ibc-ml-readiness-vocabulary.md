# IBC ML-Readiness Vocabulary

## Approved States

| State | Meaning |
|---|---|
| `OBSERVED` | Directly observed in the declared source/window. |
| `CANDIDATE` | Mechanically possible but not semantically approved. |
| `REVIEW` | Needs source-owner or product-owner decision. |
| `HOLD_JOIN_FANOUT` | Join creates row multiplication or ambiguous context. |
| `HOLD_CONTRACT_INCOMPLETE` | Source contract lacks required schema/time/grain fields. |
| `ML_HOLD_JOIN_KEY_UNRESOLVED` | No approved key bridges the needed sources. |
| `ML_HOLD_DUPLICATES` | Duplicate grain blocks candidate ML table construction. |
| `ML_HOLD_REQUIRED_NULLS` | Required fields contain nulls above the approved threshold. |
| `NOT_MATERIALIZED` | Planned artifact or table has not been built yet. |
| `N/D` | Not applicable or not determined; explain which one. |

## Recommended Wording

- Use "candidate ML table" before owner approval.
- Use "mechanically viable" only for joins that pass fanout/coverage tests.
- Use "source-owner review" when semantics are unconfirmed.
- Use "not approved for production" when the analysis is exploratory.
