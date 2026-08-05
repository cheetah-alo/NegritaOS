"""Unit tests for profile inheritance and default closure."""

import unittest

from src.negrita_brain.errors import ProfileResolutionError
from src.negrita_brain.profiles import resolve_profiles


class TestProfileResolution(unittest.TestCase):
    """Locks parent-first, de-duplicated, cycle-safe profile resolution."""

    def test_profile_inheritance_that_orders_parent_before_child(self) -> None:
        catalog = {
            "profiles": {
                "base": {"skills": ["one", "shared"]},
                "child": {"extends": "base", "skills": ["shared", "two"]},
            }
        }
        closure = resolve_profiles(catalog, ["child"])
        self.assertEqual(closure.profiles, ("base", "child"))
        self.assertEqual(closure.skills, ("one", "shared", "two"))

    def test_default_profile_that_precedes_requested_profiles(self) -> None:
        catalog = {
            "defaults": {"profiles": ["documents"]},
            "profiles": {
                "documents": {"skills": ["control"]},
                "deck": {"skills": ["story"]},
            },
        }
        closure = resolve_profiles(catalog, ["deck"])
        self.assertEqual(closure.profiles, ("documents", "deck"))
        self.assertEqual(closure.skills, ("control", "story"))

    def test_profile_cycle_that_reports_full_chain(self) -> None:
        catalog = {
            "profiles": {
                "one": {"extends": "two"},
                "two": {"extends": "one"},
            }
        }
        with self.assertRaisesRegex(ProfileResolutionError, "one -> two -> one"):
            resolve_profiles(catalog, ["one"])

    def test_unknown_parent_that_fails_closed(self) -> None:
        with self.assertRaisesRegex(ProfileResolutionError, "Unknown profile: missing"):
            resolve_profiles(
                {"profiles": {"child": {"extends": "missing"}}}, ["child"]
            )


if __name__ == "__main__":
    unittest.main()
