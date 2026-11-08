#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes.

This is a simple Python CLI that works on Termux, Linux, and other Unix-like systems.
It does not contact any network services.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from io import StringIO
from pathlib import Path
from typing import Sequence, TextIO

DEFAULT_LABELS = ["shopping", "newsletters", "travel", "projects", "banking"]

PRESET_LABELS = {
    "default": DEFAULT_LABELS.copy(),
    "minimal": ["shopping", "travel", "banking"],
    "personal": ["work", "family", "shopping", "travel"],
    "work": ["work", "team", "clients", "billing", "security"],
}

TERMINAL_BANNER = (
    "      .--------------------------------------.\n"
    "     /   EMAIL-EvIL | Inbox alias generator   \\\n"
    "    |   .----.       One inbox, many lanes    |\n"
    "    |  / .--. \\      Keep your inbox tidy     |\n"
    "     \\ '----'________________________________/\n"
)


def _clean_label(label: str) -> str:
    """Return a sanitized label."""
    cleaned = label.strip().lower().lstrip("+")
    return cleaned.strip()


def _normalize_labels(labels: Sequence[str] | None) -> list[str]:
    """Return a deduplicated list of alias labels."""
    if labels is None:
        return DEFAULT_LABELS.copy()

    normalized: list[str] = []
    seen: set[str] = set()

    for label in labels:
        cleaned = _clean_label(label)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            normalized.append(cleaned)

    return normalized or DEFAULT_LABELS.copy()


def validate_email(email: str) -> tuple[str, str]:
    """Validate an email address and split it into local/domain parts."""
    address = (email or "").strip()
    if not address:
        raise ValueError("Please provide an email address.")

    if "@" not in address:
        raise ValueError("Please provide an email address containing '@'.")

    if any(ch.isspace() for ch in address):
        raise ValueError("Email addresses must not contain spaces.")

    local_part, domain = address.rsplit("@", 1)
    if not local_part or not domain:
        raise ValueError("Please provide a valid email address.")

    if "." not in domain:
        raise ValueError("Please provide an email address with a valid-looking domain.")

    if local_part.startswith(".") or local_part.endswith("."):
        raise ValueError("Email local-part cannot start or end with a period.")

    if domain.startswith(".") or domain.endswith("."):
        raise ValueError("Email domain cannot start or end with a period.")

    return local_part, domain


def generate_aliases(email: str, labels: Sequence[str] | None = None) -> list[str]:
    """Generate plus-address aliases for an email."""
    local_part, domain = validate_email(email)
    normalized = _normalize_labels(labels)
    return [f"{local_part}+{label}@{domain}" for label in normalized]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address aliases to organize your inbox.",
        epilog="Example: email-evil alex@example.com --labels receipts travel --format json",
    )
    parser.add_argument(
        "email",
        nargs="?",
        help="Email address to generate aliases for. If omitted, you will be prompted.",
    )
    label_group = parser.add_mutually_exclusive_group()
    label_group.add_argument(
        "-l",
        "--labels",
        nargs="+",
        help="Custom labels, e.g. --labels shopping travel receipts",
    )
    label_group.add_argument(
        "--preset",
        choices=sorted(PRESET_LABELS),
        help="Use a built-in label set.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("text", "terminal", "json", "csv"),
        default="text",
        help="Output format: plain text, terminal, JSON, or CSV.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write output to a file instead of the terminal.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Hide headings and ASCII decoration.",
    )
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    """Resolve labels from CLI args."""
    if getattr(args, "preset", None):
        return PRESET_LABELS[args.preset].copy()
    if getattr(args, "labels", None) is not None:
        return _normalize_labels(args.labels)
    return DEFAULT_LABELS.copy()


def render_aliases(aliases: Sequence[str], output_format: str = "text", quiet: bool = False) -> str:
    """Format aliases as text, JSON, CSV, or terminal output."""
    aliases = list(aliases)

    if output_format == "json":
        return json.dumps(aliases, indent=2) + "\n"

    if output_format == "csv":
        buffer = StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["alias"])
        writer.writerows((alias,) for alias in aliases)
        return buffer.getvalue()

    if output_format == "terminal":
        if quiet:
            return "\n".join(aliases) + "\n"

        heading = f"  YOUR ALIASES ({len(aliases)})"
        width = max([len(heading), *(len(alias) + 4 for alias in aliases)], default=len(heading))
        border = "+" + "-" * width + "+"
        rows = [border, "|" + heading.ljust(width) + "|", border]
        rows.extend("|  " + alias.ljust(width - 4) + "  |" for alias in aliases)
        rows.append(border)
        return TERMINAL_BANNER + "\n".join(rows) + "\n"

    lines = list(aliases)
    if not quiet:
        lines.insert(0, "Generated aliases:")
    return "\n".join(lines) + "\n"


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the CLI and return an exit code."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.email is not None:
            email = args.email
        else:
            if stdin.isatty():
                email = input("Enter your email: ").strip()
            else:
                email = stdin.readline().strip()
                if not email:
                    raise ValueError("No email address was provided.")

        aliases = generate_aliases(email, resolve_labels(args))
        rendered = render_aliases(aliases, args.format, args.quiet)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        else:
            stdout.write(rendered)

    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
