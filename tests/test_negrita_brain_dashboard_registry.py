"""Tests for the read-only dashboard registry adapter."""

import tempfile
import unittest
from pathlib import Path

from negrita_brain.dashboard_registry import (
    ClientClassification,
    RegistryAdapterError,
    load_project_catalog,
    parse_project_registry,
    parse_project_registries,
    to_project_ref,
)


class TestDashboardRegistryAdapter(unittest.TestCase):
    def test_parse_project_registry_that_uses_only_explicit_client_metadata(self) -> None:
        registry = {
            "project": {
                "id": "alpha",
                "name": "Alpha Project",
                "metadata": {"client_id": "client-1"},
                "local_paths": {"primary": "/private/secret/path"},
                "secrets": {"token": "do-not-export"},
            }
        }

        entry = parse_project_registry(registry)

        self.assertEqual(entry.project_id, "alpha")
        self.assertEqual(entry.client_id, "client-1")
        self.assertEqual(entry.client_classification, ClientClassification.KNOWN)
        self.assertEqual(
            entry.to_display_dict(),
            {
                "project_id": "alpha",
                "name": "Alpha Project",
                "client_id": "client-1",
                "client_classification": "known",
            },
        )
        self.assertNotIn("secret", entry.to_display_dict())
        self.assertNotIn("path", entry.to_display_dict())

    def test_missing_client_metadata_that_maps_to_explicit_unknown(self) -> None:
        entry = parse_project_registry(
            {"project": {"id": "alpha", "name": "Alpha", "local_paths": {}}}
        )

        self.assertIsNone(entry.client_id)
        self.assertEqual(entry.client_classification, ClientClassification.UNKNOWN)
        self.assertEqual(to_project_ref(entry).client_id.reason, "not_observed")

    def test_internal_client_metadata_that_maps_to_explicit_internal(self) -> None:
        entry = parse_project_registry(
            {
                "project": {
                    "id": "alpha",
                    "name": "Alpha",
                    "metadata": {"client_id": "internal"},
                }
            }
        )

        self.assertEqual(entry.client_classification, ClientClassification.INTERNAL)
        self.assertEqual(to_project_ref(entry).client_id, "internal")

    def test_client_is_not_inferred_from_name_path_or_unrelated_metadata(self) -> None:
        entry = parse_project_registry(
            {
                "project": {
                    "id": "sample_project",
                    "name": "Sample analysis",
                    "local_paths": {"primary": "/examples/private"},
                    "owner": {"client": "Example Organization"},
                }
            }
        )

        self.assertIsNone(entry.client_id)
        self.assertEqual(entry.client_classification, ClientClassification.UNKNOWN)

    def test_legacy_project_client_label_is_not_exposed_or_promoted_to_stable_id(self) -> None:
        entry = parse_project_registry(
            {
                "project": {
                    "id": "sample_project",
                    "name": "Sample analysis",
                    "client": "Example Organization",
                }
            }
        )

        self.assertIsNone(entry.client_id)
        self.assertEqual(entry.client_classification, ClientClassification.UNKNOWN)
        self.assertNotIn("Example Organization", entry.to_display_dict().values())

    def test_legacy_project_registry_is_a_project_without_inferred_client(self) -> None:
        entry = parse_project_registry({
            "project_registry": {
                "project_id": "legacy_project",
                "project_name": "Legacy Project",
                "owner": {"client": "Private Example Organization"},
                "repository": {"location": "/private/example/location"},
            }
        })
        self.assertEqual(entry.project_id, "legacy_project")
        self.assertEqual(entry.name, "Legacy Project")
        self.assertIsNone(entry.client_id)

    def test_ambiguous_project_schemas_are_rejected(self) -> None:
        with self.assertRaises(RegistryAdapterError):
            parse_project_registry({
                "project": {"id": "alpha", "name": "Alpha"},
                "project_registry": {"project_id": "alpha", "project_name": "Alpha"},
            })

    def test_duplicate_project_ids_are_rejected(self) -> None:
        registries = [
            {"project": {"id": "same", "name": "First"}},
            {"project": {"id": "same", "name": "Second"}},
        ]

        with self.assertRaisesRegex(RegistryAdapterError, "Duplicate project id"):
            parse_project_registries(registries)

    def test_malformed_client_reference_is_rejected(self) -> None:
        malformed = [
            {"project": {"id": "alpha", "name": "Alpha", "metadata": {"client_id": {}}}},
            {"project": {"id": "alpha", "name": "Alpha", "metadata": {"client_id": ""}}},
            {"project": {"id": "alpha", "name": "Alpha", "metadata": {"client_id": "unknown"}}},
            {"project": {"id": "alpha", "name": "Alpha", "metadata": {"client_id": "client/other-project"}}},
            {"project": {"id": "alpha", "name": "Alpha", "metadata": {"client_id": "Example Co"}}},
        ]

        for registry in malformed:
            with self.subTest(registry=registry):
                with self.assertRaises(RegistryAdapterError):
                    parse_project_registry(registry)

    def test_cross_project_metadata_reference_is_not_accepted_as_client_reference(self) -> None:
        registry = {
            "project": {
                "id": "alpha",
                "name": "Alpha",
                "metadata": {"client_id": {"project_id": "other"}},
            }
        }

        with self.assertRaises(RegistryAdapterError):
            parse_project_registry(registry)

    def test_yaml_loading_isolated_from_pure_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "alpha.yaml"
            path.write_text(
                "project:\n"
                "  id: alpha\n"
                "  name: Alpha\n"
                "  metadata:\n"
                "    client_id: internal\n",
                encoding="utf-8",
            )

            catalog = load_project_catalog([path])

        self.assertEqual([entry.project_id for entry in catalog], ["alpha"])
        self.assertEqual(catalog[0].client_classification, ClientClassification.INTERNAL)


if __name__ == "__main__":
    unittest.main()
