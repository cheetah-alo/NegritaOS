# Skill: Reproducibility Review

**Type:** Domain — Engineering
**Applicable agents:** code_review_agent

## Purpose
Checks whether a workflow can be rerun by another engineer with the same expected result.

## Checks
- Inputs, environment, and commands are documented.
- Randomness is controlled where relevant.
- Outputs are written to predictable locations.
- Dependencies and credentials are separated.
- Results can be traced to source data and code version.
