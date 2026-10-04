<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Generative engine optimization skill for Claude Code. Generative engine optimization is how a page gets quoted by an answer engine.">
</p>

# Generative engine optimization skill for Claude Code

Generative engine optimization is how a page gets quoted by an answer engine.

## In 60 seconds

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install geo@gtm-operator-skills
/geo:geo
```

Or score the sample without an agent:

```bash
python3 scripts/score.py --file examples/findability-good.json       # exit 0, prints six lines, then "Next: /landing-page:page"
python3 scripts/score.py --file examples/findability-calendar.json   # exit 1: - a 40-article calendar → write one brief; the next one waits for this one's kill date
```

Part of the GTM operator suite — `/plugin install gtm@gtm-operator-skills` installs all ten.

Answer engine optimization is the same check.

On 2026-10-01 a pasted answer named a rival and a roundup. This brand was not named.

The good draft passes. A 40-article calendar fails the score.

<p align="center">
  <img src="./assets/demo.gif" alt="Generative engine optimization skill — one brief passes, a content calendar fails" width="100%">
</p>

The build guide teaches a human. The pack teaches an agent.

## Install

In Claude Code, add this repository as a plugin marketplace and install the pack:

```
/plugin marketplace add cmj-hub/claude-geo
/plugin install geo@jmc-geo
```

Or clone it and load the files from disk. The one skill lives in `skills/geo/`; its modes are in `skills/geo/modes/`.

```
git clone https://github.com/cmj-hub/claude-geo.git
```

Other agents (Codex, Cursor, and the rest) can install it with the skills CLI:

```
npx skills add cmj-hub/claude-geo --all -g --full-depth
```

The scorer is Python in this repo. It does not call a paid API.

## The modes

One command, `/geo:geo`, with a mode as the argument. Run the modes in order. Each one writes one field of `gtm/findability.json`. With no argument, `/geo:geo` reports status and starts the first missing field.

| Command | Writes | Job |
|---|---|---|
| `/geo:geo channel-decision` | `channel_decision` | Whether search is a channel for this offer, and what comes first |
| `/geo:geo buyer-question` | `buyer_question` | One question, in the buyer's words, close to a decision |
| `/geo:geo citation-record` | `citation_record` | Who an answer engine named, on one date, by one method |
| `/geo:geo indexability` | `indexability_pass` | Status, robots for search and AI crawlers, sitemap, raw HTML |
| `/geo:geo brief` | `brief`, `kill_date` | One quotable page, and the date the record is run again |
| `/geo:geo status` | nothing | What passes, what fails, and the next step |

Moved in 0.6: `/geo:brief` is now `/geo:geo brief`, and the same for every former step command.

## What you walk out with in 15 minutes

Artifact: `examples/findability-good.json`.

```bash
python3 scripts/score.py --file examples/findability-good.json
python3 scripts/score.py --file examples/findability-weak.json
python3 scripts/score.py --file examples/findability-calendar.json
```

The good draft exits 0, prints the six lines, and names the next step. The weak draft exits 1 and prints one `- axis: what is wrong → what to change` line per problem. The calendar draft exits 1. Then copy `examples/findability-template.json` to `gtm/findability.json` and drop in yours. Add `--json` for one JSON object an agent can read (`pass`, `problems` with a `fix` each, `next`).

## What the score checks

| Axis | Fails when |
|---|---|
| channel decision | One line with no reason and no first step |
| buyer question | Not a question, more than one question, a keyword list, or our question instead of the buyer's |
| citation record | No observed date, or no `Method:` |
| indexability pass | Status is not 200, robots or sitemap not recorded, or the page is blocked |
| brief | Too thin to name the page, or longer than one page's brief |
| kill date | Not a date, or outside 14 to 180 days after the citation record |

Placeholders such as `TBD`, `Unchecked`, or `None observed` fail on any axis.

## What this pack will not do

It will not publish a health-score dump. It does not start an llms.txt project. It will not fill a 40-article calendar, or any batch of ten or more posts.

## What is answer engine optimization?

The same job. A page gets quoted by an answer engine, or it does not. This pack scores that check.

## Does this write the content calendar?

No. A 40-article calendar fails the score.

## Which answer engines does it cover?

The citation record works for any engine a buyer uses: ChatGPT, Perplexity, Claude, Gemini, Copilot, Google AI Overviews and AI Mode. The indexability pass checks robots.txt for the crawlers behind them.

## Does it need llms.txt?

No. llms.txt is not a fetchability control, and no major answer engine has committed to read it. Robots, status, sitemap, and raw HTML decide whether a page can be fetched.

## On the site

- [Generative engine optimization pack](https://jaymountconsulting.com/skills/claude-geo) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack

## Free, no signup

[AI search visibility checker](https://jaymountconsulting.com/tools/geo-visibility-audit)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — architecture gaps in the GTM you already run. Free written report.

[**Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one Friday GTM read. No pitch in it.
## Privacy and security

`scripts/score.py` is standard-library Python and opens no network connection. It reads only the draft JSON you give it. The skill writes one draft, `gtm/findability.json`, in your project folder and only reads `brand-config.json`. The `indexability` mode runs read-only `curl` against the URL you name, and the `citation-record` mode runs your question in an answer engine or asks you to paste the answer; your agent asks before each request. No telemetry, no credentials, nothing published. See [SECURITY.md](SECURITY.md).

## Next

Previous: [Landing page](https://github.com/cmj-hub/claude-landing-page)

Next: [LinkedIn posts](https://github.com/cmj-hub/claude-founder-brand)

## License

MIT. Python 3 standard library only. No network.
