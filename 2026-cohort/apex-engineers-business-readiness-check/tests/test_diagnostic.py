"""Unit tests for the Business Readiness Check scoring rules."""

import unittest

from diagnostic import (
    NO,
    NOT_APPLICABLE,
    YES,
    calculate_risk,
    clean_user_text,
    find_priorities,
    generate_report,
)


class DiagnosticTests(unittest.TestCase):
    def test_all_yes_is_zero_percent_low_risk(self):
        answers = {
            "inventory": YES,
            "payments": YES,
            "customers": YES,
            "booking": YES,
        }
        result = calculate_risk(answers)
        self.assertEqual(result.risk_points, 0)
        self.assertEqual(result.applicable_points, 14)
        self.assertEqual(result.risk_percentage, 0.0)
        self.assertEqual(result.risk_level, "Low")

    def test_all_no_is_one_hundred_percent_critical_risk(self):
        answers = {
            "inventory": NO,
            "payments": NO,
            "customers": NO,
            "booking": NO,
        }
        result = calculate_risk(answers)
        self.assertEqual(result.risk_points, 14)
        self.assertEqual(result.risk_percentage, 100.0)
        self.assertEqual(result.risk_level, "Critical")

    def test_not_applicable_is_removed_from_denominator(self):
        answers = {
            "inventory": NO,
            "payments": YES,
            "customers": NO,
            "booking": NOT_APPLICABLE,
        }
        result = calculate_risk(answers)
        self.assertEqual(result.risk_points, 8)
        self.assertEqual(result.applicable_points, 12)
        self.assertEqual(result.risk_percentage, 66.7)
        self.assertEqual(result.risk_level, "High")

    def test_all_not_applicable_returns_no_score(self):
        answers = {
            "inventory": NOT_APPLICABLE,
            "payments": NOT_APPLICABLE,
            "customers": NOT_APPLICABLE,
            "booking": NOT_APPLICABLE,
        }
        result = calculate_risk(answers)
        self.assertIsNone(result.risk_percentage)
        self.assertEqual(result.risk_level, "Not calculated")

    def test_priorities_are_ordered_by_weight(self):
        answers = {
            "inventory": NO,
            "payments": YES,
            "customers": NO,
            "booking": NO,
        }
        priorities = find_priorities(answers)
        self.assertEqual(
            [key for key, _ in priorities],
            ["inventory", "customers", "booking"],
        )

    def test_missing_answer_is_rejected(self):
        answers = {"inventory": YES, "payments": YES, "customers": YES}
        with self.assertRaisesRegex(ValueError, "Missing answers"):
            calculate_risk(answers)

    def test_invalid_answer_is_rejected(self):
        answers = {
            "inventory": "Maybe",
            "payments": YES,
            "customers": YES,
            "booking": YES,
        }
        with self.assertRaisesRegex(ValueError, "Invalid answers"):
            calculate_risk(answers)

    def test_report_matches_result_and_priority(self):
        answers = {
            "inventory": NO,
            "payments": YES,
            "customers": NO,
            "booking": NOT_APPLICABLE,
        }
        result = calculate_risk(answers)
        report = generate_report(answers, result, business_name="Example Store")
        self.assertIn("Overall risk: 66.7% (High)", report)
        self.assertIn(
            "1. Prioritize POS and online inventory synchronization.", report
        )
        self.assertIn("Business name: Example Store", report)
        self.assertIn("not a formal security", report)

    def test_optional_report_text_is_normalized_and_limited(self):
        unsafe = "  Example\nStore\t" + "x" * 100
        cleaned = clean_user_text(unsafe, max_length=20)
        self.assertEqual(cleaned, "Example Store xxxxxx")
        self.assertEqual(len(cleaned), 20)


if __name__ == "__main__":
    unittest.main()
