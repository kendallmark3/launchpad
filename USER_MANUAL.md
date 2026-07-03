# User Manual

How to run Launchpad today, from a clean checkout to generated output.

## There's no UI (yet)

By design (see `intent.md` Section 4 — "Hard Constraints"), this project does not have or require
a web UI. It's a command-line tool: you point it at an intent file, it writes generated files into
your repo, and you review them like any other file. Nothing runs in a browser and nothing needs a
server.

What's implemented today is Stages 1-3 of the pipeline: normalize your intent file, generate a UX
flow, and generate a screen map. It stops there — see [Current limitations](#current-limitations)
at the end.

## 1. Prerequisites

- **Python 3** (no version manager or virtualenv required — the tool only uses the standard
  library, no `pip install` needed).
- **An Anthropic API key.** Get one at [console.anthropic.com](https://console.anthropic.com) if
  you don't already have one. Stages 2 and 3 call the Anthropic API directly, so this is required.

Check your Python version:

```bash
python3 --version
```

## 2. Set your API key

The tool reads your key from the `ANTHROPIC_API_KEY` environment variable. Set it in your shell
before running anything:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

If you skip this, the tool stops immediately with a clear error and writes nothing — it never
gets partway through and leaves a mess.

Optional: override the model (defaults to `claude-sonnet-4-5`):

```bash
export ANTHROPIC_MODEL=claude-sonnet-4-5
```

## 3. Write an intent file

An intent file is a markdown file describing the feature you want drafted. It must be named
`<feature-name>.intent.md` — the part before `.intent.md` becomes the feature name used for the
output folder and branch-style naming.

It needs these `##` sections (see `intents/customer-billing.intent.md` in this repo for a full
worked example):

```
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

Write real content under each heading — plain English is fine, this isn't a strict schema. The
tool preserves your original wording; it only reorganizes structure.

`Business Goal` and `Required Screens` are the two sections it actually needs to proceed — if
either is missing, it stops and writes nothing rather than guessing. The rest are optional: if
they're missing, it notes that in the output instead of failing.

Save your file under `intents/`, e.g. `intents/my-feature.intent.md`.

## 4. Run it

From the repo root:

```bash
python3 -m feature_launchpad ./intents/my-feature.intent.md
```

You'll see progress printed as each stage completes:

```
[1/3] Wrote generated/feature-launchpad/my-feature/01-normalized-intent.md
[2/3] Wrote generated/feature-launchpad/my-feature/02-ux-flow.md
[3/3] Wrote generated/feature-launchpad/my-feature/03-screen-map.json

Done. Stages 4+ (Figma, implementation scaffold, validation, PR) are not implemented — see CLAUDE.md.
```

Stages 2 and 3 call the Anthropic API, so each run costs a small amount of API usage and takes a
few seconds.

By default, output goes under `generated/feature-launchpad/<feature-name>/`. You can redirect it:

```bash
python3 -m feature_launchpad ./intents/my-feature.intent.md --output-root ./somewhere-else
```

## 5. Read the output

Each run writes, under `generated/feature-launchpad/<feature-name>/`:

| File | What it is |
| --- | --- |
| `01-normalized-intent.md` | Your intent file, restructured into the tool's normalized field list. Pure text transformation — no API call, no invented content. |
| `02-ux-flow.md` | Claude's UX flow write-up: entry point, step-by-step journey, decision points, alternate/empty/error/confirmation/success states, required screens, transitions, and roles. |
| `03-screen-map.json` | A JSON screen map. The source spec's schema is incomplete (see `CLAUDE.md`), so this file includes a `_assumptions` array documenting what the model inferred beyond the one confirmed field (`featureName`). |
| `launchpad-run-log.json` | A machine-readable record of which stages ran, their status, and timestamps — useful if a run fails partway through. |

Nothing here is meant to be final. Read `02-ux-flow.md` and `03-screen-map.json` like a first draft
from a colleague: check it against your actual intent, and correct anything that's off before
using it for downstream work.

## 6. If something goes wrong

- **"Missing required environment variable(s): ANTHROPIC_API_KEY"** — you didn't `export` your key
  in this shell session (env vars don't persist across terminal tabs/windows). Set it and rerun.
- **"intent file is missing 'Business Goal' and/or 'Required Screens'"** — add those two sections
  to your intent file; nothing was written.
- **"Stage 2 (UX flow) failed" / "Stage 3 (screen map) failed"** — usually a transient API issue
  (rate limit, network) or an invalid key. `01-normalized-intent.md` (and `02-ux-flow.md`, if Stage
  3 is what failed) will still be on disk along with `launchpad-run-log.json` showing which stage
  failed — you can rerun once the underlying issue is fixed; it's safe to run again since nothing
  is deleted.

## 7. Running the test suite

Not required to use the tool, but useful if you're changing it:

```bash
python3 -m unittest discover -s tests -v
```

No test-only dependencies — everything's `unittest` from the standard library.

## Current limitations

- **Stages 1-3 only.** Figma generation, code scaffolding, validation, and pull-request creation
  (Stages 4+ in the original spec) are not implemented. The source spec itself is truncated before
  those stages are fully defined — see `CLAUDE.md` for details.
- **No branch/PR automation yet.** Output is written to your working directory on whatever branch
  you're already on; the tool doesn't create branches or PRs itself.
- **Only `ANTHROPIC_API_KEY` is enforced.** The `FIGMA_*` and `GITHUB_*` variables from `intent.md`
  Section 5 aren't checked yet, since nothing uses them at this stage.
