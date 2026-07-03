"""Single source of truth for CLI commands and pipeline stages.

`cli.py` and `dashboard.py` both read from this module so the dashboard's
capabilities list can never drift from what the CLI actually does — see
`03-screen-map.json`'s `capabilitiesRegistry` note for the launchpad-status-dashboard
feature.
"""

CLI_COMMANDS = [
    {
        "name": "feature-launchpad <intent-file>",
        "description": (
            "Runs Stages 1-3 of the pipeline against an intent file, writing artifacts "
            "to generated/feature-launchpad/<feature-name>/."
        ),
    },
    {
        "name": "feature-launchpad <intent-file> --output-root <dir>",
        "description": "Same as above, writing artifacts under a different output directory.",
    },
    {
        "name": "python3 -m feature_launchpad.dashboard",
        "description": (
            "Writes a static, read-only status dashboard (env var / API reachability / "
            "capabilities) and opens it in a browser."
        ),
    },
]

STAGES = [
    {
        "id": "01-normalized-intent",
        "label": "Stage 1 — Read and Normalize Intent",
        "description": "Parses an intent file into a normalized field list. No API call.",
        "status": "implemented",
    },
    {
        "id": "02-ux-flow",
        "label": "Stage 2 — Reason About UX Flow",
        "description": "Calls the Anthropic API to produce a UX flow write-up.",
        "status": "implemented",
    },
    {
        "id": "03-screen-map",
        "label": "Stage 3 — Create Screen Map",
        "description": "Calls the Anthropic API to produce a JSON screen map.",
        "status": "implemented",
    },
    {
        "id": "04-figma-generation",
        "label": "Stage 4 — Figma Generation",
        "description": "Not implemented — the source spec is truncated before this stage is defined.",
        "status": "not_yet_implemented",
    },
    {
        "id": "05-code-scaffolding",
        "label": "Stage 5 — Implementation Scaffolding",
        "description": "Not implemented — the source spec is truncated before this stage is defined.",
        "status": "not_yet_implemented",
    },
    {
        "id": "06-validation",
        "label": "Stage 6 — Validation",
        "description": "Not implemented — the source spec is truncated before this stage is defined.",
        "status": "not_yet_implemented",
    },
    {
        "id": "07-pr-creation",
        "label": "Stage 7 — PR Creation",
        "description": "Not implemented — the source spec is truncated before this stage is defined.",
        "status": "not_yet_implemented",
    },
]
