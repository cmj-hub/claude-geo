#!/usr/bin/env python3
"""score.py prints the findability artifact or refuses the named bad draft."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "super-secret-cell"
GOOD = json.loads((ROOT / "examples" / "findability-good.json").read_text())


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def score(**changes):
    draft = {**GOOD, **changes}
    return run(["--stdin"], stdin=json.dumps(draft))


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

    def test_weak_draft_names_each_axis(self):
        result = run(["--file", str(ROOT / "examples" / "findability-weak.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("draft is incomplete", result.stdout)
        for label in ("channel decision", "buyer question", "citation record",
                      "indexability pass", "kill date"):
            self.assertIn(label + ":", result.stdout)

    def test_template_is_incomplete(self):
        result = run(["--file", str(ROOT / "examples" / "findability-template.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stdout)

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"brief": "' + CELL)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertNotEqual(array.returncode, 0)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_json_output(self):
        result = run(["--file", str(ROOT / "examples" / "findability-good.json"), "--json"])
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["pass"])
        self.assertEqual(payload["artifact"]["kill_date"], "2026-12-15")
        failing = json.loads(run(["--stdin", "--json"], stdin=json.dumps({**GOOD, "kill_date": "soon"})).stdout)
        self.assertFalse(failing["pass"])
        self.assertEqual(failing["problems"][0]["field"], "kill_date")


class Refusals(unittest.TestCase):
    def test_refusals_in_plan_fields(self):
        cases = {
            "a health-score dump": {"brief": "Publish the site health score for every page we own."},
            "an llms.txt project": {"channel_decision": "Search is a channel, so we start an llms.txt project for the site."},
            "a 40-article calendar": {"brief": "Write 25 posts on answer engines and ship them all this quarter."},
        }
        for named, change in cases.items():
            with self.subTest(named):
                result = score(**change)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout.strip(), named)

    def test_observations_may_name_llms_txt(self):
        result = score(indexability_pass="The URL returns 200, robots allows it, it is in the sitemap. An llms.txt file exists and changes nothing here.")
        self.assertEqual(result.returncode, 0, result.stdout)


class Axes(unittest.TestCase):
    def assertProblem(self, result, label):
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(label + ":", result.stdout)

    def test_placeholders_fail(self):
        self.assertProblem(score(citation_record="None observed."), "citation record")
        self.assertProblem(score(indexability_pass="Unchecked."), "indexability pass")

    def test_buyer_question(self):
        self.assertProblem(score(buyer_question="answer engine optimization agency pricing"), "buyer question")
        self.assertProblem(score(buyer_question="What should we publish next?"), "buyer question")
        self.assertProblem(score(buyer_question="What is GEO? How is it priced?"), "buyer question")
        self.assertProblem(score(buyer_question="GEO?"), "buyer question")
        self.assertProblem(score(buyer_question="geo agency | aeo agency | ai seo tool?"), "buyer question")

    def test_citation_record_needs_date_and_method(self):
        self.assertProblem(score(citation_record="A pasted answer named a rival. Method: pasted answer."), "citation record")
        self.assertProblem(score(citation_record="On 2026-10-01 a pasted answer named a rival."), "citation record")

    def test_indexability(self):
        self.assertProblem(score(indexability_pass="The URL returns 301, robots allows it, it is in the sitemap."), "indexability pass")
        self.assertProblem(score(indexability_pass="The URL returns 200 and is in the sitemap."), "indexability pass")
        self.assertProblem(score(indexability_pass="Returns 200, in the sitemap, but robots has GPTBot disallowed."), "indexability pass")
        ok = score(indexability_pass="Status 200, not blocked in robots for any AI crawler, listed in the sitemap.")
        self.assertEqual(ok.returncode, 0, ok.stdout)

    def test_brief_is_one_page(self):
        self.assertProblem(score(brief="One page."), "brief")
        self.assertProblem(score(brief=" ".join(["word"] * 200)), "brief")

    def test_kill_date_window(self):
        self.assertProblem(score(kill_date="next quarter"), "kill date")
        self.assertProblem(score(kill_date="2026-10-05"), "kill date")
        self.assertProblem(score(kill_date="2027-09-01"), "kill date")
        self.assertProblem(score(kill_date="2026-13-40"), "kill date")


if __name__ == "__main__":
    unittest.main()
