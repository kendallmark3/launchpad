"""Shared environment/version helpers used by dashboard.py and diagnostics.py.

Kept separate from registry.py (which tracks CLI commands/pipeline stages) since
this is about the local environment the tool is running in, not the tool itself.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ENV_VARS = ("ANTHROPIC_API_KEY",)
FUTURE_ENV_VARS = (
    "FIGMA_ACCESS_TOKEN",
    "FIGMA_FILE_KEY",
    "FIGMA_TEAM_ID",
    "GITHUB_TOKEN",
    "GITHUB_REPOSITORY",
)


def _status(names, required):
    return [{"name": name, "set": bool(os.environ.get(name)), "required": required} for name in names]


def env_var_status() -> list:
    return _status(REQUIRED_ENV_VARS, required=True) + _status(FUTURE_ENV_VARS, required=False)


def tool_version() -> str:
    version_file = REPO_ROOT / "VERSION"
    if version_file.is_file():
        return version_file.read_text(encoding="utf-8").strip()
    return "unknown"
