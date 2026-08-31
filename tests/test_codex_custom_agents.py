"""Tests for project-scoped Codex custom agent distribution."""

import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.sync_codex_custom_agents import configured_agents, sync_repo
from scripts.validate_codex_custom_agents import (
    validate_registry_declarations,
    validate_repo,
    validate_toml,
)


class TestCodexCustomAgents(unittest.TestCase):
    """Locks registry selection, TOML validation, and adapter materialization."""

    def _fixture(self, base: Path) -> tuple[Path, Path]:
        root = base / "NegritaOS"
        repo = base / "moneyflowlist"
        (root / "projects").mkdir(parents=True)
        (root / ".codex" / "agents").mkdir(parents=True)
        (repo / ".codex").mkdir(parents=True)
        (repo / ".codex" / "project.yaml").write_text(
            "project_id: moneyflowlist\n", encoding="utf-8"
        )
        (root / "projects" / "moneyflowlist.yaml").write_text(
            "project:\n"
            "  id: moneyflowlist\n"
            "  codex_custom_agents: [pablo]\n",
            encoding="utf-8",
        )
        (root / ".codex" / "agents" / "pablo.toml").write_text(
            'name = "pablo"\n'
            'description = "Deployment operator"\n'
            'developer_instructions = "Deploy exact commits only with explicit '
            'authorization for that exact operation; otherwise return '
            'BLOCKED_FINANCIAL_AUTHORIZATION"\n'
            'sandbox_mode = "read-only"\n',
            encoding="utf-8",
        )
        return root, repo

    def test_registry_selects_declared_agents(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root, repo = self._fixture(Path(temporary_directory))
            self.assertEqual(configured_agents(repo, root), ["pablo"])

    def test_sync_creates_canonical_symlink(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root, repo = self._fixture(Path(temporary_directory))
            sync_repo(repo, root, dry_run=False)
            destination = repo / ".codex" / "agents" / "pablo.toml"
            self.assertTrue(destination.is_symlink())
            self.assertEqual(validate_repo(repo, root), [])

    def test_invalid_name_or_sandbox_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pablo.toml"
            path.write_text(
                'name = "other"\n'
                'description = "Deployment operator"\n'
                'developer_instructions = "Deploy exact commits only with explicit '
                'authorization for that exact operation; otherwise return '
                'BLOCKED_FINANCIAL_AUTHORIZATION"\n'
                'sandbox_mode = "unsupported"\n',
                encoding="utf-8",
            )
            errors = validate_toml(path, "pablo")
            self.assertTrue(any("name must match" in error for error in errors))
            self.assertTrue(any("unsupported sandbox_mode" in error for error in errors))

    def test_missing_financial_control_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pablo.toml"
            path.write_text(
                'name = "pablo"\n'
                'description = "Deployment operator"\n'
                'developer_instructions = "Deploy exact commits"\n'
                'sandbox_mode = "read-only"\n',
                encoding="utf-8",
            )
            errors = validate_toml(path, "pablo")
            self.assertTrue(
                any("missing financial control marker" in error for error in errors)
            )

    def test_registry_validation_does_not_read_external_adapter(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            root, _ = self._fixture(base)
            registry = root / "projects" / "moneyflowlist.yaml"
            registry.write_text(
                "project:\n"
                "  id: moneyflowlist\n"
                "  local_paths:\n"
                "    primary: /restricted/external/repo\n"
                "  codex_custom_agents: [pablo]\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_registry_declarations(root), [])

    def test_unreadable_adapter_is_reported_without_traceback(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root, repo = self._fixture(Path(temporary_directory))
            with patch(
                "scripts.validate_codex_custom_agents.configured_agents",
                side_effect=PermissionError("adapter denied"),
            ):
                errors = validate_repo(repo, root)
            self.assertEqual(len(errors), 1)
            self.assertIn("cannot resolve custom agents", errors[0])
            self.assertIn("adapter denied", errors[0])


if __name__ == "__main__":
    unittest.main()
