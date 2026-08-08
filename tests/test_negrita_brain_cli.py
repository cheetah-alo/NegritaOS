"""Contract tests for Memory v2 public CLI grammar."""

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "negrita_brain_cli", ROOT / "scripts" / "negrita_brain.py"
)
assert SPEC is not None and SPEC.loader is not None
CLI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLI)


class TestBrainCli(unittest.TestCase):
    def test_resolve_that_accepts_explicit_session_key(self) -> None:
        args = CLI.build_parser().parse_args(
            [
                "resolve",
                "--provider",
                "codex",
                "--session-key",
                "thread-a",
                "--action",
                "implementation",
            ]
        )

        self.assertEqual(args.provider, "codex")
        self.assertEqual(args.session_key, "thread-a")

    def test_git_trace_that_accepts_a_workspace_root(self) -> None:
        args = CLI.build_parser().parse_args(["git-trace", "--root", "/tmp/repo"])

        self.assertEqual(args.command, "git-trace")
        self.assertEqual(args.root, Path("/tmp/repo"))

    def test_git_trailers_that_accepts_gates_and_decisions(self) -> None:
        args = CLI.build_parser().parse_args(
            [
                "git-trailers",
                "--gate",
                "write",
                "--gate",
                "commit",
                "--decision-id",
                "DEC-1",
            ]
        )

        self.assertEqual(args.command, "git-trailers")
        self.assertEqual(args.gates, ["write", "commit"])
        self.assertEqual(args.decision_ids, ["DEC-1"])

    def test_event_that_accepts_git_commit_metadata(self) -> None:
        args = CLI.build_parser().parse_args(
            [
                "event",
                "--kind",
                "commit",
                "--status",
                "OK",
                "--commit-sha",
                "abc123",
                "--parent-sha",
                "parent123",
                "--changed-file-count",
                "2",
            ]
        )

        self.assertEqual(args.commit_sha, "abc123")
        self.assertEqual(args.parent_shas, ["parent123"])
        self.assertEqual(args.changed_file_count, 2)

    def test_memory_that_exposes_all_v2_operations(self) -> None:
        parser = CLI.build_parser()
        operations = {
            parser.parse_args(["memory", "status"]).memory_command,
            parser.parse_args(
                [
                    "memory",
                    "remember",
                    "--type",
                    "discovery",
                    "--title",
                    "title",
                    "--summary",
                    "summary",
                    "--learned",
                    "learned",
                ]
            ).memory_command,
            parser.parse_args(
                ["memory", "handoff", "--title", "title", "--goal", "goal"]
            ).memory_command,
            parser.parse_args(["memory", "migrate", "--dry-run"]).memory_command,
            parser.parse_args(
                ["memory", "rebuild-index", "--dry-run"]
            ).memory_command,
        }

        self.assertEqual(
            operations,
            {"status", "remember", "handoff", "migrate", "rebuild-index"},
        )

    def test_configure_codex_that_supports_check_and_apply(self) -> None:
        parser = CLI.build_parser()

        checked = parser.parse_args(["configure", "codex", "--check"])
        applied = parser.parse_args(["configure", "codex", "--apply"])

        self.assertTrue(checked.check)
        self.assertFalse(checked.apply)
        self.assertTrue(applied.apply)


if __name__ == "__main__":
    unittest.main()
