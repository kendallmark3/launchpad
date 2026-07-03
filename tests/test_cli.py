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
            ):
                exit_code = cli.main([str(intent_path), "--output-root", str(output_root)])

            self.assertEqual(exit_code, 1)
            run_dir = output_root / "customer-billing"
            self.assertTrue((run_dir / "01-normalized-intent.md").exists())
            self.assertFalse((run_dir / "02-ux-flow.md").exists())
            run_log = json.loads((run_dir / "launchpad-run-log.json").read_text())
            statuses = {s["stage"]: s["status"] for s in run_log["stages"]}
            self.assertEqual(statuses["02-ux-flow"], "failed")


if __name__ == "__main__":
    unittest.main()
