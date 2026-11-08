#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

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
    "default": DEFAULT_LABELS,
    "minimal": ["shopping", "travel", "banking"],
    "personal": ["work", "family", "shopping", "travel"],
}
TERMINAL_BANNER = (
    "      .--------------------------------------.\n"
    "     /   EMAIL-EvIL | Inbox alias generator   \\\n"
    "    |   .----.       One inbox, many lanes    |\n"
    "    |  / .--. \\      Keep your inbox tidy     |\n"
    "     \\ '----'________________________________/\n"
)


def _normalize_labels(labels: Sequence[str] | None) -> list[str]:
    """Return a clean, deduplicated list of alias labels."""
    if labels is None:
        return DEFAULT_LABELS.copy()

    normalized: list[str] = []
    seen: set[str] = set()
    for label in labels:
        cleaned = label.strip().lower().lstrip("+")
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            normalized.append(cleaned)

    return normalized or DEFAULT_LABELS.copy()


def validate_email(email: str) -> tuple[str, str]:
    """Perform basic validation and split an email into local and domain parts."""
    address = email.strip()
    if not address or "@" not in address:
        raise ValueError("Please provide an email address containing '@'.")

    local_part, domain = address.rsplit("@", 1)
    if not local_part or not domain or "." not in domain:
        raise ValueError("Please provide an email address with a valid-looking domain.")
    if any(character.isspace() for character in address):
        raise ValueError("Email addresses must not contain spaces.")

    return local_part, domain


def generate_aliases(email: str, labels: Sequence[str] | None = None) -> list[str]:
    """Return plus-address aliases for an email address."""
    local_part, domain = validate_email(email)
    return [f"{local_part}+{label}@{domain}" for label in _normalize_labels(labels)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address aliases to organize your inbox.",
        epilog="Example: email-evil alex@example.com --labels receipts travel --format json",
    )
    parser.add_argument("email", nargs="?", help="Email address to create aliases for; prompts if omitted.")
    label_options = parser.add_mutually_exclusive_group()
    label_options.add_argument(
        "-l", "--labels", nargs="+", help="Custom labels, for example: --labels shopping receipts travel"
    )
    label_options.add_argument("--preset", choices=sorted(PRESET_LABELS), help="Use a built-in label set.")
    parser.add_argument(
        "-f", "--format", choices=("text", "terminal", "json", "csv"), default="text",
        help="Output format: plain text, ASCII terminal view, JSON, or CSV (default: text).",
    )
    parser.add_argument("-o", "--output", help="Write output to a file instead of the terminal.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Omit headings and artwork from output.")
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    """Resolve labels selected by CLI arguments."""
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    if args.labels is not None:
        return _normalize_labels(args.labels)
    return DEFAULT_LABELS.copy()


def render_aliases(aliases: Sequence[str], output_format: str = "text", quiet: bool = False) -> str:
    """Format aliases as readable text, an ASCII terminal view, JSON, or CSV."""
    if output_format == "json":
        return json.dumps(list(aliases), indent=2) + "\n"
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


def main(argv: Sequence[str] | None = None, *, stdin: TextIO | None = None, stdout: TextIO | None = None,
         stderr: TextIO | None = None) -> int:
    """Run the command-line interface; return an exit status for easy testing."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        email = args.email if args.email is not None else input("Enter your email: ").strip()
        aliases = generate_aliases(email, resolve_labels(args))
        rendered = render_aliases(aliases, args.format, args.quiet)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8", newline="")
        else:
            stdout.write(rendered)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
