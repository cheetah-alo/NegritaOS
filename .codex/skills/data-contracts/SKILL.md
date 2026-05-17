---
name: data-contracts
description: >
  Repository data contracts, schema validation, casting rules, and contract-driven errors.
  Use when modifying contract files, validation behavior, or schema-enforced transformations.
---

# Data Contracts

Use when modifying data contracts, schema validation, typed normalization, or contract-driven error behavior.

## Quick scope

- Contract JSONs: `backend/app/configs/*.json`
- API contract surface: `backend/app/api/rules_api_contract.json`
- Contract/profile loading: `backend/app/configs/profile_loader.py`
- Services enforcing contract-like rules: `backend/app/services/transaction_buc_metadata.py`, `backend/app/services/budget_buc.py`, `backend/app/services/financial_kpis.py`

## Workflow

1. Identify the source of truth for the schema or contract.
2. Validate required fields, naming, nullability, and supported values explicitly.
3. Keep casting and normalization behavior deterministic and visible.
4. Raise stable errors when a contract is violated.

## Guardrails

- Do not duplicate schema semantics across multiple modules.
- Prefer declarative contracts or clearly named validation functions.
- Update tests when contract semantics change.
