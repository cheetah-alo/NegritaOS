#!/usr/bin/env python3
"""Validate the ELAL append-only rule traceability ledger.

The validator intentionally checks document-to-contract-to-implementation
references without executing data queries or inferring business approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

CONTROLLED_RULE_STATES = {
    "CURRENT_GOVERNED_BASELINE",
    "ACTIVE_DATA_CONTRACT",
    "CONTEXT_ONLY",
    "SHADOW_CANDIDATE",
    "INSUFFICIENT_EVIDENCE",
    "DEPRECATED",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHANGE_REQUIRED_FIELDS = {
    "id",
    "recorded_on",
    "kind",
    "record_status",
    "previous_change_id",
    "supersedes",
    "rule_ids",
    "source_artifact_ids",
    "contract_ids",
    "implementation_artifact_ids",
    "validation",
    "decision",
    "policy_effect",
    "deck_product_impact",
}


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping with PyYAML or the repository Ruby fallback."""
    try:
        import yaml  # type: ignore[import-not-found]

        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (ImportError, ModuleNotFoundError):
        ruby = (
            "require 'yaml'; require 'json'; "
            "puts JSON.generate(YAML.load_file(ARGV.fetch(0)))"
        )
        output = subprocess.check_output(["ruby", "-e", ruby, str(path)], text=True)
        value = json.loads(output)
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping in {path}")
    return value


def _errors_for_missing_fields(item: dict[str, Any], required: set[str], label: str) -> list[str]:
    return [f"{label} is missing required field {field!r}" for field in sorted(required - item.keys())]


def _unique_ids(items: Any, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label} must be a list")
        return set()
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not item.get("id"):
            errors.append(f"{label}[{index}] requires a non-empty id")
            continue
        item_id = str(item["id"])
        if item_id in ids:
            errors.append(f"Duplicate {label} id: {item_id}")
        ids.add(item_id)
    return ids


def _check_known_ids(
    record: dict[str, Any],
    field: str,
    known_ids: set[str],
    label: str,
    errors: list[str],
) -> None:
    values = record.get(field)
    if not isinstance(values, list):
        errors.append(f"{label}.{field} must be a list")
        return
    for value in values:
        if value not in known_ids:
            errors.append(f"{label}.{field} references unknown id {value!r}")


def _path_exists(repo_root: Path, relative_path: Any) -> bool:
    return isinstance(relative_path, str) and (repo_root / relative_path).is_file()


