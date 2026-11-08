import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from email_aliases import (
    DEFAULT_LABELS,
    generate_aliases,
    main,
    render_aliases,
    resolve_labels,
    validate_email,
)


class ValidateEmailTests(unittest.TestCase):
    def test_strips_surrounding_whitespace(self):
        self.assertEqual(validate_email("  alex@example.com  "), ("alex", "example.com"))

    def test_rejects_missing_at_sign(self):
        with self.assertRaisesRegex(ValueError, "containing '@'"):
            validate_email("alex.example.com")

    def test_rejects_empty_email(self):
        with self.assertRaisesRegex(ValueError, "Please provide an email address"):
            validate_email("")

    def test_rejects_missing_local_part_or_domain(self):
        for email in ("@example.com", "alex@", "alex@example"):
            with self.subTest(email=email), self.assertRaises(ValueError):
                validate_email(email)

    def test_rejects_internal_spaces(self):
        with self.assertRaisesRegex(ValueError, "must not contain spaces"):
            validate_email("alex smith@example.com")

    def test_rejects_dots_at_edges(self):
        with self.assertRaisesRegex(ValueError, "cannot start or end with a period"):
            validate_email(".alex@example.com")


class GenerateAliasesTests(unittest.TestCase):
    def test_generates_default_aliases(self):
        self.assertEqual(
            generate_aliases("alex@example.com"),
            [
                "alex+shopping@example.com",
                "alex+newsletters@example.com",
                "alex+travel@example.com",
                "alex+projects@example.com",
                "alex+banking@example.com",
            ],
        )

    def test_normalizes_and_deduplicates_custom_labels(self):
        self.assertEqual(
            generate_aliases("alex@example.com", [" +Work ", "work", "TRAVEL"]),
            ["alex+work@example.com", "alex+travel@example.com"],
        )

    def test_empty_labels_fall_back_to_defaults(self):
        self.assertEqual(generate_aliases("alex@example.com", ["", " "]), generate_aliases("alex@example.com"))

    def test_presets_are_copied(self):
        args = type("Args", (), {"preset": "minimal", "labels": None})()
        first = resolve_labels(args)
        first.append("mutated")
        self.assertEqual(resolve_labels(args), ["shopping", "travel", "banking"])

    def test_resolves_custom_and_default_labels(self):
        self.assertEqual(resolve_labels(type("Args", (), {"preset": None, "labels": None})()), DEFAULT_LABELS)
        self.assertEqual(
            resolve_labels(type("Args", (), {"preset": None, "labels": ["Receipts"]})()),
            ["receipts"],
        )


class OutputFormatTests(unittest.TestCase):
    aliases = ["alex+receipts@example.com", "alex+travel@example.com"]

    def test_json_output(self):
        self.assertEqual(json.loads(render_aliases(self.aliases, "json")), self.aliases)

    def test_csv_output_has_header(self):
        rows = list(csv.reader(io.StringIO(render_aliases(self.aliases, "csv"))))
        self.assertEqual(rows, [["alias"], *[[alias] for alias in self.aliases]])

    def test_quiet_text_omits_heading(self):
        self.assertEqual(render_aliases(self.aliases, quiet=True), "\n".join(self.aliases) + "\n")

    def test_terminal_output_has_ascii_banner_and_boxed_aliases(self):
        rendered = render_aliases(self.aliases, "terminal")
        self.assertIn("EMAIL-EvIL | Inbox alias generator", rendered)
        self.assertIn("YOUR ALIASES (2)", rendered)
        self.assertIn("|  alex+receipts@example.com  |", rendered)
        self.assertIn("|  alex+travel@example.com   |", rendered)

    def test_quiet_terminal_output_omits_art_and_box(self):
        self.assertEqual(render_aliases(self.aliases, "terminal", quiet=True), "\n".join(self.aliases) + "\n")


class CliTests(unittest.TestCase):
    def test_custom_labels_and_json_output(self):
        output = io.StringIO()
        status = main(["alex@example.com", "--labels", "receipts", "travel", "--format", "json"], stdout=output)
        self.assertEqual(status, 0)
        self.assertEqual(
            json.loads(output.getvalue()),
            ["alex+receipts@example.com", "alex+travel@example.com"],
        )

    def test_preset_and_quiet_output(self):
        output = io.StringIO()
        status = main(["alex@example.com", "--preset", "minimal", "--quiet"], stdout=output)
        self.assertEqual(status, 0)
        self.assertNotIn("Generated aliases:", output.getvalue())
        self.assertEqual(len(output.getvalue().splitlines()), 3)

    def test_terminal_format_option(self):
        output = io.StringIO()
        status = main(["alex@example.com", "--labels", "receipts", "--format", "terminal"], stdout=output)
        self.assertEqual(status, 0)
        self.assertIn("EMAIL-EvIL", output.getvalue())
        self.assertIn("alex+receipts@example.com", output.getvalue())

    def test_writes_output_file(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "aliases.csv"
            status = main(["alex@example.com", "--format", "csv", "--output", str(destination)])
            self.assertEqual(status, 0)
            self.assertEqual(list(csv.reader(destination.open(encoding="utf-8")))[0], ["alias"])

    def test_invalid_email_returns_error_status(self):
        output, errors = io.StringIO(), io.StringIO()
        status = main(["not-an-email"], stdout=output, stderr=errors)
        self.assertEqual(status, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("Error:", errors.getvalue())

    def test_reads_email_from_stdin_when_argument_missing(self):
        output = io.StringIO()
        status = main([], stdout=output, stdin=io.StringIO("demo@example.com\n"))
        self.assertEqual(status, 0)
        self.assertIn("demo+shopping@example.com", output.getvalue())


if __name__ == "__main__":
    unittest.main()
