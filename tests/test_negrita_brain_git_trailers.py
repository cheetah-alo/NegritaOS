"""Contract tests for safe and idempotent Negrita Git trailers."""

import unittest

from src.negrita_brain.git_trailers import (
    append_trailers,
    build_brain_trailers,
    parse_trailers,
)


class TestGitTrailers(unittest.TestCase):
    """Verifies trailer parsing and construction without Git or filesystem I/O."""

    def test_append_that_adds_missing_trailers_to_a_commit_message(self) -> None:
        message = "feat: capture session context"
        result = append_trailers(
            message,
            {
                "Negrita-Contract": "a" * 64,
                "Negrita-Session": "NBS-demo",
            },
        )

        self.assertIn("feat: capture session context\n\n", result)
        self.assertEqual(parse_trailers(result)["Negrita-Session"], "NBS-demo")

    def test_append_that_is_idempotent_when_trailers_are_already_present(self) -> None:
        message = "feat: capture session\n\nNegrita-Session: NBS-demo"
        trailers = {"Negrita-Session": "NBS-demo", "Negrita-Gates": "write"}

        once = append_trailers(message, trailers)
        twice = append_trailers(once, trailers)

        self.assertEqual(twice, once)
        self.assertEqual(twice.count("Negrita-Session:"), 1)

    def test_append_that_preserves_an_existing_value_when_input_conflicts(self) -> None:
        message = "feat: capture session\n\nNegrita-Contract: original"

        result = append_trailers(message, {"Negrita-Contract": "replacement"})

        self.assertEqual(result, message)
        self.assertEqual(parse_trailers(result)["Negrita-Contract"], "original")

    def test_append_that_rejects_unknown_and_multiline_trailers(self) -> None:
        with self.assertRaises(ValueError):
            append_trailers("subject", {"Unknown": "value"})
        with self.assertRaises(ValueError):
            append_trailers("subject", {"Negrita-Session": "line\nforged"})

    def test_build_that_derives_contract_session_worktree_gates_and_decisions(self) -> None:
        contract = {
            "session_id": "NBS-demo",
            "contract_sha256": "b" * 64,
            "git": {"worktree_id": "c" * 64},
        }

        trailers = build_brain_trailers(
            contract,
            gates=["write", "commit", "write"],
            decision_ids=["DEC-1", "DEC-2"],
        )

        self.assertEqual(trailers["Negrita-Contract"], "b" * 64)
        self.assertEqual(trailers["Negrita-Gates"], "write, commit")
        self.assertEqual(trailers["Negrita-Decision"], "DEC-1, DEC-2")


if __name__ == "__main__":
    unittest.main()
