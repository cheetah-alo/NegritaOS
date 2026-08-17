import unittest
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.quick_validate import validate_skill


class TestQuickValidate(unittest.TestCase):
    def _write_skill(self, root: Path, body: str) -> Path:
        skill = root / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: example\n"
            "description: Example skill.\n"
            "---\n\n"
            f"{body}\n",
            encoding="utf-8",
        )
        return skill

    def test_glob_references_pass_when_pattern_matches(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "rules").mkdir()
            (root / "rules" / "example.md").write_text("rule", encoding="utf-8")
            (root / ".codex").mkdir()
            (root / ".codex" / "system.md").write_text("system", encoding="utf-8")
            skill = self._write_skill(root, "Use `rules/*` and `.codex/*`.")

            with patch("pathlib.Path.cwd", return_value=root):
                self.assertEqual(validate_skill(skill), [])

    def test_glob_references_report_when_pattern_has_no_matches(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = self._write_skill(root, "Use `rules/*`.")

            with patch("pathlib.Path.cwd", return_value=root):
                self.assertEqual(
                    validate_skill(skill),
                    ["referenced path pattern has no matches: rules/*"],
                )

    def test_command_spans_are_not_treated_as_missing_paths(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = self._write_skill(root, "Run `.codex/skills/tool/run.sh --dry-run`.")

            with patch("pathlib.Path.cwd", return_value=root):
                self.assertEqual(validate_skill(skill), [])

    def test_skill_sync_dry_run_succeeds(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        script = repo_root / ".codex/skills/skill-sync/assets/sync.sh"
        result = subprocess.run(
            [str(script), "--dry-run"],
            check=False,
            capture_output=True,
            cwd=repo_root,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
