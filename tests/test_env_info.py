import os
import unittest
from unittest import mock

from feature_launchpad import env_info


class EnvVarStatusTests(unittest.TestCase):
    def test_reports_required_var_set_and_future_vars_unset(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True):
            statuses = env_info.env_var_status()

        by_name = {v["name"]: v for v in statuses}
        self.assertTrue(by_name["ANTHROPIC_API_KEY"]["set"])
        self.assertTrue(by_name["ANTHROPIC_API_KEY"]["required"])
        self.assertFalse(by_name["FIGMA_ACCESS_TOKEN"]["set"])
        self.assertFalse(by_name["FIGMA_ACCESS_TOKEN"]["required"])

    def test_reports_all_unset_when_environment_is_empty(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            statuses = env_info.env_var_status()

        self.assertTrue(all(not v["set"] for v in statuses))


class ToolVersionTests(unittest.TestCase):
    def test_reads_version_file(self):
        version = env_info.tool_version()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
