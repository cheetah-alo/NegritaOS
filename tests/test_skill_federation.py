"""Unit tests for federated skill catalog behavior."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.materialize_project_skills import materialize, selected_skills
from scripts.sync_skill_catalog import render_profiles, update_agents
from scripts.validate_config_resolution import validate_resolution
from scripts.validate_skill_catalog import CATALOG, _load_yaml, validate_catalog, validate_project
from scripts.validate_source_quality_contract import (
    measure_ingestion_latency_seconds,
    validate_source_contract,
    validate_source_quality_evidence,
)


class TestSkillProfileSelection(unittest.TestCase):
    """Verifies deterministic profile expansion for project adapters."""

    def test_skill_profiles_that_deduplicate_skills_when_profiles_overlap(self) -> None:
        catalog = {
            "profiles": {
                "first": {"skills": ["one", "shared"]},
                "second": {"skills": ["shared", "two"]},
            }
        }
        selected = selected_skills(catalog, {"skill_profiles": ["first", "second"]})
        self.assertEqual(selected, ["one", "shared", "two"])

    def test_skill_profiles_that_return_empty_selection_when_none_declared(self) -> None:
        catalog = {"profiles": {"first": {"skills": ["one"]}}}
        selected = selected_skills(catalog, {})
        self.assertEqual(selected, [])

    def test_dry_run_does_not_create_missing_skill_directory(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            adapter = repo / ".codex"
            adapter.mkdir()
            (adapter / "project.yaml").write_text(
                "negrita_registry: registry.yaml\n", encoding="utf-8"
            )
            (repo / "registry.yaml").write_text(
                "project:\n  skill_profiles:\n    - analytical-dashboard\n",
                encoding="utf-8",
            )
            self.assertEqual(materialize(repo, dry_run=True), 0)
            self.assertFalse((adapter / "skills").exists())

    def test_materialize_preserves_canonical_skill_id_when_source_is_a_symlink(self) -> None:
        """Compatibility symlinks must not rename the adapter entrypoint."""
        with TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            adapter = repo / ".codex"
            adapter.mkdir()
            (adapter / "project.yaml").write_text(
                "negrita_registry: registry.yaml\n", encoding="utf-8"
            )
            (repo / "registry.yaml").write_text(
                "project:\n  skill_profiles:\n    - document-delivery\n",
                encoding="utf-8",
            )

            self.assertEqual(materialize(repo, dry_run=False), 0)
            self.assertTrue((adapter / "skills" / "local-memory-protocol" / "SKILL.md").is_file())
            self.assertFalse((adapter / "skills" / "memory-protocol").exists())

    def test_postgresql_profile_accepts_its_declared_dialect(self) -> None:
        catalog = {
            "profiles": {
                "data-source-postgresql": {
                    "data_source": {
                        "provider": "postgresql",
                        "dialects": ["postgresql"],
                    }
                }
            }
        }
        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory) / "project.yaml"
            project_path.write_text(
                "project:\n"
                "  skill_profiles: [data-source-postgresql]\n"
                "  integration_branch: main\n"
                "  data_source:\n"
                "    provider: postgresql\n"
                "    dialect: postgresql\n"
                "    source_of_truth: governed_remote_source\n"
                "    access: read_only\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_project(catalog, project_path), [])


class TestSkillCatalogSynchronization(unittest.TestCase):
    """Verifies generated profile documentation preserves surrounding content."""

    def test_profile_rendering_that_sorts_profiles_when_catalog_order_changes(self) -> None:
        catalog = {
            "profiles": {
                "z-profile": {"skills": ["z-skill"]},
                "a-profile": {"skills": ["a-skill"]},
            }
        }
        rendered = render_profiles(catalog)
        self.assertLess(rendered.index("a-profile"), rendered.index("z-profile"))

    def test_agents_update_that_replaces_generated_section_when_present(self) -> None:
        current = "before\n\n## Federated Skill Profiles\nold\n\n## Auto-invoke Skills\nafter"
        updated = update_agents(current, "## Federated Skill Profiles\nnew\n\n")
        self.assertIn("before", updated)
        self.assertIn("new", updated)
        self.assertIn("## Auto-invoke Skills", updated)

    def test_catalog_requires_direct_canonical_activation_paths(self) -> None:
        """Canonical skills must be discoverable from one direct entrypoint root."""
        self.assertEqual(validate_catalog(_load_yaml(CATALOG)), [])


class TestConfigurationResolution(unittest.TestCase):
    """Prevents active project configuration from bypassing the canonical chain."""

    def test_active_project_resolves_agents_skills_rules_and_wrappers(self) -> None:
        errors, _, project_id = validate_resolution()
        self.assertEqual(project_id, "negritaos")
        self.assertEqual(errors, [])


class TestBigQuerySourceQualityContract(unittest.TestCase):
    """Locks grain, timestamp, latency, freshness, and evidence semantics."""

    def _contract(self, capture_time: object = "logical_source_capture_time") -> dict:
        return {
            "grain": {
                "entity": "event",
                "key_columns": ["logical_event_id"],
                "expected_cardinality": "one_row_per_event",
                "join_expectations": [
                    {"left": "events", "right": "calls", "relationship": "many_to_one"}
                ],
            },
            "timestamps": {
                "event_time": "logical_event_time",
                "source_capture_time": capture_time,
                "bq_loaded_at": "logical_bq_loaded_at",
                "timezone": "UTC",
                "latency_definition": "bq_loaded_at_minus_source_capture_time",
                "freshness_definition": "now_minus_latest_bq_loaded_at",
            },
            "latency_sla": {"p95_minutes": 60},
            "status": {
                "missing_capture_time": "NOT_APPLICABLE",
                "missing_load_time": "CONTRACT_INCOMPLETE",
                "invalid_latency": "CONTRACT_INCOMPLETE",
            },
        }

    def test_contract_requires_distinct_capture_and_load_semantics(self) -> None:
        errors, warnings = validate_source_contract(self._contract())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_capture_time_is_explicitly_not_applicable(self) -> None:
        errors, warnings = validate_source_contract(self._contract(capture_time=None))
        self.assertEqual(errors, [])
        self.assertIn("NOT_APPLICABLE", warnings[0])

    def test_latency_does_not_fallback_to_event_time(self) -> None:
        status, latency = measure_ingestion_latency_seconds(None, "2026-07-29T10:02:00+00:00")
        self.assertEqual(status, "NOT_APPLICABLE")
        self.assertIsNone(latency)

    def test_negative_latency_is_incomplete(self) -> None:
        status, latency = measure_ingestion_latency_seconds(
            "2026-07-29T10:03:00+00:00", "2026-07-29T10:02:00+00:00"
        )
        self.assertEqual(status, "CONTRACT_INCOMPLETE")
        self.assertEqual(latency, -60)

    def test_evidence_requires_grain_latency_freshness_and_query_hashes(self) -> None:
        errors, warnings = validate_source_quality_evidence(
            {
                "grain": {
                    "row_count": 100,
                    "distinct_key_count": 100,
                    "duplicate_rate": 0,
                    "join_cardinality": "many_to_one",
                },
                "latency": {
                    "status": "PASS",
                    "p50_seconds": 30,
                    "p95_seconds": 90,
                    "max_seconds": 120,
                },
                "freshness": {
                    "status": "PASS",
                    "latest_loaded_at": "2026-07-29T10:02:00+00:00",
                    "age_seconds": 60,
                },
                "queries": {"sql_hashes": ["sha256:example"]},
            }
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_canonical_bigquery_analysis_projects_declare_profile_and_source(self) -> None:
        catalog = _load_yaml(CATALOG)
        for project_name in (
            "proj_data_analytics.yaml",
            "ibc_fiber_network.yaml",
            "hot_onedrive_workspace.yaml",
            "elal_journey_dashboard.yaml",
        ):
            project_path = Path("projects") / project_name
            self.assertEqual(validate_project(catalog, project_path), [])


if __name__ == "__main__":
    unittest.main()
