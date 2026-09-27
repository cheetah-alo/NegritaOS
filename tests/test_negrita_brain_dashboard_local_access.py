"""Unit tests for the local-only CAT-005B policy loader."""

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from negrita_brain.dashboard_local_access import LocalPolicyError, load_local_catalog_scope


class TestDashboardLocalAccess(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.config_path = self.root / "policy.json"

    def _write_policy(self, payload: object, mode: int = 0o600) -> None:
        self.config_path.write_text(json.dumps(payload), encoding="utf-8")
        self.config_path.chmod(mode)

    def test_missing_config_returns_default_deny_scope(self) -> None:
        scope = load_local_catalog_scope(self.config_path)

        self.assertEqual(scope.project_client_grants, frozenset())
        self.assertEqual(scope.project_grants, frozenset())
        self.assertEqual(scope.unknown_client_projects, frozenset())

    def test_valid_config_loads_pair_and_unknown_project_grants(self) -> None:
        self._write_policy(
            {
                "schema_version": 1,
                "project_client_grants": [{"project_id": "alpha", "client_id": "client-a"}],
                "unknown_client_projects": ["mystery"],
            }
        )

        scope = load_local_catalog_scope(self.config_path)

        self.assertEqual(scope.project_client_grants, frozenset({("alpha", "client-a")}))
        self.assertEqual(scope.project_grants, frozenset({"mystery"}))
        self.assertEqual(scope.unknown_client_projects, frozenset({"mystery"}))

    def test_group_or_world_permissions_are_rejected(self) -> None:
        self._write_policy(
            {"schema_version": 1, "project_client_grants": [], "unknown_client_projects": []},
            mode=0o640,
        )

        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_symlink_is_rejected(self) -> None:
        target = self.root / "target.json"
        target.write_text("{}", encoding="utf-8")
        target.chmod(0o600)
        self.config_path.symlink_to(target)

        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_malformed_json_is_rejected(self) -> None:
        self.config_path.write_text("{not-json", encoding="utf-8")
        self.config_path.chmod(0o600)

        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_unknown_keys_are_rejected(self) -> None:
        self._write_policy(
            {
                "schema_version": 1,
                "project_client_grants": [],
                "unknown_client_projects": [],
                "extra": True,
            }
        )

        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_duplicate_and_malformed_ids_are_rejected(self) -> None:
        invalid_payloads = [
            {
                "schema_version": 1,
                "project_client_grants": [{"project_id": "Alpha", "client_id": "client-a"}],
                "unknown_client_projects": [],
            },
            {
                "schema_version": 1,
                "project_client_grants": [{"project_id": "alpha", "client_id": "client-a"}] * 2,
                "unknown_client_projects": [],
            },
            {
                "schema_version": 1,
                "project_client_grants": [],
                "unknown_client_projects": ["unknown", "unknown"],
            },
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self._write_policy(payload)
                with self.assertRaises(LocalPolicyError):
                    load_local_catalog_scope(self.config_path)

    def test_unknown_project_cannot_also_have_client_pair_grant(self) -> None:
        self._write_policy(
            {
                "schema_version": 1,
                "project_client_grants": [{"project_id": "shared", "client_id": "client-a"}],
                "unknown_client_projects": ["shared"],
            }
        )

        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_project_cannot_be_granted_to_two_clients(self) -> None:
        self._write_policy({
            "schema_version": 1,
            "project_client_grants": [
                {"project_id": "alpha", "client_id": "client_a"},
                {"project_id": "alpha", "client_id": "client_b"},
            ],
            "unknown_client_projects": [],
        })
        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_float_schema_version_is_rejected(self) -> None:
        self._write_policy({
            "schema_version": 1.0,
            "project_client_grants": [],
            "unknown_client_projects": [],
        })
        with self.assertRaises(LocalPolicyError):
            load_local_catalog_scope(self.config_path)

    def test_symlink_swap_before_open_is_rejected(self) -> None:
        payload = {"schema_version": 1, "project_client_grants": [], "unknown_client_projects": []}
        self._write_policy(payload)
        target = self.root / "target.json"
        target.write_text(json.dumps(payload), encoding="utf-8")
        target.chmod(0o600)
        original_open = os.open

        def swap_before_open(path: Path, flags: int) -> int:
            self.config_path.unlink()
            self.config_path.symlink_to(target)
            return original_open(path, flags)

        with patch("negrita_brain.dashboard_local_access.os.open", side_effect=swap_before_open):
            with self.assertRaises(LocalPolicyError):
                load_local_catalog_scope(self.config_path)


if __name__ == "__main__":
    unittest.main()
