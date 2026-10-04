#!/usr/bin/env python3
"""Score a findability draft.

Prints a channel decision, a buyer question, a citation record, an indexability
pass, one brief, and one kill date. Refuses a health-score dump, an llms.txt
project, or a 40-article calendar.

Each of the six axes is checked, not just filled in. A failing draft prints one
line per problem, named by axis, and exits 1.

Stdlib only. No network.

  python3 scripts/score.py --file gtm/findability.json
  python3 scripts/score.py --stdin
  python3 scripts/score.py --file gtm/findability.json --json

Every failing line reads `- <what is wrong> -> <what to change>`, and the last
line names the next step.

Exit codes: 0 passes, 1 refused or failing, 2 bad input.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000

FIELDS = (
    ("channel_decision", "channel decision"),
    ("buyer_question", "buyer question"),
    ("citation_record", "citation record"),
    ("indexability_pass", "indexability pass"),
    ("brief", "brief"),
    ("kill_date", "kill date"),
)
LABELS = dict(FIELDS)

# The /geo:geo mode that writes each field.
MODES = {
    "channel_decision": "channel-decision",
    "buyer_question": "buyer-question",
    "citation_record": "citation-record",
    "indexability_pass": "indexability",
    "brief": "brief",
    "kill_date": "brief",
}

NEXT_PASS = "/landing-page:page"
NEXT_FAIL = "fix the lines above and run this again."
EXAMPLE = "example:\n  python3 scripts/score.py --file examples/findability-good.json"

REFUSAL_FIXES = {
    "a health-score dump": "pick one buyer question and score one page for it",
    "an llms.txt project": "check fetchability with /geo:geo indexability instead",
    "a 40-article calendar": "write one brief; the next one waits for this one's kill date",
}

# Refusals are read from the plan fields only. The citation record and the
# indexability pass are observations, and may name llms.txt or a score they saw.
PLAN_FIELDS = ("channel_decision", "buyer_question", "brief")

HEALTH_RE = re.compile(r"health[-\s]?score", re.IGNORECASE)
LLMS_RE = re.compile(r"llms(?:-full)?\.txt", re.IGNORECASE)
CALENDAR_RE = re.compile(
    r"\b\d{2,}[-\s]?(?:article|post|page|blog|piece)s?\b"
    r"|content[-\s]calendar|editorial[-\s]calendar",
    re.IGNORECASE,
)

PLACEHOLDER_RE = re.compile(
    r"^(?:tbd|tbc|todo|n/?a|none|none observed|unknown|unchecked|pending|-+|\?+|\.+)\.?$",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
METHOD_RE = re.compile(r"\bmethod\s*:\s*\S", re.IGNORECASE)
STATUS_RE = re.compile(r"\b(?:return(?:s|ed|ing)?|status(?: code)?|http)\W*([1-5]\d\d)\b", re.IGNORECASE)
BLOCKED_RE = re.compile(
    r"(?<!not )(?<!n't )(?<!no )\b(?:blocked|disallowed|noindex(?:ed)?|login[-\s]walled|paywalled)\b",
    re.IGNORECASE,
)
LIST_SEPARATORS_RE = re.compile(r"[|;]|,.*,.*,")

QUESTION_MIN_WORDS = 5
QUESTION_MAX_WORDS = 30
DECISION_MIN_WORDS = 8
BRIEF_MIN_WORDS = 8
BRIEF_MAX_WORDS = 150
KILL_MIN_DAYS = 14
KILL_MAX_DAYS = 180


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input("file not found")
        if not path.is_file():
            fail_input("not a file")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input("cannot read file")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("file is not UTF-8 text")


def load_payload(args: argparse.Namespace) -> object:
    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail_input("input is not UTF-8 text")
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def nonempty_text(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def word_count(text: str) -> int:
    return len(text.split())


def parse_date(text: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return None


def refusal_for(values: dict) -> str:
    blob = "\n".join(values[key] for key in PLAN_FIELDS)
    if HEALTH_RE.search(blob):
        return "a health-score dump"
    if LLMS_RE.search(blob):
        return "an llms.txt project"
    if CALENDAR_RE.search(blob):
        return "a 40-article calendar"
    return ""


def check_channel_decision(text: str) -> list:
    if word_count(text) < DECISION_MIN_WORDS:
        return [("too short to be a decision", "say why search is or is not a channel for this offer, and what comes first")]
    return []


def check_buyer_question(text: str) -> list:
    problems = []
    if not text.endswith("?"):
        problems.append(("not written as a question", "write it as a buyer would type it, ending in ?"))
    if text.count("?") > 1:
        problems.append(("more than one question", "keep one question; give the other its own brief"))
    if LIST_SEPARATORS_RE.search(text):
        problems.append(("reads like a keyword list", "write the sentence a buyer would type"))
    words = word_count(text)
    if words < QUESTION_MIN_WORDS:
        problems.append(("too short to be the buyer's own words", "quote the buyer's full question"))
    if words > QUESTION_MAX_WORDS:
        problems.append(("too long for one question", f"cut it to {QUESTION_MAX_WORDS} words or fewer"))
    if re.match(r"^what should we (?:publish|write|post)\b", text, re.IGNORECASE):
        problems.append(("that is our question, not the buyer's", "use a question a buyer asked on a call, a ticket, or a thread"))
    return problems


def check_citation_record(text: str) -> list:
    problems = []
    if not DATE_RE.search(text) or parse_date(DATE_RE.search(text).group(1)) is None:
        problems.append(("no date", "add the date the answer was observed (YYYY-MM-DD)"))
    if not METHOD_RE.search(text):
        problems.append(("no method", "add the method, as 'Method: pasted answer' or another method from the mode"))
    return problems


def check_indexability_pass(text: str) -> list:
    problems = []
    statuses = STATUS_RE.findall(text)
    if not statuses:
        problems.append(("no HTTP status", "record the status, as 'returns 200'"))
    elif any(not code.startswith("2") for code in statuses):
        problems.append(("the URL does not return 200", "fix the URL until it returns 200 in one hop"))
    if not re.search(r"robots", text, re.IGNORECASE):
        problems.append(("robots not recorded", "record whether robots.txt allows the page"))
    if not re.search(r"sitemap", text, re.IGNORECASE):
        problems.append(("sitemap not recorded", "record whether the URL is in the sitemap"))
    if BLOCKED_RE.search(text):
        problems.append(("the page is blocked", "unblock the crawler or drop noindex, then run the pass again"))
    return problems


def check_brief(text: str) -> list:
    words = word_count(text)
    if words < BRIEF_MIN_WORDS:
        return [("too short to be a brief", "name the page and what its first paragraph says")]
    if words > BRIEF_MAX_WORDS:
        return [("more than one page", "cut it to one page; split the rest into later briefs")]
    return []


def check_kill_date(text: str, citation_record: str) -> list:
    kill = parse_date(text)
    if kill is None:
        return [("not a date", "write the kill date as YYYY-MM-DD")]
    match = DATE_RE.search(citation_record)
    observed = parse_date(match.group(1)) if match else None
    if observed is None:
        return []
    days = (kill - observed).days
    if days < KILL_MIN_DAYS:
        return [(f"under {KILL_MIN_DAYS} days after the citation record", "set it 6 to 12 weeks after the page ships")]
    if days > KILL_MAX_DAYS:
        return [(f"over {KILL_MAX_DAYS} days after the citation record", f"set it within {KILL_MAX_DAYS} days of the citation record")]
    return []


def score(values: dict) -> list:
    """Return (key, problem, fix) triples. Empty means the draft passes."""
    problems = []
    for key, _label in FIELDS:
        if not values[key]:
            problems.append((key, "missing", f"run /geo:geo {MODES[key]}"))
        elif PLACEHOLDER_RE.match(values[key]):
            problems.append((key, "a placeholder is not a record", f"run /geo:geo {MODES[key]} and write what you observed"))
    if problems:
        return problems
    checks = (
        ("channel_decision", check_channel_decision(values["channel_decision"])),
        ("buyer_question", check_buyer_question(values["buyer_question"])),
        ("citation_record", check_citation_record(values["citation_record"])),
        ("indexability_pass", check_indexability_pass(values["indexability_pass"])),
        ("brief", check_brief(values["brief"])),
        ("kill_date", check_kill_date(values["kill_date"], values["citation_record"])),
    )
    for key, found in checks:
        problems.extend((key, problem, fix) for problem, fix in found)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a findability draft",
        epilog=EXAMPLE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", help="Path to a JSON object (gtm/findability.json)")
    parser.add_argument("--input", dest="file", help=argparse.SUPPRESS)
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    parser.add_argument("--json", action="store_true", help="Print the result as one JSON object")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    values = {key: nonempty_text(data.get(key)) for key, _label in FIELDS}
    named = refusal_for(values)
    problems = [] if named else score(values)
    passed = not named and not problems

    if args.json:
        result = {"pass": passed, "refused": named or None}
        if named:
            result["fix"] = REFUSAL_FIXES[named]
        result["problems"] = [
            {"field": key, "problem": text, "fix": fix} for key, text, fix in problems
        ]
        if passed:
            result["artifact"] = values
        result["next"] = NEXT_PASS if passed else NEXT_FAIL
        print(json.dumps(result, indent=2))
    elif named:
        print(f"refused: {named}")
        print(f"- {named} → {REFUSAL_FIXES[named]}")
        print(f"Next: {NEXT_FAIL}")
    elif problems:
        print("draft is incomplete")
        for key, text, fix in problems:
            print(f"- {LABELS[key]}: {text} → {fix}")
        print(f"Next: {NEXT_FAIL}")
    else:
        for key, label in FIELDS:
            print(f"{label}: {values[key]}")
        print(f"Next: {NEXT_PASS}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
