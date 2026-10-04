---
name: geo
description: "Score generative engine optimization (GEO) and answer engine optimization (AEO) findability for one buyer question. Use when a page must be quotable by ChatGPT, Perplexity, Claude, Gemini, Copilot, or Google AI Overviews, and when a content calendar or health-score dump must be refused."
models: ""
---

# Generative engine optimization

Generative engine optimization is how a page gets quoted by an answer engine.

Answer engine optimization is the same check.

This pack scores findability for one question. It refuses a 40-article calendar and a health-score dump. It does not start an llms.txt project.

The build guide teaches a human. This pack teaches an agent.

## Nested skills

Installers should load the skills under `skills/`. Run them in this order:

1. `skills/channel-decision` — whether search is a channel for this offer, and what comes first
2. `skills/buyer-question` — one buyer question, in the buyer's words
3. `skills/citation-record` — who was attached to one answer, on one date, by one method
4. `skills/indexability` — whether one URL can be fetched and listed by search and AI crawlers
5. `skills/brief` — one quotable page brief and one kill date

Each nested skill owns its checklist. This root skill only names the pack and the score gate.

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

From a plugin install the scorer is `${CLAUDE_PLUGIN_ROOT}/scripts/score.py`. From a clone it is `scripts/score.py`.

```bash
python3 scripts/score.py --file examples/findability-good.json
python3 scripts/score.py --file examples/findability-weak.json
python3 scripts/score.py --file examples/findability-calendar.json
python3 scripts/score.py --file draft.json --json
```

The good draft exits 0 and prints the six lines. The weak draft exits 1 and names each failing axis. The calendar draft exits 1. `--json` prints the same result for an agent to read.

## The loop

On the kill date, run `citation-record` again with the same question and method. Named or cited: keep the page and pick the next question. Not named: rewrite once or kill the page. One brief ships before the next is written.

Python 3 standard library only. No network.
