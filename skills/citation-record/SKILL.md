---
name: citation-record
description: "Write one citation record for one buyer question. Use when you need the names an answer actually attached, with a date and a method. The score file still needs every findability key."
models: ""
---

# Citation record

A citation record names who was attached to one answer, on one date, by one method. A guessed list is not a record.

The scorer reads six strings: `channel_decision`, `buyer_question`, `citation_record`, `indexability_pass`, `brief`, and `kill_date`. This skill writes `citation_record`. The other five still have to be in the file.

## Inputs

- The one buyer question.
- One answer you saw. Not a list you wish were true.
- The date of that answer.
- How you saw it, in plain words.

## Decision rules

`citation_record` includes a date written `YYYY-MM-DD`, the names that answer attached, and the word Method. The sample method is a pasted answer. Replace it with how you saw the answer. Do not invent a name. "None observed" fails. A guessed list fails the judgment even when the date is real.

Write "This brand was not named" only when that is what you saw.

`buyer_question` ends with one question mark. `channel_decision` contains channel and one. `indexability_pass` records 200 or status, robots, and sitemap for one URL. `brief` contains "one page". `kill_date` is `YYYY-MM-DD`.

The scorer also refuses a health-score dump, an llms.txt project, and a 40-article calendar.

## Procedure

1. Lock the buyer question.
2. Write the observed names, the date, and the method into `citation_record`. If you did not see an answer, stop.
3. Fill the other five keys from checks you have already done. Do not leave them blank to "finish later."
4. From the repo root, run `python3 scripts/score.py --file draft.json`.

## Filled example

Example only. Replace every line. The rival, the roundup, and the date are not a client result.

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

`citation record is not a record` means the date or the word Method is missing. `draft is incomplete` means a key is blank. The named refusals for a calendar, a health-score dump, and an llms.txt project mean this is the wrong job.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Lock `buyer_question`.
- [ ] 2. Write `citation_record` with the date, the names you saw, and Method. Then fill `channel_decision`, `indexability_pass`, `brief`, and `kill_date`.
- [ ] 3. From the repo root, run `python3 scripts/score.py --file draft.json`.

Check again until the script exits 0.

Return to step 2 if step 3 fails.
