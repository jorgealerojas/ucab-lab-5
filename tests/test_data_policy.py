import unittest

from app.data_policy import apply_policy, checksum, validate_record


class DataPolicyTests(unittest.TestCase):
    def test_accepts_valid_record(self):
        result = validate_record(
            {"id": "a", "category": "temp", "value": 20.5, "timestamp": "2026-01-01"}
        )
        self.assertTrue(result.accepted)
        self.assertEqual((), result.reasons)

    def test_rejects_nested_restricted_field(self):
        result = validate_record(
            {
                "id": "a",
                "category": "temp",
                "value": 20,
                "timestamp": "2026-01-01",
                "contact": {"telefono": "000"},
            }
        )
        self.assertFalse(result.accepted)
        self.assertIn("telefono", result.reasons[0])

    def test_rejects_missing_and_invalid_fields(self):
        result = validate_record({"id": "", "value": "high"})
        self.assertFalse(result.accepted)
        self.assertEqual(3, len(result.reasons))

    def test_rejects_duplicate_identifier(self):
        record = {"id": "a", "category": "temp", "value": 20, "timestamp": "2026"}
        accepted, rejected = apply_policy([record, dict(record)])
        self.assertEqual(1, len(accepted))
        self.assertEqual(["id duplicado"], rejected[0]["reasons"])

    def test_requires_list_document(self):
        with self.assertRaisesRegex(ValueError, "lista JSON"):
            apply_policy({"id": "a"})

    def test_checksum_is_independent_of_key_order(self):
        self.assertEqual(checksum({"a": 1, "b": 2}), checksum({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
