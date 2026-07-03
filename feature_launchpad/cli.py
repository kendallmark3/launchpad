"""Feature Launchpad CLI — orchestrates Stages 1-3 defined in intent.md Section 8.

Stages 4 onward are not implemented: intent.md is truncated before those stages
are defined (see the truncation note at the end of that file, and CLAUDE.md).
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from feature_launchpad import env, intent_parser, registry, screen_map, ux_flow
from feature_launchpad.http_client import AnthropicAPIError

STAGE_1, STAGE_2, STAGE_3 = (stage["id"] for stage in registry.STAGES[:3])

# intent.md Section 5 lists ANTHROPIC_API_KEY, FIGMA_ACCESS_TOKEN, FIGMA_FILE_KEY,
# FIGMA_TEAM_ID, GITHUB_TOKEN, and GITHUB_REPOSITORY as required. Only
# ANTHROPIC_API_KEY is enforced here because Stages 4+ (Figma generation, PR
# creation) — the only stages that use the other variables — aren't implemented yet.
REQUIRED_ENV_VARS = ("ANTHROPIC_API_KEY",)


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="feature-launchpad", description=__doc__)
    parser.add_argument("intent_file", type=Path, help="Path to a *.intent.md file")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("generated/feature-launchpad"),
        help="Directory generated artifacts are written under (default: %(default)s)",
    )
    return parser.parse_args(argv)


def _write_run_log(run_dir: Path, run_log: dict) -> None:
    (run_dir / "launchpad-run-log.json").write_text(json.dumps(run_log, indent=2) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        env.require(REQUIRED_ENV_VARS)
    except env.MissingEnvVarError as exc:
        print(f"feature-launchpad: {exc}", file=sys.stderr)
        return 1

    if not args.intent_file.is_file():
        print(f"feature-launchpad: intent file not found: {args.intent_file}", file=sys.stderr)
        return 1

    normalized = intent_parser.normalize(args.intent_file)

    if "Business Goal" in normalized.missing_sections or "Required Screens" in normalized.missing_sections:
        print(
            "feature-launchpad: intent file is missing 'Business Goal' and/or "
            "'Required Screens' — not enough information to safely draft. No files "
            "were written.",
            file=sys.stderr,
        )
        return 1

    run_dir = args.output_root / normalized.feature_name
    run_dir.mkdir(parents=True, exist_ok=True)

    run_log = {
        "featureName": normalized.feature_name,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "stages": [],
    }

    def record_stage(name: str, status: str, detail: str = "") -> None:
        run_log["stages"].append(
            {
                "stage": name,
                "status": status,
                "detail": detail,
                "at": datetime.now(timezone.utc).isoformat(),
            }
        )

    (run_dir / "01-normalized-intent.md").write_text(normalized.content, encoding="utf-8")
    record_stage(STAGE_1, "completed")
    if normalized.missing_sections:
        record_stage(
            STAGE_1,
            "warning",
            f"Missing optional sections: {', '.join(normalized.missing_sections)}",
        )
    print(f"[1/3] Wrote {run_dir / '01-normalized-intent.md'}")

    try:
        flow = ux_flow.generate(normalized.content)
    except AnthropicAPIError as exc:
        record_stage(STAGE_2, "failed", str(exc))
        _write_run_log(run_dir, run_log)
        print(f"feature-launchpad: Stage 2 (UX flow) failed: {exc}", file=sys.stderr)
        return 1

    (run_dir / "02-ux-flow.md").write_text(flow, encoding="utf-8")
    record_stage(STAGE_2, "completed")
    print(f"[2/3] Wrote {run_dir / '02-ux-flow.md'}")

    try:
        screens = screen_map.generate(normalized.content, flow)
    except (AnthropicAPIError, json.JSONDecodeError) as exc:
        record_stage(STAGE_3, "failed", str(exc))
        _write_run_log(run_dir, run_log)
        print(f"feature-launchpad: Stage 3 (screen map) failed: {exc}", file=sys.stderr)
        return 1

    (run_dir / "03-screen-map.json").write_text(json.dumps(screens, indent=2) + "\n", encoding="utf-8")
    record_stage(STAGE_3, "completed")
    print(f"[3/3] Wrote {run_dir / '03-screen-map.json'}")

    run_log["completedAt"] = datetime.now(timezone.utc).isoformat()
    _write_run_log(run_dir, run_log)

    print("\nDone. Stages 4+ (Figma, implementation scaffold, validation, PR) are not implemented — see CLAUDE.md.")
    return 0
