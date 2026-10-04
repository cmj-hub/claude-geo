---
name: geo
description: "Score generative engine optimization (GEO) and answer engine optimization (AEO) findability for one buyer question, and route to the five step skills. Use when a page must be quotable by ChatGPT, Perplexity, Claude, Gemini, Copilot, or Google AI Overviews, and when a content calendar or health-score dump must be refused. Not for drafting the landing page itself (use landing-page)."
models: ""
---

# Generative engine optimization

Generative engine optimization is how a page gets quoted by an answer engine.

Answer engine optimization is the same check.

This pack scores findability for one question. It refuses a 40-article calendar and a health-score dump. It does not start an llms.txt project.

The build guide teaches a human. This pack teaches an agent.

## Nested skills

The plugin loads this skill and the five under `skills/`. Run them in this order:

1. `/geo:channel-decision` (`skills/channel-decision`) — whether search is a channel for this offer, and what comes first
2. `/geo:buyer-question` (`skills/buyer-question`) — one buyer question, in the buyer's words
3. `/geo:citation-record` (`skills/citation-record`) — who was attached to one answer, on one date, by one method
4. `/geo:indexability` (`skills/indexability`) — whether one URL can be fetched and listed by search and AI crawlers
5. `/geo:brief` (`skills/brief`) — one quotable page brief and one kill date

Start at the first field still missing in the draft. Each nested skill owns its checklist. This root skill only names the pack and the score gate.

## From brand-config.json

If `brand-config.json` sits at the project root, read `psp.vocabulary`. Those are the buyer's own words; `buyer-question` phrases the question in them. Read only. This pack writes nothing to the file. If the block is missing, say that the psp pack makes it (`/plugin install psp@gtm-operator-skills`) and take the words from real sources. Do not invent them.

## The draft

Every skill writes one field of one JSON draft. Start from `examples/findability-template.json`:

| Field | Written by |
|---|---|
| `channel_decision` | `channel-decision` |
| `buyer_question` | `buyer-question` |
| `citation_record` | `citation-record` |
| `indexability_pass` | `indexability` |
| `brief`, `kill_date` | `brief` |

## Run

`${CLAUDE_SKILL_DIR}` is this skill's directory (the plugin root). From a clone, run the same commands from the repo root without the prefix.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/findability-good.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/findability-weak.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/findability-calendar.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file draft.json --json
```

The good draft exits 0 and prints the six lines. The weak draft exits 1 and names each failing axis. The calendar draft exits 1. `--json` prints the same result for an agent to read.

## The loop

On the kill date, run `citation-record` again with the same question and method. Named or cited: keep the page and pick the next question. Not named: rewrite once or kill the page. One brief ships before the next is written.

Python 3 standard library only. No network.

## Works with the suite

This is step 9 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `psp.vocabulary` (the buyer's words) from `brand-config.json`, if present.
- **Writes:** nothing outside the draft. It never touches another pack's keys.
- **Before this:** psp (`/psp:psp`), when there is no buyer vocabulary yet.
- **After this:** landing-page (`/landing-page:page`), to draft the page the brief describes.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.
