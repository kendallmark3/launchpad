import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from feature_launchpad import diagnostics

SUCCESSFUL_RUN_LOG = {
    "featureName": "example-feature",
    "startedAt": "2026-07-04T00:00:00+00:00",
    "completedAt": "2026-07-04T00:00:05+00:00",
    "stages": [
        {"stage": "01-normalized-intent", "status": "completed", "detail": "", "at": "2026-07-04T00:00:01+00:00"},
        {"stage": "02-ux-flow", "status": "completed", "detail": "", "at": "2026-07-04T00:00:02+00:00"},
        {"stage": "03-screen-map", "status": "completed", "detail": "", "at": "2026-07-04T00:00:03+00:00"},
    ],
}

FAILED_RUN_LOG = {
    "featureName": "example-feature",
    "startedAt": "2026-07-04T00:00:00+00:00",
    "stages": [
        {"stage": "01-normalized-intent", "status": "completed", "detail": "", "at": "2026-07-04T00:00:01+00:00"},
        {"stage": "02-ux-flow", "status": "failed", "detail": "boom", "at": "2026-07-04T00:00:02+00:00"},
    ],
}


class BuildTests(unittest.TestCase):
    def test_history_entry_reflects_success(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            result = diagnostics.build(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: True,
            )

        entry = result["history"][-1]
        self.assertEqual(entry["featureName"], "example-feature")
        self.assertEqual(entry["status"], "success")
        self.assertEqual(entry["stagesCompleted"], ["01-normalized-intent", "02-ux-flow", "03-screen-map"])
        self.assertEqual(result["environment"]["apiReachable"], True)

    def test_history_entry_reflects_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = diagnostics.build(
                run_log=FAILED_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: False,
            )

        entry = result["history"][-1]
        self.assertEqual(entry["status"], "failed")
        self.assertEqual(entry["stagesCompleted"], ["01-normalized-intent"])

    def test_skips_reachability_check_when_api_key_unset(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            called = []
            result = diagnostics.build(
                run_log=FAILED_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: called.append(True) or True,
            )

        self.assertEqual(called, [])
        self.assertIsNone(result["environment"]["apiReachable"])

    def test_includes_pipeline_stages_and_cli_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = diagnostics.build(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: False,
            )

        self.assertGreaterEqual(len(result["pipeline"]["stages"]), 7)
        self.assertGreaterEqual(len(result["pipeline"]["cliCommands"]), 1)

    def test_resolves_check_reachability_dynamically_when_not_passed(self):
        # Regression test: check_reachability must be looked up at call time so
        # mocking feature_launchpad.http_client.check_reachability (as cli.py's
        # tests do, since cli.py never passes this parameter explicitly) works.
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), tempfile.TemporaryDirectory() as tmp:
            with mock.patch("feature_launchpad.http_client.check_reachability", return_value=True):
                result = diagnostics.build(
                    run_log=SUCCESSFUL_RUN_LOG,
                    output_root=Path(tmp) / "feature-launchpad",
                    diagnostics_path=Path(tmp) / "diagnostics.json",
                )

        self.assertEqual(result["environment"]["apiReachable"], True)


class ScanFeaturesTests(unittest.TestCase):
    def test_scans_existing_run_logs_and_flags_known_implementations(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "feature-launchpad"
            feature_dir = output_root / "blackjack-game"
            feature_dir.mkdir(parents=True)
            (feature_dir / "launchpad-run-log.json").write_text(json.dumps(SUCCESSFUL_RUN_LOG).replace(
                "example-feature", "blackjack-game"
            ))
            (feature_dir / "01-normalized-intent.md").write_text("content")

            result = diagnostics.build(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=output_root,
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: False,
            )

        feature = next(f for f in result["features"] if f["featureName"] == "blackjack-game")
        self.assertEqual(feature["handWrittenImplementation"], "blackjack-game/")
        self.assertIn("01-normalized-intent.md", feature["generatedArtifacts"])

    def test_unknown_feature_has_no_implementation_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "feature-launchpad"
            feature_dir = output_root / "some-other-feature"
            feature_dir.mkdir(parents=True)
            (feature_dir / "launchpad-run-log.json").write_text(json.dumps(SUCCESSFUL_RUN_LOG).replace(
                "example-feature", "some-other-feature"
            ))

            result = diagnostics.build(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=output_root,
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: False,
            )

        feature = next(f for f in result["features"] if f["featureName"] == "some-other-feature")
        self.assertIsNone(feature["handWrittenImplementation"])

    def test_returns_empty_list_when_output_root_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = diagnostics.build(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=Path(tmp) / "does-not-exist",
                diagnostics_path=Path(tmp) / "diagnostics.json",
                check_reachability=lambda: False,
            )

        self.assertEqual(result["features"], [])


class WriteTests(unittest.TestCase):
    # write() doesn't expose check_reachability, so these clear the environment
    # to guarantee the reachability check is skipped (ANTHROPIC_API_KEY unset)
    # rather than depending on / hitting the network with whatever key happens
    # to be set in the developer's shell.
    def test_write_persists_and_accumulates_history(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            diagnostics_path = Path(tmp) / "diagnostics.json"
            output_root = Path(tmp) / "feature-launchpad"

            diagnostics.write(run_log=SUCCESSFUL_RUN_LOG, output_root=output_root, diagnostics_path=diagnostics_path)
            second = diagnostics.write(run_log=SUCCESSFUL_RUN_LOG, output_root=output_root, diagnostics_path=diagnostics_path)

            self.assertTrue(diagnostics_path.is_file())
            self.assertEqual(len(second["history"]), 2)
            on_disk = json.loads(diagnostics_path.read_text())
            self.assertEqual(len(on_disk["history"]), 2)

    def test_write_creates_parent_directory(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            diagnostics_path = Path(tmp) / "nested" / "diagnostics.json"
            diagnostics.write(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=diagnostics_path,
            )
            self.assertTrue(diagnostics_path.is_file())

    def test_corrupt_existing_diagnostics_file_does_not_crash(self):
        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            diagnostics_path = Path(tmp) / "diagnostics.json"
            diagnostics_path.write_text("not valid json")

            result = diagnostics.write(
                run_log=SUCCESSFUL_RUN_LOG,
                output_root=Path(tmp) / "feature-launchpad",
                diagnostics_path=diagnostics_path,
            )

            self.assertEqual(len(result["history"]), 1)


if __name__ == "__main__":
    unittest.main()
