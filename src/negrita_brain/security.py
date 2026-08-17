"""Security scanning helpers for NegritaOS validation scripts."""

from __future__ import annotations

from typing import Any


def detect_secrets_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract stable finding metadata from a detect-secrets JSON report."""
    results = report.get("results", {})
    if not isinstance(results, dict):
        return []
    findings: list[dict[str, Any]] = []
    for fallback_filename, entries in sorted(results.items()):
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            findings.append(
                {
                    "filename": str(entry.get("filename") or fallback_filename),
                    "line_number": entry.get("line_number"),
                    "type": str(entry.get("type") or "Unknown"),
                    "is_verified": entry.get("is_verified"),
                }
            )
    return findings


def detect_secrets_finding_keys(report: dict[str, Any]) -> set[tuple[Any, ...]]:
    """Return comparable finding identities without exposing secret values."""
    results = report.get("results", {})
    if not isinstance(results, dict):
        return set()
    keys: set[tuple[Any, ...]] = set()
    for fallback_filename, entries in sorted(results.items()):
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            keys.add(
                (
                    str(entry.get("filename") or fallback_filename),
                    entry.get("line_number"),
                    str(entry.get("type") or "Unknown"),
                    str(entry.get("hashed_secret") or ""),
                )
            )
    return keys
