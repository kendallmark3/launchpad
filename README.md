# Launchpad

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](./CHANGELOG.md)
[![Status: spec-only](https://img.shields.io/badge/status-spec--only-yellow.svg)](./CLAUDE.md)

An automated **feature launchpad**: every feature starts from structured intent and comes out the
other end as a developer-reviewable pull request.

```
intent in → Figma artifact out → Claude/API reasoning → scaffolded code → validation evidence → PR
```

This is not intended to replace designers, architects, or developers. It's meant to produce the
first serious draft of a feature — visual design, code scaffold, validation notes, and an open PR —
so a human can review and take it from there.

> **Status:** design only. There is no implementation yet. The full spec lives in
> [`intent.md`](./intent.md), which is itself an incomplete draft (it cuts off mid-way through
> "Stage 3 — Create Screen Map"). See [`CLAUDE.md`](./CLAUDE.md) for a fuller breakdown of what's
> defined so far and what's still missing.

## Target experience

```
/feature-launchpad ./intents/customer-billing.intent.md
```

produces a `feature/customer-billing-dashboard` branch containing generated design/planning
artifacts (UX flow, screen map, Figma payload, implementation plan, validation report, PR summary)
alongside the actual code and test changes.

## Core principle

- The **intent file** is the source of truth.
- **Figma** is the visual execution layer.
- **Claude/Anthropic reasoning** is the design and implementation intelligence layer.
- The **repository** is the delivery layer.
- The **pull request** is the handoff artifact — a human always reviews before merge.

## Constraints

Version one is meant to be simple, local, and dependency-light: no orchestration frameworks
(LangChain, CrewAI, AutoGen, etc.), no database, no queue, no server, no web UI, no Docker, no
cloud deployment. Just direct HTTP calls to the Anthropic and Figma APIs, using each language's
standard library wherever possible. Every run happens on a new feature branch, and existing source
is never overwritten without a backup or diff.

## Reading more

- [`intent.md`](./intent.md) — the original (partial) spec: mission, required env vars, input intent
  file format, output artifacts, and workflow stages.
- [`CLAUDE.md`](./CLAUDE.md) — guidance for Claude Code sessions working in this repo, including
  where the spec is ambiguous or incomplete.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to contribute right now (mostly: closing spec gaps).
- [`CHANGELOG.md`](./CHANGELOG.md) — notable changes, following Keep a Changelog / SemVer.
- [`SECURITY.md`](./SECURITY.md) — how to report a vulnerability; secret-handling expectations.
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) — community standards for this project.

## Project status

| | |
| --- | --- |
| Implementation | None yet — spec only |
| Spec completeness | Partial — truncated mid "Stage 3" (see `CLAUDE.md`) |
| Version | `0.1.0` (tracks the spec/scaffolding, not shipped code — see [`VERSION`](./VERSION)) |
| License | [Apache 2.0](./LICENSE) |

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Given the current state, the highest-value
contribution is closing gaps in `intent.md` (it cuts off mid-schema in Stage 3) rather than
starting an implementation against an incomplete spec.
