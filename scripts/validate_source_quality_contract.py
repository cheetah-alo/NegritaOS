#!/usr/bin/env python3
"""Validate reusable analysis source-quality contracts and evidence."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

try:
    from .validate_skill_catalog import _load_yaml
except ImportError:
    from validate_skill_catalog import _load_yaml


REQUIRED_GRAIN_KEYS = ("entity", "key_columns", "expected_cardinality")
REQUIRED_TIMESTAMP_KEYS = (
    "event_time",
    "source_capture_time",
    "bq_loaded_at",
    "timezone",
)
ALLOWED_STATUSES = {
    "PASS",
    "WARN_LATENCY_SLA_EXCEEDED",
    "NOT_APPLICABLE",
    "CONTRACT_INCOMPLETE",
    "BLOCKED_DATA",
    "BLOCKED_NO_SUPPORT",
}


def _mapping(value: Any, path: str, errors: list[str]) -> Mapping[str, Any]:
    """Return a mapping or record a contract error."""
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")
        return {}
    return value


def _required_string(mapping: Mapping[str, Any], key: str, path: str, errors: list[str]) -> None:
    """Require a non-empty string at a contract path."""
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string")


def validate_source_contract(contract: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    """Validate logical grain, timestamp, SLA, and status declarations."""
    errors: list[str] = []
    warnings: list[str] = []
    grain = _mapping(contract.get("grain"), "grain", errors)
    timestamps = _mapping(contract.get("timestamps"), "timestamps", errors)
    latency_sla = _mapping(contract.get("latency_sla"), "latency_sla", errors)
    statuses = _mapping(contract.get("status"), "status", errors)

    for key in REQUIRED_GRAIN_KEYS:
        if key not in grain:
            errors.append(f"grain.{key} is required")
    keys = grain.get("key_columns")
    if not isinstance(keys, list) or not keys or not all(isinstance(item, str) and item for item in keys):
        errors.append("grain.key_columns must be a non-empty list of strings")
    relationships = grain.get("join_expectations", [])
    if not isinstance(relationships, list):
        errors.append("grain.join_expectations must be a list")
    else:
        for index, relationship in enumerate(relationships):
            item = _mapping(relationship, f"grain.join_expectations[{index}]", errors)
            for key in ("left", "right", "relationship"):
                _required_string(item, key, f"grain.join_expectations[{index}]", errors)

    for key in REQUIRED_TIMESTAMP_KEYS:
        if key not in timestamps:
            errors.append(f"timestamps.{key} is required")
    if timestamps.get("latency_definition") != "bq_loaded_at_minus_source_capture_time":
        errors.append("timestamps.latency_definition must use source capture and BigQuery load time")
    if timestamps.get("freshness_definition") != "now_minus_latest_bq_loaded_at":
        errors.append("timestamps.freshness_definition must be separate from ingestion latency")

    capture_time = timestamps.get("source_capture_time")
    if capture_time is None:
        if statuses.get("missing_capture_time") != "NOT_APPLICABLE":
            errors.append("missing source_capture_time requires status.missing_capture_time=NOT_APPLICABLE")
        else:
            warnings.append("source_capture_time is unavailable; measured ingestion latency is NOT_APPLICABLE")
    else:
        _required_string(timestamps, "source_capture_time", "timestamps", errors)

    if capture_time is not None:
        p95 = latency_sla.get("p95_minutes")
        if not isinstance(p95, (int, float)) or p95 <= 0:
            errors.append("latency_sla.p95_minutes must be positive when source capture time exists")

    for key, expected in (
        ("missing_load_time", "CONTRACT_INCOMPLETE"),
        ("invalid_latency", "CONTRACT_INCOMPLETE"),
    ):
        if statuses.get(key) != expected:
            errors.append(f"status.{key} must be {expected}")

    return errors, warnings


def parse_timestamp(value: str) -> datetime:
    """Parse an ISO timestamp and require an explicit timezone."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed


def measure_ingestion_latency_seconds(capture_time: str | None, loaded_at: str | None) -> tuple[str, float | None]:
    """Measure capture-to-load latency without falling back to event time."""
    if capture_time is None:
        return "NOT_APPLICABLE", None
    if loaded_at is None:
        return "CONTRACT_INCOMPLETE", None
    try:
        latency = (parse_timestamp(loaded_at) - parse_timestamp(capture_time)).total_seconds()
    except (TypeError, ValueError):
        return "CONTRACT_INCOMPLETE", None
    if latency < 0:
        return "CONTRACT_INCOMPLETE", latency
    return "PASS", latency


def validate_source_quality_evidence(evidence: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    """Validate the run-manifest source_quality evidence section."""
    errors: list[str] = []
    warnings: list[str] = []
    grain = _mapping(evidence.get("grain"), "source_quality.grain", errors)
    latency = _mapping(evidence.get("latency"), "source_quality.latency", errors)
    freshness = _mapping(evidence.get("freshness"), "source_quality.freshness", errors)
    queries = _mapping(evidence.get("queries"), "source_quality.queries", errors)

    for key in ("row_count", "distinct_key_count", "duplicate_rate", "join_cardinality"):
        if key not in grain:
            errors.append(f"source_quality.grain.{key} is required")
    if grain.get("duplicate_rate") is not None and not isinstance(grain.get("duplicate_rate"), (int, float)):
        errors.append("source_quality.grain.duplicate_rate must be numeric")

    status = latency.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"source_quality.latency.status must be one of {sorted(ALLOWED_STATUSES)}")
    if status == "PASS":
        for key in ("p50_seconds", "p95_seconds", "max_seconds"):
            if not isinstance(latency.get(key), (int, float)) or latency.get(key) < 0:
                errors.append(f"source_quality.latency.{key} must be a non-negative number")
    if status == "NOT_APPLICABLE":
        warnings.append("source_quality.latency is not measurable from source capture time")

    for key in ("status", "latest_loaded_at", "age_seconds"):
        if key not in freshness:
            errors.append(f"source_quality.freshness.{key} is required")
    if freshness.get("status") not in ALLOWED_STATUSES:
        errors.append(f"source_quality.freshness.status must be one of {sorted(ALLOWED_STATUSES)}")
    if not isinstance(queries.get("sql_hashes"), list) or not queries.get("sql_hashes"):
        errors.append("source_quality.queries.sql_hashes must be a non-empty list")
    return errors, warnings


def _load_document(path: Path) -> Mapping[str, Any]:
    """Load JSON/YAML documents with the repository's parser fallback."""
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        value = _load_yaml(path)
    if not isinstance(value, Mapping):
        raise ValueError(f"expected mapping in {path}")
    return value


def main() -> int:
    """Validate a source contract and optional run evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    try:
        errors, warnings = validate_source_contract(_load_document(args.contract))
        if args.evidence:
            evidence_errors, evidence_warnings = validate_source_quality_evidence(
                _load_document(args.evidence)
            )
            errors.extend(evidence_errors)
            warnings.extend(evidence_warnings)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"[FAIL] source-quality contract: {exc}")
        return 1
    if errors:
        print("[FAIL] source-quality contract")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"[WARN] {warning}")
        return 1
    print("[OK] source-quality contract")
    for warning in warnings:
        print(f"[WARN] {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
