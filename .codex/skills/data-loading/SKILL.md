---
name: data-loading
description: >
  Repository data loading, ingestion, source resolution, and lineage-aware input handling.
  Use when changing ingestion logic, parser behavior, source resolution, or loading workflows.
---

# Data Loading

Use when modifying input ingestion, parser logic, source resolution, or deterministic loading behavior.

## Quick scope

- Ingestion service: `backend/app/services/ingestion.py`
- Transaction ingestion orchestration: `backend/app/services/transaction_ingest_service.py`
- Parsers and normalization-adjacent loading helpers: `backend/app/services/parsers.py`
- File coordination and locking: `backend/app/services/file_locking.py`
- Profile/config source resolution: `backend/app/configs/profile_loader.py`

## Workflow

1. Resolve the source and profile deterministically.
2. Load and parse raw inputs through explicit service boundaries.
3. Validate required fields, normalization assumptions, and source-dependent constraints.
4. Emit traceable logs and keep side effects explicit.

## Guardrails

- Do not hide parsing or normalization inside API routers.
- Keep file-system assumptions explicit and testable.
- Add or update `unittest` coverage when loading behavior changes.