def validate_ledger(ledger_path: Path, repo_root: Path | None = None) -> list[str]:
    """Return all structural and reference errors found in *ledger_path*."""
    errors: list[str] = []

    try:
        data = load_yaml(ledger_path)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return [f"Cannot read ledger {ledger_path}: {exc}"]
    if repo_root is None:
        source_repository = data.get("source_repository")
        if not isinstance(source_repository, dict) or not isinstance(source_repository.get("root"), str):
            return ["source_repository.root must identify the ELAL source project"]
        root = Path(source_repository["root"]).expanduser()
    else:
        root = repo_root
    if not root.is_dir():
        return [f"ELAL source project root does not exist: {root}"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("ledger_policy", {}).get("mode") != "append_only":
        errors.append("ledger_policy.mode must be append_only")

    states = data.get("controlled_rule_states")
    if not isinstance(states, list) or set(states) != CONTROLLED_RULE_STATES:
        errors.append("controlled_rule_states must contain exactly the supported rule states")

    source_ids = _unique_ids(data.get("source_artifacts"), "source_artifacts", errors)
    contract_ids = _unique_ids(data.get("contracts"), "contracts", errors)
    implementation_ids = _unique_ids(data.get("implementation_artifacts"), "implementation_artifacts", errors)
    rule_ids = _unique_ids(data.get("rule_registry"), "rule_registry", errors)
    change_ids = _unique_ids(data.get("change_log"), "change_log", errors)

    for source in data.get("source_artifacts", []):
        if not isinstance(source, dict):
            continue
        label = f"source_artifacts[{source.get('id', '?')}]"
        source_path = root / str(source.get("path", ""))
        if not _path_exists(root, source.get("path")):
            errors.append(f"{label}.path does not exist: {source.get('path')!r}")
        elif source.get("format") in {"PDF", "DOCX"}:
            expected_digest = str(source.get("sha256", ""))
            if not SHA256_RE.fullmatch(expected_digest):
                errors.append(f"{label}.sha256 must be a lowercase SHA-256 digest")
            elif hashlib.sha256(source_path.read_bytes()).hexdigest() != expected_digest:
                errors.append(f"{label}.sha256 does not match the immutable source artifact")
        if not isinstance(source.get("observed_pages"), int) or source["observed_pages"] < 1:
            errors.append(f"{label}.observed_pages must be a positive integer")

    for collection_name in ("contracts", "implementation_artifacts"):
        for item in data.get(collection_name, []):
            if isinstance(item, dict) and not _path_exists(root, item.get("path")):
                errors.append(f"{collection_name}[{item.get('id', '?')}].path does not exist: {item.get('path')!r}")

    for rule in data.get("rule_registry", []):
        if not isinstance(rule, dict):
            continue
        label = f"rule_registry[{rule.get('id', '?')}]"
        if rule.get("state") not in CONTROLLED_RULE_STATES:
            errors.append(f"{label}.state is not controlled: {rule.get('state')!r}")
        _check_known_ids(rule, "source_artifact_ids", source_ids, label, errors)
        _check_known_ids(rule, "contract_ids", contract_ids, label, errors)
        _check_known_ids(rule, "implementation_artifact_ids", implementation_ids, label, errors)
        if not isinstance(rule.get("decision_boundary"), str) or not rule["decision_boundary"].strip():
            errors.append(f"{label}.decision_boundary must be a non-empty string")

    previous_change_id: str | None = None
    for index, change in enumerate(data.get("change_log", [])):
        if not isinstance(change, dict):
            errors.append(f"change_log[{index}] must be a mapping")
            continue
        label = f"change_log[{change.get('id', index)}]"
        errors.extend(_errors_for_missing_fields(change, CHANGE_REQUIRED_FIELDS, label))
        if index == 0:
            if change.get("previous_change_id") is not None:
                errors.append(f"{label}.previous_change_id must be null for the first record")
        elif change.get("previous_change_id") != previous_change_id:
            errors.append(f"{label}.previous_change_id must equal {previous_change_id!r}")
        previous_change_id = change.get("id")
        _check_known_ids(change, "rule_ids", rule_ids, label, errors)
        _check_known_ids(change, "source_artifact_ids", source_ids, label, errors)
        _check_known_ids(change, "contract_ids", contract_ids, label, errors)
        _check_known_ids(change, "implementation_artifact_ids", implementation_ids, label, errors)
        if change.get("supersedes") is not None and change["supersedes"] not in change_ids:
            errors.append(f"{label}.supersedes references unknown change id {change['supersedes']!r}")
        if not isinstance(change.get("validation"), list) or not change["validation"]:
            errors.append(f"{label}.validation must be a non-empty list")
        decision = change.get("decision")
        if not isinstance(decision, dict) or not all(decision.get(key) for key in ("owner", "status", "approval_ref")):
            errors.append(f"{label}.decision requires non-empty owner, status, and approval_ref")
        if not isinstance(change.get("deck_product_impact"), str) or not change["deck_product_impact"].strip():
            errors.append(f"{label}.deck_product_impact must be a non-empty string")

    if not data.get("change_log"):
        errors.append("change_log must contain the baseline record")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "projects/elal_rule_traceability.yaml",
        help="Path to the ledger YAML file.",
    )
    args = parser.parse_args()
    errors = validate_ledger(args.ledger.resolve())
    if errors:
        print("FAILED: ELAL rule traceability ledger")
        for error in errors:
            print(f"- {error}")
        return 1
    digest = hashlib.sha256(args.ledger.read_bytes()).hexdigest()
    print(f"OK: ELAL rule traceability ledger ({args.ledger}, sha256={digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
