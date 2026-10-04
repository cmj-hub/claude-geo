# Security

## What this pack does on your machine

- One script runs locally: `scripts/score.py`, standard-library Python 3. No dependencies are installed.
- It reads only the draft JSON you pass it (`--file draft.json`, or the bundled `examples/`). The skills read `psp.vocabulary` from `brand-config.json` when it exists, and never write to it.
- The skills write one JSON draft in your project folder, one field per step. Nothing else on disk is changed.
- Network: the script opens no network connection. Two skills may reach public pages through the agent, and only when you run them: `indexability` runs read-only `curl` requests (status, headers, HTML, `robots.txt`, sitemap) against the one URL and site you name; `citation-record` asks the agent to run your buyer question in an answer engine it can reach, or asks you to paste the answer. No skill pre-approves a web tool in `allowed-tools`, so your agent asks before each request.
- No telemetry. Nothing is logged or sent anywhere by the pack.
- No credentials are asked for or stored.
- Nothing is published. The pack scores a brief; you ship the page.

## Reporting a vulnerability

Email jay@jaymountconsulting.com with "security" and the repo name in the subject, or open a private advisory under this repo's Security tab. Do not open a public issue for a vulnerability. Expect a reply within five business days.

## Supported versions

Only the latest release on `main` gets fixes.
