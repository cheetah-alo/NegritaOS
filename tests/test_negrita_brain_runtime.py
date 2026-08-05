"""Unit tests for immutable sessions, gates, safe events, and closure."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.errors import SessionError
from src.negrita_brain.installer import Installer
from src.negrita_brain.runtime import (
    close_session,
    gate_action,
    load_active_session,
    record_event,
    resolve_session,
)


ROOT = Path(__file__).resolve().parents[1]


class RuntimeFixture(unittest.TestCase):
    """Creates a minimal code workspace backed by the real canonical registry."""

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
        Installer(ROOT, base / "backups", self.memory).install(self.repo)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def resolve(self) -> dict:
        """Resolve a test session into isolated memory."""
        return resolve_session(
            self.repo, "codex", ["planning"], ROOT, self.memory
        )


class TestRuntimeContract(RuntimeFixture):
    """Verifies deterministic contract and state behavior."""

    def test_resolve_that_persists_hash_and_document_defaults(self) -> None:
        contract = self.resolve()
        contract_path = self.memory / "negritaos" / "runtime" / "sessions"
        contract_path = contract_path / contract["session_id"] / "contract.json"
        self.assertEqual(len(contract["contract_sha256"]), 64)
        self.assertIn("document-control", contract["skills"])
        self.assertTrue(contract_path.is_file())

    def test_resolve_that_maps_global_mode_to_project_agent(self) -> None:
        contract = self.resolve()
        self.assertEqual(contract["modes"], ["LP"])
        self.assertEqual(contract["agents"], ["team_lead_ds_agent"])
        self.assertEqual(contract["warnings"], [])

    def test_gate_that_blocks_code_mutation_without_contract(self) -> None:
        result = gate_action(self.repo, "write", negritaos_root=ROOT, memory_base=self.memory)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIsNone(result["session_id"])

    def test_resolve_that_blocks_uninstalled_code_workspace(self) -> None:
        (self.repo / "AGENTS.md").unlink()
        contract = self.resolve()
        self.assertEqual(contract["state"], "BLOCKED")
        self.assertEqual(contract["quality_gates"]["doctor_status"], "FAIL")

    def test_gate_that_enforces_document_route_with_ready_contract(self) -> None:
        self.resolve()
        blocked = gate_action(
            self.repo,
            "write",
            Path("report.pdf"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        allowed = gate_action(
            self.repo,
            "write",
            Path("documents/report__updated_20260805_120000.pdf"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        self.assertEqual(blocked["decision"], "BLOCK")
        self.assertEqual(allowed["decision"], "ALLOW")

    def test_event_that_discards_prompt_and_output_fields(self) -> None:
        contract = self.resolve()
        event = record_event(
            self.repo,
            "tool_completed",
            "OK",
            {"tool": "Write", "prompt": "secret", "tool_output": "secret"},
            ROOT,
            self.memory,
        )
        ledger = self.memory / "negritaos" / "runtime" / "sessions"
        ledger = ledger / contract["session_id"] / "events.jsonl"
        text = ledger.read_text(encoding="utf-8")
        self.assertNotIn("secret", text)
        self.assertEqual(event["tool"], "Write")

    def test_close_that_makes_future_mutation_fail_closed(self) -> None:
        self.resolve()
        closed = close_session(self.repo, "done", memory_base=self.memory, negritaos_root=ROOT)
        gated = gate_action(self.repo, "write", negritaos_root=ROOT, memory_base=self.memory)
        self.assertEqual(closed["status"], "COMPLETE")
        self.assertEqual(gated["decision"], "BLOCK")

    def test_repeated_close_that_does_not_rewrite_summary(self) -> None:
        self.resolve()
        close_session(
            self.repo,
            "done",
            memory_base=self.memory,
            negritaos_root=ROOT,
        )

        with self.assertRaisesRegex(SessionError, "already closed"):
            close_session(
                self.repo,
                "replacement",
                memory_base=self.memory,
                negritaos_root=ROOT,
            )

    def test_contract_tamper_that_is_detected_by_hash(self) -> None:
        contract = self.resolve()
        contract_path = self.memory / "negritaos" / "runtime" / "sessions"
        contract_path = contract_path / contract["session_id"] / "contract.json"
        value = json.loads(contract_path.read_text(encoding="utf-8"))
        value["provider"] = "tampered"
        contract_path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(SessionError, "hash mismatch"):
            load_active_session(self.repo, ROOT, self.memory)


if __name__ == "__main__":
    unittest.main()
