# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-03

### Added

- `intents/blackjack-game.intent.md`: a feature intent for a browser-playable blackjack game with
  betting, doubling, splitting, insurance, and a basic-strategy hint mode — run through Stages 1-3
  (see `generated/feature-launchpad/blackjack-game/`).
- `blackjack-game/`: a hand-written implementation of that intent (Stage 4+ doesn't exist in this
  project, so — as with the status dashboard — this is a one-off build from the intent's
  `03-screen-map.json`, not pipeline output). A client-only Vite + React app: full blackjack rules
  (6-deck shoe, hit/stand/double/split/insurance, dealer stands on all 17s, blackjack pays 3:2),
  bankroll and session stats persisted to `localStorage`, and a strategy-hint toggle backed by a
  standard basic-strategy table. 41 unit/integration tests (Vitest + React Testing Library)
  covering hand evaluation, dealer play, payout resolution, and the strategy table. Verified
  end-to-end in a real browser (Playwright) with no console errors.
- Note: this is a separate Node/React project living inside a Python-stdlib repo — see
  `blackjack-game/README.md` for its own setup/run instructions; it has no effect on
  `feature_launchpad`'s own dependency-free constraints.

## [0.3.0] - 2026-07-03

### Added

- Unit tests for the remaining untested modules: `tests/test_http_client.py` (request
  construction, default/env-var model selection, refusal/HTTP-error/URL-error handling),
  `tests/test_ux_flow.py`, and `tests/test_screen_map.py` (including the fenced-code-block
  stripping and JSON-decode-error paths in Stage 3). All Stage 1-3 modules now have direct test
  coverage.
- `intents/launchpad-status-dashboard.intent.md`: a feature intent for a read-only status/health
  dashboard for the launchpad tool itself, run through Stages 1-3 (see
  `generated/feature-launchpad/launchpad-status-dashboard/`).
- `feature_launchpad/dashboard.py` (`python3 -m feature_launchpad.dashboard`): a hand-written
  implementation of that intent — Stage 4+ (code scaffolding) doesn't exist in this project, so
  this is a one-off build from the intent's `03-screen-map.json`, not pipeline output. Writes a
  self-contained, static HTML snapshot (env var presence, Anthropic API reachability, CLI
  commands/pipeline-stage status, doc links) and opens it in a browser. No server process is
  started; re-run to refresh. See `USER_MANUAL.md` Section 8.
- `feature_launchpad/registry.py`: single source of truth for CLI commands and pipeline stages,
  used by both `cli.py` (stage-log ids) and `dashboard.py` (capabilities list), so the two can't
  drift apart.
- `http_client.check_reachability()`: a lightweight `GET /v1/models` connectivity check that costs
  no tokens, used by the dashboard's health check.
- Unit tests for `dashboard.py`, `registry.py`, and the new `check_reachability()` helper.

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

[Unreleased]: https://github.com/kendallmark3/launchpad/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/kendallmark3/launchpad/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/kendallmark3/launchpad/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kendallmark3/launchpad/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kendallmark3/launchpad/releases/tag/v0.1.0
