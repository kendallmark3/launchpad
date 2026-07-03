import unittest

from feature_launchpad import registry


class RegistryTests(unittest.TestCase):
    def test_stages_have_required_fields(self):
        for stage in registry.STAGES:
            self.assertIn("id", stage)
            self.assertIn("label", stage)
            self.assertIn("description", stage)
            self.assertIn(stage["status"], ("implemented", "not_yet_implemented"))

    def test_stages_1_through_3_are_implemented(self):
        implemented = [s["id"] for s in registry.STAGES if s["status"] == "implemented"]
        self.assertEqual(implemented, ["01-normalized-intent", "02-ux-flow", "03-screen-map"])

    def test_cli_commands_have_required_fields(self):
        for command in registry.CLI_COMMANDS:
            self.assertIn("name", command)
            self.assertIn("description", command)


if __name__ == "__main__":
    unittest.main()
