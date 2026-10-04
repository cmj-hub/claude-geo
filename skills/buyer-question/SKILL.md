---
name: buyer-question
description: "Choose one buyer question, one brief, and one kill date. Use when the next page has to answer a question a buyer would type. The score file still needs channel_decision, citation_record, and indexability_pass."
models: ""
---

# Buyer question

One question. One brief. One kill date. A calendar of topics is a different job.

The scorer does not read this slice alone. It reads one JSON object with six non-empty strings: `channel_decision`, `buyer_question`, `citation_record`, `indexability_pass`, `brief`, and `kill_date`. This skill writes the question, the brief, and the kill date. You still fill the other three keys, or the script exits 1.

## Inputs

- One question a buyer would type.
- The one claim the page can make.
- The date you will kill the page.
- A channel sentence, a citation record, and an indexability pass, or the pass is not done.

## Decision rules

`buyer_question` is one sentence in the buyer's words. It ends with one question mark. A keyword list fails. "What should we publish?" fails the judgment even if the mark is right. Pick the question the page can answer.

`brief` contains the words "one page". The first paragraph answers that question with one claim only this brand can say. You choose the claim. The scorer checks the words "one page", not the quality of the claim.

`kill_date` is a real date, `YYYY-MM-DD`. The sample date is a placeholder. Replace it.

`channel_decision` must contain the word channel and the word one. If this question is worth one page, search is a channel. Say you will own that one question before any new URL.

`citation_record` needs a `YYYY-MM-DD`, the names you actually saw, and the word Method. Do not guess names.

`indexability_pass` needs 200 or the word status, plus robots, plus sitemap, for one URL. "Unchecked" fails.

A 40-article calendar, a health-score dump, or an llms.txt project is refused.

## Procedure

1. Write the buyer question. Stop if it is a list.
2. Write the brief. Open with "One page."
3. Write the kill date.
4. Write the channel decision for that same question.
5. If you already have a seen answer and a checked URL, write the citation record and the indexability pass. If you do not, stop and do those checks before you score.
6. Save `draft.json`. From the repo root, run `python3 scripts/score.py --file draft.json`.

## Filled example

Example only. Replace every line. Names and dates in the sample are not a client result.

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

`draft is incomplete` means a key is blank. `buyer question is not one question` means the question mark is wrong. `brief is not one page` means the words "one page" are missing. `kill date is not a date` means the date is not `YYYY-MM-DD`. `a 40-article calendar`, `a health-score dump`, and `an llms.txt project` mean stop.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Write `buyer_question` in the buyer's words, one question mark at the end.
- [ ] 2. Write `brief` and `kill_date`, then the other three keys: `channel_decision`, `citation_record`, `indexability_pass`.
- [ ] 3. From the repo root, run `python3 scripts/score.py --file draft.json`.

Review again until the script exits 0.

Go back to step 1 if the question is a keyword list.
