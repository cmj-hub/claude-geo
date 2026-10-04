# Changelog

## 0.6.0 — 2026-10-04

- One skill per pack: `geo` is the only skill. The five step skills are modes it reads on demand. Always-on cost drops from ~708 to ~181 tokens.
- `/geo:geo` takes a mode as its argument (`argument-hint` lists them). No argument runs `status`: what passes, what fails, the next step.
- The draft lives at `gtm/findability.json` (the suite's shared work folder), not `draft.json`.
- Scorer: every failing line reads `- field: what is wrong → what to change`; the last line names the next step (`Next: /landing-page:page` on a pass). `--json` adds `fix` per problem, `fix` on a refusal, and `next`. `--input` is a hidden alias for `--file`. `--help` shows an example.
- README "In 60 seconds" block. Trigger evals under `evals/` and a manual `evals.yml` workflow.
- `plugin.json` drops the `skills` key; default discovery finds `skills/geo/`.

### Moved

- `SKILL.md` → `skills/geo/SKILL.md`.
- `skills/<step>/SKILL.md` → `skills/geo/modes/<step>.md` for `channel-decision`, `buyer-question`, `citation-record`, `indexability`, `brief`.
- `/geo:brief` → `/geo:geo brief`; likewise `/geo:channel-decision`, `/geo:buyer-question`, `/geo:citation-record`, `/geo:indexability`.
- `draft.json` → `gtm/findability.json`.

## 0.5.1 — 2026-10-04

- `SECURITY.md`: what runs locally, which skills reach public pages and how, how to report a vulnerability.
- README privacy and security section.

## 0.5.0 — 2026-10-04

- `plugin.json` lists `"skills": ["./"]` so the root `geo` skill loads next to the five under `skills/`.
- Root skill routes to the step skills by command (`/geo:buyer-question` and the rest).
- Root and `buyer-question` read `psp.vocabulary` from `brand-config.json` when present; never invent it.
- "Works with the suite" section: step 9, hands off to landing-page.
- Root skill calls the scorer and examples through `${CLAUDE_SKILL_DIR}`.
- README adds the suite marketplace and `npx skills add` install lines.
- Manifest: author URL, keywords. Version synced in `marketplace.json`.

## 0.4.0 — 2026-10-04

- Scorer checks each axis instead of only checking that fields are filled: question shape, citation date and method, HTTP status / robots / sitemap / blocked pages, brief length, and a kill date 14 to 180 days after the citation record.
- Placeholders (`TBD`, `Unchecked`, `None observed`) fail.
- Refusals read the plan fields only, and catch any batch of ten or more posts or a content calendar, not only "40-article".
- `--json` output for agents.
- New skills: `channel-decision` and `brief` (with the kill-date loop).
- `buyer-question`, `citation-record`, and `indexability` now carry the protocol, not just a checklist: where real questions come from, a repeatable citation method, and an AI-crawler robots table with read-only checks.
- Skills call the scorer through `${CLAUDE_PLUGIN_ROOT}` so it runs from a plugin install.
- `.claude-plugin/marketplace.json` for `/plugin marketplace add cmj-hub/claude-geo`.
- New fixtures: `findability-template.json`, `findability-weak.json`. Tests cover every axis. CI runs them.

## 0.3.0

- Plugin manifest and icon.
