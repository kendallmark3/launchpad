# Feature Intent

## Business Goal

Give developers and operators a lightweight, read-only visual surface into the Feature
Launchpad tool itself — current environment/health status, and what capabilities (CLI
commands / pipeline stages) are available — without requiring them to read source code
or run commands to find out. This reduces onboarding friction and repeated "is this
configured correctly?" / "what can this tool do?" questions.

## User Personas

- **Developer** — runs `feature-launchpad` locally; wants to confirm required env vars
  and Anthropic API connectivity before kicking off a real pipeline run.
- **New Contributor** — orienting to the repo; wants to see available commands and
  pipeline stages without reading all of the source first.

## User Journey

1. User opens the GUI locally (e.g. a local static page or lightweight local view).
2. They see a health-check panel: which required env vars are set vs. missing, and
   whether the Anthropic API is reachable.
3. They see a list of available CLI commands/pipeline stages (Stages 1-3 implemented;
   Stages 4+ not yet implemented) with a one-line description of each.
4. They can browse links into existing docs (README.md, USER_MANUAL.md) for more detail.
5. To actually generate an intent file or run a pipeline stage, the user is directed to
   the existing CLI — the GUI itself never submits, generates, or runs anything.

## Required Screens

- Health Check / Status (required env var presence, Anthropic API reachability, tool
  version)
- Capabilities / Endpoints (list of CLI commands and pipeline stages, with status:
  implemented vs. not yet implemented)
- Docs (links to / rendered excerpts of README.md and USER_MANUAL.md)

## Functional Requirements

- Display pass/fail status for each required env var, masked — never render secret
  values.
- Perform a lightweight connectivity check against the Anthropic API and show
  reachable/unreachable (reusing the existing HTTP client rather than adding a new one).
- List available CLI stages/commands with short descriptions, sourced from a single
  place shared with the CLI so the list can't drift out of sync with reality.
- Clearly mark which pipeline stages are implemented (Stages 1-3) vs. not (Stages 4+).
- Link to CLI usage instructions for generating intent files and running the pipeline —
  the GUI does not duplicate or replace that functionality.
- Read-only: the GUI must never write, modify, or trigger generation of any file.

## Non-Functional Requirements

- No new required runtime dependency beyond the Python standard library, consistent
  with the project's existing "prefer stdlib, no SDK-heavy abstraction layers"
  constraint.
- Must run entirely locally; the only outbound network call is the existing Anthropic
  API reachability check.
- Should render in under 2 seconds on a developer machine.
- Must not require any credentials beyond what `feature-launchpad` already requires.

## Design Constraints

- Must not replace, wrap, or change the existing CLI workflow for authoring intent
  files or running Stages 1-3 (`feature-launchpad <intent-file>`) — the CLI remains the
  only way to actually run the pipeline. This is explicit per the requester: the GUI is
  additive, not a replacement for intent generation.
- The existing hard constraint in this repo's spec is "no server process, no web UI."
  A GUI inherently needs *some* local rendering surface (e.g. a static HTML file opened
  locally, versus a running local server) — which approach to take is an open question
  for implementation to resolve with the maintainer, not assumed here.
- Should reuse existing repo content (README.md, USER_MANUAL.md) as the source of
  displayed documentation rather than duplicating it into a second copy that can drift.

## API / Data Requirements

- Reads local environment variables (`ANTHROPIC_API_KEY`, and `FIGMA_*`/`GITHUB_*` once
  those are enforced by later stages) to report presence/absence only.
- Makes a minimal outbound request to the Anthropic API to confirm reachability, reusing
  `feature_launchpad/http_client.py` rather than introducing a second HTTP path.
- Introduces no new external API surface beyond this reachability check.

## Acceptance Criteria

- A user can determine, without reading source code, whether their environment is
  correctly configured to run `feature-launchpad`.
- A user can see, at a glance, what the tool currently supports (Stages 1-3) and what is
  not yet implemented (Stages 4+).
- Opening or viewing the GUI never creates, modifies, or deletes any file under
  `generated/` or elsewhere in the repo.
- The existing CLI command (`feature-launchpad <intent-file>`) continues to work
  unchanged after this feature ships.

## Validation Expectations

- Unit tests covering the env-var status check (set / missing / masked-value cases).
- A test or smoke check confirming the capabilities list is generated from the same
  source the CLI uses, rather than hand-duplicated text that can go stale.
- Manual verification that no filesystem writes occur from simply viewing the GUI.

## Out of Scope

- Any GUI-driven way to author a new intent file, submit one, or kick off/monitor a
  pipeline run — that remains CLI-only, per this task's explicit scope.
- Stages 4+ (Figma generation, code scaffolding, validation, PR creation) — not
  implemented yet, regardless of interface.
- Authentication or multi-user access — this is a local, single-developer tool.
