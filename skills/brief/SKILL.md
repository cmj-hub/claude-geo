---
name: brief
description: "Write one page brief that an answer engine can quote, plus one kill date. Use when the buyer question, citation record, and indexability pass are done and the next step is the page itself, or when someone asks how to structure content so ChatGPT, Perplexity, or AI Overviews will cite it."
models: ""
---

# Brief

One page. One brief. One kill date. The brief says what the page must say and in what order. It is not the page.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Read the citation record. Note who was named and which pages were cited.
- [ ] 2. Write the first paragraph's job (below).
- [ ] 3. Name the one claim only this brand can say.
- [ ] 4. List the follow-up questions the page answers, as headings.
- [ ] 5. Set the kill date.
- [ ] 6. Write `brief` and `kill_date`. Run the scorer.

Review again until the scorer exits 0.

## What makes a page quotable

Answer engines lift passages, not pages. Every rule here makes one passage easy to lift.

- **The first paragraph answers the buyer question.** Directly, in 40 to 60 words, without needing the rest of the page. No preamble, no "in today's landscape".
- **One claim only this brand can say.** A number from your own data, a named method, a price, a dated result. Generic advice is already in the answer from someone else.
- **Specifics over adjectives.** Numbers, named tools, named roles, dates. "Cuts setup from 3 weeks to 4 days" gets quoted; "fast setup" does not.
- **Headings are follow-up questions.** Use the questions the engine suggests next and the ones the buyer asks after the first answer. Each section opens with its own direct answer.
- **A comparison table when buyers compare.** Rows are options, columns are what the buyer weighs. Tables are easy to lift.
- **Who says so.** A named author with a reason to know, and a visible updated date.
- **Structured data that matches the page.** `Article` or `WebPage` with `author` and `dateModified`; `Organization` with `sameAs` links on the site. Use `FAQPage` only for a real on-page Q&A. Markup that does not match visible text is ignored or penalised.

## The kill date

The kill date is when the citation record is run again with the same method.

- Set it 6 to 12 weeks after the page ships. Engines take weeks to recrawl and re-ground. The scorer accepts 14 to 180 days after the citation record.
- On the kill date, re-run `citation-record` with the same question, engines, and method.
- If this brand is now named or cited: keep the page and pick the next buyer question.
- If not: rewrite the first paragraph and the one claim once, or kill the page and pick a different question. Do not add more pages on the same question.

## Refuse

- A brief that covers more than one page. Split it into separate briefs, one at a time.
- A 40-article calendar. One brief ships before the next is written.

## Output

The `brief` and `kill_date` fields. Example:

> One page. First paragraph answers the buyer question with one claim only this brand can say.

> 2026-12-15

## Score

Write the field into `draft.json` (start from `examples/findability-template.json`), then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}/scripts/score.py" --file draft.json
```

Exit 0 prints the six lines. Exit 1 names each failing field; fix that field first. Fields other skills own may read `missing` until those skills run.
