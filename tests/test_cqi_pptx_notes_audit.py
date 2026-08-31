"""Behavioral tests for CQI PowerPoint speaker-note contracts."""

from __future__ import annotations

import shutil
import subprocess
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
AUDITOR = (
    ROOT
    / ".codex"
    / "skills"
    / "cqi-analytical-pptx"
    / "scripts"
    / "audit_pptx_notes.mjs"
)

VALID_NOTES = """[Talk track]
Question: Which candidate behaves as intended?
Executive answer: Candidate A preserves the target distribution.
How to read: Compare each candidate with the baseline column.
What stands out: Candidate A has the smallest absolute delta.
Interpretation: The candidate limits distortion in this window.
Evidence boundary: The comparison does not certify production behavior.
Operational implication: Advance Candidate A to the next validation gate.
Transition: The next slide tests lifecycle stability.
[/Talk track]
[Evidence]
Source: run-scoped comparison extract
Window: 2026-01-01 to 2026-01-31
Grain: account-day
Population: eligible accounts
Denominator: distinct eligible accounts
Association: exact account key
Deduplication: one row per account-day
Evidence status: OBSERVED
Limitation: one-month retrospective window
Allowed conclusion: Candidate A is stable in the declared window.
[/Evidence]
"""


@unittest.skipUnless(shutil.which("node") and shutil.which("unzip"), "node and unzip required")
class TestCqiPptxNotesAudit(unittest.TestCase):
    """Requires substantive talk-track and evidence fields when requested."""

    def _run_audit(self, notes: str) -> subprocess.CompletedProcess[str]:
        with TemporaryDirectory() as temporary_directory:
            deck = Path(temporary_directory) / "fixture.pptx"
            note_xml = "<root>" + "".join(
                f"<a:t>{escape(line)}</a:t>" for line in notes.splitlines()
            ) + "</root>"
            with zipfile.ZipFile(deck, "w") as archive:
                archive.writestr("ppt/slides/slide1.xml", "<root/>")
                archive.writestr("ppt/notesSlides/notesSlide1.xml", note_xml)
            return subprocess.run(
                ["node", str(AUDITOR), "--deck", str(deck), "--require-talk-track"],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_complete_talk_track_and_evidence_that_pass(self) -> None:
        result = self._run_audit(VALID_NOTES)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("evidence and talk-track blocks", result.stdout)

    def test_missing_talk_track_that_fails(self) -> None:
        evidence_only = VALID_NOTES[VALID_NOTES.index("[Evidence]") :]
        result = self._run_audit(evidence_only)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing [Talk track] block", result.stderr)

    def test_empty_talk_track_field_that_fails(self) -> None:
        result = self._run_audit(
            VALID_NOTES.replace(
                "Interpretation: The candidate limits distortion in this window.",
                "Interpretation:",
            )
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty talk-track field Interpretation:", result.stderr)


if __name__ == "__main__":
    unittest.main()
