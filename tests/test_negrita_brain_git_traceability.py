"""Unit tests for privacy-preserving Git worktree snapshots."""

import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.negrita_brain.git_traceability import classify_worktree, snapshot_git


class TestGitTraceability(unittest.TestCase):
    """Verifies Git identity and status semantics at the subprocess boundary."""

    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repo"
        (self.root / ".git").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _completed(self, output: str = "", returncode: int = 0) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(["git"], returncode, output, "")

    def _runner(self, command: list[str], **_: object) -> subprocess.CompletedProcess:
        args = tuple(command[1:])
        outputs = {
            ("rev-parse", "--git-common-dir"): ".git",
            ("rev-parse", "--git-dir"): ".git",
            ("branch", "--show-current"): "feature/example",
            ("rev-parse", "HEAD"): "head123",
            ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"): "origin/main",
            ("status", "--porcelain=v1"): " M src/a.py\nA  src/b.py\n?? scratch.txt",
            ("merge-base", "HEAD", "origin/main"): "base123",
            ("rev-list", "--left-right", "--count", "origin/main...HEAD"): "2 3",
        }
        if args in outputs:
            return self._completed(outputs[args])
        return self._completed(returncode=1)

    def test_snapshot_that_reports_branch_base_and_dirty_counts(self) -> None:
        with patch(
            "src.negrita_brain.git_traceability.subprocess.run",
            side_effect=self._runner,
        ):
            snapshot = snapshot_git(self.root)

        self.assertEqual(snapshot["worktree_class"], "feature")
        self.assertEqual(snapshot["ahead"], 3)
        self.assertEqual(snapshot["behind"], 2)

    def test_snapshot_that_never_exposes_worktree_paths(self) -> None:
        with patch(
            "src.negrita_brain.git_traceability.subprocess.run",
            side_effect=self._runner,
        ):
            snapshot = snapshot_git(self.root)

        self.assertNotIn(str(self.root), str(snapshot))
        self.assertEqual(len(snapshot["worktree_id"]), 64)

    def test_classification_that_marks_temporary_and_detached_worktrees(self) -> None:
        temporary = classify_worktree(Path("/private/tmp/session"), "feature/x", "head")
        detached = classify_worktree(Path("/workspace/repo"), None, "head")

        self.assertEqual(temporary, "temporary")
        self.assertEqual(detached, "detached")


if __name__ == "__main__":
    unittest.main()
