"""Unit tests for immutable sessions, gates, safe events, and closure."""

import json
import hashlib
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.negrita_brain.errors import MemoryPermissionError, SessionError
from src.negrita_brain.installer import Installer
from src.negrita_brain.runtime import (
    close_session,
    close_stale_runtime_sessions,
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
        subprocess.run(
            ["git", "init", "-q", str(self.repo)], check=True, capture_output=True
        )
        (self.repo / ".codex" / "project.yaml").write_text(
            "project_id: negritaos\n"
            f"negrita_registry: {ROOT / 'projects' / 'negritaos.yaml'}\n",
            encoding="utf-8",
        )
        Installer(ROOT, base / "backups", self.memory).install(self.repo)
        subprocess.run(
            ["git", "add", "."], cwd=self.repo, check=True, capture_output=True
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=NegritaOS Tests",
                "-c",
                "user.email=tests@invalid.local",
                "commit",
                "-qm",
                "test fixture",
            ],
            cwd=self.repo,
            check=True,
            capture_output=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def resolve(self) -> dict:
        """Resolve a test session into isolated memory."""
        return resolve_session(
            self.repo, "codex", ["planning"], ROOT, self.memory
        )

    def evidence_ref(
        self,
        reviewer: dict,
        category: str,
        *,
        status: str = "PASS",
    ) -> str:
        """Create one hashed evidence receipt in canonical test memory."""
        relative = (
            Path("runtime")
            / "sessions"
            / reviewer["session_id"]
            / "evidence"
            / f"{category}.json"
        )
        receipt = {
            "schema_version": 1,
            "category": category,
            "status": status,
            "subject_worktree_sha256": reviewer["git"]["worktree_sha256"],
            "completed_at": "2026-09-01T12:00:00+02:00",
        }
        if status == "PASS":
            receipt.update({"command": "python3 -m unittest", "exit_code": 0})
        else:
            receipt.update(
                {
                    "reason": "No SQL change in the reviewed worktree",
                    "authorized_by": "human",
                }
            )
        path = self.memory / "negritaos" / relative
        write_json(path, receipt)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return f"{category}=memory:{relative}@sha256:{digest}"


class TestRuntimeContract(RuntimeFixture):
    """Verifies deterministic contract and state behavior."""

    def test_resolve_that_persists_hash_and_user_selected_document_route(self) -> None:
        contract = self.resolve()
        contract_path = self.memory / "negritaos" / "runtime" / "sessions"
        contract_path = contract_path / contract["session_id"] / "contract.json"
        self.assertEqual(len(contract["contract_sha256"]), 64)
        self.assertIn("document-control", contract["skills"])
        self.assertEqual(contract["artifact_route"]["selection"], "user_selected")
        self.assertTrue(contract["artifact_route"]["directory"].endswith("documents"))
        self.assertTrue(
            contract["artifact_route"]["manifest"].endswith(
                "documents/document_manifest.jsonl"
            )
        )
        self.assertIn("pptx", contract["artifact_route"]["require_explicit_path_for"])
        self.assertEqual(contract["browser_context"]["routing_policy"], "governed")
        self.assertEqual(
            contract["browser_context"]["default_profile"],
            "personal_cheetah_alo",
        )
        self.assertIn("governed-browser-routing", contract["skills"])
        self.assertEqual(
            contract["commit_identity"],
            {"policy": None, "status": "not_applicable"},
        )
        self.assertEqual(contract["model_route"]["tier"], "luna_high")
        self.assertEqual(contract["model_route"]["model"], "gpt-5.6-luna")
        self.assertEqual(
            contract["model_route"]["reasoning_effort"],
            "high",
        )
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

    def test_resolve_that_routes_global_project_hours_agent(self) -> None:
        contract = resolve_session(
            self.repo, "codex", ["tracking_hours"], ROOT, self.memory
        )

        self.assertEqual(contract["modes"], ["HOURS"])
        self.assertEqual(contract["agents"], ["project_hours_tracker_agent"])
        self.assertIn("project_hours_tracker_agent", contract["available_agents"])
        self.assertIn("project-hours-tracking", contract["agent_skills"])
        self.assertIn("project-hours-tracking", contract["skills"])
        self.assertEqual(contract["model_route"]["tier"], "luna_high")

    def test_resolve_that_routes_global_model_governance_card_agent(self) -> None:
        contract = resolve_session(
            self.repo, "codex", ["model_governance_card"], ROOT, self.memory
        )

        self.assertEqual(contract["modes"], ["MCARD"])
        self.assertEqual(contract["agents"], ["model_governance_card_agent"])
        self.assertIn("model_governance_card_agent", contract["available_agents"])
        self.assertIn("model-governance-card", contract["agent_skills"])
        self.assertIn("model-governance-card", contract["skills"])
        self.assertEqual(contract["model_route"]["tier"], "terra_high")

    def test_resolve_that_escalates_material_semantics_to_terra(self) -> None:
        contract = resolve_session(
            self.repo,
            "codex",
            ["code_review"],
            ROOT,
            self.memory,
            risk_signals=["semantic_contract_change"],
        )
        self.assertEqual(contract["model_route"]["tier"], "terra_high")
        self.assertEqual(contract["model_route"]["change_impact"], "high")
        self.assertTrue(contract["model_route"]["independent_review"]["required"])

    def test_independent_review_rejects_builder_session_reuse(self) -> None:
        builder = resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="builder-alias-a",
            environ={"CODEX_THREAD_ID": "builder-native-task"},
        )
        with self.assertRaises(ValueError):
            resolve_session(
                self.repo,
                "codex",
                ["code_review"],
                ROOT,
                self.memory,
                session_key="builder-alias-b",
                environ={"CODEX_THREAD_ID": "builder-native-task"},
                change_impact="high",
                review_role="independent_reviewer",
                review_of_session=builder["session_id"],
            )

    def test_independent_review_accepts_separate_session_and_records_target(self) -> None:
        builder = resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="builder-task",
            environ={"CODEX_THREAD_ID": "builder-native-task"},
        )
        reviewer = resolve_session(
            self.repo,
            "codex",
            ["code_review"],
            ROOT,
            self.memory,
            session_key="reviewer-task",
            environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            change_impact="high",
            review_role="independent_reviewer",
            review_of_session=builder["session_id"],
        )
        review = reviewer["model_route"]["independent_review"]
        self.assertEqual(reviewer["model_route"]["tier"], "terra_high")
        self.assertEqual(review["target"]["session_id"], builder["session_id"])
        self.assertEqual(
            review["target"]["reviewed_worktree_sha256"],
            reviewer["git"]["worktree_sha256"],
        )

    def test_high_impact_commit_requires_current_independent_pass(self) -> None:
        builder_environment = {"CODEX_THREAD_ID": "builder-native-task"}
        reviewer_environment = {"CODEX_THREAD_ID": "reviewer-native-task"}
        builder = resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="builder-task",
            environ=builder_environment,
            risk_signals=["semantic_contract_change"],
        )
        blocked = gate_action(
            self.repo,
            "commit",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="builder-task",
            environ=builder_environment,
        )
        self.assertEqual(blocked["decision"], "BLOCK")

        reviewer = resolve_session(
            self.repo,
            "codex",
            ["code_review"],
            ROOT,
            self.memory,
            session_key="reviewer-task",
            environ=reviewer_environment,
            change_impact="high",
            review_role="independent_reviewer",
            review_of_session=builder["session_id"],
        )
        closed = close_session(
            self.repo,
            status="PASS",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="reviewer-task",
            evidence_refs=[self.evidence_ref(reviewer, "applicable_tests")],
            environ=reviewer_environment,
        )
        self.assertEqual(
            closed["review"]["evidence"]["applicable_tests"]["status"],
            "PASS",
        )

        allowed = gate_action(
            self.repo,
            "commit",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="builder-task",
            environ=builder_environment,
        )
        self.assertEqual(allowed["decision"], "ALLOW")
        self.assertEqual(
            allowed["independent_review"]["review_session_id"],
            reviewer["session_id"],
        )

        (self.repo / "changed_after_review.py").write_text("VALUE = 1\n", encoding="utf-8")
        stale = gate_action(
            self.repo,
            "commit",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="builder-task",
            environ=builder_environment,
        )
        self.assertEqual(stale["decision"], "BLOCK")

    def test_independent_pass_requires_declared_evidence(self) -> None:
        builder = resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="builder-task",
            environ={"CODEX_THREAD_ID": "builder-native-task"},
            change_impact="high",
        )
        resolve_session(
            self.repo,
            "codex",
            ["code_review"],
            ROOT,
            self.memory,
            session_key="reviewer-task",
            environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            change_impact="high",
            review_role="independent_reviewer",
            review_of_session=builder["session_id"],
        )
        with self.assertRaisesRegex(SessionError, "missing evidence"):
            close_session(
                self.repo,
                status="PASS",
                negritaos_root=ROOT,
                memory_base=self.memory,
                provider="codex",
                session_key="reviewer-task",
                environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            )

    def test_independent_pass_rejects_unresolvable_or_inapplicable_test_evidence(self) -> None:
        builder = resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="builder-task",
            environ={"CODEX_THREAD_ID": "builder-native-task"},
            change_impact="high",
        )
        reviewer = resolve_session(
            self.repo,
            "codex",
            ["code_review"],
            ROOT,
            self.memory,
            session_key="reviewer-task",
            environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            change_impact="high",
            review_role="independent_reviewer",
            review_of_session=builder["session_id"],
        )
        with self.assertRaisesRegex(SessionError, "Evidence refs must use"):
            close_session(
                self.repo,
                status="PASS",
                negritaos_root=ROOT,
                memory_base=self.memory,
                provider="codex",
                session_key="reviewer-task",
                evidence_refs=["applicable_tests=MODEL_SAYS_PASS"],
                environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            )
        with self.assertRaisesRegex(SessionError, "cannot be NOT_APPLICABLE"):
            close_session(
                self.repo,
                status="PASS",
                negritaos_root=ROOT,
                memory_base=self.memory,
                provider="codex",
                session_key="reviewer-task",
                evidence_refs=[
                    self.evidence_ref(
                        reviewer,
                        "applicable_tests",
                        status="NOT_APPLICABLE",
                    )
                ],
                environ={"CODEX_THREAD_ID": "reviewer-native-task"},
            )

    def test_commit_gate_blocks_contract_that_predates_model_routing(self) -> None:
        contract = self.resolve()
        contract_path = self.memory / "negritaos" / "runtime" / "sessions"
        contract_path = contract_path / contract["session_id"] / "contract.json"
        legacy = json.loads(contract_path.read_text(encoding="utf-8"))
        legacy["model_route"] = None
        legacy.pop("contract_sha256")
        legacy["contract_sha256"] = sha256_json(legacy)
        write_json(contract_path, legacy)

        result = gate_action(
            self.repo,
            "commit",
            negritaos_root=ROOT,
            memory_base=self.memory,
        )

        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("re-run resolve", result["reasons"][-1])

        with self.assertRaisesRegex(ValueError, "predates model routing"):
            resolve_session(
                self.repo,
                "codex",
                ["code_review"],
                ROOT,
                self.memory,
                session_key="reviewer-task",
                environ={"CODEX_THREAD_ID": "reviewer-native-task"},
                change_impact="high",
                review_role="independent_reviewer",
                review_of_session=contract["session_id"],
            )

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
            Path("team-lead-qaqc/documents/report__updated_20260805_120000.pdf"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        selected_repo_path = gate_action(
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
        external_unversioned = gate_action(
            self.repo,
            "write",
            Path("/tmp/report.pdf"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        internal_skill_source = gate_action(
            self.repo,
            "write",
            Path(".codex/skills/example/SKILL.md"),
            negritaos_root=ROOT,
            memory_base=self.memory,
        )
        internal_writing_source = gate_action(
            self.repo,
            "write",
            Path("skills/writing/example.md"),
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
        self.assertEqual(selected_repo_path["decision"], "ALLOW")
        self.assertEqual(external["decision"], "ALLOW")
        self.assertEqual(external_unversioned["decision"], "BLOCK")
        self.assertEqual(internal_skill_source["decision"], "ALLOW")
        self.assertEqual(internal_writing_source["decision"], "ALLOW")
        self.assertEqual(missing_destination["decision"], "BLOCK")
        self.assertIn("not tracked by default", external["reasons"][-1])

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

    def test_stale_runtime_closure_requires_authorization_and_skips_recent(self) -> None:
        home = self.memory / "negritaos"
        sessions = home / "runtime" / "sessions"
        now = datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)

        def write_contract(session_id: str, created_at: datetime) -> Path:
            session_dir = sessions / session_id
            contract = {
                "actions": ["review"],
                "created_at": created_at.isoformat(),
                "provider": "codex",
                "schema_version": 2,
                "session_id": session_id,
                "session_identity": {"key_hash": session_id[-8:]},
                "state": "READY",
            }
            contract["contract_sha256"] = sha256_json(contract)
            write_json(session_dir / "contract.json", contract)
            return session_dir

        stale_dir = write_contract("stale-session", now - timedelta(days=3))
        recent_dir = write_contract("recent-session", now)

        preview = close_stale_runtime_sessions(
            self.repo,
            negritaos_root=ROOT,
            memory_base=self.memory,
            older_than_days=1,
            now=now,
        )
        self.assertEqual(preview["planned_count"], 1)
        self.assertFalse((stale_dir / "state.json").exists())

        with self.assertRaisesRegex(SessionError, "authorized_by"):
            close_stale_runtime_sessions(
                self.repo,
                negritaos_root=ROOT,
                memory_base=self.memory,
                older_than_days=1,
                apply_changes=True,
                now=now,
            )

        closed = close_stale_runtime_sessions(
            self.repo,
            negritaos_root=ROOT,
            memory_base=self.memory,
            older_than_days=1,
            apply_changes=True,
            authorized_by="human",
            authorization_reason="Approved stale runtime cleanup",
            now=now,
        )

        self.assertEqual(closed["closed_count"], 1)
        self.assertTrue((stale_dir / "state.json").is_file())
        self.assertFalse((recent_dir / "state.json").exists())

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
