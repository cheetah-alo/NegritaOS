"""Tests for project-scoped Codex custom agent distribution."""

import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.sync_codex_custom_agents import (
    configured_agents,
    global_custom_agents,
    sync_user_home,
    sync_repo,
)
from scripts.validate_codex_custom_agents import (
    validate_registry_declarations,
    validate_repo,
    validate_toml,
    validate_user_home,
)


class TestCodexCustomAgents(unittest.TestCase):
    """Locks registry selection, TOML validation, and adapter materialization."""

    def _fixture(self, base: Path) -> tuple[Path, Path]:
        root = base / "NegritaOS"
        repo = base / "moneyflowlist"
        (root / "projects").mkdir(parents=True)
        (root / ".codex" / "agents").mkdir(parents=True)
        (root / "core" / "orchestration").mkdir(parents=True)
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
        (root / "core" / "orchestration" / "model_escalation_policy.yaml").write_text(
            "model_escalation_policy:\n"
            "  global_codex_custom_agents: []\n"
            "  tiers:\n"
            "    luna_high:\n"
            "      model: gpt-5.6-luna\n"
            "      reasoning_effort: high\n"
            "  custom_agent_tiers:\n"
            "    pablo: luna_high\n",
            encoding="utf-8",
        )
        (root / ".codex" / "agents" / "pablo.toml").write_text(
            'name = "pablo"\n'
            'description = "Deployment operator"\n'
            'model = "gpt-5.6-luna"\n'
            'model_reasoning_effort = "high"\n'
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

    def test_sync_user_home_creates_global_agent_symlink(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            root, _ = self._fixture(base)
            policy = root / "core" / "orchestration" / "model_escalation_policy.yaml"
            policy.write_text(
                policy.read_text(encoding="utf-8").replace(
                    "global_codex_custom_agents: []",
                    "global_codex_custom_agents: [pablo]",
                ),
                encoding="utf-8",
            )
            codex_home = base / "codex-home"

            self.assertEqual(
                sync_user_home(root, codex_home, dry_run=False), ["pablo"]
            )
            destination = codex_home / "agents" / "pablo.toml"
            self.assertTrue(destination.is_symlink())
            self.assertEqual(validate_user_home(codex_home, root), [])

    def test_global_distribution_requires_every_canonical_toml(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root, _ = self._fixture(Path(temporary_directory))
            policy = root / "core" / "orchestration" / "model_escalation_policy.yaml"
            policy.write_text(
                policy.read_text(encoding="utf-8")
                + "  custom_agent_distribution:\n"
                + "    all_canonical_agents_global: true\n",
                encoding="utf-8",
            )

            errors = validate_registry_declarations(root)

            self.assertTrue(
                any("not globally declared: pablo" in error for error in errors)
            )

    def test_invalid_name_or_sandbox_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pablo.toml"
            path.write_text(
                'name = "other"\n'
                'description = "Deployment operator"\n'
                'model = "gpt-5.6-luna"\n'
                'model_reasoning_effort = "high"\n'
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
                'model = "gpt-5.6-luna"\n'
                'model_reasoning_effort = "high"\n'
                'developer_instructions = "Deploy exact commits"\n'
                'sandbox_mode = "read-only"\n',
                encoding="utf-8",
            )
            errors = validate_toml(path, "pablo")
            self.assertTrue(
                any("missing financial control marker" in error for error in errors)
            )

    def test_model_tier_drift_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pablo.toml"
            path.write_text(
                'name = "pablo"\n'
                'description = "Deployment operator"\n'
                'model = "gpt-5.6-sol"\n'
                'model_reasoning_effort = "high"\n'
                'developer_instructions = "Use explicit authorization for that exact '
                'operation or return BLOCKED_FINANCIAL_AUTHORIZATION"\n',
                encoding="utf-8",
            )
            errors = validate_toml(path, "pablo")
            self.assertTrue(any("model must be 'gpt-5.6-luna'" in error for error in errors))

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

    def test_global_agent_name_cannot_escape_canonical_directory(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root, _ = self._fixture(Path(temporary_directory))
            policy = root / "core" / "orchestration" / "model_escalation_policy.yaml"
            policy.write_text(
                "model_escalation_policy:\n"
                "  global_codex_custom_agents: [../../escape]\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "invalid global custom agent name"):
                global_custom_agents(root)


if __name__ == "__main__":
    unittest.main()
