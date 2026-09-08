"""Ensure inaccessible adapters do not prevent distribution to usable targets."""

import argparse
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import sync_claude_agent_aliases as claude_sync
from scripts import sync_codex_custom_agents as codex_sync
from scripts.negrita_brain_hook import _prompt_routing


class TestAstraDistribution(unittest.TestCase):
    """Test partial rollout behavior and user-home delivery under OS denials."""

    def test_explicit_astra_alias_takes_precedence_over_domain_words(self):
        for prompt in ("@agent:Astra review this PR", "--agent astra inspect architecture", "Astral: revisa este PDF"):
            actions, _, _ = _prompt_routing({"prompt": prompt})
            self.assertEqual(actions, ["astra_review"])

    def test_mentioning_astra_in_documentation_is_not_an_invocation(self):
        actions, _, _ = _prompt_routing({"prompt": "Write documentation comparing Astra prices"})
        self.assertNotEqual(actions, ["astra_review"])

    def test_codex_continues_after_denial_and_still_updates_user_home(self):
        args = argparse.Namespace(repo=[Path('/tmp/denied'), Path('/tmp/usable')],
                                  all_projects=False, user_home=True, codex_home=None, write=True)
        with patch.object(codex_sync, '_parse_args', return_value=args), \
                patch.object(codex_sync, 'sync_repo', side_effect=[PermissionError('denied'), None]) as sync, \
                patch.object(codex_sync, 'sync_user_home', return_value=['astra-reviewer']) as home:
            self.assertEqual(codex_sync.main(), 1)
            self.assertEqual(sync.call_count, 2)
            home.assert_called_once()

    def test_claude_continues_after_denial(self):
        args = argparse.Namespace(repo=[Path('/tmp/denied'), Path('/tmp/usable')],
                                  all_projects=False, canonical_only=False, write=True)
        with patch.object(claude_sync, '_parse_args', return_value=args), \
                patch.object(claude_sync, 'sync_canonical', return_value=[]), \
                patch.object(claude_sync, 'sync_repo', side_effect=[PermissionError('denied'), None]) as sync:
            self.assertEqual(claude_sync.main(), 1)
            self.assertEqual(sync.call_count, 2)


if __name__ == '__main__':
    unittest.main()
