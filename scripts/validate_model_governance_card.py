#!/usr/bin/env python3
"""Validate evidence-bound ML, analytical-rule, and hybrid governance cards."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .validate_skill_catalog import _load_yaml
except ImportError:
    from validate_skill_catalog import _load_yaml


MODEL_KINDS = {"ml_predictive", "analytical_rule", "hybrid"}
EVIDENCE_STATUSES = {"OBSERVED", "VERIFIED", "PENDING", "NOT_APPLICABLE", "BLOCKED"}
LIFECYCLE_STATUSES = {
    "DRAFT",
    "CONTRACT_INCOMPLETE",
    "VALIDATION_HOLD",
    "VALIDATED",
    "PRODUCTION_CANDIDATE",
    "DEPLOYED",
    "RETIRED",
}
PLACEHOLDER = re.compile(
    r"\b(tbd|todo)\b|\[add\b|working on (define )?strategy",
    re.IGNORECASE,
)


def _mapping(value: Any, path: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")
        return {}
    return value


def _required_string(
    mapping: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string")


def _required_iso_timestamp(
    mapping: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> None:
    _required_string(mapping, key, path, errors)
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}.{key} must be an ISO timestamp")
        return
    if parsed.tzinfo is None:
        errors.append(f"{path}.{key} must include a timezone")


def _string_list(
    mapping: Mapping[str, Any], key: str, path: str, errors: list[str], *, nonempty: bool
) -> list[str]:
    value = mapping.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        errors.append(f"{path}.{key} must be a string list")
        return []
    if nonempty and not value:
        errors.append(f"{path}.{key} must not be empty")
    return value


def _status(
    mapping: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> str | None:
    value = mapping.get(key)
    if value not in EVIDENCE_STATUSES:
        errors.append(f"{path}.{key} must be one of {sorted(EVIDENCE_STATUSES)}")
        return None
    if value == "NOT_APPLICABLE" and not str(mapping.get("reason", "")).strip():
        errors.append(f"{path}.reason is required for NOT_APPLICABLE status")
    return str(value)


def _placeholder_paths(value: Any, path: str = "model_governance_card") -> list[str]:
    paths: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            paths.extend(_placeholder_paths(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(_placeholder_paths(item, f"{path}[{index}]"))
    elif isinstance(value, str):
        if value.startswith("REQUIRED") or PLACEHOLDER.search(value):
            paths.append(path)
    return paths


def _validate_metric(metric: Any, index: int, errors: list[str]) -> None:
    path = f"validation.metrics[{index}]"
    item = _mapping(metric, path, errors)
    for key in (
        "name",
        "definition",
        "dataset",
        "support",
        "baseline",
        "evidence_ref",
        "interpretation",
        "limitation",
    ):
        _required_string(item, key, path, errors)
    if item.get("value") is None:
        errors.append(f"{path}.value is required")
    status = _status(item, "status", path, errors)
    if status == "VERIFIED" and not str(item.get("evidence_ref", "")).strip():
        errors.append(f"{path}.evidence_ref is required for VERIFIED metrics")
    if item.get("threshold") is None and not str(item.get("threshold_reason", "")).strip():
        errors.append(f"{path} needs threshold or threshold_reason")


def _validate_monitoring(indicator: Any, index: int, errors: list[str]) -> None:
    path = f"monitoring.indicators[{index}]"
    item = _mapping(indicator, path, errors)
    for key in (
        "name",
        "baseline",
        "control_limit",
        "direction",
        "frequency",
        "owner",
        "source",
        "response_action",
        "evidence_ref",
    ):
        _required_string(item, key, path, errors)
    _status(item, "status", path, errors)


def _validate_quality_check(check: Any, index: int, errors: list[str]) -> None:
    path = f"data.quality_checks[{index}]"
    item = _mapping(check, path, errors)
    for key in ("name", "result", "evidence_ref"):
        _required_string(item, key, path, errors)
    status = _status(item, "status", path, errors)
    if status == "VERIFIED" and not str(item.get("evidence_ref", "")).strip():
        errors.append(f"{path}.evidence_ref is required for VERIFIED checks")


def _validate_population_counts(
    populations: Mapping[str, Any], errors: list[str]
) -> str | None:
    status = populations.get("reconciliation_status")
    if status not in EVIDENCE_STATUSES:
        errors.append("data.population_counts.reconciliation_status is invalid")
        status = None
    numeric_keys = (
        "source",
        "eligible",
        "train_or_backtest",
        "validation",
        "test",
        "scored",
    )
    for key in numeric_keys:
        value = populations.get(key)
        if value is not None and (
            not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0
        ):
            errors.append(f"data.population_counts.{key} must be non-negative or null")
    eligible = populations.get("eligible")
    source = populations.get("source")
    if isinstance(source, (int, float)) and isinstance(eligible, (int, float)):
        if eligible > source:
            errors.append("data.population_counts.eligible cannot exceed source")
    split_values = [populations.get(key) for key in ("train_or_backtest", "validation", "test")]
    if isinstance(eligible, (int, float)) and all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in split_values
    ):
        if sum(split_values) > eligible:
            errors.append("train/backtest + validation + test cannot exceed eligible")
    return str(status) if status is not None else None


def _validate_ml(logic: Mapping[str, Any], errors: list[str]) -> None:
    ml = _mapping(logic.get("ml"), "logic.ml", errors)
    for key in (
        "target_definition",
        "prediction_horizon",
        "feature_cutoff",
        "algorithm",
        "config_ref",
        "split_strategy",
        "entity_time_isolation",
        "imbalance_strategy",
        "threshold_policy",
        "calibration",
    ):
        _required_string(ml, key, "logic.ml", errors)
    if not isinstance(ml.get("feature_count"), int) or ml.get("feature_count", 0) <= 0:
        errors.append("logic.ml.feature_count must be a positive integer")


def _validate_rules(logic: Mapping[str, Any], errors: list[str]) -> None:
    rules = _mapping(logic.get("rules"), "logic.rules", errors)
    for key in (
        "rule_catalog_version",
        "input_grain",
        "eligibility_policy",
        "score_or_band_definition",
        "precedence_policy",
        "overlap_conflict_policy",
        "missing_value_policy",
        "state_persistence_policy",
        "change_approval_policy",
    ):
        _required_string(rules, key, "logic.rules", errors)


def validate_model_governance_card(document: Mapping[str, Any]) -> list[str]:
    """Return validation errors for one governance-card document."""
    errors: list[str] = []
    card = _mapping(document.get("model_governance_card"), "model_governance_card", errors)
    if card.get("schema_version") != 1:
        errors.append("model_governance_card.schema_version must be 1")
    for key in ("card_id", "card_version"):
        _required_string(card, key, "model_governance_card", errors)
    for key in ("created_at", "updated_at", "evidence_cutoff"):
        _required_iso_timestamp(card, key, "model_governance_card", errors)

    model = _mapping(card.get("model"), "model", errors)
    for key in ("id", "name", "version", "business_objective", "decision_supported", "scope"):
        _required_string(model, key, "model", errors)
    kind = model.get("kind")
    if kind not in MODEL_KINDS:
        errors.append(f"model.kind must be one of {sorted(MODEL_KINDS)}")
    lifecycle = model.get("lifecycle_status")
    if lifecycle not in LIFECYCLE_STATUSES:
        errors.append(f"model.lifecycle_status must be one of {sorted(LIFECYCLE_STATUSES)}")

    owners = _mapping(card.get("owners"), "owners", errors)
    for key in (
        "business_owner",
        "technical_owner",
        "validation_owner",
        "deployment_owner",
        "monitoring_owner",
    ):
        _required_string(owners, key, "owners", errors)

    evidence = _mapping(card.get("evidence"), "evidence", errors)
    _required_string(evidence, "source_revision", "evidence", errors)
    for key in ("run_ids", "config_hashes", "query_hashes", "artifact_refs", "validation_refs"):
        _string_list(evidence, key, "evidence", errors, nonempty=False)

    data = _mapping(card.get("data"), "data", errors)
    _string_list(data, "sources", "data", errors, nonempty=True)
    _string_list(data, "entity_keys", "data", errors, nonempty=True)
    for key in ("grain", "prediction_or_scoring_time", "target_or_outcome_time"):
        _required_string(data, key, "data", errors)
    temporal = _mapping(data.get("temporal_window"), "data.temporal_window", errors)
    _required_string(temporal, "start", "data.temporal_window", errors)
    _required_string(temporal, "end", "data.temporal_window", errors)
    populations = _mapping(data.get("population_counts"), "data.population_counts", errors)
    reconciliation = _validate_population_counts(populations, errors)
    quality_checks = data.get("quality_checks")
    if not isinstance(quality_checks, list):
        errors.append("data.quality_checks must be a list")
        quality_checks = []
    for index, check in enumerate(quality_checks):
        _validate_quality_check(check, index, errors)

    logic = _mapping(card.get("logic"), "logic", errors)
    if kind in {"ml_predictive", "hybrid"}:
        _validate_ml(logic, errors)
    if kind in {"analytical_rule", "hybrid"}:
        _validate_rules(logic, errors)
    if kind == "hybrid":
        _required_string(logic, "hybrid_interface", "logic", errors)

    validation = _mapping(card.get("validation"), "validation", errors)
    validation_status = _status(validation, "status", "validation", errors)
    for key in ("design", "baseline", "interpretation"):
        _required_string(validation, key, "validation", errors)
    leakage = _mapping(
        validation.get("leakage_assessment"),
        "validation.leakage_assessment",
        errors,
    )
    leakage_status = _status(
        leakage, "status", "validation.leakage_assessment", errors
    )
    _required_string(leakage, "summary", "validation.leakage_assessment", errors)
    _required_string(
        leakage, "evidence_ref", "validation.leakage_assessment", errors
    )
    metrics = validation.get("metrics")
    if not isinstance(metrics, list):
        errors.append("validation.metrics must be a list")
        metrics = []
    for index, metric in enumerate(metrics):
        _validate_metric(metric, index, errors)

    explainability = _mapping(card.get("explainability"), "explainability", errors)
    _status(explainability, "status", "explainability", errors)
    _required_string(explainability, "method", "explainability", errors)

    operations = _mapping(card.get("operational_evaluation"), "operational_evaluation", errors)
    _status(operations, "status", "operational_evaluation", errors)
    for key in ("action_policy", "capacity_or_cost", "human_review"):
        _required_string(operations, key, "operational_evaluation", errors)

    monitoring = _mapping(card.get("monitoring"), "monitoring", errors)
    monitoring_status = _status(monitoring, "status", "monitoring", errors)
    indicators = monitoring.get("indicators")
    if not isinstance(indicators, list):
        errors.append("monitoring.indicators must be a list")
        indicators = []
    for index, indicator in enumerate(indicators):
        _validate_monitoring(indicator, index, errors)

    governance = _mapping(card.get("governance"), "governance", errors)
    governance_status = _status(governance, "status", "governance", errors)
    for key in ("rollback_policy", "retraining_or_change_policy", "allowed_claim", "prohibited_claim"):
        _required_string(governance, key, "governance", errors)

    if lifecycle in {"VALIDATED", "PRODUCTION_CANDIDATE", "DEPLOYED"}:
        if validation_status != "VERIFIED" or not metrics:
            errors.append(f"{lifecycle} requires VERIFIED validation with metrics")
        if leakage_status != "VERIFIED":
            errors.append(f"{lifecycle} requires VERIFIED leakage assessment")
        if reconciliation != "VERIFIED":
            errors.append(f"{lifecycle} requires VERIFIED population reconciliation")
        if not quality_checks:
            errors.append(f"{lifecycle} requires data quality checks")
        if not evidence.get("validation_refs"):
            errors.append(f"{lifecycle} requires evidence.validation_refs")
    if lifecycle in {"PRODUCTION_CANDIDATE", "DEPLOYED"}:
        if monitoring_status != "VERIFIED" or not indicators:
            errors.append(f"{lifecycle} requires VERIFIED monitoring indicators")
        if governance_status != "VERIFIED":
            errors.append(f"{lifecycle} requires VERIFIED governance")
        if operations.get("status") != "VERIFIED":
            errors.append(f"{lifecycle} requires VERIFIED operational evaluation")
        if any(
            isinstance(indicator, Mapping) and indicator.get("status") != "VERIFIED"
            for indicator in indicators
        ):
            errors.append(f"{lifecycle} requires VERIFIED monitoring indicator evidence")
    if lifecycle == "DEPLOYED":
        for key in ("deployment_revision", "approval_ref"):
            _required_string(governance, key, "governance", errors)

    for path in _placeholder_paths(card):
        errors.append(f"{path} contains a placeholder")
    return errors


def _load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8")) if path.suffix.lower() == ".json" else _load_yaml(path)
    if not isinstance(value, Mapping):
        raise ValueError(f"expected a mapping in {path}")
    return value


def main() -> int:
    """Validate one YAML or JSON model-governance card from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", type=Path, required=True)
    args = parser.parse_args()
    try:
        errors = validate_model_governance_card(_load(args.card.expanduser().resolve()))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[FAIL] model governance card: {exc}")
        return 1
    if errors:
        print("[FAIL] model governance card")
        for error in errors:
            print(f"- {error}")
        return 1
    print("[OK] model governance card")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
