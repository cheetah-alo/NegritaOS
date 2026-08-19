"""Unit tests for deliverable classification, routing, and legacy cataloging."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.negrita_brain.config import load_project
from src.negrita_brain.documents import (
    _safe_digest,
    audit_documents,
    catalog_legacy,
    is_compliant_deliverable,
    is_deliverable,
)


ROOT = Path(__file__).resolve().parents[1]


class TestDocumentControl(unittest.TestCase):
    """Separates source documentation from governed deliverables."""

    def test_source_documentation_that_is_excluded_from_deliverables(self) -> None:
        root = Path("/workspace")
        self.assertFalse(is_deliverable(root / "README.md", root))
        self.assertFalse(is_deliverable(root / "docs" / "architecture.md", root))
        self.assertFalse(is_deliverable(root / "src" / "template.html", root))
        self.assertFalse(
            is_deliverable(root / ".venv-pr-quality" / "lib" / "report.html", root)
        )

    def test_timestamped_document_that_is_compliant(self) -> None:
        root = Path("/workspace")
        compliant = root / "documents" / "report__updated_20260805_120000.pdf"
        self.assertTrue(is_deliverable(compliant, root))
        self.assertTrue(is_compliant_deliverable(compliant, root))
        external = Path("/external/report__updated_20260805_120000.pdf")
        self.assertTrue(is_compliant_deliverable(external, root, user_selected_route=True))
        selected_repo_path = Path("/workspace/reports/report__updated_20260805_120000.pdf")
        self.assertTrue(
            is_compliant_deliverable(
                selected_repo_path, root, user_selected_route=True
            )
        )

    def test_configured_canonical_directory_that_is_enforced(self) -> None:
        root = Path("/workspace")
        canonical = root / "team-lead-qaqc" / "documents"
        compliant = canonical / "report__updated_20260805_120000.pdf"
        outside = root / "documents" / "report__updated_20260805_120000.pdf"
        self.assertTrue(
            is_compliant_deliverable(
                compliant,
                root,
                canonical_directory="team-lead-qaqc/documents",
            )
        )
        self.assertFalse(
            is_compliant_deliverable(
                outside,
                root,
                canonical_directory="team-lead-qaqc/documents",
            )
        )

    def test_cloud_artifact_that_is_not_downloaded_for_hash(self) -> None:
        cloud_root = Path("/Users/example/Library/CloudStorage/OneDrive-Personal/project")
        self.assertIsNone(_safe_digest(cloud_root / "missing.pdf", cloud_root))

    def test_catalog_that_appends_once_per_unchanged_artifact(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            repo = base / "repo"
            memory = base / "memory"
            (repo / ".codex").mkdir(parents=True)
            (repo / "analysis").mkdir()
            (repo / ".codex" / "project.yaml").write_text(
                "project_id: negritaos\n"
                f"negrita_registry: {ROOT / 'projects' / 'negritaos.yaml'}\n",
                encoding="utf-8",
            )
            (repo / "analysis" / "report.pdf").write_bytes(b"evidence")
            context = load_project(repo, ROOT)
            first = catalog_legacy(context, memory)
            second = catalog_legacy(context, memory)
            ledger = Path(first["ledger"])
            record = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(first["added"], 1)
            self.assertEqual(second["skipped"], 1)
            self.assertEqual(len(record["sha256"]), 64)

    def test_audit_that_ignores_source_tree(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "brands").mkdir()
            (root / "brands" / "guide.html").write_text("source", encoding="utf-8")
            (root / "report.pdf").write_bytes(b"report")
            audit = audit_documents(root)
            self.assertEqual(audit["deliverables"], ["report.pdf"])
            self.assertEqual(audit["outside_documents"], ["report.pdf"])

    def test_nested_documents_directory_that_is_outside_canonical_route(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested = root / "analysis" / "documents"
            nested.mkdir(parents=True)
            artifact = nested / "report__updated_20260805_120000.pdf"
            artifact.write_bytes(b"report")

            audit = audit_documents(root)

            self.assertEqual(
                audit["outside_documents"],
                ["analysis/documents/report__updated_20260805_120000.pdf"],
            )


if __name__ == "__main__":
    unittest.main()
