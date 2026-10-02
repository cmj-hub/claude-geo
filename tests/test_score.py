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


if __name__ == "__main__":
    unittest.main()
