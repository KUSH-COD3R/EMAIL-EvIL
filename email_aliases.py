#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_LABELS = ["shopping", "newsletters", "travel", "projects", "banking"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def generate_aliases(email: str, labels: list[str] | None = None) -> list[str]:
    """Return a list of plus-address aliases for a valid email address."""
    if labels is None:
        labels = DEFAULT_LABELS.copy()

    if not isinstance(email, str):
        raise ValueError("Email address must be a string.")

    normalized = email.strip()
    if not normalized or not EMAIL_RE.fullmatch(normalized):
        raise ValueError("Please provide a valid email address containing '@' and a domain.")

    local_part, domain = normalized.split("@", 1)
    clean_labels = []
    for label in labels:
        if label is None:
            continue
        cleaned = str(label).strip().lower()
        if cleaned and re.fullmatch(r"[a-z0-9._-]+", cleaned):
            clean_labels.append(cleaned)

    if not clean_labels:
        clean_labels = DEFAULT_LABELS.copy()

    return [f"{local_part}+{label}@{domain}" for label in clean_labels]


def _parse_labels(raw_labels: list[str] | None, comma_labels: str | None) -> list[str]:
    parsed: list[str] = []
    if raw_labels:
        parsed.extend(raw_labels)
    if comma_labels:
        parsed.extend(part.strip() for part in comma_labels.split(",") if part.strip())
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate plus-address email aliases for inbox organization."
    )
    parser.add_argument("email", nargs="?", help="Base email address to generate aliases for.")
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Alias label. Repeat the option for multiple labels.",
    )
    parser.add_argument(
        "--labels",
        help="Comma-separated alias labels, e.g. shopping,travel,newsletters.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for the generated aliases.",
    )
    parser.add_argument(
        "--output",
        help="Optional file path to write the generated aliases to.",
    )
    args = parser.parse_args(argv)

    email_value = args.email or input("Enter your email: ").strip()
    try:
        alias_list = generate_aliases(email_value, _parse_labels(args.label, args.labels))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(alias_list, indent=2) if args.format == "json" else "\n".join(alias_list)
    if args.format == "text":
        rendered = "Generated aliases:\n" + rendered if alias_list else "Generated aliases:\n"

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
