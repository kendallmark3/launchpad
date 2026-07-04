"""Status dashboard — a read-only, static companion view for the launchpad CLI.

Implements the `launchpad-status-dashboard` feature intent
(`intents/launchpad-status-dashboard.intent.md`). There is no Stage 4+ (code
scaffolding) in this project yet, so this module is a one-off hand-written
implementation of that intent's `03-screen-map.json`, not pipeline output.

Per that intent's Design Constraints, this must not become a running server: it
writes a self-contained HTML snapshot (data embedded inline, no fetch) and exits.
Re-run it to refresh the snapshot. This keeps the project's "no server process,
no web UI" hard constraint intact for the core pipeline — this is an optional,
separate dev tool.
"""

import argparse
import html
import json
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

from feature_launchpad import env_info, http_client, registry

REPO_ROOT = env_info.REPO_ROOT
DOC_FILES = ("README.md", "USER_MANUAL.md")
DEFAULT_OUTPUT = REPO_ROOT / "generated" / "feature-launchpad" / "launchpad-status-dashboard" / "dashboard.html"


def _doc_links():
    return [{"label": name, "exists": (REPO_ROOT / name).is_file()} for name in DOC_FILES]


def build_snapshot(*, check_reachability=http_client.check_reachability) -> dict:
    env_vars = env_info.env_var_status()
    api_key_set = any(v["name"] == "ANTHROPIC_API_KEY" and v["set"] for v in env_vars)

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "toolVersion": env_info.tool_version(),
        "envVars": env_vars,
        "apiReachable": check_reachability() if api_key_set else None,
        "cliCommands": registry.CLI_COMMANDS,
        "stages": registry.STAGES,
        "docs": _doc_links(),
    }


def _status_badge(ok, *, unknown_label="Not checked") -> str:
    if ok is None:
        return f'<span class="badge badge-unknown">{unknown_label}</span>'
    if ok:
        return '<span class="badge badge-ok">&#10003; OK</span>'
    return '<span class="badge badge-fail">&#10007; Not set</span>'


def _render_env_vars(env_vars) -> str:
    rows = []
    for var in env_vars:
        if var["set"]:
            badge = _status_badge(True)
        elif var["required"]:
            badge = _status_badge(False)
        else:
            badge = '<span class="badge badge-unknown">Not set (not yet required)</span>'
        required_label = "required" if var["required"] else "optional, future"
        rows.append(
            f'<tr><td><code>{html.escape(var["name"])}</code></td>'
            f'<td>{required_label}</td><td>{badge}</td></tr>'
        )
    return "\n".join(rows)


def _render_stages(stages) -> str:
    rows = []
    for stage in stages:
        badge = (
            '<span class="badge badge-ok">implemented</span>'
            if stage["status"] == "implemented"
            else '<span class="badge badge-unknown">not yet implemented</span>'
        )
        rows.append(
            f'<tr><td>{html.escape(stage["label"])}</td>'
            f'<td>{html.escape(stage["description"])}</td><td>{badge}</td></tr>'
        )
    return "\n".join(rows)


def _render_commands(commands) -> str:
    items = []
    for command in commands:
        items.append(
            f'<li><code>{html.escape(command["name"])}</code>'
            f'<br><span class="muted">{html.escape(command["description"])}</span></li>'
        )
    return "\n".join(items)


def _render_docs(docs) -> str:
    items = []
    for doc in docs:
        if doc["exists"]:
            items.append(f'<li><a href="../../../{html.escape(doc["label"])}">{html.escape(doc["label"])}</a></li>')
        else:
            items.append(f'<li class="muted">{html.escape(doc["label"])} (not found)</li>')
    return "\n".join(items)


