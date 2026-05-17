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
description: >
  Centralized exception strategy for the churn ML-as-code platform.
  Covers: telecom-specific anomaly handling, ML feature engineering failures,
  leakage detection errors, structured error propagation, and governance integration.
version: 1.1.0
priority: critical
---

#  **Error Handling `error-handling.instructions.md`**



#  **ERROR-HANDLING STANDARD ( ML + Churn Analytics + Data Engineering)**

This document defines **how all Python modules across the churn platform must handle errors**:
- feature engineering,
- data validation,
- leakage audits,
- model training / AutoML,
- metadata/governance pipelines.

The goals are:
- **no silent failures**,  
- **consistent taxonomy**,  
- **rich logs**,  
- **traceability in governance JSON**,  
- **zero ambiguity during audits**.

---

# **1. Core Principles (ML + Churn Analytics Context)**

###  1.1 No bare except

 `except:`
 `except ValueError as exc:`
 `except KeyError as exc:`
 `except Exception as exc:`

Telecom churn pipelines ingest:

* millions of customer events,
* billing records,
* usage KPIs,
* outages logs,
* network technical complaints.

A bare `except` would hide catastrophic data issues.

---

###  1.2 No `pass`

Never swallow anomalies such as:

* missing churn target labels
* inconsistent billing cycles
* corrupted window-level aggregates
* empty SHAP distributions
* segmentation leakage
* network-feature dropouts

All must raise structured errors.

---

###  1.3 Every exception MUST include:

* **error code** (ERR_…)
* **module + function name**
* **domain context** (customer_id, date_window, feature_name, segment)
* **action attempted**
* **expected vs. actual values**

Example format:

```
ERR_FEATURE_NEGATIVE_USAGE:
feature_engineering.compute_hourly_usage  
Detected negative usage value.  
Context: customer_id=948192, hour=2025-09-02 13:00, usage=-15.2 MB
```

This is the telecom equivalent of the refinery “negative volume”.

---

# **2. Log BEFORE raising**

```python
logger.error(
    "ERR_MISSING_TARGET_LABEL — customer_id=%s date=%s",
    customer_id, record_date
)
raise TelecomFeatureError("Missing target label for churn computation.")
```

This ensures:

* MLflow
* governance JSON
* error dashboards
* Telco audit logs

all capture the event.

---

# **3. Domain-Specific Telecom ML Exceptions**

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
```

### Why?

Telecom churn systems require different handling for:

| Error Type                      | Example                                          |
| ------------------------------- | ------------------------------------------------ |
| **Data anomaly**                | Negative minutes-of-usage, drop in network KPIs  |
| **Telemetry anomaly**           | Sudden spike in dropped calls or failed SMS      |
| **Billing inconsistency**       | Duplicate invoices, invalid cycle windows        |
| **Feature engineering failure** | Incorrect aggregation windows                    |
| **Leakage risk**                | Predictive coverage using future information     |
| **Model error**                 | Training instability, AutoML failure, OOM on GPU |

---

# **4. PEP-463 Exception-catching expression (allowed in ML feature defaults)**

Correct usage:

```python
minutes = try_parse_minutes(raw) except ValueError: 0
segment = segment_rules.get(customer_id) except KeyError: "unknown"
```

Never use PEP-463 to mask critical failures like:

* corrupted feature matrices
* missing churn targets
* broken temporal splits

---

# **5. Use logger.warning() for telecom warnings**

 `print("WARNING: billing cycle missing")`


```python
logger.warning(
    "WARN_MISSING_BILLING_FIELD — customer_id=%s field=%s",
    customer_id, "invoice_amount"
)
```

---

# **6. All errors must propagate into governance JSON**

Every exception populates:

* `phase` (feature_engineering, training, validation, leakage_audit, metrics_eval)
* `error_type`
* `module`
* `offending_record_ids`
* `temporal_window`
* `feature_list`
* `auto_correction_applied?`

This directly supports:

* churn-model repeatability
* regulatory compliance
* GDPR audit trails
* reproducible model registry entries

---

#  2. **UPDATED METHOD TEMPLATES IN TELECOM CONTEXT**

Your methods were refinery-based ("tanks", "volumes", "streams").
Now they are **telecom churn–based**:

* streaming customer events
* merging feature windows
* verifying subscriber distributions
* ensuring feature weights sum to 1
* detecting anomalies in initial feature maps

---

#  **2.1 Example Replacement of `refill_from_stream()` in Telecom Terms**

### Original meaning

Refilling a tank from crude flow →
**Merging new network/billing events into customer feature state**

### New telecom version

**"update_feature_state_from_event()"**

```python
import logging

logger = logging.getLogger(__name__)

