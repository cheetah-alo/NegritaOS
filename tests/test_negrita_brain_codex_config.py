"""Tests for idempotent Codex writable-root configuration."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.codex_config import configure_codex
from src.negrita_brain.errors import ConfigurationError


class TestCodexConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        base = Path(self.temporary.name)
        self.config = base / ".codex" / "config.toml"
        self.backups = base / "backups"
        self.memory = base / ".negritaos" / "memory"
        self.config.parent.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_apply_that_preserves_existing_config_and_creates_backup(self) -> None:
        self.config.write_text(
            'model = "gpt-test"\n\n[features]\nmemories = true\n',
            encoding="utf-8",
        )

        result = configure_codex(
            True, self.config, self.memory, self.backups
        )
        text = self.config.read_text(encoding="utf-8")

        self.assertTrue(result["restart_required"])
        self.assertTrue(Path(result["backup_path"]).is_file())
        self.assertIn('model = "gpt-test"', text)
        self.assertIn("[sandbox_workspace_write]", text)
        self.assertIn(str(self.memory), text)

    def test_second_apply_that_is_idempotent(self) -> None:
        configure_codex(True, self.config, self.memory, self.backups)
        second = configure_codex(True, self.config, self.memory, self.backups)

        self.assertFalse(second["changed"])
        self.assertFalse(second["restart_required"])
        self.assertIsNone(second["backup_path"])

    def test_existing_writable_roots_that_are_extended(self) -> None:
        self.config.write_text(
            '[sandbox_workspace_write]\nwritable_roots = ["/tmp/existing"]\n',
            encoding="utf-8",
        )

        configure_codex(True, self.config, self.memory, self.backups)
        text = self.config.read_text(encoding="utf-8")

        self.assertIn("/tmp/existing", text)
        self.assertIn(str(self.memory), text)

    def test_multiline_roots_that_fail_without_rewriting(self) -> None:
        original = '[sandbox_workspace_write]\nwritable_roots = [\n  "/tmp"\n]\n'
        self.config.write_text(original, encoding="utf-8")

        with self.assertRaisesRegex(ConfigurationError, "Multiline"):
            configure_codex(True, self.config, self.memory, self.backups)

        self.assertEqual(self.config.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
