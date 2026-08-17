"""Unit tests for security scan report parsing."""

import unittest

from src.negrita_brain.security import (
    detect_secrets_finding_keys,
    detect_secrets_findings,
)


class TestDetectSecretsFindings(unittest.TestCase):
    """Validate stable extraction from detect-secrets output."""

    def test_extracts_findings_without_secret_values(self) -> None:
        report = {
            "results": {
                "config/example.env": [
                    {
                        "filename": "config/example.env",
                        "hashed_" + "sec" + "ret": "abc123",
                        "is_verified": False,
                        "line_number": 7,
                        "type": "Secret " + "Keyword",
                    }
                ]
            }
        }

        findings = detect_secrets_findings(report)

        self.assertEqual(
            findings,
            [
                {
                    "filename": "config/example.env",
                    "is_verified": False,
                    "line_number": 7,
                    "type": "Secret " + "Keyword",
                }
            ],
        )
        self.assertNotIn("hashed_secret", findings[0])

    def test_ignores_malformed_results(self) -> None:
        self.assertEqual(detect_secrets_findings({"results": []}), [])
        self.assertEqual(detect_secrets_findings({"results": {"a.py": {}}}), [])
        self.assertEqual(detect_secrets_findings({"results": {"a.py": ["bad"]}}), [])

    def test_finding_keys_include_hashed_secret_for_baseline_comparison(self) -> None:
        report = {
            "results": {
                "a.py": [
                    {
                        "hashed_" + "sec" + "ret": "hash",
                        "line_number": 3,
                        "type": "Secret " + "Keyword",
                    }
                ]
            }
        }

        self.assertEqual(
            detect_secrets_finding_keys(report),
            {("a.py", 3, "Secret " + "Keyword", "hash")},
        )

    def test_finding_keys_ignore_malformed_values(self) -> None:
        self.assertEqual(detect_secrets_finding_keys({"results": []}), set())
        self.assertEqual(detect_secrets_finding_keys({"results": {"a.py": {}}}), set())
        self.assertEqual(
            detect_secrets_finding_keys({"results": {"a.py": ["bad"]}}),
            set(),
        )

    def test_finding_keys_use_fallback_filename_and_defaults(self) -> None:
        report = {"results": {"fallback.py": [{}]}}

        self.assertEqual(
            detect_secrets_finding_keys(report),
            {("fallback.py", None, "Unknown", "")},
        )
