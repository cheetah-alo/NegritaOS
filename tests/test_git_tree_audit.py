import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.git_tree_audit import _classify, _status, audit_repo


class GitTreeAuditTests(unittest.TestCase):
    def test_dirty_worktree_requires_recovery(self) -> None:
        classification = _classify("feature/x", 1, 0, {"dirty": True}, True, 5)
        self.assertEqual(classification, "RECOVERY_REQUIRED")

    def test_long_branch_requires_pr(self) -> None:
        classification = _classify("feature/x", 6, 0, {"dirty": False}, True, 5)
        self.assertEqual(classification, "PR_REQUIRED")

    def test_missing_integration_branch_blocks_audit(self) -> None:
        classification = _classify("feature/x", None, None, {"dirty": False}, False, 5)
        self.assertEqual(classification, "BLOCKED_CONFIG_RESOLUTION")

    def test_status_separates_untracked_and_modified_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "tracked.txt").write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "tracked.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "-qm", "init"],
                check=True,
            )
            (root / "tracked.txt").write_text("two\n", encoding="utf-8")
            (root / "new.txt").write_text("new\n", encoding="utf-8")
            status = _status(root)
            self.assertEqual(status["unstaged"], 1)
            self.assertEqual(status["untracked"], 1)

    def test_non_git_root_is_reported_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = audit_repo(Path(tmp))
            self.assertEqual(report["state"], "NOT_GIT")
            self.assertEqual(report["branches"], [])


if __name__ == "__main__":
    unittest.main()
