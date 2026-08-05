"""Unit tests for Negrita Brain project health checks."""

import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.doctor import doctor_project
from src.negrita_brain.installer import Installer
from src.negrita_brain.runtime import resolve_session


ROOT = Path(__file__).resolve().parents[1]


class TestDoctor(unittest.TestCase):
    """Exercise healthy, warning, and failed doctor outcomes."""

    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        base = Path(self.temporary.name)
        self.repo = base / "repo"
        self.memory = base / "memory"
        (self.repo / ".codex").mkdir(parents=True)
        (self.repo / ".git").mkdir()
        (self.repo / ".codex" / "project.yaml").write_text(
            "project_id: negritaos\n"
            f"negrita_registry: {ROOT / 'projects' / 'negritaos.yaml'}\n",
            encoding="utf-8",
        )
        Installer(ROOT, base / "backups", self.memory).install(self.repo)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_doctor_that_passes_for_installed_workspace(self) -> None:
        report = doctor_project(self.repo, ROOT, self.memory)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["issues"], [])
        self.assertIn("document-control", report["resolved_skills"])

    def test_doctor_that_warns_for_open_session(self) -> None:
        contract = resolve_session(
            self.repo,
            "codex",
            ["planning"],
            ROOT,
            self.memory,
        )

        report = doctor_project(self.repo, ROOT, self.memory)

        self.assertEqual(report["status"], "WARN")
        open_issue = next(
            issue for issue in report["issues"] if issue["code"] == "OPEN_SESSIONS"
        )
        self.assertIn(contract["session_id"], open_issue["message"])

    def test_doctor_that_fails_for_entrypoint_and_hook_drift(self) -> None:
        (self.repo / "CLAUDE.md").unlink()
        (self.repo / ".codex" / "settings.json").write_text(
            "{invalid",
            encoding="utf-8",
        )

        report = doctor_project(self.repo, ROOT, self.memory)
        codes = {issue["code"] for issue in report["issues"]}

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("ENTRYPOINT_CLAUDE", codes)
        self.assertIn("HOOKS_INVALID", codes)

    def test_doctor_that_fails_for_missing_materialized_skill(self) -> None:
        (self.repo / ".codex" / "skills" / "document-control").unlink()

        report = doctor_project(self.repo, ROOT, self.memory)

        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any(issue["code"] == "SKILL_MISSING" for issue in report["issues"])
        )

    def test_doctor_that_fails_for_missing_memory_home(self) -> None:
        shutil.rmtree(self.memory / "negritaos")

        report = doctor_project(self.repo, ROOT, self.memory)

        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any(issue["code"] == "MEMORY_HOME" for issue in report["issues"])
        )


if __name__ == "__main__":
    unittest.main()
