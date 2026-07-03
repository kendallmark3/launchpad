import io
import json
import os
import unittest
import urllib.error
from unittest import mock

from feature_launchpad import http_client


def _fake_response(payload: dict):
    response = mock.MagicMock()
    response.read.return_value = json.dumps(payload).encode("utf-8")
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class CreateMessageTests(unittest.TestCase):
    def test_returns_concatenated_text_blocks(self):
        payload = {
            "content": [
                {"type": "text", "text": "Hello, "},
                {"type": "text", "text": "world."},
            ]
        }
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=_fake_response(payload)
        ):
            result = http_client.create_message("a prompt")

        self.assertEqual(result, "Hello, world.")

    def test_ignores_non_text_content_blocks(self):
        payload = {"content": [{"type": "tool_use", "text": "ignored"}, {"type": "text", "text": "kept"}]}
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=_fake_response(payload)
        ):
            result = http_client.create_message("a prompt")

        self.assertEqual(result, "kept")

    def test_sends_api_key_and_default_model(self):
        payload = {"content": [{"type": "text", "text": "ok"}]}
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=_fake_response(payload)
        ) as urlopen:
            http_client.create_message("a prompt", max_tokens=123)

        request = urlopen.call_args[0][0]
        self.assertEqual(request.get_header("X-api-key"), "test-key")
        self.assertEqual(request.get_header("Anthropic-version"), http_client.API_VERSION)
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["model"], http_client.DEFAULT_MODEL)
        self.assertEqual(body["max_tokens"], 123)
        self.assertEqual(body["messages"], [{"role": "user", "content": "a prompt"}])

    def test_uses_anthropic_model_env_var_when_set(self):
        payload = {"content": [{"type": "text", "text": "ok"}]}
        env = {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MODEL": "claude-custom-model"}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=_fake_response(payload)
        ) as urlopen:
            http_client.create_message("a prompt")

        body = json.loads(urlopen.call_args[0][0].data.decode("utf-8"))
        self.assertEqual(body["model"], "claude-custom-model")

    def test_raises_on_refusal_stop_reason(self):
        payload = {"stop_reason": "refusal", "content": []}
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=_fake_response(payload)
        ):
            with self.assertRaises(http_client.AnthropicAPIError) as ctx:
                http_client.create_message("a prompt")
        self.assertIn("refusal", str(ctx.exception))

    def test_raises_on_http_error_with_response_detail(self):
        http_error = urllib.error.HTTPError(
            url=http_client.API_URL,
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(b'{"error": "rate limited"}'),
        )
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", side_effect=http_error
        ):
            with self.assertRaises(http_client.AnthropicAPIError) as ctx:
                http_client.create_message("a prompt")
        self.assertIn("429", str(ctx.exception))
        self.assertIn("rate limited", str(ctx.exception))

    def test_raises_on_url_error(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("connection refused")
        ):
            with self.assertRaises(http_client.AnthropicAPIError) as ctx:
                http_client.create_message("a prompt")
        self.assertIn("connection refused", str(ctx.exception))

    def test_raises_key_error_when_api_key_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                http_client.create_message("a prompt")


class CheckReachabilityTests(unittest.TestCase):
    def test_returns_false_when_api_key_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch("urllib.request.urlopen") as urlopen:
            self.assertFalse(http_client.check_reachability())
        urlopen.assert_not_called()

    def test_returns_true_on_200(self):
        response = mock.MagicMock()
        response.status = 200
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", return_value=response
        ) as urlopen:
            self.assertTrue(http_client.check_reachability())

        request = urlopen.call_args[0][0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url, http_client.MODELS_URL)
        self.assertEqual(request.get_header("X-api-key"), "test-key")

    def test_returns_false_on_http_error(self):
        http_error = urllib.error.HTTPError(
            url=http_client.MODELS_URL, code=401, msg="Unauthorized", hdrs=None, fp=io.BytesIO(b"")
        )
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "bad-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", side_effect=http_error
        ):
            self.assertFalse(http_client.check_reachability())

    def test_returns_false_on_url_error(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), mock.patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("connection refused")
        ):
            self.assertFalse(http_client.check_reachability())


if __name__ == "__main__":
    unittest.main()
