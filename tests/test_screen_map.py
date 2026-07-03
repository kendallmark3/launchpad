import json
import unittest
from unittest import mock

from feature_launchpad import screen_map


class GenerateTests(unittest.TestCase):
    def test_parses_plain_json_response(self):
        raw = json.dumps({"featureName": "customer-billing", "screens": []})
        with mock.patch("feature_launchpad.screen_map.create_message", return_value=raw):
            result = screen_map.generate("normalized intent", "ux flow")

        self.assertEqual(result, {"featureName": "customer-billing", "screens": []})

    def test_strips_fenced_json_code_block(self):
        payload = {"featureName": "customer-billing"}
        raw = "```json\n" + json.dumps(payload) + "\n```"
        with mock.patch("feature_launchpad.screen_map.create_message", return_value=raw):
            result = screen_map.generate("intent", "flow")

        self.assertEqual(result, payload)

    def test_strips_bare_fenced_code_block(self):
        payload = {"featureName": "customer-billing"}
        raw = "```\n" + json.dumps(payload) + "\n```"
        with mock.patch("feature_launchpad.screen_map.create_message", return_value=raw):
            result = screen_map.generate("intent", "flow")

        self.assertEqual(result, payload)

    def test_raises_json_decode_error_on_invalid_json(self):
        with mock.patch("feature_launchpad.screen_map.create_message", return_value="not json"):
            with self.assertRaises(json.JSONDecodeError):
                screen_map.generate("intent", "flow")

    def test_prompt_includes_intent_and_ux_flow(self):
        with mock.patch(
            "feature_launchpad.screen_map.create_message", return_value='{"featureName": "x"}'
        ) as create_message:
            screen_map.generate("--- INTENT MARKER ---", "--- FLOW MARKER ---")

        prompt = create_message.call_args[0][0]
        self.assertIn("--- INTENT MARKER ---", prompt)
        self.assertIn("--- FLOW MARKER ---", prompt)
        self.assertIn("_assumptions", prompt)
        self.assertIn("featureName", prompt)


if __name__ == "__main__":
    unittest.main()
