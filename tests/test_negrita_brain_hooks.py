"""Unit tests for Claude hook mutation classification."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "negrita_brain_hook", ROOT / "scripts" / "negrita_brain_hook.py"
)
assert SPEC is not None and SPEC.loader is not None
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


class TestHookClassification(unittest.TestCase):
    """Ensures mutating Claude tools reach the fail-closed gate."""

    def test_edit_tool_that_is_classified_as_write(self) -> None:
        action, path = HOOK._action_and_path("Edit", {"file_path": "src/app.py"})
        self.assertEqual(action, "write")
        self.assertEqual(path, Path("src/app.py"))

    def test_git_commit_that_reaches_the_independent_review_gate(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "git commit -m test"})
        self.assertEqual(action, "commit")

    def test_wrapped_git_commit_forms_reach_the_independent_review_gate(self) -> None:
        commands = (
            "git -C repo commit -m test",
            "git -c user.name=test commit -m test",
            "/usr/bin/git commit -m test",
            "command git commit -m test",
            "bash -c 'git commit -m test'",
            "$GIT commit -m test",
        )
        for command in commands:
            with self.subTest(command=command):
                action, _ = HOOK._action_and_path("Bash", {"command": command})
                self.assertEqual(action, "commit")

    def test_other_mutating_bash_that_is_classified_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "git add src/app.py"})
        self.assertEqual(action, "write")

    def test_read_only_bash_that_remains_read(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "git status --short"})
        self.assertEqual(action, "read")

    def test_unknown_bash_that_fails_closed_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "custom-tool deploy"})
        self.assertEqual(action, "write")

    def test_shell_redirection_that_is_classified_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "echo value > output.txt"})
        self.assertEqual(action, "write")

    def test_bash_deliverable_that_exposes_destination_to_document_gate(self) -> None:
        action, path = HOOK._action_and_path(
            "Bash",
            {
                "command": (
                    "cp source.pdf "
                    "documents/report__updated_20260805_120000.pdf"
                )
            },
        )

        self.assertEqual(action, "write")
        self.assertEqual(
            path,
            Path("documents/report__updated_20260805_120000.pdf"),
        )

    def test_claude_session_id_that_is_used_as_brain_session_key(self) -> None:
        self.assertEqual(HOOK._session_key({"session_id": "claude-123"}), "claude-123")
        self.assertIsNone(HOOK._session_key({"session_id": ""}))

    def test_hook_context_exposes_model_semantics_without_false_claude_identity(self) -> None:
        context = HOOK._brain_context(
            {
                "state": "READY",
                "session_id": "NBS-test",
                "profiles": ["document-delivery"],
                "model_route": {
                    "tier": "terra_high",
                    "recommended_codex_model": "gpt-5.6-terra",
                    "change_impact": "high",
                    "independent_review": {"required": True},
                },
            }
        )

        self.assertIn("model_tier=terra_high", context)
        self.assertIn("codex_delegate=gpt-5.6-terra", context)
        self.assertIn("independent_review_required=True", context)
        self.assertIn("re-resolve with explicit action/risk signals", context)

    def test_prompt_routing_detects_semantic_and_production_risk_without_returning_prompt(self) -> None:
        prompt = "Change the score threshold for the production candidate"

        actions, signals, impact = HOOK._prompt_routing({"prompt": prompt})

        self.assertEqual(actions, ["model_review"])
        self.assertIn("score_or_segmentation_contract_decision", signals)
        self.assertIn("production_candidate_final_review", signals)
        self.assertEqual(impact, "production_candidate")
        self.assertNotIn(prompt, repr((actions, signals, impact)))

    def test_user_prompt_refreshes_contract_with_prompt_specific_route(self) -> None:
        contract = {
            "state": "READY",
            "session_id": "NBS-test",
            "profiles": [],
            "model_route": {
                "tier": "sol_high",
                "recommended_codex_model": "gpt-5.6-sol",
                "change_impact": "production_candidate",
                "independent_review": {"required": True},
            },
        }
        payload = {
            "cwd": str(ROOT),
            "session_id": "claude-123",
            "prompt": "Approve a production candidate architecture change",
        }
        with patch.object(HOOK, "close_session"), patch.object(
            HOOK, "resolve_session", return_value=contract
        ) as resolve, patch.object(HOOK, "_hook_output"):
            result = HOOK.handle("UserPromptSubmit", payload)

        self.assertEqual(result, 0)
        kwargs = resolve.call_args.kwargs
        self.assertEqual(resolve.call_args.args[2], ["architecture"])
        self.assertIn("architecture_decision", kwargs["risk_signals"])
        self.assertIn("production_candidate_final_review", kwargs["risk_signals"])
        self.assertEqual(kwargs["change_impact"], "production_candidate")


if __name__ == "__main__":
    unittest.main()
