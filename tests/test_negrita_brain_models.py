"""Tests for atomic and concurrent persistence primitives."""

import json
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.models import append_jsonl, atomic_write_text, write_json


class TestPersistencePrimitives(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_atomic_text_that_replaces_content_without_temp_residue(self) -> None:
        target = self.root / "state.json"
        target.write_text("old", encoding="utf-8")

        atomic_write_text(target, "new")

        self.assertEqual(target.read_text(encoding="utf-8"), "new")
        self.assertEqual(list(self.root.glob(".state.json.*.tmp")), [])

    def test_concurrent_json_writes_that_always_publish_a_complete_object(self) -> None:
        target = self.root / "pointer.json"

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda value: write_json(target, {"value": value}), range(50)))

        published = json.loads(target.read_text(encoding="utf-8"))
        self.assertIn(published["value"], range(50))
        self.assertEqual(list(self.root.glob(".pointer.json.*.tmp")), [])

    def test_concurrent_jsonl_appends_that_preserve_every_record(self) -> None:
        ledger = self.root / "observations.jsonl"

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda value: append_jsonl(ledger, {"id": value}), range(100)))

        records = [json.loads(line) for line in ledger.read_text().splitlines()]
        self.assertEqual(len(records), 100)
        self.assertEqual({record["id"] for record in records}, set(range(100)))


if __name__ == "__main__":
    unittest.main()
