import unittest

from email_aliases import DEFAULT_LABELS, generate_aliases, resolve_labels, validate_email


class ValidateEmailTests(unittest.TestCase):
    def test_strips_surrounding_whitespace(self):
        self.assertEqual(validate_email("  alex@example.com  "), ("alex", "example.com"))

    def test_rejects_missing_at_sign(self):
        with self.assertRaisesRegex(ValueError, "containing '@'"):
            validate_email("alex.example.com")

    def test_rejects_missing_local_part(self):
        with self.assertRaisesRegex(ValueError, "valid email address with a domain"):
            validate_email("@example.com")

    def test_rejects_missing_domain_or_dot(self):
        for email in ("alex@", "alex@example"):
            with self.subTest(email=email), self.assertRaises(ValueError):
                validate_email(email)


class GenerateAliasesTests(unittest.TestCase):
    def test_generates_default_aliases(self):
        aliases = generate_aliases("alex@example.com")
        self.assertEqual(
            aliases,
            [
                "alex+shopping@example.com",
                "alex+newsletters@example.com",
                "alex+travel@example.com",
                "alex+projects@example.com",
                "alex+banking@example.com",
            ],
        )

    def test_normalizes_and_deduplicates_custom_labels(self):
        aliases = generate_aliases("alex@example.com", [" +Work ", "work", "TRAVEL"])
        self.assertEqual(
            aliases,
            ["alex+work@example.com", "alex+travel@example.com"],
        )

    def test_empty_labels_fall_back_to_defaults(self):
        self.assertEqual(generate_aliases("alex@example.com", ["", " "]), generate_aliases("alex@example.com"))

    def test_custom_labels_keep_order(self):
        self.assertEqual(
            generate_aliases("alex@example.com", ["receipts", "events"]),
            ["alex+receipts@example.com", "alex+events@example.com"],
        )


class ResolveLabelsTests(unittest.TestCase):
    def test_default_labels(self):
        args = type("Args", (), {"preset": None, "labels": None})()
        self.assertEqual(resolve_labels(args), DEFAULT_LABELS)

    def test_preset_labels(self):
        args = type("Args", (), {"preset": "minimal", "labels": None})()
        self.assertEqual(resolve_labels(args), ["shopping", "travel", "banking"])

    def test_custom_labels(self):
        args = type("Args", (), {"preset": None, "labels": ["Receipts"]})()
        self.assertEqual(resolve_labels(args), ["receipts"])


if __name__ == "__main__":
    unittest.main()
