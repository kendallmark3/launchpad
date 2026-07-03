"""Minimal direct-HTTP client for the Anthropic Messages API.

Per intent.md Section 4 ("Hard Constraints"), the launchpad must call the Anthropic
API directly over HTTP rather than through the SDK, using only the standard library.
"""

import json
import os
import urllib.error
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-5"  # the default named in intent.md Section 5's own example


class AnthropicAPIError(RuntimeError):
    pass


def create_message(prompt: str, *, max_tokens: int = 4096) -> str:
    """Send a single-turn user message and return the concatenated text content."""
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    body = json.dumps(
        {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": API_VERSION,
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AnthropicAPIError(f"Anthropic API returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise AnthropicAPIError(f"Failed to reach the Anthropic API: {exc.reason}") from exc

    if payload.get("stop_reason") == "refusal":
        raise AnthropicAPIError("Anthropic API declined the request (stop_reason: refusal).")

    return "".join(
        block.get("text", "") for block in payload.get("content", []) if block.get("type") == "text"
    )
