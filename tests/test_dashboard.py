import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from feature_launchpad import dashboard


class BuildSnapshotTests(unittest.TestCase):
    def test_reports_missing_required_env_var_and_skips_reachability_check(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: True)

        api_key = next(v for v in snapshot["envVars"] if v["name"] == "ANTHROPIC_API_KEY")
        self.assertFalse(api_key["set"])
        self.assertTrue(api_key["required"])
        self.assertIsNone(snapshot["apiReachable"])

    def test_checks_reachability_when_api_key_set(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: True)

        api_key = next(v for v in snapshot["envVars"] if v["name"] == "ANTHROPIC_API_KEY")
        self.assertTrue(api_key["set"])
        self.assertTrue(snapshot["apiReachable"])

    def test_future_env_vars_marked_optional(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: False)

        figma_var = next(v for v in snapshot["envVars"] if v["name"] == "FIGMA_ACCESS_TOKEN")
        self.assertFalse(figma_var["required"])

    def test_includes_cli_commands_and_stages_from_registry(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: False)

        self.assertEqual(snapshot["cliCommands"], dashboard.registry.CLI_COMMANDS)
        self.assertEqual(snapshot["stages"], dashboard.registry.STAGES)


class RenderHtmlTests(unittest.TestCase):
    def test_renders_self_contained_html_with_no_external_resources(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: True)
        rendered = dashboard.render_html(snapshot)

        self.assertIn("<!doctype html>", rendered)
        self.assertNotIn("http://", rendered)
        self.assertNotIn("https://", rendered)
        self.assertIn("ANTHROPIC_API_KEY", rendered)
        self.assertIn("Stage 1", rendered)

    def test_escapes_env_var_names_in_output(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            snapshot = dashboard.build_snapshot(check_reachability=lambda: False)
        snapshot["envVars"][0]["name"] = "<script>alert(1)</script>"

        rendered = dashboard.render_html(snapshot)

        self.assertNotIn("<script>alert(1)</script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)


class MainTests(unittest.TestCase):
    def test_writes_html_and_snapshot_without_opening_browser(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "dashboard.html"

            with mock.patch("feature_launchpad.dashboard.webbrowser.open") as browser_open:
                exit_code = dashboard.main(["--output", str(output_path), "--no-open"])

            self.assertEqual(exit_code, 0)
            browser_open.assert_not_called()
            self.assertTrue(output_path.is_file())
            snapshot = json.loads((Path(tmp) / "status-snapshot.json").read_text())
            self.assertIn("envVars", snapshot)

    def test_opens_browser_by_default(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "dashboard.html"

            with mock.patch("feature_launchpad.dashboard.webbrowser.open") as browser_open:
                dashboard.main(["--output", str(output_path)])

            browser_open.assert_called_once_with(output_path.resolve().as_uri())


if __name__ == "__main__":
    unittest.main()
