"""Unit tests for federated skill catalog behavior."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.materialize_project_skills import materialize, selected_skills
from scripts.sync_skill_catalog import render_profiles, update_agents
from scripts.validate_skill_catalog import validate_project


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


if __name__ == "__main__":
    unittest.main()
