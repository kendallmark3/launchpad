# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Nothing yet.

## [0.2.0] - 2026-07-03

### Added

- First implementation pass: `feature_launchpad/`, a stdlib-only Python package implementing
  Stages 1-3 of `intent.md` Section 8 (Read and Normalize Intent; Reason About UX Flow; Create
  Screen Map). Calls the Anthropic API directly over HTTP via `urllib`, per the spec's hard
  constraints — no `anthropic` SDK dependency.
- CLI entry point: `python3 -m feature_launchpad ./intents/<name>.intent.md`.
- Required-env-var check (`ANTHROPIC_API_KEY`) that stops the workflow with no repo modification
  when missing, per `intent.md` Section 5. `FIGMA_*`/`GITHUB_*` are not yet enforced since the
  stages that use them aren't implemented.
- Sample intent fixture `intents/customer-billing.intent.md`, matching the required input shape
  from `intent.md` Section 6.
- Unit tests (`tests/`, stdlib `unittest`) covering env validation, Stage 1 normalization, and the
  CLI's stop-early behavior.

### Notes

- Output layout decision: generated artifacts are written to
  `generated/feature-launchpad/<feature-name>/`, resolving (for this implementation) the
  unreconciled directory-layout ambiguity flagged in `CLAUDE.md`.
- Stage 3's JSON schema is under-specified in the source spec (truncated after `featureName`); the
  model is asked to record its own schema assumptions rather than the launchpad asserting an
  undocumented schema as authoritative. See `feature_launchpad/screen_map.py`.

## [0.1.0] - 2026-07-02

### Added

- Initial repository scaffolding: license, contribution guidelines, code of conduct, security
  policy, issue/PR templates, and standard project metadata files.
- Cleaned up `intent.md` formatting (removed chat-paste artifacts; content and wording unchanged).

[Unreleased]: https://github.com/kendallmark3/launchpad/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/kendallmark3/launchpad/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kendallmark3/launchpad/releases/tag/v0.1.0
