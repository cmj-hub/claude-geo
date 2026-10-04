---
name: geo
description: "Score generative engine optimization findability for one buyer question. Use when a page must be quotable by an answer engine, and when a content calendar or health-score dump must be refused."
models: ""
---

# Generative engine optimization

Generative engine optimization is how a page gets quoted by an answer engine.

Answer engine optimization is the same check.

This pack scores findability for one question. It refuses a 40-article calendar and a health-score dump. It does not start an llms.txt project.

The build guide teaches a human. This pack teaches an agent.

You walk out with one findability pass: six strings in one JSON object. A stranger can write that object from this file alone.

This pack does not add a paid product. The public next steps already on the site are Friday Signal and the Growth Audit.

## Inputs

Bring these. Do not borrow them from a file that is not in this repo.

- The offer the page is for.
- One question a buyer would type, in the buyer's words.
- One answer you actually saw: the date, the names that answer attached, and how you saw it.
- One URL you checked: whether it returns 200, whether robots allows it, and whether the sitemap lists it.
- The date you will kill the page if it is still not the one quoted.

If you do not have the answer or the URL check, stop. Do not guess a name. Do not invent a count.

## The six keys

The scorer reads one JSON object. Every value is a string. Empty fails.

1. `channel_decision` — search is a channel, or it is not, for this one question.
2. `buyer_question` — the one question.
3. `citation_record` — who was attached to one answer, on one date, by one method.
4. `indexability_pass` — whether that one URL can be fetched and listed.
5. `brief` — the one page you will write.
6. `kill_date` — the date you stop, as `YYYY-MM-DD`.

## Decision rules

Channel. If one buyer question is worth one page, search is a channel. Say that, and say you will own that one question before any new URL. The line must contain the word channel and the word one. A keyword list is not a channel decision. A 40-article calendar, a health-score dump, or an llms.txt project is the wrong job. Stop.

Buyer question. One question, in the buyer's words. It ends with one question mark. It is not a list of keywords. It is not "what should we publish?"

Citation record. One answer you saw. Include a date written `YYYY-MM-DD`, the names that answer attached, and the word Method plus how you saw it. The sample method is a pasted answer. Replace it with how you saw the answer. A guessed list is not a record. "None observed" is not a record.

Indexability pass. One URL. Say that it returns 200, or say the status. Say whether robots allows it. Say whether the sitemap lists it. Use those words: 200 or status, robots, sitemap. This is not a site grade. "Unchecked" fails.

Brief. Start so the line contains "one page". The first paragraph answers the buyer question with one claim only this brand can say. You decide the claim. The scorer only checks that the brief is one page.

Kill date. A real calendar date, `YYYY-MM-DD`. The sample date is a placeholder. Replace it. It is not a client result.

## Procedure

Do this in order. Write your own lines. Then copy the shape, not the sample facts.

1. Write `channel_decision`. Two short sentences are enough.
2. Write `buyer_question`. One sentence. One question mark at the end.
3. Write `citation_record` from the answer you saw. Date, names, Method. If you did not see it, stop.
4. Write `indexability_pass` from the URL you checked. If you did not check it, stop.
5. Write `brief`. Open with "One page." Name the one claim the first paragraph will make.
6. Write `kill_date`.
7. Save the object as `draft.json` at the repo root.
8. From the repo root, run `python3 scripts/score.py --file draft.json`.

Exit 0 prints the six lines. Exit 1 prints one reason and does not print the pass. Fix that line and run again.

## Nested skills

The skills under `skills/` are the three slices. Each one names these same six keys. Following one slice still has to produce the whole object, or the scorer exits 1.

- `skills/buyer-question` — the question, the brief, and the kill date
- `skills/citation-record` — who was attached to one answer, on one date, by one method
- `skills/indexability` — whether one URL can be fetched and listed

## Filled example

Example only. Replace every line. The date, the rival, and the roundup are not a client result. The kill date is not a promise.

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

The same object is `examples/findability-good.json` in this repo.

## What exit 1 means

- `a health-score dump` — the draft talks about a health score. Stop.
- `an llms.txt project` — the draft starts that project. Stop.
- `a 40-article calendar` — the draft is a calendar. Stop.
- `draft is incomplete` — one of the six strings is missing or blank.
- `channel decision is not one channel` — the line does not say channel and one.
- `buyer question is not one question` — it does not end with one question mark.
- `citation record is not a record` — no `YYYY-MM-DD`, or the word Method is missing.
- `indexability pass is not one URL` — it does not record 200 or status, robots, and sitemap.
- `brief is not one page` — the words "one page" are missing.
- `kill date is not a date` — it is not a real `YYYY-MM-DD`.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Lock one buyer question. End it with one question mark.
- [ ] 2. Write the citation record from an answer you saw, and the indexability pass from a URL you checked.
- [ ] 3. Write the channel decision, the one-page brief, and the kill date.
- [ ] 4. Save the six keys and run `python3 scripts/score.py --file draft.json` from the repo root.

Review again until the script exits 0.

Go back to step 1 if the question is a keyword list.

## Run

```bash
python3 scripts/score.py --file examples/findability-good.json
python3 scripts/score.py --file examples/findability-calendar.json
```

The good draft exits 0 and prints the six lines. The calendar draft exits 1.

Python 3 standard library only. No network.
