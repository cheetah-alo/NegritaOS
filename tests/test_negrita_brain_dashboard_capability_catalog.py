"""Unit tests for the local capability catalog."""

from __future__ import annotations

import json
import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from negrita_brain.dashboard_capability_catalog import (
    LocalCapabilityError,
    LocalCapabilityService,
)


class TestLocalCapabilityService(unittest.TestCase):
    """Verify authorization, extraction, redaction, and deterministic views."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "projects").mkdir()
        (self.root / "skills").mkdir()
        self.access = self.root / "access.json"
        self._write_global_sources()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write_global_sources(self) -> None:
        (self.root / "skills" / "catalog.yaml").write_text(
            "defaults: {profiles: []}\nprofiles: {base: {skills: [skill_a]}}\n"
            "skills: [{id: skill_a}]\n",
            encoding="utf-8",
        )
        (self.root / "integrator.yaml").write_text(
            "negrita_os:\n  global_rules: [rules/global/global_rules.yaml]\n"
            "  agents: {agent_a: {}}\n",
            encoding="utf-8",
        )

    def _write_policy(self, *projects: tuple[str, str]) -> None:
        self.access.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "project_client_grants": [
                        {"project_id": project_id, "client_id": client_id}
                        for project_id, client_id in projects
                    ],
                    "unknown_client_projects": [],
                }
            ),
            encoding="utf-8",
        )
        os.chmod(self.access, 0o600)

    def _service(self) -> LocalCapabilityService:
        return LocalCapabilityService(self.root, self.access)

    def test_canonical_project_returns_registered_and_resolved_items(self) -> None:
        self._write_policy(("alpha", "client_a"))
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n  metadata: {client_id: client_a}\n"
            "  agents: [agent_a]\n  skill_profiles: [base]\n",
            encoding="utf-8",
        )
        result = self._service().read_capabilities()
        self.assertEqual(result["state"], "READY")
        self.assertEqual(
            [(item["kind"], item["id"], item["configuration_state"]) for item in result["items"]],
            [
                ("agent", "agent_a", "REGISTERED"),
                (
                    "rule",
                    "rule-" + hashlib.sha256(
                        b"rules/global/global_rules.yaml"
                    ).hexdigest(),
                    "DECLARED",
                ),
                ("skill", "skill_a", "RESOLVED"),
            ],
        )

    def test_unregistered_agent_is_declared_without_claiming_registration(self) -> None:
        self._write_policy(("alpha", "client_a"))
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n  metadata: {client_id: client_a}\n"
            "  agents: [agent_b]\n  skill_profiles: [base]\n",
            encoding="utf-8",
        )
        items = self._service().read_capabilities(kind="agent")["items"]
        self.assertEqual(items[0]["configuration_state"], "DECLARED")

    def test_legacy_project_redacts_paths_and_declares_duplicate_items_once(self) -> None:
        self.access.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "project_client_grants": [],
                    "unknown_client_projects": ["legacy"],
                }
            ),
            encoding="utf-8",
        )
        os.chmod(self.access, 0o600)
        (self.root / "projects" / "legacy.yaml").write_text(
            "project_registry:\n  project_id: legacy\n  project_name: Legacy\n"
            "  owner: {client: ignored}\n  agents: {primary: [agent_a], secondary: [agent_a]}\n"
            "  skills: {required: [skills/legacy_skill.md]}\n"
            "  rules: {inherit: rules/global/global_rules.yaml, "
            "domains: [rules/domain.yaml], project_specific: [local_rule]}\n",
            encoding="utf-8",
        )
        result = self._service().read_capabilities()
        items = result["items"]
        self.assertEqual(sum(item["kind"] == "agent" for item in items), 1)
        self.assertTrue(all("/" not in item["id"] and "/" not in item["name"] for item in items))
        self.assertEqual(sum(item["kind"] == "rule" for item in items), 3)

    def test_denied_project_is_not_read_or_included(self) -> None:
        self._write_policy(("visible", "client_a"))
        (self.root / "projects" / "visible.yaml").write_text(
            "project:\n  id: visible\n  name: Visible\n"
            "  metadata: {client_id: client_a}\n  agents: [visible_agent]\n",
            encoding="utf-8",
        )
        (self.root / "projects" / "hidden.yaml").write_text(
            "project:\n  id: hidden\n  name: Hidden\n"
            "  metadata: {client_id: client_b}\n  agents: [secret_agent]\n",
            encoding="utf-8",
        )
        result = self._service().read_capabilities()
        self.assertEqual({item["project_id"] for item in result["items"]}, {"visible"})
        self.assertNotIn("secret_agent", {item["id"] for item in result["items"]})

    def test_malformed_source_raises_redacted_typed_error(self) -> None:
        self._write_policy(("alpha", "client_a"))
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n  metadata: {client_id: client_other}\n",
            encoding="utf-8",
        )
        with self.assertRaises(LocalCapabilityError) as raised:
            self._service().read_capabilities()
        self.assertNotIn(str(self.root), str(raised.exception))
        self.assertNotIn("client_other", str(raised.exception))

    def test_malformed_global_yaml_raises_redacted_typed_error(self) -> None:
        self._write_policy(("alpha", "client_a"))
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n"
            "  metadata: {client_id: client_a}\n",
            encoding="utf-8",
        )
        (self.root / "skills" / "catalog.yaml").write_text(
            "profiles: [unterminated", encoding="utf-8"
        )
        with self.assertRaises(LocalCapabilityError) as raised:
            self._service().read_capabilities()
        self.assertNotIn("unterminated", str(raised.exception))

    def test_hidden_source_changes_do_not_change_visible_view_hash(self) -> None:
        self._write_policy(("visible", "client_a"))
        for project_id, client_id, agent in (
            ("visible", "client_a", "agent_a"),
            ("hidden", "client_b", "agent_b"),
        ):
            (self.root / "projects" / f"{project_id}.yaml").write_text(
                f"project:\n  id: {project_id}\n  name: {project_id}\n"
                f"  metadata: {{client_id: {client_id}}}\n  agents: [{agent}]\n",
                encoding="utf-8",
            )
        before = self._service().read_capabilities("visible")
        (self.root / "projects" / "hidden.yaml").write_text(
            "project:\n  id: hidden\n  name: changed\n"
            "  metadata: {client_id: client_b}\n  agents: [changed_secret]\n",
            encoding="utf-8",
        )
        after = self._service().read_capabilities("visible")
        self.assertEqual(before["provenance"], after["provenance"])


if __name__ == "__main__":
    unittest.main()
