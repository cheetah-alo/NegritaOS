"""Unit tests for append-only decisions and ADR projection."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.decisions import (
    accept_decision,
    propose_decision,
    read_decision_state,
    supersede_decision,
)
from src.negrita_brain.errors import DecisionError


ROOT = Path(__file__).resolve().parents[1]


class TestDecisionLedger(unittest.TestCase):
    """Verifies legal decision transitions without rewriting history."""

    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        base = Path(self.temporary.name)
        self.repo = base / "repo"
        self.memory = base / "memory"
        (self.repo / ".codex").mkdir(parents=True)
        (self.repo / ".git").mkdir()
        (self.repo / ".codex" / "project.yaml").write_text(
            "project_id: negritaos\n"
            f"negrita_registry: {ROOT / 'projects' / 'negritaos.yaml'}\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def ledger(self) -> Path:
        """Return the isolated decision ledger path."""
        return self.memory / "negritaos" / "decisions" / "ledger.jsonl"

    def test_architecture_candidate_that_creates_versioned_adr(self) -> None:
        record = propose_decision(
            self.repo,
            "Use profile inheritance",
            "Remove duplicated profile declarations.",
            "architecture",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        adr = self.repo / record["adr_path"]
        self.assertEqual(record["event"], "CANDIDATE")
        self.assertTrue(adr.is_file())
        self.assertIn(record["decision_id"], adr.read_text(encoding="utf-8"))

    def test_accept_that_appends_without_removing_candidate(self) -> None:
        candidate = propose_decision(
            self.repo,
            "Decision",
            "Summary",
            "governance",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        accepted = accept_decision(
            self.repo,
            candidate["decision_id"],
            "owner",
            "commit:abc",
            ROOT,
            self.memory,
        )
        lines = self.ledger.read_text(encoding="utf-8").splitlines()
        self.assertEqual(accepted["event"], "ACCEPTED")
        self.assertEqual(len(lines), 2)

    def test_accept_that_updates_architecture_adr_status(self) -> None:
        candidate = propose_decision(
            self.repo,
            "Architecture",
            "Summary",
            "architecture",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        accept_decision(
            self.repo, candidate["decision_id"], "owner", "commit:abc", ROOT, self.memory
        )
        adr = (self.repo / candidate["adr_path"]).read_text(encoding="utf-8")
        self.assertIn("status: ACCEPTED", adr)
        self.assertIn("commit:abc", adr)

    def test_repeated_accept_that_is_idempotent(self) -> None:
        candidate = propose_decision(
            self.repo,
            "Architecture",
            "Summary",
            "architecture",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        accept_decision(self.repo, candidate["decision_id"], "owner", "ref", ROOT, self.memory)
        repeated = accept_decision(
            self.repo, candidate["decision_id"], "owner", "ref", ROOT, self.memory
        )
        self.assertTrue(repeated["idempotent"])
        self.assertEqual(len(self.ledger.read_text(encoding="utf-8").splitlines()), 2)
        adr = (self.repo / candidate["adr_path"]).read_text(encoding="utf-8")
        self.assertEqual(adr.count("## Status Transition"), 1)

    def test_supersede_that_links_replacement_candidate(self) -> None:
        original = propose_decision(
            self.repo,
            "Old",
            "Old summary",
            "contract",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        result = supersede_decision(
            self.repo,
            original["decision_id"],
            "New",
            "New summary",
            "contract",
            ROOT,
            self.memory,
        )
        state = read_decision_state(self.ledger)
        self.assertEqual(state[original["decision_id"]]["event"], "SUPERSEDED")
        self.assertEqual(
            state[original["decision_id"]]["superseded_by"],
            result["replacement"]["decision_id"],
        )

    def test_accept_unknown_decision_that_fails(self) -> None:
        with self.assertRaisesRegex(DecisionError, "Unknown decision"):
            accept_decision(
                self.repo, "NBD-MISSING", "owner", "ref", ROOT, self.memory
            )


if __name__ == "__main__":
    unittest.main()
