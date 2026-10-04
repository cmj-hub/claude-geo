# Changelog

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