def render_html(snapshot: dict) -> str:
    overall_ok = all(v["set"] for v in snapshot["envVars"] if v["required"]) and snapshot["apiReachable"]
    overall_banner = (
        '<div class="banner banner-ok">Environment configured correctly — ready to run feature-launchpad.</div>'
        if overall_ok
        else '<div class="banner banner-warn">Some configuration items need attention — see below.</div>'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Feature Launchpad — Status Dashboard</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 760px; margin: 2.5rem auto; padding: 0 1.5rem;
    line-height: 1.5; color: #1a1a1a; background: #fff;
  }}
  h1 {{ font-size: 1.5rem; margin-bottom: 0.25rem; }}
  h2 {{ font-size: 1.1rem; margin-top: 2.5rem; border-bottom: 1px solid #ddd; padding-bottom: 0.4rem; }}
  .meta {{ color: #666; font-size: 0.85rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 0.75rem; }}
  td {{ padding: 0.5rem 0.4rem; border-bottom: 1px solid #eee; vertical-align: top; font-size: 0.92rem; }}
  code {{ background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; font-size: 0.88em; }}
  .muted {{ color: #777; font-size: 0.85rem; }}
  .badge {{ display: inline-block; padding: 0.15rem 0.55rem; border-radius: 999px; font-size: 0.78rem; font-weight: 600; white-space: nowrap; }}
  .badge-ok {{ background: #d9f2e3; color: #146c3a; }}
  .badge-fail {{ background: #fbdada; color: #a01515; }}
  .badge-unknown {{ background: #efefef; color: #666; }}
  .banner {{ padding: 0.75rem 1rem; border-radius: 6px; margin-top: 1rem; font-size: 0.92rem; }}
  .banner-ok {{ background: #d9f2e3; color: #146c3a; }}
  .banner-warn {{ background: #fdf3d0; color: #7a5b00; }}
  ul {{ padding-left: 1.2rem; }}
  li {{ margin-bottom: 0.6rem; }}
  .info {{ font-size: 0.85rem; color: #666; background: #f7f7f7; padding: 0.6rem 0.9rem; border-radius: 6px; margin-top: 1rem; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #16181d; color: #e6e6e6; }}
    h2 {{ border-color: #333; }}
    td {{ border-color: #2a2a2a; }}
    code {{ background: #262933; }}
    .info {{ background: #1f2229; }}
  }}
</style>
</head>
<body>
<h1>Feature Launchpad — Status Dashboard</h1>
<p class="meta">Generated {html.escape(snapshot["generatedAt"])} · tool version {html.escape(snapshot["toolVersion"])}
· static snapshot, not live — re-run <code>python3 -m feature_launchpad.dashboard</code> to refresh</p>

<h2>Health Check</h2>
{overall_banner}
<table>
<tr><td><strong>Environment variable</strong></td><td><strong>Required</strong></td><td><strong>Status</strong></td></tr>
{_render_env_vars(snapshot["envVars"])}
<tr><td>Anthropic API connectivity</td><td>—</td><td>{_status_badge(snapshot["apiReachable"], unknown_label="Not checked (no API key set)")}</td></tr>
</table>

<h2>Capabilities</h2>
<p class="muted">CLI commands</p>
<ul>
{_render_commands(snapshot["cliCommands"])}
</ul>
<p class="muted">Pipeline stages</p>
<table>
<tr><td><strong>Stage</strong></td><td><strong>Description</strong></td><td><strong>Status</strong></td></tr>
{_render_stages(snapshot["stages"])}
</table>
<div class="info">This dashboard is read-only. To generate an intent file or run the pipeline, use the CLI — see the Documentation links below.</div>

<h2>Documentation</h2>
<ul>
{_render_docs(snapshot["docs"])}
</ul>
</body>
</html>
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="feature-launchpad-dashboard", description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the dashboard HTML to (default: %(default)s)",
    )
    parser.add_argument("--no-open", action="store_true", help="Don't open the dashboard in a browser after writing it")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    snapshot = build_snapshot()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(snapshot), encoding="utf-8")
    (args.output.parent / "status-snapshot.json").write_text(
        json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Wrote {args.output}")
    if not args.no_open:
        webbrowser.open(args.output.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
