# Feature Launchpad — Intent → Figma → Code → Validation → PR

> **Source note:** This document originated as a pasted chat response and is reproduced here with
> formatting cleaned up — curly quotes, duplicated blank lines, and chat-UI markup artifacts
> (e.g. `:::writing{...}`) removed. Content and wording are otherwise unchanged from the original.
> The source was truncated mid-schema in **Stage 3 — Create Screen Map**; see the note at the end
> of this file. Do not assume any stage or output detail beyond what appears below — confirm with
> the repo owner first. See [CLAUDE.md](./CLAUDE.md) for a fuller breakdown of what's missing.

## 1. Mission

Create an automated feature launchpad that starts every feature from structured intent and
produces a developer-reviewable pull request.

The system must take feature intent as input, reason about the feature, generate or update Figma
artifacts, validate the design and implementation plan against the intent, scaffold the feature
code, run basic validation, and prepare a pull request for developer review.

This is not intended to fully replace designers, architects, or developers. It is intended to
create the first serious feature draft: visual design, code scaffold, validation notes, and PR.

## 2. North Star

A developer should be able to run one Claude Code workflow and produce:

- Parsed feature intent
- UX flow
- Screen map
- Figma generation payload or Figma update instructions
- Reasoning notes from Anthropic API
- Feature implementation scaffold
- Unit or smoke validation where possible
- Evidence report
- Pull request branch ready for developer review

The target experience:

```sh
/feature-launchpad ./intents/customer-billing.intent.md
```

The result:

```text
feature/customer-billing-dashboard
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

## 3. Core Principle

- The intent file is the source of truth.
- Figma is the visual execution layer.
- Claude/Anthropic reasoning is the design and implementation intelligence layer.
- The repository is the delivery layer.
- The pull request is the handoff artifact.

## 4. Hard Constraints

The first version must be simple, local, and dependency-light.

Required constraints:

- No external framework dependency for the orchestrator.
- Use built-in Node.js or Python standard library where possible.
- Use direct HTTP calls for the Anthropic API.
- Use direct HTTP calls for the Figma API, or Figma MCP-compatible tool invocation where
  available.
- Do not require a database.
- Do not require a queue.
- Do not require a server.
- Do not require a web UI.
- Do not require LangChain, LlamaIndex, CrewAI, AutoGen, or agent frameworks.
- Do not require Docker for version one.
- Do not require cloud deployment for version one.
- Output all generated artifacts into the repo.
- Never overwrite existing source code without creating a backup or diff.
- All code changes must be created on a new feature branch.
- A human developer must review the pull request before merge.

## 5. Required Environment Variables

The launchpad must read the following environment variables:

```sh
ANTHROPIC_API_KEY=...
FIGMA_ACCESS_TOKEN=...
FIGMA_FILE_KEY=...
FIGMA_TEAM_ID=...
GITHUB_TOKEN=...
GITHUB_REPOSITORY=owner/repo
```

Optional:

```sh
FIGMA_PARENT_NODE_ID=...
DEFAULT_BRANCH=main
ANTHROPIC_MODEL=claude-sonnet-4-5
```

If any required variable is missing, the workflow must stop with a clear message and must not
modify the repo.

## 6. Inputs

The workflow accepts a single feature intent file.

Example:

```sh
/feature-launchpad ./intents/customer-billing-dashboard.intent.md
```

The input intent file must include:

```markdown
# Feature Intent

## Business Goal

## User Personas

## User Journey

## Required Screens

## Functional Requirements

## Non-Functional Requirements

## Design Constraints

## API / Data Requirements

## Acceptance Criteria

## Validation Expectations

## Out of Scope
```

If sections are missing, the launchpad must generate a clarification report and continue only if
enough information exists to safely create a draft.

## 7. Output Artifacts

The launchpad must create the following files:

```text
generated/feature-launchpad/
├── 01-normalized-intent.md
├── 02-ux-flow.md
├── 03-screen-map.json
├── 04-figma-generation-payload.json
├── 05-figma-result.md
├── 06-implementation-plan.md
├── 07-code-generation-prompt.md
├── 08-validation-checklist.md
├── 09-validation-report.md
├── 10-pr-summary.md
└── launchpad-run-log.json
```

> **Note:** This list does not fully reconcile with the `generated/` layout shown in Section 2
> (North Star). Both appear in the original source as written. Clarify which is authoritative
> before implementing rather than guessing.

## 8. Workflow Stages

### Stage 1 — Read and Normalize Intent

Read the input intent file.

Create `01-normalized-intent.md`.

The normalized intent must include:

- Feature name
- Business goal
- Target users
- Primary workflow
- Screens
- Components
- Data fields
- API expectations
- Error states
- Edge cases
- Acceptance criteria
- Accessibility expectations
- Security expectations
- Open questions

The launchpad must preserve the original intent language and only normalize structure.

### Stage 2 — Reason About UX Flow

Call the Anthropic API directly.

Prompt Claude to create `02-ux-flow.md`.

The UX flow must include:

- User entry point
- Step-by-step journey
- Decision points
- Alternate paths
- Empty states
- Error states
- Confirmation states
- Success states
- Required screens
- Screen transitions
- User permissions or roles

The response must be written as markdown.

### Stage 3 — Create Screen Map

Call the Anthropic API directly.

Create `03-screen-map.json`.

The screen map must be valid JSON and include:

```json
{
  "featureName": ""
}
```

> **⚠️ Truncated here.** This is where the original pasted document ends — mid-schema in Stage 3,
> with a `[Message clipped]` artifact from the source chat UI. The full `03-screen-map.json`
> schema, Stages 4 and onward, and any sections following Workflow Stages are **not present in any
> known source** and must not be fabricated or assumed. Get the rest of the spec from the repo
> owner before implementing beyond this point.
