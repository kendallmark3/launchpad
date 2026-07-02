# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repository holds a product/design spec for a tool called the "Feature Launchpad"
(`intent.md`), plus standard repo scaffolding (license, changelog, contribution/security/conduct
policies, issue/PR templates, a markdown-lint CI workflow). **No implementation exists yet**:
there is no source code, package manifest, build system, linter, or test suite for the launchpad
itself. There is nothing to build or unit-test — the only CI is markdown linting.

Note: `intent.md` was originally pasted from a chat UI and has since had its formatting cleaned up
(curly quotes, chat-markup artifacts, doubled blank lines removed) — content and wording are
unchanged. It still cuts off mid-document inside "Stage 3 — Create Screen Map" (see the explicit
truncation note at the end of that file). Stages beyond Stage 3, and the final sections of the
spec, are missing from the source of truth. Confirm with the user before assuming any unstated
stage/output details.

Versioning: the `VERSION` file and `CHANGELOG.md` currently track the *spec and scaffolding*, not
shipped code — there's no code to version yet. Bump them for spec changes too, not just
implementation work.

## What the spec describes

`intent.md` specifies an automated pipeline, invoked as a single command, that turns a structured
"feature intent" markdown file into a developer-reviewable pull request:

```
/feature-launchpad ./intents/customer-billing.intent.md
```

Pipeline: **intent in → Figma artifact out → Claude/Anthropic API reasoning → scaffolded code →
validation evidence → PR ready for human review.**

### Core principle (from the spec)

- The intent file is the source of truth.
- Figma is the visual execution layer.
- Claude/Anthropic reasoning is the design and implementation intelligence layer.
- The repository is the delivery layer.
- The pull request is the handoff artifact.

### Hard constraints for any implementation

These are explicit, load-bearing requirements from the spec — respect them if/when building this out:

- No external orchestration framework (no LangChain, LlamaIndex, CrewAI, AutoGen, or similar agent
  frameworks).
- Prefer built-in Node.js or Python standard library over third-party dependencies.
- Call the Anthropic API and the Figma API directly over HTTP (or via Figma MCP-compatible tool
  invocation where available) — no SDK-heavy abstraction layers.
- No database, no queue, no server process, no web UI.
- No Docker, no cloud deployment (for v1).
- All generated artifacts are written into the repo, not to external state.
- Never overwrite existing source code without a backup or diff.
- All code changes happen on a new feature branch; a human must review the PR before merge.
- Required env vars: `ANTHROPIC_API_KEY`, `FIGMA_ACCESS_TOKEN`, `FIGMA_FILE_KEY`, `FIGMA_TEAM_ID`,
  `GITHUB_TOKEN`, `GITHUB_REPOSITORY`. Optional: `FIGMA_PARENT_NODE_ID`, `DEFAULT_BRANCH`,
  `ANTHROPIC_MODEL`. If a required var is missing, the workflow must stop with a clear message and
  make no repo modifications.

### Expected output layout (per spec)

A run against an intent file is expected to produce a feature branch containing:

```
feature/<feature-name>/
├── generated/
│   ├── ux-flow.md
│   ├── screen-map.json
│   ├── figma-payload.json
│   ├── implementation-plan.md
│   ├── validation-report.md
│   └── pr-summary.md
├── src/
│   └── feature code changes
└── tests/
    └── generated or updated tests
```

The spec's "Output Artifacts" section separately lists a more granular `generated/feature-launchpad/`
directory (`01-normalized-intent.md` through `10-pr-summary.md` plus `launchpad-run-log.json`) — the
two artifact lists don't fully reconcile with each other in the current draft; clarify with the user
before implementing rather than guessing which is authoritative.

### Workflow stages defined so far

1. **Read and Normalize Intent** — parse the input intent file into `01-normalized-intent.md`,
   preserving original language while normalizing structure (feature name, business goal, target
   users, primary workflow, screens, components, data fields, API expectations, error/edge cases,
   acceptance criteria, accessibility/security expectations, open questions).
2. **Reason About UX Flow** — direct Anthropic API call producing `02-ux-flow.md` (entry point,
   step-by-step journey, decision points, alternate/empty/error/confirmation/success states,
   required screens, transitions, permissions/roles).
3. **Create Screen Map** — direct Anthropic API call producing `03-screen-map.json` (schema cuts off
   in the source doc after `"featureName"`).

Stages 4+ are not present in `intent.md` as currently saved.

### Required intent file input shape

Per the spec, an input intent file must have these sections: Business Goal, User Personas, User
Journey, Required Screens, Functional Requirements, Non-Functional Requirements, Design Constraints,
API / Data Requirements, Acceptance Criteria, Validation Expectations, Out of Scope. If sections are
missing, the launchpad is specified to generate a clarification report and proceed only if there's
enough information to safely draft.
