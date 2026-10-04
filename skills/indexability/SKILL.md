---
name: indexability
description: "Record an indexability pass for one URL. Use when a page must be fetchable before anyone asks whether it can be cited. The score file still needs every findability key."
models: ""
---

# Indexability

An indexability pass says whether one URL can be fetched and listed. It is not a site grade.

The scorer reads six strings: `channel_decision`, `buyer_question`, `citation_record`, `indexability_pass`, `brief`, and `kill_date`. This skill writes `indexability_pass`. The other five still have to be in the file.

## Inputs

- One URL.
- Whether that URL returns 200, or the status you got instead.
- Whether robots allows it.
- Whether the sitemap lists it.
- The buyer question, the citation record, the brief, the channel decision, and the kill date.

## Decision rules

`indexability_pass` is about one URL. The line must say 200 or status, and it must say robots, and it must say sitemap. "Unchecked" fails. A score for the whole site fails the judgment. Do not turn this into a health-score dump.

`buyer_question` ends with one question mark. `citation_record` has a `YYYY-MM-DD` and the word Method, from an answer you saw. `brief` contains "one page". `channel_decision` contains channel and one. `kill_date` is `YYYY-MM-DD`.

A 40-article calendar and an llms.txt project are refused.

## Procedure

1. Name the one URL.
2. Record status, robots, and sitemap in `indexability_pass`. If you have not checked, stop.
3. Fill the other five keys. The question, the record, and the brief are part of the same pass.
4. From the repo root, run `python3 scripts/score.py --file draft.json`.

## Filled example

Example only. Replace every line. The URL check in the sample is a placeholder, not a measured client result.

```json
{
  "channel_decision": "Search is a channel for this offer. Own one orientation question before any new URL.",
  "buyer_question": "How do I know which buyer question is worth one page?",
  "citation_record": "On 2026-10-01 a pasted answer named a rival and a roundup. This brand was not named. Method: pasted answer.",
  "indexability_pass": "The chosen URL returns 200, is allowed in robots, and is listed in the sitemap.",
  "brief": "One page. First paragraph answers the buyer question with one claim only this brand can say.",
  "kill_date": "2026-12-15"
}
```

## If the script exits 1

`indexability pass is not one URL` means 200 or status, robots, or sitemap is missing. `draft is incomplete` means a key is blank. `a health-score dump` means stop.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Name the one URL.
- [ ] 2. Write `indexability_pass` with status, robots, and sitemap. Then fill `channel_decision`, `buyer_question`, `citation_record`, `brief`, and `kill_date`.
- [ ] 3. From the repo root, run `python3 scripts/score.py --file draft.json`.

Check again until the script exits 0.

Go back to step 2 if step 3 fails.
