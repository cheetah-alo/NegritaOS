"""Focused structural contract for the ELAL rule traceability control."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

NEGRITAOS_ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = NEGRITAOS_ROOT / ".codex/skills/elal-rule-traceability"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from validate_rule_traceability import load_yaml, validate_ledger  # noqa: E402


class ElalRuleTraceabilityContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger_path = NEGRITAOS_ROOT / "projects/elal_rule_traceability.yaml"
        self.ledger = load_yaml(self.ledger_path)

    def test_ledger_references_are_valid(self) -> None:
        self.assertEqual(validate_ledger(self.ledger_path), [])

    def test_active_call_rail_and_shadow_boundaries_are_explicit(self) -> None:
        rules = {rule["id"]: rule for rule in self.ledger["rule_registry"]}
        self.assertEqual(rules["RUL-CALL-RAIL-FRPR"]["state"], "ACTIVE_DATA_CONTRACT")
        self.assertEqual(rules["RUL-OVERBOOKING"]["state"], "SHADOW_CANDIDATE")
        self.assertEqual(rules["RUL-TIER-TREATMENT-NO-SCORE"]["state"], "CONTEXT_ONLY")
        self.assertIn("FULL OUTER JOIN", rules["RUL-CALL-RAIL-FRPR"]["decision_boundary"])

    def test_historical_documents_are_hash_pinned(self) -> None:
        protected = {item["id"]: item for item in self.ledger["source_artifacts"]}
        self.assertEqual(len(protected["SRC-RULE-DOC-20260729"]["sha256"]), 64)
        self.assertEqual(len(protected["SRC-FRICTION-V7"]["sha256"]), 64)
        self.assertEqual(len(protected["SRC-PROMISE-V2"]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
