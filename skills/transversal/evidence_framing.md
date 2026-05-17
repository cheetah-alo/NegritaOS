# Skill: Evidence Framing

**Type:** Transversal
**Applicable agents:** All

## Purpose
Governs how claims are labeled, sourced, and bounded across all outputs.
Ensures that the distinction between fact, inference, and hypothesis is always explicit.

## Evidence Classification System

| Label | Definition | Required Action |
|---|---|---|
| `CONFIRMED` | Directly observed, measured, or cited from a credible source | State the source or data point |
| `PROBABLE` | Strongly suggested by evidence but not directly measured | State the supporting evidence |
| `HYPOTHESIS` | Plausible interpretation requiring further validation | Label explicitly; suggest validation path |
| `ASSUMPTION` | Unverified premise the analysis depends on | State it upfront; note if it is testable |
| `SPECULATION` | No evidentiary basis | Do not include. If present in input, flag and discard. |

## Application Rules

1. Every claim in an output must carry one of the above labels, either explicitly or by position:
   - Claims in the **Evidence** section: treated as CONFIRMED or PROBABLE
   - Claims in the **Interpretation** section: may be PROBABLE or HYPOTHESIS
   - Claims in the **Recommendations** section: must reference CONFIRMED or PROBABLE findings

2. Never present a HYPOTHESIS as a CONFIRMED finding.

3. When evidence is missing, state what is missing and what it would take to confirm the claim:
   > "HYPOTHESIS: The model overfit on temporal features. Requires time-based cross-validation to confirm."

4. When sources are cited:
   - Academic: Author, Year, Title, Venue
   - Web: Title, URL, Date accessed
   - Internal: Dataset name, version, extraction date

## Anti-Patterns

- "The data shows X" when the data only suggests X
- Recommendations without traceable supporting evidence
- Citing a source without specifying what claim it supports
- Using hedging language to imply certainty: "it seems likely that..." as if it is settled
