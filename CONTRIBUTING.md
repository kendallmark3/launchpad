# Contributing

Thanks for your interest in the Feature Launchpad project.

## Current status

This repository is spec-only — see [`intent.md`](./intent.md) for the (partial) product/design
spec and [`CLAUDE.md`](./CLAUDE.md) for known gaps in that spec. There is no implementation yet:
no source code, package manifest, build system, linter, or test suite. Keep that in mind before
opening an implementation PR — align on the spec gaps first (see "Spec questions" below).

## How to contribute right now

Given the current state, the most valuable contributions are:

1. **Filling spec gaps.** `intent.md` is truncated mid-way through "Stage 3 — Create Screen Map."
   Stages 4+ and the final sections are missing. If you have the rest of the source document,
   or authority to define what's missing, open an issue or PR against `intent.md`.
2. **Resolving spec inconsistencies.** The "Output Artifacts" section documents two different
   directory layouts for generated files (`generated/` vs. `generated/feature-launchpad/`) that
   don't fully reconcile. Flag these rather than silently picking one when implementing.
3. **First implementation.** Once the spec is complete enough to build against, implementation
   PRs should respect the hard constraints in `intent.md` Section 4 (no orchestration frameworks,
   standard-library-first, no database/queue/server/Docker for v1, etc.).

## Spec questions

Open a GitHub issue using the "Spec question / clarification" template before assuming an answer
to an ambiguous or missing part of `intent.md`. Do not guess and silently implement — the hard
constraints in the spec exist precisely to avoid scope creep and unauthorized architectural
choices.

## Pull requests

- Keep PRs scoped to one concern (one spec clarification, one stage of implementation, etc.).
- All changes land on a feature branch and require review before merge — no direct pushes to
  the default branch, and no self-merges once there's more than one maintainer.
- Update `CHANGELOG.md` under `[Unreleased]` for any user-visible or spec-visible change.
- Reference the intent.md section(s) your change relates to in the PR description.

## Commit style

Use short, imperative-mood commit subjects (e.g. "Add Stage 4 spec section", not "Added" or
"Adding"). Explain *why* in the body when the reason isn't obvious from the diff.

## Code of conduct

Participation in this project is governed by [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## Security issues

Do not open a public issue for a security concern — see [`SECURITY.md`](./SECURITY.md).
