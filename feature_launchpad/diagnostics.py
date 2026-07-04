"""Project diagnostics — a structured (JSON), machine-readable snapshot of what
this launchpad has produced so far, plus a running history of pipeline runs.

Written to generated/diagnostics.json every time `feature-launchpad` completes a
run (success or failure) — distinct from the per-feature, prose-heavy
`NN-*.md`/`launchpad-run-log.json` output, this is meant to answer "what state is
this project in, and what's happened over time" in one place, at a glance.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from feature_launchpad import env_info, http_client, registry

DIAGNOSTICS_FILENAME = "diagnostics.json"


def _load_existing_history(diagnostics_path: Path) -> list:
    if not diagnostics_path.is_file():
        return []
    try:
        return json.loads(diagnostics_path.read_text(encoding="utf-8")).get("history", [])
    except (json.JSONDecodeError, OSError):
        return []


def _completed_stages(run_log: dict) -> list:
    return [stage["stage"] for stage in run_log.get("stages", []) if stage.get("status") == "completed"]


def _run_status(run_log: dict) -> str:
    return "failed" if any(stage.get("status") == "failed" for stage in run_log.get("stages", [])) else "success"


def _scan_features(output_root: Path) -> list:
    if not output_root.is_dir():
        return []

    features = []
    for feature_dir in sorted(p for p in output_root.iterdir() if p.is_dir()):
        run_log_path = feature_dir / "launchpad-run-log.json"
        if not run_log_path.is_file():
            continue
        try:
            run_log = json.loads(run_log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        feature_name = run_log.get("featureName", feature_dir.name)
        artifacts = sorted(
            p.name for p in feature_dir.iterdir() if p.is_file() and p.name != "launchpad-run-log.json"
        )
        features.append(
            {
                "featureName": feature_name,
                "stagesCompleted": _completed_stages(run_log),
                "lastRunAt": run_log.get("completedAt") or run_log.get("startedAt"),
                "generatedArtifacts": artifacts,
                "handWrittenImplementation": registry.KNOWN_IMPLEMENTATIONS.get(feature_name),
            }
        )
    return features


def build(*, run_log: dict, output_root: Path, diagnostics_path: Path, check_reachability=None) -> dict:
    # Resolved at call time (not bound as a def-time default) so callers that go
    # through cli.py — which doesn't expose this parameter — can still mock
    # feature_launchpad.http_client.check_reachability in tests.
    if check_reachability is None:
        check_reachability = http_client.check_reachability

    env_vars = env_info.env_var_status()
    api_key_set = any(v["name"] == "ANTHROPIC_API_KEY" and v["set"] for v in env_vars)

    history_entry = {
        "runAt": run_log.get("completedAt") or run_log.get("startedAt"),
        "featureName": run_log.get("featureName"),
        "stagesCompleted": _completed_stages(run_log),
        "status": _run_status(run_log),
    }

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "toolVersion": env_info.tool_version(),
        "pipeline": {
            "stages": registry.STAGES,
            "cliCommands": registry.CLI_COMMANDS,
        },
        "environment": {
            "envVars": env_vars,
            "apiReachable": check_reachability() if api_key_set else None,
        },
        "features": _scan_features(output_root),
        "history": _load_existing_history(diagnostics_path) + [history_entry],
    }


def write(*, run_log: dict, output_root: Path, diagnostics_path: Path) -> dict:
    diagnostics = build(run_log=run_log, output_root=output_root, diagnostics_path=diagnostics_path)
    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    diagnostics_path.write_text(json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8")
    return diagnostics
