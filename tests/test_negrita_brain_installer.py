"""Unit tests for managed entrypoints, hooks, and idempotent installation."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.doctor import doctor_project
from src.negrita_brain.installer import Installer, merge_hook_settings


ROOT = Path(__file__).resolve().parents[1]


class TestInstaller(unittest.TestCase):
    """Verifies local content preservation and repeatable installation."""

    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        base = Path(self.temporary.name)
        self.repo = base / "repo"
        self.memory = base / "memory"
        self.backups = base / "backups"
        (self.repo / ".codex").mkdir(parents=True)
        (self.repo / ".git").mkdir()
        (self.repo / ".codex" / "project.yaml").write_text(
            "project_id: negritaos\n"
            f"negrita_registry: {ROOT / 'projects' / 'negritaos.yaml'}\n",
            encoding="utf-8",
        )
        (self.repo / "AGENTS.md").write_text("# Local agent guidance\n", encoding="utf-8")
        (self.repo / ".codex" / "settings.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PostToolUse": [
                            {"hooks": [{"type": "command", "command": "custom-check"}]}
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        self.installer = Installer(ROOT, self.backups, self.memory)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_install_that_preserves_local_content_and_hooks(self) -> None:
        result = self.installer.install(self.repo)
        agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        settings = (self.repo / ".codex" / "settings.json").read_text(encoding="utf-8")
        self.assertTrue(result["changed"])
        self.assertIn("Local agent guidance", agents)
        self.assertIn("custom-check", settings)

    def test_second_install_that_is_idempotent(self) -> None:
        self.installer.install(self.repo)
        second = self.installer.install(self.repo)
        self.assertFalse(second["changed"])

    def test_install_that_materializes_default_document_skills(self) -> None:
        self.installer.install(self.repo)
        self.assertTrue((self.repo / ".codex" / "skills" / "document-control").exists())
        self.assertTrue((self.repo / ".codex" / "skills" / "docs-alignment").exists())

    def test_doctor_that_passes_installed_workspace(self) -> None:
        self.installer.install(self.repo)
        report = doctor_project(self.repo, ROOT, self.memory)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["issues"], [])

    def test_doctor_that_fails_closed_before_installation(self) -> None:
        report = doctor_project(self.repo, ROOT, self.memory)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("ENTRYPOINT_AGENTS", codes)
        self.assertIn("HOOKS_INCOMPLETE", codes)

    def test_hook_merge_that_installs_all_required_events(self) -> None:
        merged = merge_hook_settings({}, ROOT / "scripts" / "negrita_brain_hook.py")
        self.assertEqual(
            set(merged["hooks"]),
            {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop", "SessionEnd"},
        )

    def test_install_all_that_discovers_registered_primary_paths(self) -> None:
        canonical = Path(self.temporary.name) / "canonical"
        (canonical / "projects").mkdir(parents=True)
        (canonical / "skills").mkdir()
        (canonical / "core" / "orchestration").mkdir(parents=True)
        for skill in ("docs-alignment", "document-control"):
            (canonical / ".codex" / "skills" / skill).mkdir(parents=True)
        (canonical / "projects" / "alpha.yaml").write_text(
            "project:\n"
            "  id: alpha\n"
            f"  local_paths:\n    primary: {self.repo}\n"
            f"  memory_home: {self.memory / 'alpha'}\n",
            encoding="utf-8",
        )
        (canonical / "projects" / "broken.yaml").write_text(
            "project:\n  id: broken\n"
            f"  local_paths:\n    primary: {Path(self.temporary.name) / 'missing'}\n",
            encoding="utf-8",
        )
        (canonical / "skills" / "catalog.yaml").write_text(
            "defaults:\n  profiles: [document-delivery]\n"
            "profiles:\n  document-delivery:\n"
            "    skills: [docs-alignment, document-control]\n"
            "skills: []\n",
            encoding="utf-8",
        )
        (canonical / "core" / "orchestration" / "negrita_brain_policy.yaml").write_text(
            "negrita_brain:\n  schema_version: 1\n", encoding="utf-8"
        )
        (self.repo / ".codex" / "project.yaml").write_text(
            "project_id: alpha\n"
            f"negrita_registry: {canonical / 'projects' / 'alpha.yaml'}\n",
            encoding="utf-8",
        )
        installer = Installer(canonical, self.backups, self.memory)
        report = installer.install_all()
        self.assertEqual(report["project_count"], 2)
        self.assertEqual(report["failed"], 1)
        self.assertTrue((self.repo / "CLAUDE.md").is_file())


if __name__ == "__main__":
    unittest.main()
