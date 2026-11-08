"""Command-line interface for EMAIL-EvIL."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .aliases import generate_aliases


def _parse_labels(raw_labels: list[str] | None, comma_labels: str | None) -> list[str]:
    parsed: list[str] = []
    if raw_labels:
        parsed.extend(raw_labels)
    if comma_labels:
        parsed.extend(part.strip() for part in comma_labels.split(",") if part.strip())
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate plus-address email aliases for inbox organization.",
    )
    parser.add_argument("email", nargs="?", help="Base email address used to generate aliases.")
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Alias label. Repeat the option to add multiple labels.",
    )
    parser.add_argument(
        "--labels",
        help="Comma-separated labels such as work,travel,finance.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for the generated aliases.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path to write the aliases to.",
    )
    args = parser.parse_args(argv)

    email_value = args.email or input("Enter your email: ").strip()
    try:
        aliases = generate_aliases(email_value, _parse_labels(args.label, args.labels))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        rendered = json.dumps(aliases, indent=2)
    else:
        rendered = "Generated aliases:\n" + "\n".join(aliases)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
