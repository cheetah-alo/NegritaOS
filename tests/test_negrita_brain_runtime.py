"""Unit tests for immutable sessions, gates, safe events, and closure."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.negrita_brain.errors import MemoryPermissionError, SessionError
from src.negrita_brain.installer import Installer
from src.negrita_brain.runtime import (
    close_session,
    gate_action,
    load_active_session,
    record_event,
    resolve_session,
    resolve_session_identity,
)
from src.negrita_brain.models import sha256_json, write_json


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
        self.assertEqual(contract["artifact_route"]["selection"], "user_selected")
        self.assertIn("pptx", contract["artifact_route"]["require_explicit_path_for"])
        self.assertTrue(contract_path.is_file())

    def test_resolve_that_maps_global_mode_to_project_agent(self) -> None:
        contract = self.resolve()
        self.assertEqual(contract["modes"], ["LP"])
        self.assertEqual(contract["agents"], ["team_lead_ds_agent"])
        self.assertFalse(
            any("No router mode" in warning for warning in contract["warnings"])
        )

    def test_resolve_that_includes_selected_agent_codex_skills(self) -> None:
        contract = resolve_session(
            self.repo, "codex", ["plot_analysis"], ROOT, self.memory
        )
        self.assertEqual(contract["modes"], ["PA"])
        self.assertEqual(contract["agents"], ["plot_analysis_agent"])
        self.assertIn("evidence-first-plot-analysis", contract["agent_skills"])
        self.assertIn("evidence-first-plot-analysis", contract["skills"])

    def test_gate_that_blocks_code_mutation_without_contract(self) -> None:
        result = gate_action(self.repo, "write", negritaos_root=ROOT, memory_base=self.memory)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIsNone(result["session_id"])

    def test_gate_that_allows_explicit_legacy_recovery_authorization(self) -> None:
        with patch(
            "src.negrita_brain.runtime._git_state",
            return_value={"branch": "fix/close-legacy-memory-v1-sessions"},
        ):
            result = gate_action(
                self.repo,
                "commit",
                negritaos_root=ROOT,
                memory_base=self.memory,
                authorize_legacy_recovery=True,
                authorized_by="human",
                authorization_reason="Commit the selector repair",
                recovery_scope="legacy-memory-v1",
            )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["authorization"]["authorized_by"], "human")

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
        external = gate_action(
            self.repo,
            "write",
            Path("/tmp/report__updated_20260805_120000.pdf"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        missing_destination = gate_action(
            self.repo,
            "deliverable",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        self.assertEqual(blocked["decision"], "BLOCK")
        self.assertEqual(allowed["decision"], "ALLOW")
        self.assertEqual(external["decision"], "ALLOW")
        self.assertEqual(missing_destination["decision"], "BLOCK")
        self.assertIn("External deliverable route", external["reasons"][-1])

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
        self.assertNotIn("closure_note", closed)
        self.assertNotIn("summary", closed)
        self.assertEqual(gated["decision"], "BLOCK")

    def test_codex_and_claude_sessions_that_use_distinct_active_pointers(self) -> None:
        first = resolve_session(
            self.repo,
            "codex",
            ["planning"],
            ROOT,
            self.memory,
            session_key="thread-a",
        )
        second = resolve_session(
            self.repo,
            "claude",
            ["planning"],
            ROOT,
            self.memory,
            session_key="claude-session-b",
        )

        first_loaded = load_active_session(
            self.repo, ROOT, self.memory, "codex", "thread-a"
        )[1]
        second_loaded = load_active_session(
            self.repo, ROOT, self.memory, "claude", "claude-session-b"
        )[1]

        self.assertEqual(first_loaded["session_id"], first["session_id"])
        self.assertEqual(second_loaded["session_id"], second["session_id"])
        self.assertNotEqual(
            first["session_identity"]["key_hash"],
            second["session_identity"]["key_hash"],
        )

    def test_session_identity_that_prefers_explicit_then_codex_native_key(self) -> None:
        explicit = resolve_session_identity(
            "codex", "explicit-key", {"CODEX_THREAD_ID": "native-key"}
        )
        native = resolve_session_identity(
            "codex", None, {"CODEX_THREAD_ID": "native-key"}
        )

        self.assertEqual(explicit.source, "explicit")
        self.assertEqual(native.source, "CODEX_THREAD_ID")
        self.assertNotIn("native-key", native.key_hash)

    def test_v2_close_that_does_not_rewrite_durable_index(self) -> None:
        index = self.memory / "negritaos" / "index.md"
        index.write_text("# Curated memory\n", encoding="utf-8")
        contract = resolve_session(
            self.repo,
            "codex",
            ["planning"],
            ROOT,
            self.memory,
            session_key="thread-a",
        )

        close_session(
            self.repo,
            "done",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="thread-a",
        )

        session_dir = self.memory / "negritaos" / "runtime" / "sessions"
        session_dir = session_dir / contract["session_id"]
        self.assertEqual(index.read_text(encoding="utf-8"), "# Curated memory\n")
        self.assertTrue((session_dir / "state.json").is_file())
        self.assertFalse((session_dir / "summary.json").exists())

    def test_legacy_session_that_closes_only_with_explicit_authorization(self) -> None:
        home = self.memory / "negritaos"
        session_dir = home / "runtime" / "sessions" / "legacy-session"
        contract = {
            "schema_version": 1,
            "session_id": "legacy-session",
            "project": {"workspace_kind": "code"},
            "provider": "codex",
            "state": "READY",
        }
        contract["contract_sha256"] = sha256_json(contract)
        write_json(session_dir / "contract.json", contract)
        write_json(
            home / "runtime" / "active_session.json",
            {
                "contract_path": str(session_dir / "contract.json"),
                "project_id": "negritaos",
                "session_id": "legacy-session",
                "state": "READY",
            },
        )
        index = home / "index.md"
        index.write_text("# Existing memory\n", encoding="utf-8")

        with self.assertRaisesRegex(SessionError, "Explicit authorization"):
            close_session(
                self.repo,
                "legacy done",
                negritaos_root=ROOT,
                memory_base=self.memory,
                legacy_session_id="legacy-session",
            )

        closed = close_session(
            self.repo,
            "legacy done",
            negritaos_root=ROOT,
            memory_base=self.memory,
            legacy_session_id="legacy-session",
            authorize_legacy_close=True,
            authorized_by="human",
            authorization_reason="Approved legacy session migration",
        )

        self.assertEqual(closed["schema_version"], 1)
        self.assertTrue((session_dir / "summary.json").is_file())
        self.assertEqual(index.read_text(encoding="utf-8"), "# Existing memory\n")
        self.assertTrue(Path(closed["backup_path"]).is_dir())
        self.assertEqual(closed["authorization"]["authorized_by"], "human")

    def test_session_key_does_not_fall_back_to_global_legacy_pointer(self) -> None:
        home = self.memory / "negritaos"
        session_dir = home / "runtime" / "sessions" / "legacy-session"
        contract = {
            "schema_version": 1,
            "session_id": "legacy-session",
            "project": {"workspace_kind": "code"},
            "provider": "codex",
            "state": "READY",
        }
        contract["contract_sha256"] = sha256_json(contract)
        write_json(session_dir / "contract.json", contract)
        write_json(
            home / "runtime" / "active_session.json",
            {
                "contract_path": str(session_dir / "contract.json"),
                "project_id": "negritaos",
                "session_id": "legacy-session",
                "state": "READY",
            },
        )

        with self.assertRaisesRegex(SessionError, "--legacy-session-id"):
            close_session(
                self.repo,
                "legacy done",
                negritaos_root=ROOT,
                memory_base=self.memory,
                provider="codex",
                session_key="thread-without-v2-pointer",
            )

    def test_permission_error_that_is_not_configuration_failure(self) -> None:
        with patch(
            "src.negrita_brain.runtime.write_json",
            side_effect=PermissionError("Operation not permitted"),
        ):
            with self.assertRaises(MemoryPermissionError) as captured:
                resolve_session(
                    self.repo,
                    "codex",
                    ["planning"],
                    ROOT,
                    self.memory,
                    session_key="thread-a",
                )

        self.assertEqual(captured.exception.code, "MEMORY_WRITE_PERMISSION")
        self.assertEqual(captured.exception.status, "PERMISSION_REQUIRED")

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
