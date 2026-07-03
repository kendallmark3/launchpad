# Launchpad

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](./CHANGELOG.md)
[![Status: Stages 1-3 implemented](https://img.shields.io/badge/status-stages%201--3%20implemented-brightgreen.svg)](./CLAUDE.md)

An automated **feature launchpad**: every feature starts from structured intent and comes out the
other end as a developer-reviewable pull request.

```
intent in → Figma artifact out → Claude/API reasoning → scaffolded code → validation evidence → PR
```

This is not intended to replace designers, architects, or developers. It's meant to produce the
first serious draft of a feature — visual design, code scaffold, validation notes, and an open PR —
so a human can review and take it from there.

> **Status:** partial implementation. Stages 1-3 of the pipeline (normalize intent → UX flow →
> screen map) are implemented in [`feature_launchpad/`](./feature_launchpad/); Stages 4+ (Figma
> generation, code scaffold, validation, PR) don't exist yet because [`intent.md`](./intent.md)
> itself cuts off mid-way through "Stage 3 — Create Screen Map". See [`CLAUDE.md`](./CLAUDE.md) for
> a fuller breakdown of what's defined so far and what's still missing.

## Running it today

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 -m feature_launchpad ./intents/customer-billing.intent.md
```

This runs Stages 1-3 and writes `generated/feature-launchpad/customer-billing/`:
`01-normalized-intent.md`, `02-ux-flow.md`, `03-screen-map.json`, and a `launchpad-run-log.json`.
If `ANTHROPIC_API_KEY` isn't set, the workflow stops immediately with a clear message and writes
nothing, per `intent.md` Section 5.

Run the test suite (standard library `unittest`, no extra dependencies):

```bash
python3 -m unittest discover -s tests -v
```

## Target experience (not yet fully implemented)

```
/feature-launchpad ./intents/customer-billing.intent.md
```

produces a `feature/customer-billing-dashboard` branch containing generated design/planning
artifacts (UX flow, screen map, Figma payload, implementation plan, validation report, PR summary)
alongside the actual code and test changes. Today's CLI produces the first three generated
artifacts only, on the current branch — branch/PR automation is part of the unimplemented Stages
4+.

## Example: an intent taken all the way to a working app

Since Stages 4+ don't exist yet, [`blackjack-game/`](./blackjack-game/) is a hand-written (not
pipeline-generated) implementation of [`intents/blackjack-game.intent.md`](./intents/blackjack-game.intent.md),
built from that intent's Stage 1-3 output. It's a standalone client-only Vite + React app — see
`blackjack-game/README.md` to run it. This shows what a Stage 4+ code-scaffolding step would need
to produce, without claiming the pipeline actually does this yet.

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

The one exception is an optional, read-only status dashboard (`python3 -m feature_launchpad.dashboard`,
see `USER_MANUAL.md`) — a static HTML snapshot, not a running server, that shows environment health
and current tool capabilities. The pipeline itself still needs no server and no web UI.

## Reading more

- [`USER_MANUAL.md`](./USER_MANUAL.md) — step-by-step guide to running the CLI today: setup, writing
  an intent file, reading the output, and troubleshooting.
- [`intent.md`](./intent.md) — the original (partial) spec: mission, required env vars, input intent
  file format, output artifacts, and workflow stages.
- [`CLAUDE.md`](./CLAUDE.md) — guidance for Claude Code sessions working in this repo, including
  where the spec is ambiguous or incomplete.
- [`feature_launchpad/`](./feature_launchpad/) — the Stage 1-3 implementation (stdlib-only Python;
  see module docstrings for how each stage maps to `intent.md` Section 8).
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to contribute right now (mostly: closing spec gaps).
- [`CHANGELOG.md`](./CHANGELOG.md) — notable changes, following Keep a Changelog / SemVer.
- [`SECURITY.md`](./SECURITY.md) — how to report a vulnerability; secret-handling expectations.
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) — community standards for this project.

## Project status

| | |
| --- | --- |
| Implementation | Stages 1-3 (`feature_launchpad/`); Stages 4+ don't exist yet |
| Spec completeness | Partial — truncated mid "Stage 3" (see `CLAUDE.md`) |
| Version | `0.2.0` (see [`VERSION`](./VERSION) and [`CHANGELOG.md`](./CHANGELOG.md)) |
| License | [Apache 2.0](./LICENSE) |

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). High-value contributions right now: closing gaps in
`intent.md` (it cuts off mid-schema in Stage 3), or implementing Stage 4 (Figma generation) once
that gap is resolved.
