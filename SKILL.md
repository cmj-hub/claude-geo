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

## Nested skills

Installers should load the skills under `skills/`:

- `skills/buyer-question` — one buyer question, one brief, one kill date
- `skills/citation-record` — who was attached to one answer, on one date, by one method
- `skills/indexability` — whether one URL can be fetched and listed

Each nested skill owns its checklist. This root skill only names the pack and the score gate.

## Run

```bash
python3 scripts/score.py --file examples/findability-good.json
python3 scripts/score.py --file examples/findability-calendar.json
```

The good draft exits 0 and prints the six lines. The calendar draft exits 1.

Python 3 standard library only. No network.
