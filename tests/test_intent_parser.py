import tempfile
import unittest
from pathlib import Path

from feature_launchpad import intent_parser

SAMPLE = """# Feature Intent

## Business Goal

Increase self-serve upgrade conversions.

## User Personas

Growth PM, Support Rep.

## Required Screens

Billing dashboard, Plan comparison.

## Acceptance Criteria

User can upgrade without contacting support.
"""


class NormalizeTests(unittest.TestCase):
    def test_extracts_feature_name_from_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "customer-billing.intent.md"
            path.write_text(SAMPLE, encoding="utf-8")
            result = intent_parser.normalize(path)
        self.assertEqual(result.feature_name, "customer-billing")

    def test_preserves_verbatim_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.intent.md"
            path.write_text(SAMPLE, encoding="utf-8")
            result = intent_parser.normalize(path)
        self.assertIn("Increase self-serve upgrade conversions.", result.content)

    def test_flags_missing_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.intent.md"
            path.write_text(SAMPLE, encoding="utf-8")
            result = intent_parser.normalize(path)
        self.assertIn("User Journey", result.missing_sections)
        self.assertIn("Out of Scope", result.missing_sections)
        self.assertNotIn("Business Goal", result.missing_sections)

    def test_full_sample_intent_file_has_no_missing_required_sections(self):
        sample_path = Path(__file__).resolve().parent.parent / "intents" / "customer-billing.intent.md"
        result = intent_parser.normalize(sample_path)
        self.assertEqual(result.missing_sections, [])


if __name__ == "__main__":
    unittest.main()
