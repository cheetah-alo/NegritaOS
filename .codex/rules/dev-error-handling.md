---
id: error-handling
domain: dev
enforcement: strict
applyTo: [python, pipelines, feature-engineering, training]
depends_on:
  - logging
  - naming-guidelines
  - data-contracts
provides:
  - exception-taxonomy
  - domain-errors
  - governance-propagation
version: 1.1.0
priority: critical
---

# Error Handling Rules

## Core Principles

- No bare `except:` — always catch specific types.
- No `pass` — never swallow exceptions silently.
- Log with `logger.error(...)` BEFORE raising.
- Every exception must include: error code (`ERR_*`), module + function, domain context (customer_id, date_window, feature_name), action attempted, expected vs. actual.

## Domain Exception Hierarchy

```python
class DataError(Exception): ...
class ChurnModelError(Exception): ...
class FeatureEngineeringError(DataError): ...
class DataAnomalyError(DataError): ...
class LeakageRiskError(DataError): ...
class NormalizationError(FeatureEngineeringError): ...
class SubscriberAggregationError(FeatureEngineeringError): ...
class BillingRecordError(DataError): ...
class NetworkEventError(DataError): ...
class MissingColumnError(DataError): ...
```

## Error Code Conventions

Prefix: `ERR_` — e.g., `ERR_MISSING_TARGET_LABEL`, `ERR_NEGATIVE_USAGE_DELTA`, `ERR_ZERO_SUBFEATURE_SUM`, `ERR_MISSING_REQUIRED_COLUMNS`.

## Pattern

```python
logger.error(
    "ERR_CODE: module.function — context: key=%s value=%s",
    key, value
)
raise DomainSpecificError("module.function: descriptive message.") from exc
```

## Governance Propagation

Every exception must populate governance JSON with:
- `phase`, `error_type`, `module`, `offending_record_ids`, `temporal_window`, `feature_list`, `auto_correction_applied`.

## Warnings

Use `logger.warning(...)` for recoverable anomalies (missing billing field, null usage).
Never use `print("WARNING: ...")`.

## Learnings
- Log before raising so governance and MLflow always capture the event. (2)
- Domain-specific exceptions enable targeted retry and audit logic. (1)
