#!/usr/bin/env python3
"""Score a findability draft.

Prints a channel decision, a buyer question, a citation record, an indexability
pass, one brief, and one kill date. Refuses a health-score dump, an llms.txt
project, or a 40-article calendar. A non-empty string still fails when the
channel is not one channel, the question is not one question, the record has
no date and method, the pass skips status or robots or sitemap, the brief is
not one page, or the kill date is not YYYY-MM-DD.

Stdlib only. No network.

  python3 scripts/score.py --file draft.json
  python3 scripts/score.py --stdin
"""

from __future__ import annotations

import argparse
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

HEALTH_RE = re.compile(r"health[-\s]?score", re.IGNORECASE)
LLMS_RE = re.compile(r"llms\.txt", re.IGNORECASE)
CALENDAR_RE = re.compile(r"40[-\s]?article", re.IGNORECASE)


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


def refusal_for(blob: str) -> str:
    if HEALTH_RE.search(blob):
        return "a health-score dump"
    if LLMS_RE.search(blob):
        return "an llms.txt project"
    if CALENDAR_RE.search(blob):
        return "a 40-article calendar"
    return ""



def is_iso_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    year, month, day = (int(part) for part in value.split("-"))
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    if month in (4, 6, 9, 11) and day > 30:
        return False
    if month == 2:
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        if day > (29 if leap else 28):
            return False
    return True


def substance_failure(values: dict) -> str:
    channel = values["channel_decision"]
    if not (re.search(r"\bchannel\b", channel, re.IGNORECASE) and re.search(r"\bone\b", channel, re.IGNORECASE)):
        return "channel decision is not one channel"
    question = values["buyer_question"]
    if question.count("?") != 1 or not question.endswith("?"):
        return "buyer question is not one question"
    record = values["citation_record"]
    if not (re.search(r"\d{4}-\d{2}-\d{2}", record) and re.search(r"\bmethod\b", record, re.IGNORECASE)):
        return "citation record is not a record"
    passed = values["indexability_pass"]
    low = passed.lower()
    if not ("robots" in low and "sitemap" in low and ("200" in passed or "status" in low)):
        return "indexability pass is not one URL"
    if not re.search(r"\bone page\b", values["brief"], re.IGNORECASE):
        return "brief is not one page"
    if not is_iso_date(values["kill_date"]):
        return "kill date is not a date"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a findability draft")
    parser.add_argument("--file", help="Path to a JSON object")
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    args = parser.parse_args()
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    values = {key: nonempty_text(data.get(key)) for key, _label in FIELDS}
    blob = "\n".join(values.values())
    named = refusal_for(blob)
    if named:
        print(named)
        return 1
    if any(not values[key] for key, _label in FIELDS):
        print("draft is incomplete")
        return 1
    substance = substance_failure(values)
    if substance:
        print(substance)
        return 1
    for key, label in FIELDS:
        print(f"{label}: {values[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
