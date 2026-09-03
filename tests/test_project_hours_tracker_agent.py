"""Contract tests for Gisel project-hours tracking."""

import tomllib
import unittest
from pathlib import Path

from scripts.sync_claude_agent_aliases import _load_modes
from scripts.validate_skill_catalog import _load_yaml


ROOT = Path(__file__).resolve().parents[1]


class TestProjectHoursTrackerAgent(unittest.TestCase):
    """Keep Gisel's skill, router, agent, and aliases aligned."""

    def test_catalog_exposes_default_project_hours_profile(self) -> None:
        catalog = _load_yaml(ROOT / "skills/catalog.yaml")

        self.assertIn("project-hours-tracking", catalog["defaults"]["profiles"])
        profile = catalog["profiles"]["project-hours-tracking"]
        self.assertEqual(profile["skills"], ["project-hours-tracking"])
        self.assertIn("project_hours_tracker_agent", profile["required_agents"])

    def test_router_declares_gisel_as_global_agent(self) -> None:
        router = _load_yaml(
            ROOT / "core/orchestration/metaagent_router.yaml"
        )["metaagent_router"]
        mode = router["modes"]["project_hours_tracking"]

        self.assertEqual(mode["id"], "HOURS")
        self.assertEqual(mode["native_alias"], "gisel")
        self.assertIs(mode["global_agent"], True)
        self.assertEqual(mode["agent"], "project_hours_tracker_agent")
        self.assertIn("gisel", [row["alias"] for row in _load_modes(ROOT)])

    def test_canonical_agent_and_codex_alias_preserve_safety_contract(self) -> None:
        integrator = _load_yaml(ROOT / "integrator.yaml")["negrita_os"]
        manifest = _load_yaml(
            ROOT / "strategic-layer/project-hours-tracker/agent.yaml"
        )["agent"]
        codex_agent = tomllib.loads(
            (ROOT / ".codex/agents/gisel.toml").read_text(encoding="utf-8")
        )
        skill = (
            ROOT / ".codex/skills/project-hours-tracking/SKILL.md"
        ).read_text(encoding="utf-8")
        claude_alias = (ROOT / ".codex/agents/gisel.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("project_hours_tracker_agent", integrator["agents"])
        self.assertEqual(manifest["display_name"], "Gisel")
        self.assertEqual(codex_agent["name"], "gisel")
        self.assertIn("Never invent hours", codex_agent["developer_instructions"])
        self.assertIn("identical SHA-256", codex_agent["developer_instructions"])
        self.assertIn("canonical_mode: HOURS", claude_alias)
        self.assertIn("global_agent: true", claude_alias)
        self.assertIn("RETENTION_HOLD", skill)
        self.assertIn("mcp__codex_app__load_workspace_dependencies", skill)
        self.assertIn("BLOCKED_SPREADSHEET_RUNTIME", skill)
        self.assertIn("not a certified timesheet", skill)


if __name__ == "__main__":
    unittest.main()
