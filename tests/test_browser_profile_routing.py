"""Tests for deterministic project-aware Brave profile routing."""

import unittest
from pathlib import Path

from scripts.validate_browser_profile_routing import validate_all
from src.negrita_brain.browser_routing import (
    BrowserRoutingError,
    build_brave_command,
    load_browser_routing_config,
    resolve_browser_route,
)
from src.negrita_brain.config import load_yaml


ROOT = Path(__file__).resolve().parents[1]


class TestBrowserProfileRouting(unittest.TestCase):
    """Verifies profile isolation across project, purpose, and URL signals."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_browser_routing_config(ROOT)
        cls.cqi_project = load_yaml(ROOT / "projects/proj_data_analytics.yaml")[
            "project"
        ]
        cls.personal_project = load_yaml(ROOT / "projects/negritaos.yaml")["project"]

    def test_registered_projects_that_all_declare_governed_browser_context(self) -> None:
        errors, checked = validate_all(ROOT)

        self.assertEqual(errors, [])
        self.assertGreaterEqual(checked, 20)

    def test_bigquery_that_routes_to_tech_work_from_personal_project(self) -> None:
        route = resolve_browser_route(
            self.personal_project,
            self.config,
            url="https://console.cloud.google.com/bigquery?project=private",
        )

        self.assertEqual(route.profile, "cqi_technical")
        self.assertEqual(route.display_name, "Tech Work")
        self.assertEqual(route.profile_directory, "Profile 2")
        self.assertEqual(route.target_host, "console.cloud.google.com")
        self.assertNotIn("private", str(route.as_dict()))

    def test_jira_that_routes_cqi_project_to_documentation_profile(self) -> None:
        route = resolve_browser_route(
            self.cqi_project,
            self.config,
            url="https://cqisense.atlassian.net/browse/DATA-1",
        )

        self.assertEqual(route.profile, "cqi_documentation")
        self.assertEqual(route.display_name, "CQI Sense")
        self.assertEqual(route.resolution_source, "purpose:jira")

    def test_personal_documentation_that_stays_in_tokio_tools(self) -> None:
        route = resolve_browser_route(
            self.personal_project,
            self.config,
            purpose="documentation",
            url="https://www.notion.so/example",
        )

        self.assertEqual(route.profile, "personal_cheetah_alo")
        self.assertEqual(route.display_name, "Tokio tools")
        self.assertEqual(route.profile_directory, "Default")

    def test_github_organization_that_overrides_current_project_scope(self) -> None:
        cqisense = resolve_browser_route(
            self.personal_project,
            self.config,
            url="https://github.com/cqisense/proj_data_analytics",
        )
        cheetah = resolve_browser_route(
            self.cqi_project,
            self.config,
            url="https://github.com/cheetah-alo/NegritaOS",
        )

        self.assertEqual(cqisense.profile, "cqi_technical")
        self.assertEqual(cheetah.profile, "personal_cheetah_alo")

    def test_conflicting_purpose_that_blocks_instead_of_falling_back(self) -> None:
        with self.assertRaises(BrowserRoutingError):
            resolve_browser_route(
                self.cqi_project,
                self.config,
                purpose="jira",
                url="https://github.com/cqisense/proj_data_analytics",
            )

    def test_unsafe_url_that_blocks_userinfo_and_external_http(self) -> None:
        for url in (
            "https://user:secret@example.com/path",  # pragma: allowlist secret - rejection fixture
            "http://example.com/path",
            "javascript:alert(1)",
        ):
            with self.subTest(url=url), self.assertRaises(BrowserRoutingError):
                resolve_browser_route(self.cqi_project, self.config, url=url)

    def test_local_http_that_is_allowed_for_project_default(self) -> None:
        route = resolve_browser_route(
            self.personal_project,
            self.config,
            url="http://127.0.0.1:3000/dashboard",
        )

        self.assertEqual(route.profile, "personal_cheetah_alo")
        self.assertEqual(route.resolution_source, "project_default")

    def test_azure_that_requires_explicit_profile_selection(self) -> None:
        route = resolve_browser_route(
            self.personal_project,
            self.config,
            explicit_profile="azure",
            url="https://portal.azure.com/",
        )

        self.assertEqual(route.profile, "azure")
        self.assertEqual(route.profile_directory, "Profile 3")

    def test_launch_command_that_uses_profile_directory_without_shell(self) -> None:
        route = resolve_browser_route(
            self.cqi_project,
            self.config,
            purpose="bigquery",
        )
        command = build_brave_command(
            route,
            self.config,
            "https://console.cloud.google.com/bigquery",
        )

        self.assertEqual(command[1], "--profile-directory=Profile 2")
        self.assertIn("--new-window", command)
        self.assertEqual(command[-1], "https://console.cloud.google.com/bigquery")


if __name__ == "__main__":
    unittest.main()
