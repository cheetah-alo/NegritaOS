"""Focused tests for the local-only CAT-005B catalog service."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from negrita_brain import config
from negrita_brain.dashboard_local_service import LocalCatalogError, LocalCatalogService
from negrita_brain.dashboard_read_model import CatalogReadState


class TestLocalCatalogService(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.projects = self.root / "projects"
        self.projects.mkdir()
        self.access = self.root / "access.json"
        self.now = datetime(2026, 9, 27, 14, 30, tzinfo=timezone.utc)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write_policy(
        self,
        grants: list[tuple[str, str]] | None = None,
        unknown: list[str] | None = None,
    ) -> None:
        self.access.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "project_client_grants": [
                        {"project_id": project_id, "client_id": client_id}
                        for project_id, client_id in (grants or [])
                    ],
                    "unknown_client_projects": unknown or [],
                }
            ),
            encoding="utf-8",
        )
        os.chmod(self.access, 0o600)

    def _write_project(self, project_id: str, name: str, client_id: str | None = None) -> Path:
        path = self.projects / f"{project_id}.yaml"
        path.write_text(
            "project:\n"
            f"  id: {project_id}\n"
            f"  name: {name}\n"
            "  metadata:\n"
            f"    client_id: {client_id}\n" if client_id is not None else
            "project:\n"
            f"  id: {project_id}\n"
            f"  name: {name}\n",
            encoding="utf-8",
        )
        return path

    def _service(self) -> LocalCatalogService:
        return LocalCatalogService(self.root, self.access, now=lambda: self.now)

    def test_empty_policy_returns_empty_without_reading_registry_yaml(self) -> None:
        self._write_policy()
        with patch("negrita_brain.dashboard_local_service.config.load_yaml") as load_yaml:
            result = self._service().read_catalog()
        load_yaml.assert_not_called()
        self.assertEqual(result.state, CatalogReadState.EMPTY)
        self.assertEqual(result.projects, ())

    def test_only_allowlisted_project_files_are_read(self) -> None:
        self._write_policy([("alpha", "client_a")])
        self._write_project("alpha", "Alpha", "client_a")
        self._write_project("extra", "Extra", "client_extra")
        with patch("negrita_brain.dashboard_local_service.config.load_yaml", wraps=config.load_yaml) as load_yaml:
            result = self._service().read_catalog()
        self.assertEqual([project.project_id for project in result.projects], ["alpha"])
        self.assertEqual([call.args[0].name for call in load_yaml.call_args_list], ["alpha.yaml"])

    def test_unknown_policy_entry_is_explicitly_supported(self) -> None:
        self._write_policy(unknown=["mystery"])
        self._write_project("mystery", "Mystery")
        result = self._service().read_catalog()
        self.assertEqual(result.state, CatalogReadState.READY)
        self.assertIsNone(result.projects[0].client_id)

    def test_legacy_project_registry_is_read_with_unknown_client(self) -> None:
        self._write_policy(unknown=["legacy_project"])
        (self.projects / "legacy_project.yaml").write_text(
            "project_registry:\n"
            "  project_id: legacy_project\n"
            "  project_name: Legacy Project\n"
            "  owner:\n"
            "    client: Private Example Organization\n",
            encoding="utf-8",
        )
        result = self._service().read_catalog()
        self.assertEqual(result.projects[0].project_id, "legacy_project")
        self.assertIsNone(result.projects[0].client_id)

    def test_missing_source_is_typed_and_does_not_expose_path_or_client(self) -> None:
        self._write_policy([("alpha", "secret_client")])
        with self.assertRaises(LocalCatalogError) as raised:
            self._service().read_catalog()
        self.assertNotIn(str(self.root), str(raised.exception))
        self.assertNotIn("secret_client", str(raised.exception))

    def test_mismatched_registry_policy_is_an_error(self) -> None:
        self._write_policy([("alpha", "client_a")])
        self._write_project("alpha", "Alpha", "client_other")
        with self.assertRaises(LocalCatalogError):
            self._service().read_catalog()

    def test_symlinked_file_and_projects_directory_are_rejected(self) -> None:
        self._write_policy([("alpha", "client_a")])
        outside = self.root / "outside.yaml"
        outside.write_text("project:\n  id: alpha\n  name: Alpha\n  metadata:\n    client_id: client_a\n", encoding="utf-8")
        try:
            (self.projects / "alpha.yaml").symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable")
        with self.assertRaises(LocalCatalogError):
            self._service().read_catalog()

        (self.projects / "alpha.yaml").unlink()
        self.projects.rmdir()
        self.projects.symlink_to(self.root)
        with self.assertRaises(LocalCatalogError):
            self._service().read_catalog()

    def test_filters_are_applied_to_the_scoped_public_model(self) -> None:
        self._write_policy([("alpha", "client_a"), ("beta", "client_b")])
        self._write_project("alpha", "Alpha", "client_a")
        self._write_project("beta", "Beta", "client_b")
        result = self._service().read_catalog(
            requested_project_id="beta", requested_client_id="client_b"
        )
        self.assertEqual([project.project_id for project in result.projects], ["beta"])


if __name__ == "__main__":
    unittest.main()