class FeatureEngineeringError(Exception): ...
class DataAnomalyError(Exception): ...
class TelecomFeatureMergeError(Exception): ...

def update_feature_state_from_event(self, cm, event, time_lapse: float, allow_outliers: bool = False):
    method_name = "FeatureState.update_feature_state_from_event"

    # 1. Compute usage_delta from event
    try:
        usage_delta = event.kpi_value * time_lapse
    except Exception as exc:
        logger.error(
            "ERR_EVENT_KPI_COMPUTE: %s — failed computing usage delta. "
            "customer_id=%s event=%s kpi_value=%s time_lapse=%s error=%s",
            method_name, getattr(event, "customer_id", None),
            getattr(event, "name", None),
            getattr(event, "kpi_value", None),
            time_lapse, exc
        )
        raise FeatureEngineeringError(
            f"{method_name}: unable to compute usage delta for event."
        ) from exc

    # 2. Negative usage anomaly
    if usage_delta < 0:
        logger.error(
            "ERR_NEGATIVE_USAGE_DELTA: %s — customer_id=%s delta=%s",
            method_name, getattr(event, "customer_id", None), usage_delta
        )
        raise DataAnomalyError(
            f"{method_name}: computed negative usage delta (delta={usage_delta})."
        )

    # 3. Missing event properties
    if event.properties is None:
        logger.error(
            "ERR_EVENT_PROPERTIES_MISSING: %s — customer_id=%s event=%s",
            method_name, getattr(event, "customer_id", None), getattr(event, "name", None)
        )
        raise FeatureEngineeringError(
            f"{method_name}: missing event properties for feature merge."
        )

    # 4. Merge event into feature profile
    try:
        self._merge_event_properties(event, usage_delta)
    except Exception as exc:
        logger.error(
            "ERR_EVENT_MERGE_FAILED: %s — customer_id=%s event=%s error=%s",
            method_name, getattr(event, "customer_id", None), getattr(event, "name", None), exc
        )
        raise TelecomFeatureMergeError(
            f"{method_name}: failed to merge event into feature state."
        ) from exc

    logger.debug(
        "Feature update successful — customer_id=%s delta=%s",
        getattr(event, "customer_id", None), usage_delta
    )
```

---

#  **2.2 Telecom Version of Your Tank `__init__` (CustomerFeatureState)**

```python
class FeatureNormalizationError(Exception): ...

def __init__(self, customer_id, base_features, segment, usage, properties, product, retention_ratio=None):
    self.customer_id = customer_id

    if retention_ratio is not None and retention_ratio >= 1:
        raise FeatureNormalizationError(
            f"CustomerFeatureState.__init__: retention_ratio must be < 1 "
            f"(received={retention_ratio})."
        )

    self.segment = segment
    self.product = product
    self.usage = usage
    self.properties = properties
    self.retention_ratio = retention_ratio

    self.last_interaction = None
    self.last_complaint_ts = None
```

---

#  **2.3 Telecom Version of `fill_initial_tank_properties_correctly`**

### Telecom meaning

Normalize subscriber feature components (e.g., usage distribution, traffic breakdown).

```python
class NormalizationError(Exception): ...
class MissingFeatureWarning(Warning): ...

@staticmethod
def normalize_initial_feature_map(cm, db, scenario_id, customer_id, product, feature_map) -> dict:
    logger = logging.getLogger(__name__)
    method_name = "CustomerFeatureState.normalize_initial_feature_map"

    # Identify subfeatures to validate (APP usage share, call category share, etc.)
    subfeatures = (
        getattr(cm, "TRAFFIC_DISTRIBUTION_RULES", {}).get(product) or
        getattr(cm, "INITIAL_SUBFEATURES_TO_CHECK", {}).get(product)
    )

    if not subfeatures:
        return feature_map

    total = 0
    for sf in subfeatures:
        value = feature_map.get(sf)

        if value is None:
            logger.warning(
                "WARN_MISSING_SUBFEATURE: %s — customer_id=%s feature=%s defaulted_to=0",
                method_name, customer_id, sf
            )
            feature_map[sf] = 0
        else:
            total += value

    if total == 0:
        logger.error(
            "ERR_ZERO_SUBFEATURE_SUM: %s — customer_id=%s product=%s subfeatures=%s",
            method_name, customer_id, product, subfeatures
        )
        raise NormalizationError(
            f"{method_name}: all subfeatures are zero; cannot normalize."
        )

    if total != 1:
        logger.warning(
            "WARN_NORMALIZING_SUBFEATURES: %s — customer_id=%s sum=%s normalizing_to=1",
            method_name, customer_id, total
        )

        for sf in subfeatures:
            feature_map[sf] /= total

    return feature_map
