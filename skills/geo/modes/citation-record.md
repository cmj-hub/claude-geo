# Citation record

Mode `citation-record`: who an answer engine named for one question, on one date, by one method. Writes `citation_record`.

A citation record names who was attached to one answer, on one date, by one method. A guessed list is not a record.

It is the baseline. On the kill date, the same method is run again and the two records are compared.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Lock the buyer question. Use the exact wording from the `buyer-question` mode.
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

Write the field into `gtm/findability.json` (create `gtm/` if missing; start from `${CLAUDE_PLUGIN_ROOT}/examples/findability-template.json`), then run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py --file gtm/findability.json
```

Exit 0 prints the six lines. Exit 1 prints `- field: what is wrong → what to change` per problem; fix that field first. Fields other skills own may read `missing` until those skills run.
