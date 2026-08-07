"""Tests for canonical durable memory, migration, and index governance."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.errors import SessionError
from src.negrita_brain.installer import Installer
from src.negrita_brain.memory import (
    INDEX_START,
    handoff,
    memory_status,
    migrate_memory,
    rebuild_index,
    remember,
)
from src.negrita_brain.runtime import close_session, resolve_session


ROOT = Path(__file__).resolve().parents[1]


class MemoryFixture(unittest.TestCase):
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
        self.home = self.memory / "negritaos"

    def tearDown(self) -> None:
        self.temporary.cleanup()


class TestDurableMemory(MemoryFixture):
    def test_remember_that_appends_one_reusable_observation(self) -> None:
        resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="thread-a",
        )

        result = remember(
            self.repo,
            "discovery",
            "Pointer isolation",
            "Provider sessions require separate pointers.",
            "Never use one workspace-global active pointer.",
            ["memory-v2"],
            ["src/negrita_brain/runtime.py"],
            ROOT,
            self.memory,
            "codex",
            "thread-a",
        )

        records = [
            json.loads(line)
            for line in (self.home / "observations.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["memory_id"], result["memory_id"])
        self.assertEqual(records[0]["session_id"], result["session_id"])

    def test_handoff_that_creates_one_session_and_managed_index(self) -> None:
        resolve_session(
            self.repo,
            "codex",
            ["implementation"],
            ROOT,
            self.memory,
            session_key="thread-a",
        )
        (self.home / "index.md").write_text(
            "# Existing curated memory\n\nKeep this section.\n", encoding="utf-8"
        )

        result = handoff(
            self.repo,
            "Memory v2 implementation",
            "Separate runtime and durable memory.",
            discoveries=["The v1 close path rewrote index.md."],
            accomplished=["Added provider-scoped pointers."],
            next_steps=["Run full validation."],
            files=["src/negrita_brain/memory.py"],
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="thread-a",
        )

        session = self.home / result["durable_ref"]
        index = (self.home / "index.md").read_text(encoding="utf-8")
        self.assertTrue(session.is_file())
        self.assertIn("Keep this section.", index)
        self.assertIn(INDEX_START, index)
        self.assertIn(session.name, index)

    def test_plain_close_that_does_not_create_durable_memory(self) -> None:
        contract = resolve_session(
            self.repo,
            "codex",
            ["planning"],
            ROOT,
            self.memory,
            session_key="thread-a",
        )

        close_session(
            self.repo,
            "No reusable finding",
            negritaos_root=ROOT,
            memory_base=self.memory,
            provider="codex",
            session_key="thread-a",
        )

        session_dir = self.home / "runtime" / "sessions" / contract["session_id"]
        self.assertTrue((session_dir / "state.json").is_file())
        self.assertFalse((session_dir / "summary.json").exists())
        self.assertFalse((self.home / "observations.jsonl").exists())
        self.assertEqual(memory_status(self.repo, ROOT, self.memory)["durable_session_count"], 0)


class TestMemoryMigration(MemoryFixture):
    def test_migration_that_is_idempotent_and_preserves_sources(self) -> None:
        legacy = self.home / "runtime" / "sessions" / "legacy-session"
        legacy.mkdir(parents=True)
        (legacy / "contract.json").write_text(
            json.dumps({"schema_version": 1}), encoding="utf-8"
        )
        before = (legacy / "contract.json").read_bytes()

        preview = migrate_memory(self.repo, False, ROOT, self.memory)
        applied = migrate_memory(self.repo, True, ROOT, self.memory)
        repeated = migrate_memory(self.repo, True, ROOT, self.memory)

        self.assertGreater(preview["new_records"], 0)
        self.assertEqual(applied["new_records"], preview["new_records"])
        self.assertEqual(repeated["new_records"], 0)
        self.assertEqual((legacy / "contract.json").read_bytes(), before)
        catalog = self.home / "catalog" / "legacy_memory.jsonl"
        records = [json.loads(line) for line in catalog.read_text().splitlines()]
        self.assertTrue(all(record["canonical_reference"] for record in records))

    def test_rebuild_that_refuses_open_v1_and_backs_up_after_close(self) -> None:
        legacy = self.home / "runtime" / "sessions" / "legacy-session"
        legacy.mkdir(parents=True)
        (legacy / "contract.json").write_text(
            json.dumps({"schema_version": 1}), encoding="utf-8"
        )
        index = self.home / "index.md"
        index.write_text("# negritaos Memory\n\n## Runtime Sessions\n", encoding="utf-8")

        with self.assertRaisesRegex(SessionError, "Memory v1 sessions are active"):
            rebuild_index(self.repo, True, ROOT, self.memory)

        (legacy / "summary.json").write_text("{}", encoding="utf-8")
        result = rebuild_index(self.repo, True, ROOT, self.memory)

        self.assertTrue(result["changed"])
        self.assertTrue(Path(result["backup_path"]).is_file())
        self.assertIn(INDEX_START, index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
