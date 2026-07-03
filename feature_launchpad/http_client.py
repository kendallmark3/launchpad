"""Minimal direct-HTTP client for the Anthropic Messages API.

Per intent.md Section 4 ("Hard Constraints"), the launchpad must call the Anthropic
API directly over HTTP rather than through the SDK, using only the standard library.
"""

import json
import os
import urllib.error
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
MODELS_URL = "https://api.anthropic.com/v1/models"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-5"  # the default named in intent.md Section 5's own example


class AnthropicAPIError(RuntimeError):
    pass


def check_reachability(*, timeout: float = 5.0) -> bool:
    """Return True if the Anthropic API is reachable with the configured key.

    Uses GET /v1/models rather than /v1/messages so a status check never spends
    tokens. Returns False (rather than raising) for any connectivity, auth, or
    HTTP-level failure — callers only need reachable/unreachable, not the reason.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return False

    request = urllib.request.Request(
        MODELS_URL,
        method="GET",
        headers={"x-api-key": api_key, "anthropic-version": API_VERSION},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return False


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
