"""Stage 2 — Reason About UX Flow (intent.md Section 8, Stage 2).

Calls the Anthropic API directly to produce 02-ux-flow.md from the normalized intent.
"""

from feature_launchpad.http_client import create_message

PROMPT_TEMPLATE = """You are producing Stage 2 of an automated feature launchpad: the UX \
flow for a software feature, based on the normalized feature intent below.

Write the UX flow as markdown. It MUST cover, as headed sections:
- User entry point
- Step-by-step journey
- Decision points
- Alternate paths
- Empty states
- Error states
- Confirmation states
- Success states
- Required screens
- Screen transitions
- User permissions or roles

Base your answer only on the intent below. Where the intent doesn't specify something, \
say so explicitly rather than inventing unstated business rules.

--- NORMALIZED INTENT ---
{normalized_intent}
"""


def generate(normalized_intent: str) -> str:
    prompt = PROMPT_TEMPLATE.format(normalized_intent=normalized_intent)
    return create_message(prompt, max_tokens=4096)
