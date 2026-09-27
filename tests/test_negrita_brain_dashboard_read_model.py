"""Unit tests for the bounded CAT-005 authorized project catalog."""

from datetime import datetime, timezone
import json
import unittest

from negrita_brain.dashboard_read_model import (
    CatalogProvenance,
    CatalogReadModelError,
    CatalogReadState,
    CatalogScopeGrant,
    build_project_catalog_read_model,
)
from negrita_brain.dashboard_registry import ClientClassification, ProjectCatalogEntry


def _provenance() -> CatalogProvenance:
    return CatalogProvenance("opaque-snapshot-1", "a" * 64, datetime(2026, 9, 27, tzinfo=timezone.utc))


def _entry(project_id: str, client_id: str | None, classification: ClientClassification) -> ProjectCatalogEntry:
    return ProjectCatalogEntry(project_id, project_id.title(), client_id, classification)


class TestDashboardProjectCatalogReadModel(unittest.TestCase):
    def test_authorized_known_project_is_ready_and_allowlisted(self) -> None:
        entries = (_entry("zeta", "client-z", ClientClassification.KNOWN), _entry("alpha", "client-a", ClientClassification.KNOWN))
        result = build_project_catalog_read_model(
            entries,
            _provenance(),
            CatalogScopeGrant(frozenset({("alpha", "client-a")})),
        )
        self.assertEqual(result.state, CatalogReadState.READY)
        self.assertEqual([item.project_id for item in result.projects], ["alpha"])
        self.assertEqual(set(result.to_dict()["projects"][0]), {"project_id", "name", "client_id", "client_classification"})

    def test_unauthorized_known_project_is_empty_without_names_or_cross_scope_counts(self) -> None:
        result = build_project_catalog_read_model(
            (_entry("secret", "client-s", ClientClassification.KNOWN),), _provenance(), CatalogScopeGrant()
        )
        self.assertEqual(result.state, CatalogReadState.EMPTY)
        self.assertEqual(result.projects, ())
        self.assertNotIn("secret", repr(result.to_dict()))

    def test_unknown_requires_project_grant_and_explicit_unknown_allowance(self) -> None:
        entry = _entry("unknown", None, ClientClassification.UNKNOWN)
        self.assertEqual(
            build_project_catalog_read_model(entry_tuple := (entry,), _provenance(), CatalogScopeGrant(frozenset({("unknown", "client-x")}))).projects,
            (),
        )
        result = build_project_catalog_read_model(
            entry_tuple,
            _provenance(),
            CatalogScopeGrant(frozenset(), frozenset({"unknown"}), frozenset({"unknown"})),
        )
        self.assertEqual(result.state, CatalogReadState.READY)
        self.assertIsNone(result.projects[0].client_id)

    def test_internal_requires_explicit_internal_pair(self) -> None:
        entry = _entry("brain", "internal", ClientClassification.INTERNAL)
        denied = build_project_catalog_read_model((entry,), _provenance(), CatalogScopeGrant())
        allowed = build_project_catalog_read_model((entry,), _provenance(), CatalogScopeGrant(frozenset({("brain", "internal")})))
        self.assertEqual(denied.state, CatalogReadState.EMPTY)
        self.assertEqual(allowed.state, CatalogReadState.READY)

    def test_requested_filters_apply_after_authorization(self) -> None:
        entries = (_entry("alpha", "client-a", ClientClassification.KNOWN), _entry("beta", "client-b", ClientClassification.KNOWN))
        scope = CatalogScopeGrant(frozenset({("alpha", "client-a"), ("beta", "client-b")}))
        self.assertEqual(
            build_project_catalog_read_model(entries, _provenance(), scope, requested_project_id="beta").projects[0].project_id,
            "beta",
        )
        hidden = build_project_catalog_read_model(entries, _provenance(), CatalogScopeGrant(frozenset({("alpha", "client-a")})), requested_project_id="beta")
        self.assertEqual(hidden.state, CatalogReadState.EMPTY)

    def test_invalid_metadata_and_classification_are_rejected(self) -> None:
        invalid = [
            lambda: CatalogProvenance("", "a" * 64, datetime.now(timezone.utc)),
            lambda: CatalogProvenance("snapshot", "bad", datetime.now(timezone.utc)),
            lambda: CatalogProvenance("snapshot", "a" * 64, datetime.now()),
            lambda: build_project_catalog_read_model((_entry("bad", "internal", ClientClassification.KNOWN),), _provenance(), CatalogScopeGrant()),
            lambda: build_project_catalog_read_model((_entry("bad", None, ClientClassification.INTERNAL),), _provenance(), CatalogScopeGrant()),
            lambda: build_project_catalog_read_model((_entry("bad", "client", "known"),), _provenance(), CatalogScopeGrant()),  # type: ignore[arg-type]
        ]
        for operation in invalid:
            with self.subTest(operation=operation):
                with self.assertRaises(CatalogReadModelError):
                    operation()

    def test_duplicate_and_malformed_entries_are_rejected(self) -> None:
        entry = _entry("alpha", "client-a", ClientClassification.KNOWN)
        with self.assertRaises(CatalogReadModelError):
            build_project_catalog_read_model((entry, entry), _provenance(), CatalogScopeGrant(frozenset({("alpha", "client-a")})))
        with self.assertRaises(CatalogReadModelError):
            build_project_catalog_read_model((object(),), _provenance(), CatalogScopeGrant())  # type: ignore[arg-type]

    def test_public_provenance_is_scoped_and_json_serializable(self) -> None:
        visible = _entry("alpha", "client-a", ClientClassification.KNOWN)
        hidden_old = _entry("private", "client-p", ClientClassification.KNOWN)
        hidden_new = ProjectCatalogEntry("private", "Changed private title", "client-p", ClientClassification.KNOWN)
        scope = CatalogScopeGrant(frozenset({("alpha", "client-a")}))
        earlier = build_project_catalog_read_model(
            (visible, hidden_old), CatalogProvenance("source-one", "a" * 64, datetime(2026, 9, 27, tzinfo=timezone.utc)), scope
        ).to_dict()
        later = build_project_catalog_read_model(
            (visible, hidden_new), CatalogProvenance("source-two", "b" * 64, datetime(2026, 9, 27, 1, tzinfo=timezone.utc)), scope
        ).to_dict()
        self.assertEqual(earlier, later)
        self.assertNotIn("Changed private title", json.dumps(later))

    def test_public_dto_serializes_without_source_timestamp(self) -> None:
        result = build_project_catalog_read_model((), _provenance(), CatalogScopeGrant())
        serialized = json.dumps(result.to_dict())
        self.assertNotIn("captured_at", serialized)


if __name__ == "__main__":
    unittest.main()
