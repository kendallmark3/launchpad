import unittest
from unittest import mock

from feature_launchpad import ux_flow


class GenerateTests(unittest.TestCase):
    def test_returns_model_output_verbatim(self):
        with mock.patch("feature_launchpad.ux_flow.create_message", return_value="# UX Flow\n...") as create_message:
            result = ux_flow.generate("normalized intent text")

        self.assertEqual(result, "# UX Flow\n...")
        create_message.assert_called_once()

    def test_prompt_includes_normalized_intent_and_required_sections(self):
        with mock.patch("feature_launchpad.ux_flow.create_message", return_value="ok") as create_message:
            ux_flow.generate("--- SAMPLE INTENT CONTENT ---")

        prompt = create_message.call_args[0][0]
        self.assertIn("--- SAMPLE INTENT CONTENT ---", prompt)
        for section in (
            "User entry point",
            "Step-by-step journey",
            "Decision points",
            "Alternate paths",
            "Empty states",
            "Error states",
            "Confirmation states",
            "Success states",
            "Required screens",
            "Screen transitions",
            "User permissions or roles",
        ):
            self.assertIn(section, prompt)

    def test_passes_max_tokens_to_create_message(self):
        with mock.patch("feature_launchpad.ux_flow.create_message", return_value="ok") as create_message:
            ux_flow.generate("intent")

        self.assertEqual(create_message.call_args.kwargs.get("max_tokens"), 4096)


if __name__ == "__main__":
    unittest.main()
