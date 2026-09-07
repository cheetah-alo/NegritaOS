"""Tests for CQI corporate commit identity policy enforcement."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.negrita_brain.commit_identity import (
    CommitIdentity,
    email_is_allowed,
    identity_violations,
    commit_identities,
    load_commit_identity_policies,
    parse_git_log,
    resolve_policy,
    validate_policy_document,
    validate_project_policy_references,
)
from scripts.check_cqi_commit_identity import github_range


POLICY = {
    "enforcement": "strict",
    "project_scope": ["project_a"],
    "allowed_email_domains": ["cqisense.com"],
    "allow_subdomains": True,
    "inspect": ["author", "committer"],
    "range": "introduced_commits_only",
    "legacy_history": "excluded",
    "hard_stop": True,
    "remediation": {
        "automatic_history_rewrite": False,
        "require_explicit_user_authorization": True,
        "force_mode": "force_with_lease_only",
    },
}


class TestCommitIdentity(unittest.TestCase):
    def test_corporate_root_and_subdomain_are_allowed(self) -> None:
        self.assertTrue(email_is_allowed("person@cqisense.com", ["cqisense.com"], True))
        self.assertTrue(
            email_is_allowed("contractor@ext.cqisense.com", ["cqisense.com"], True)
        )
        self.assertFalse(email_is_allowed("person@gmail.com", ["cqisense.com"], True))
        self.assertFalse(
            email_is_allowed(
                "person@users.noreply.github.com", ["cqisense.com"], True
            )
        )

    def test_author_and_committer_violations_are_redacted(self) -> None:
        commits = (
            CommitIdentity(
                sha="a" * 40,
                subject="bad identity",
                author_name="Author",
                author_email="author@gmail.com",
                committer_name="Committer",
                committer_email="committer@github.com",
            ),
        )

        violations = identity_violations(commits, POLICY)

        self.assertEqual(len(violations), 2)
        self.assertEqual(violations[0].redacted_email, "***@gmail.com")
        self.assertEqual(violations[1].redacted_email, "***@github.com")
        self.assertNotIn("author@gmail.com", repr(violations))

    def test_git_log_parser_preserves_complete_records(self) -> None:
        raw = (
            b"abc\0subject\0Author\0a@cqisense.com\0Committer\0"
            b"c@cqisense.com\x1e\n"
        )
        commits = parse_git_log(raw)
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].sha, "abc")

    def test_multiple_legacy_exclusions_are_negative_revisions(self) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout=b"")
        with patch("src.negrita_brain.commit_identity.subprocess.run", return_value=completed) as run:
            commits = commit_identities(
                Path("/tmp/repo"), "base", "head", ("legacy-a", "legacy-b")
            )
        self.assertEqual(commits, ())
        command = run.call_args.args[0]
        self.assertIn("^legacy-a", command)
        self.assertIn("^legacy-b", command)
        self.assertNotIn("--not", command)

    def test_github_pull_request_range_uses_event_commit_shas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            event = Path(tmp) / "event.json"
            event.write_text(
                json.dumps(
                    {
                        "pull_request": {
                            "base": {"sha": "base-sha"},
                            "head": {"sha": "head-sha"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            resolved = github_range(
                Path(tmp),
                {
                    "GITHUB_EVENT_PATH": str(event),
                    "GITHUB_SHA": "synthetic-merge-sha",
                },
            )
        self.assertEqual(resolved, ("base-sha", "head-sha"))

    def test_policy_document_requires_strict_range_and_rewrite_safety(self) -> None:
        document = {"schema_version": 1, "policies": {"cqi": POLICY}}
        self.assertEqual(validate_policy_document(document), [])

        invalid = {
            "schema_version": 1,
            "policies": {
                "cqi": {
                    **POLICY,
                    "range": "all_history",
                    "remediation": {
                        **POLICY["remediation"],
                        "automatic_history_rewrite": True,
                    },
                }
            },
        }
        errors = validate_policy_document(invalid)
        self.assertTrue(any("introduced_commits_only" in error for error in errors))
        self.assertTrue(any("automatic_history_rewrite" in error for error in errors))

    def test_project_policy_resolution_is_explicit(self) -> None:
        document = {
            "schema_version": 1,
            "policies": {"cqi_corporate_only_v1": POLICY},
        }
        resolved = resolve_policy(
            {"commit_identity_policy": "cqi_corporate_only_v1"}, document
        )
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved[0], "cqi_corporate_only_v1")
        self.assertIsNone(resolve_policy({}, document))

    def test_policy_scope_and_project_opt_in_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            projects.mkdir()
            (projects / "project_a.yaml").write_text(
                "project:\n"
                "  id: project_a\n"
                "  commit_identity_policy: cqi_corporate_only_v1\n",
                encoding="utf-8",
            )
            document = {
                "schema_version": 1,
                "policies": {"cqi_corporate_only_v1": POLICY},
            }
            self.assertEqual(
                validate_project_policy_references(root, document), []
            )
            (projects / "project_a.yaml").write_text(
                "project:\n  id: project_a\n", encoding="utf-8"
            )
            errors = validate_project_policy_references(root, document)
            self.assertTrue(any("policy scope requires" in error for error in errors))

    def test_canonical_policy_covers_all_declared_cqi_projects(self) -> None:
        root = Path(__file__).resolve().parents[1]
        document = load_commit_identity_policies(root)
        self.assertEqual(validate_project_policy_references(root, document), [])


if __name__ == "__main__":
    unittest.main()
