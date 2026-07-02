# Security Policy

## Current status

This repository is currently spec-only (see [`CLAUDE.md`](./CLAUDE.md)) — there is no running
service, deployed endpoint, or shipped code yet. That said, the spec in [`intent.md`](./intent.md)
describes a system that will handle API keys/tokens for the Anthropic API, Figma API, and GitHub
(`ANTHROPIC_API_KEY`, `FIGMA_ACCESS_TOKEN`, `GITHUB_TOKEN`, etc.), so security practice starts now,
before implementation.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for a suspected security vulnerability.

Instead, report it privately via GitHub's
["Report a vulnerability"](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)
flow under this repository's Security tab, or contact the maintainer directly.

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce, or a proof of concept
- Any relevant logs, configs, or affected file paths

You should expect an initial response within 5 business days.

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.x (pre-implementation spec) | :white_check_mark: (spec review only) |

Once an implementation ships, this table will be updated to track supported release lines.

## Handling of secrets

Per `intent.md` Section 5, the launchpad reads required credentials from environment variables and
must **stop with a clear message and make no repo modifications** if any required variable is
missing. Any implementation must never log, persist, or commit these values (`ANTHROPIC_API_KEY`,
`FIGMA_ACCESS_TOKEN`, `FIGMA_FILE_KEY`, `FIGMA_TEAM_ID`, `GITHUB_TOKEN`) to the repository or to
generated artifacts under `generated/`.
