# Contributing

Thanks for opening this repo. A few notes on how this project works
before you contribute.

## What kinds of contributions land

- **Bug reports** — open an issue with a reproducible case. The
  scripts in `scripts/` are deterministic, so bugs there are usually
  one-line fixes.
- **New sub-skills** that extend the existing framework. Discuss in
  an issue first if it's a substantial addition.
- **Calibration improvements** to the scoring scripts — if you can
  show a case where the script scores wrong, that's gold.
- **Cross-runtime ports** (Cursor, Gemini CLI, Codex) — install is
  via the skills CLI; see the README Install section.
- **Translation** of the framework reference docs.

## What doesn't land

- Renaming the findability artifacts (channel decision, buyer question,
  citation record, indexability pass, brief, kill date) — these are
  course-anchored.
- Turning the pack into a health-score dump, an llms.txt project, or a
  40-article calendar.
- Adding LLM calls inside the skills. The whole point is that the
  skills are deterministic.
- Adding paid-API dependencies to scripts. Scripts must work zero-dep.
- Renaming `claude-*` → `<other-runtime>-*`. We ship per-runtime ports
  as separate plugins instead.

## Development setup

```bash
git clone https://github.com/cmj-hub/claude-geo.git
cd claude-geo
# Install into local agents
npx skills add cmj-hub/claude-geo --all -g --full-depth
```

For Python scripts:

```bash
# All scripts are zero-dep Python 3.8+ — just run them
python3 scripts/score.py --help
python3 scripts/score.py --file examples/findability-good.json
```

## Pull-request checklist

- [ ] Skill names follow the spec (lowercase, hyphens, ≤64 chars,
      directory matches `name:` in frontmatter)
- [ ] Sub-skill descriptions include trigger phrases inline
- [ ] If you touch a script, smoke-test it and paste output in the PR
- [ ] If you add a new sub-skill, list it in the README companion table
- [ ] CHANGELOG.md updated (when present)
- [ ] No new dependencies (any of: pip packages, npm packages, API
      keys, paid services)

## Reporting calibration issues with scoring scripts

If `score.py` scores something obviously wrong:

1. Paste the input that produced the wrong score
2. State your expected exit code + printed lines vs actual
3. Note which axis is mis-calibrated (channel decision, buyer
   question, citation record, indexability, brief, or kill date)

The scorer is stdlib-only and deterministic. New calibration cases add
to fixtures under `examples/` and `tests/`, not to script side paths
that call a network — keep the deterministic path stable.

## License

By contributing, you agree your contributions ship under the MIT
license already on this repo.

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
Part of the JMC public-build spine — see [/build](https://jaymountconsulting.com/build).
