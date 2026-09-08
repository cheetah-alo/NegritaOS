"""Exercise real Git commits, pushes and retained hooks in disposable repositories."""

import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from src.negrita_brain.git_identity_core import allowed, ci_range, effective_violations, push_scan, scan
from src.negrita_brain.git_identity_core import git as core_git
from src.negrita_brain.git_identity_install import audit, ci_files, configure, restore


ROOT = Path(__file__).resolve().parents[1]
EMAIL = "jacky.barraza@cqisense.com"
POLICY = {"allowed_email_domains": ["cqisense.com"], "allow_subdomains": True}


class TestIdentityHooks(unittest.TestCase):
    """Use commits and a bare remote to test the actual guard boundaries."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo with spaces"
        self.repo.mkdir()
        self.run_git("init", "-q", "-b", "main")
        self.run_git("config", "user.name", "Fixture User")
        self.run_git("config", "user.email", "fixture@gmail.com")
        self.run_git("config", "commit.gpgsign", "false")
        self.run_git("commit", "--allow-empty", "-qm", "legacy")
        self.base = self.run_git("rev-parse", "HEAD").stdout.strip()
        (self.repo / ".codex").mkdir()
        (self.repo / ".codex/project.yaml").write_text(
            "project_id: ibc_fiber_network\n"
            f"negrita_registry: {ROOT / 'projects/ibc_fiber_network.yaml'}\n"
        )

    def run_git(self, *args, env=None, check=True):
        """Run Git in the temporary workspace with optional identity overrides."""
        return subprocess.run(["git", "-C", str(self.repo), *args], env=env,
                              capture_output=True, text=True, check=check)

    def test_installer_is_idempotent_and_preserves_other_hooks(self):
        hooks = self.repo / ".git/hooks"
        old = hooks / "pre-commit"
        old.write_text("#!/bin/sh\necho retained >&2\n")
        old.chmod(0o755)
        other = hooks / "commit-msg"
        other.write_text("#!/bin/sh\nexit 0\n")
        other.chmod(0o755)
        before = old.read_bytes()
        result = configure(self.repo, ROOT, apply=True, with_ci=True)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(Path(result["backup"]).is_dir())
        self.assertEqual(old.read_bytes(), before)
        self.assertFalse(configure(self.repo, ROOT, apply=True, with_ci=True)["changed"])
        commit = self.run_git("commit", "--allow-empty", "-qm", "corporate")
        self.assertIn("retained", commit.stderr)
        self.assertEqual(audit(self.repo, ROOT)["status"], "PASS")

    def test_actual_commit_rejects_env_and_author_flag_overrides(self):
        configure(self.repo, ROOT, apply=True)
        for variable in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
            with self.subTest(variable=variable):
                env = {**os.environ, variable: "someone@gmail.com"}
                result = self.run_git("commit", "--allow-empty", "-qm", "bad", env=env, check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("someone@gmail.com", result.stderr)
        result = self.run_git("commit", "--allow-empty", "-qm", "bad flag",
                              "--author=Other <other@cqisense.com>", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_local_exact_identity_is_stricter_than_team_policy(self):
        configure(self.repo, ROOT, apply=True)
        self.run_git("config", "user.email", "other@cqisense.com")
        self.assertEqual(len(effective_violations(self.repo, EMAIL)), 2)
        self.assertTrue(allowed("other@cqisense.com", POLICY))
        for malformed in ("a@gmail.com@cqisense.com", "a@.cqisense.com", "a@cqisense.com.evil.test"):
            self.assertFalse(allowed(malformed, POLICY))

    def test_push_checks_commits_even_when_current_email_is_correct(self):
        remote = Path(self.temp.name) / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.run_git("remote", "add", "origin", str(remote))
        self.run_git("push", "-q", "origin", "main")
        configure(self.repo, ROOT, apply=True)
        env = {**os.environ, "GIT_AUTHOR_EMAIL": "wrong@gmail.com"}
        self.run_git("-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", "bad", env=env)
        result = self.run_git("push", "origin", "main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("***@gmail.com", result.stderr)
        self.assertNotIn("wrong@gmail.com", result.stderr)

    def test_new_branch_excludes_remote_legacy_and_deleted_refs(self):
        remote = Path(self.temp.name) / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.run_git("remote", "add", "origin", str(remote))
        self.run_git("push", "-q", "origin", "main")
        configure(self.repo, ROOT, apply=True)
        self.run_git("checkout", "-qb", "feature/test")
        self.run_git("commit", "--allow-empty", "-qm", "new")
        self.run_git("push", "origin", "feature/test")
        zero = "0" * 40
        self.assertEqual(push_scan(self.repo, str(remote), f"(delete) {zero} refs/heads/main {self.base}", POLICY), [])

    def test_preserved_pre_push_receives_same_stdin_and_can_block(self):
        remote = Path(self.temp.name) / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.run_git("remote", "add", "origin", str(remote))
        self.run_git("push", "-q", "origin", "main")
        hook = self.repo / ".git/hooks/pre-push"
        hook.write_text('#!/bin/sh\nread a b c d\ntest "$a" = "refs/heads/main" || exit 9\n'
                        'echo retained-push >&2\nexit 7\n')
        hook.chmod(0o755)
        configure(self.repo, ROOT, apply=True)
        self.run_git("commit", "--allow-empty", "-qm", "valid")
        result = self.run_git("push", "origin", "main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("retained-push", result.stderr)

    def test_ci_only_scans_introduced_commits_and_ignores_mailmap(self):
        self.run_git("config", "user.email", EMAIL)
        self.run_git("commit", "--allow-empty", "-qm", "valid")
        result = scan(self.repo, "HEAD", [self.base], POLICY)
        self.assertEqual(result["commits_checked"], 1)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(scan(self.repo, "HEAD", [], POLICY)["status"], "FAIL")
        (self.repo / ".mailmap").write_text(f"User <{EMAIL}> Fixture User <fixture@gmail.com>\n")
        self.assertEqual(scan(self.repo, "HEAD", [], POLICY)["status"], "FAIL")

    def test_ref_option_injection_and_missing_base_fail_closed(self):
        for base in ("--all", "does-not-exist"):
            with self.assertRaises(ValueError):
                scan(self.repo, "HEAD", [base], POLICY)

    def test_ci_uses_pr_head_and_rejects_missing_push_base(self):
        head = "b" * 40
        event = {"pull_request": {"base": {"sha": self.base}, "head": {"sha": head}}}
        self.assertEqual(ci_range(event, "pull_request_target"), (head, [self.base]))
        with self.assertRaises(ValueError):
            ci_range({"before": "0" * 40, "after": head}, "push")

    def test_ci_materialization_has_no_private_paths_and_detects_edits(self):
        configure(self.repo, ROOT, apply=True, with_ci=True)
        state = json.loads((self.repo / ".git/identity-guard.json").read_text())
        for relative in state["ci_hashes_by_checkout"][str(self.repo.resolve())]:
            text = (self.repo / relative).read_text()
            self.assertNotIn("Negrita", text)
            self.assertNotIn("/Users/", text)
        target = self.repo / "scripts/check_git_identity.py"
        target.write_text(target.read_text() + "\n# Local edit\n")
        with self.assertRaises(ValueError):
            configure(self.repo, ROOT, apply=True, with_ci=True)

    def test_restore_returns_original_local_identity_and_retains_ci(self):
        configure(self.repo, ROOT, apply=True, with_ci=True)
        result = restore(self.repo)
        self.assertEqual(result["status"], "RESTORED")
        self.assertEqual(self.run_git("config", "--local", "user.email").stdout.strip(), "fixture@gmail.com")
        self.assertTrue((self.repo / "scripts/check_git_identity.py").exists())

    def test_empty_range_does_not_hide_invalid_policy(self):
        with self.assertRaises(ValueError):
            scan(self.repo, "HEAD", ["HEAD"], {})

    def test_shallow_clone_is_not_certified(self):
        clone = Path(self.temp.name) / "shallow"
        self.run_git("clone", "--depth=1", self.repo.as_uri(), str(clone))
        with self.assertRaises(ValueError):
            scan(clone, "HEAD", [], POLICY)

    def test_installed_hook_is_independent_of_canonical_adapter(self):
        configure(self.repo, ROOT, apply=True)
        (self.repo / ".codex/project.yaml").unlink()
        self.run_git("commit", "--allow-empty", "-qm", "stable runtime")

    def test_worktree_override_blocks_before_any_shared_config_write(self):
        self.run_git("config", "extensions.worktreeConfig", "true")
        linked = Path(self.temp.name) / "linked"
        self.run_git("worktree", "add", "-qb", "feature/linked", str(linked))
        subprocess.run(["git", "-C", str(linked), "config", "--worktree", "user.email", "other@gmail.com"],
                       check=True)
        config = (self.repo / ".git/config").read_bytes()
        with self.assertRaises(ValueError):
            configure(linked, ROOT, apply=True)
        with self.assertRaises(ValueError):
            configure(self.repo, ROOT, apply=True)
        self.assertEqual((self.repo / ".git/config").read_bytes(), config)
        self.assertFalse((self.repo / ".git/identity-guard.json").exists())

    def test_activation_failure_restores_owned_files_and_config(self):
        original_email = self.run_git("config", "--local", "user.email").stdout

        def fail_last_config(repo, *args, **kwargs):
            if args[:4] == ("config", "--local", "--replace-all", "core.hooksPath"):
                raise OSError("simulated activation error")
            return core_git(repo, *args, **kwargs)

        with patch("src.negrita_brain.git_identity_install.git", side_effect=fail_last_config):
            with self.assertRaises(OSError):
                configure(self.repo, ROOT, apply=True, with_ci=True)
        self.assertEqual(self.run_git("config", "--local", "user.email").stdout, original_email)
        self.assertFalse((self.repo / ".git/identity-hooks").exists())
        self.assertFalse((self.repo / ".git/identity-guard.json").exists())
        self.assertFalse((self.repo / "scripts/check_git_identity.py").exists())
        self.assertFalse((self.repo / ".git/identity-runtime").exists())

    def test_linked_worktrees_keep_independent_ci_update_receipts(self):
        linked = Path(self.temp.name) / "linked"
        self.run_git("worktree", "add", "-qb", "feature/linked", str(linked))
        (linked / ".codex").mkdir()
        (linked / ".codex/project.yaml").write_bytes((self.repo / ".codex/project.yaml").read_bytes())
        configure(self.repo, ROOT, apply=True, with_ci=True)
        configure(linked, ROOT, apply=True, with_ci=True)
        files = ci_files(ROOT, POLICY)
        files["scripts/check_git_identity.py"] += b"\n# New canonical version\n"
        with patch("src.negrita_brain.git_identity_install.ci_files", return_value=files):
            self.assertEqual(configure(self.repo, ROOT, apply=True, with_ci=True)["status"], "PASS")
            self.assertEqual(configure(linked, ROOT, apply=True, with_ci=True)["status"], "PASS")
        self.assertEqual((linked / "scripts/check_git_identity.py").read_bytes(),
                         (self.repo / "scripts/check_git_identity.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
