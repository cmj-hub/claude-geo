#!/usr/bin/env python3
"""score.py prints the findability artifact or refuses the named bad draft."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "super-secret-cell"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScoreFindability(unittest.TestCase):
    def test_good_draft_prints_artifact(self):
        result = run(["--file", str(ROOT / "examples" / "findability-good.json")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("channel decision:", result.stdout)
        self.assertIn("buyer question:", result.stdout)
        self.assertIn("citation record:", result.stdout)
        self.assertIn("indexability pass:", result.stdout)
        self.assertIn("brief:", result.stdout)
        self.assertIn("kill date:", result.stdout)

    def test_calendar_exits_1(self):
        result = run(["--file", str(ROOT / "examples" / "findability-calendar.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a 40-article calendar", result.stdout)
        self.assertNotIn("channel decision:", result.stdout)

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"brief": "' + CELL)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertNotEqual(array.returncode, 0)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_blank_field_is_incomplete(self):
        payload = {
            "channel_decision": "Search is a channel for this offer. Own one question before any new URL.",
            "buyer_question": "Which one question is worth one page?",
            "citation_record": "On 2026-10-01 a pasted answer named a rival. Method: pasted answer.",
            "indexability_pass": "The URL returns 200, is allowed in robots, and is listed in the sitemap.",
            "brief": "   ",
            "kill_date": "2026-12-15",
        }
        import json
        result = run(["--stdin"], stdin=json.dumps(payload))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip(), "draft is incomplete")

    def test_substance_kill_date_and_record(self):
        import json
        base = {
            "channel_decision": "Search is a channel for this offer. Own one question before any new URL.",
            "buyer_question": "Which one question is worth one page?",
            "citation_record": "On 2026-10-01 a pasted answer named a rival. Method: pasted answer.",
            "indexability_pass": "The URL returns 200, is allowed in robots, and is listed in the sitemap.",
            "brief": "One page. First paragraph answers the question.",
            "kill_date": "soon",
        }
        bad_date = run(["--stdin"], stdin=json.dumps(base))
        self.assertEqual(bad_date.returncode, 1)
        self.assertEqual(bad_date.stdout.strip(), "kill date is not a date")
        self.assertNotIn("channel decision:", bad_date.stdout)
        base["kill_date"] = "2026-12-15"
        base["citation_record"] = "A rival was named."
        bad_record = run(["--stdin"], stdin=json.dumps(base))
        self.assertEqual(bad_record.returncode, 1)
        self.assertEqual(bad_record.stdout.strip(), "citation record is not a record")
        base["citation_record"] = "On 2026-10-01 a pasted answer named a rival. Method: pasted answer."
        base["buyer_question"] = "a keyword list"
        bad_question = run(["--stdin"], stdin=json.dumps(base))
        self.assertEqual(bad_question.returncode, 1)
        self.assertEqual(bad_question.stdout.strip(), "buyer question is not one question")


if __name__ == "__main__":
    unittest.main()
