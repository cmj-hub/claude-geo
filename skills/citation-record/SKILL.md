---
name: citation-record
description: "Write one dated citation record for one buyer question: which brands, pages, and sources an answer engine actually named, on what date, by what method. Use when someone asks whether they show up in ChatGPT, Perplexity, Claude, Gemini, Copilot, or Google AI Overviews, or when a visibility claim has no date or method behind it."
models: ""
---

# Citation record

A citation record names who was attached to one answer, on one date, by one method. A guessed list is not a record.

It is the baseline. On the kill date, the same method is run again and the two records are compared.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Lock the buyer question. Use the exact wording from `buyer-question`.
- [ ] 2. Pick the engines. At least one the buyer actually uses. Write them down.
- [ ] 3. Run the question with the protocol below.
- [ ] 4. Write the observed names, the date, and the method.
- [ ] 5. Run the scorer.

Check again until the scorer exits 0.

Return to step 3 if step 5 fails.

## Protocol

- Paste the question verbatim. Do not add the brand name, a location, or "best".
- Use a fresh session. Logged out or a clean profile where the engine allows it. Personal memory and history change the answer.
- Run it three times per engine. Answers vary between runs. Record what showed up in most runs, and say so.
- Record, for each engine: the brands named in the answer text, the pages linked or cited as sources, and whether this brand was named, cited, both, or neither.
- Save the raw answer text or a screenshot with the date. The record points to it.

If the agent cannot reach an engine, it asks the human to paste the answer. A pasted answer is a valid method. A remembered answer is not.

## Method vocabulary

Write the method as `Method: ...` using one of these:

- `pasted answer` — a human ran the question and pasted the text.
- `manual run, N runs, <engine>` — the agent or human ran it N times in a clean session.
- `API run, N runs, <model>` — the question was sent through an API. Say so; API answers can differ from the consumer app.
- `tool export, <tool name>` — a tracking tool's export for this exact question and date.

## Do not

- Do not infer citations from rankings. A blue-link position is not a citation.
- Do not average across many questions into one visibility score. That is a health-score dump.
- Do not record a date you did not run it.

## Output

The `citation_record` field. Example:

> On 2026-10-01 a pasted answer named a rival and a roundup. This brand was not named. Method: pasted answer.

## Score

Write the field into `draft.json` (start from `examples/findability-template.json`), then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}/scripts/score.py" --file draft.json
```

Exit 0 prints the six lines. Exit 1 names each failing field; fix that field first. Fields other skills own may read `missing` until those skills run.
