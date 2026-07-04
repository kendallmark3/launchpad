import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from feature_launchpad import cli

SAMPLE_INTENT = (Path(__file__).resolve().parent.parent / "intents" / "customer-billing.intent.md").read_text()


class MainEnvCheckTests(unittest.TestCase):
    def test_stops_with_no_files_written_when_api_key_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            intent_path = Path(tmp) / "customer-billing.intent.md"
            intent_path.write_text(SAMPLE_INTENT, encoding="utf-8")
            output_root = Path(tmp) / "generated"

            exit_code = cli.main([str(intent_path), "--output-root", str(output_root)])

            self.assertEqual(exit_code, 1)
            self.assertFalse(output_root.exists())

    def test_stage_1_runs_and_stops_before_stage_2_when_api_call_fails(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            intent_path = Path(tmp) / "customer-billing.intent.md"
            intent_path.write_text(SAMPLE_INTENT, encoding="utf-8")
            output_root = Path(tmp) / "generated"

            with mock.patch(
                "feature_launchpad.ux_flow.create_message",
                side_effect=cli.AnthropicAPIError("simulated network failure"),
            ), mock.patch("feature_launchpad.http_client.check_reachability", return_value=False):
                exit_code = cli.main([str(intent_path), "--output-root", str(output_root)])

            self.assertEqual(exit_code, 1)
            run_dir = output_root / "customer-billing"
            self.assertTrue((run_dir / "01-normalized-intent.md").exists())
            self.assertFalse((run_dir / "02-ux-flow.md").exists())
            run_log = json.loads((run_dir / "launchpad-run-log.json").read_text())
            statuses = {s["stage"]: s["status"] for s in run_log["stages"]}
            self.assertEqual(statuses["02-ux-flow"], "failed")


class DiagnosticsIntegrationTests(unittest.TestCase):
    def test_successful_run_writes_project_diagnostics(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            intent_path = Path(tmp) / "customer-billing.intent.md"
            intent_path.write_text(SAMPLE_INTENT, encoding="utf-8")
            output_root = Path(tmp) / "generated" / "feature-launchpad"

            with mock.patch("feature_launchpad.ux_flow.create_message", return_value="# UX Flow\n"), mock.patch(
                "feature_launchpad.screen_map.create_message", return_value='{"featureName": "customer-billing"}'
            ), mock.patch("feature_launchpad.http_client.check_reachability", return_value=True):
                exit_code = cli.main([str(intent_path), "--output-root", str(output_root)])

            self.assertEqual(exit_code, 0)
            diagnostics_path = output_root.parent / "diagnostics.json"
            self.assertTrue(diagnostics_path.is_file())

            diagnostics = json.loads(diagnostics_path.read_text())
            self.assertEqual(diagnostics["environment"]["apiReachable"], True)
            self.assertEqual(len(diagnostics["history"]), 1)
            self.assertEqual(diagnostics["history"][0]["featureName"], "customer-billing")
            self.assertEqual(diagnostics["history"][0]["status"], "success")
            feature_names = {f["featureName"] for f in diagnostics["features"]}
            self.assertIn("customer-billing", feature_names)

    def test_failed_run_still_writes_diagnostics_with_failed_status(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            intent_path = Path(tmp) / "customer-billing.intent.md"
            intent_path.write_text(SAMPLE_INTENT, encoding="utf-8")
            output_root = Path(tmp) / "generated" / "feature-launchpad"

            with mock.patch(
                "feature_launchpad.ux_flow.create_message",
                side_effect=cli.AnthropicAPIError("simulated failure"),
            ), mock.patch("feature_launchpad.http_client.check_reachability", return_value=False):
                exit_code = cli.main([str(intent_path), "--output-root", str(output_root)])

            self.assertEqual(exit_code, 1)
            diagnostics_path = output_root.parent / "diagnostics.json"
            diagnostics = json.loads(diagnostics_path.read_text())
            self.assertEqual(diagnostics["history"][0]["status"], "failed")
            self.assertEqual(diagnostics["environment"]["apiReachable"], False)

    def test_history_accumulates_across_multiple_runs(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            intent_path = Path(tmp) / "customer-billing.intent.md"
            intent_path.write_text(SAMPLE_INTENT, encoding="utf-8")
            output_root = Path(tmp) / "generated" / "feature-launchpad"

            with mock.patch("feature_launchpad.ux_flow.create_message", return_value="# UX Flow\n"), mock.patch(
                "feature_launchpad.screen_map.create_message", return_value='{"featureName": "customer-billing"}'
            ), mock.patch("feature_launchpad.http_client.check_reachability", return_value=True):
                cli.main([str(intent_path), "--output-root", str(output_root)])
                cli.main([str(intent_path), "--output-root", str(output_root)])

            diagnostics_path = output_root.parent / "diagnostics.json"
            diagnostics = json.loads(diagnostics_path.read_text())
            self.assertEqual(len(diagnostics["history"]), 2)


if __name__ == "__main__":
    unittest.main()
