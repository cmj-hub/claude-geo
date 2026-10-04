---
name: geo
description: "Score generative engine optimization (GEO) and answer engine optimization (AEO) findability for one buyer question: channel decision, buyer question, citation record, indexability pass, one page brief, and one kill date. Use when a page must be quotable by ChatGPT, Perplexity, Claude, Gemini, Copilot, or Google AI Overviews, when someone asks whether they show up in AI answers, or when a content calendar or health-score dump must be refused. Not for drafting the landing page itself (use landing-page)."
argument-hint: "[channel-decision | buyer-question | citation-record | indexability | brief | status]"
allowed-tools: Read Write Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py:*)
models: ""
---

# Generative engine optimization

Generative engine optimization is how a page gets quoted by an answer engine.

Answer engine optimization is the same check.

This pack scores findability for one question. It refuses a 40-article calendar and a health-score dump. It does not start an llms.txt project.

The build guide teaches a human. This pack teaches an agent.

## Before any mode

1. If `brand-config.json` sits at the project root, read `psp.vocabulary` (below).
2. Read `gtm/findability.json` if it exists. That is the draft. If it does not exist, create `gtm/` if missing and copy `${CLAUDE_PLUGIN_ROOT}/examples/findability-template.json` to `gtm/findability.json`.

## Modes

If `$ARGUMENTS` names a mode, go straight to it. If `$ARGUMENTS` is empty, run `status` and then the first mode whose field is still missing. Read the mode file with the Read tool and follow it.

| You say / argument | Mode file | Writes |
|---|---|---|
| `channel-decision`, "is search a channel for us" | [modes/channel-decision.md](modes/channel-decision.md) | `channel_decision` |
| `buyer-question`, "which question should the page answer" | [modes/buyer-question.md](modes/buyer-question.md) | `buyer_question` |
| `citation-record`, "do we show up in ChatGPT" | [modes/citation-record.md](modes/citation-record.md) | `citation_record` |
| `indexability`, "can crawlers fetch this URL" | [modes/indexability.md](modes/indexability.md) | `indexability_pass` |
| `brief`, "how should the page be written" | [modes/brief.md](modes/brief.md) | `brief`, `kill_date` |
| `status`, or no argument | this file, Status | nothing |

Run the modes in the table's order. Each mode owns its checklist. This skill owns the draft and the score gate.

Moved in 0.6: the five step skills are modes now. `/geo:brief` is `/geo:geo brief`; the same holds for every former step command.

## Status

Run the scorer on `gtm/findability.json`. Say which fields pass, which line fails, and the next step: the mode named in the first failing line, or `/landing-page:page` when it exits 0. On the kill date, say `/geo:geo citation-record`.

## From brand-config.json

If `brand-config.json` sits at the project root, read `psp.vocabulary`. Those are the buyer's own words; `buyer-question` phrases the question in them. Read only. This pack writes nothing to the file. If the block is missing, say that the psp pack makes it (`/plugin install psp@gtm-operator-skills`) and take the words from real sources. Do not invent them.

## Run

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py --file gtm/findability.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py --file gtm/findability.json --json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py --file ${CLAUDE_PLUGIN_ROOT}/examples/findability-good.json
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score.py --file ${CLAUDE_PLUGIN_ROOT}/examples/findability-weak.json
```

Exit 0 prints the six lines and `Next: /landing-page:page`. Exit 1 prints one `- field: what is wrong → what to change` line per problem, or the refusal (calendar, health score, llms.txt), then `Next: fix the lines above and run this again.` Exit 2 means the file is unusable. `--json` prints one object with `pass`, `problems` (each with a `fix`), and `next`.

## The loop

On the kill date, run `/geo:geo citation-record` again with the same question and method. Named or cited: keep the page and pick the next question. Not named: rewrite once or kill the page. One brief ships before the next is written.

Python 3 standard library only. No network.

## Works with the suite

This is step 9 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `psp.vocabulary` (the buyer's words) from `brand-config.json`, if present.
- **Writes:** `gtm/findability.json` only. It never touches another pack's keys.
- **Before this:** psp (`/psp:psp`), when there is no buyer vocabulary yet.
- **After this:** landing-page (`/landing-page:page`), to draft the page the brief describes.

When the scorer exits 0, end with: `Next: /landing-page:page`. If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.
