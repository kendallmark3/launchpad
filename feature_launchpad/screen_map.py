"""Stage 3 — Create Screen Map (intent.md Section 8, Stage 3).

The schema for 03-screen-map.json is truncated in the source spec right after
"featureName" (see CLAUDE.md and the truncation note at the end of intent.md).
This stage asks the model to produce a reasonable screen map built around the
one confirmed field, and to record its own schema assumptions in a
"_assumptions" array, rather than the launchpad silently asserting an
undocumented schema as authoritative.
"""

import json

from feature_launchpad.http_client import create_message

PROMPT_TEMPLATE = """You are producing Stage 3 of an automated feature launchpad: a JSON \
screen map for a software feature, based on the normalized intent and UX flow below.

The source specification for this screen map's schema is incomplete — it only confirms \
the document must be valid JSON with a top-level "featureName" string field. Beyond \
that, use your judgment to produce a useful screen map (e.g. a "screens" array with a \
name, purpose, and key components per screen), and list any schema assumptions you made \
in a top-level "_assumptions" array of strings.

Respond with ONLY the JSON document — no markdown code fences, no commentary.

--- NORMALIZED INTENT ---
{normalized_intent}

--- UX FLOW ---
{ux_flow}
"""


def generate(normalized_intent: str, ux_flow: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(normalized_intent=normalized_intent, ux_flow=ux_flow)
    raw = create_message(prompt, max_tokens=4096).strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):]
    return json.loads(raw)
