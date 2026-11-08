#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
import textwrap
from io import StringIO
from pathlib import Path
from typing import Sequence, TextIO

__version__ = "1.0.0"

DEFAULT_LABELS = ["shopping", "newsletters", "travel", "projects", "banking"]
PRESET_LABELS = {
    "default": DEFAULT_LABELS,
    "minimal": ["shopping", "travel", "banking"],
    "personal": ["work", "family", "shopping", "travel"],
}


def _terminal_width() -> int:
    """Return a safe terminal width, including when output is redirected."""
    return max(10, shutil.get_terminal_size((80, 24)).columns)


def _banner_color(text: str, color_code: str) -> str:
    """Add color only for interactive terminals; respect NO_COLOR."""
    if sys.stdout.isatty() and "NO_COLOR" not in os.environ:
        return f"\033[{color_code}m{text}\033[0m"
    return text


def _render_terminal_banner() -> str:
    """Render a compact, slightly sinister ASCII banner for Termux/mobile."""
    width = min(46, max(18, _terminal_width()))
    inner = width - 2
    art = (
        "  .-''''-.  ",
        " /  .--.  \\ ",
        "|  (o)(o)  |",
        "|   \\__/   |",
        " \\  ____  /",
        "  '------'  ",
    )
    title = ("EMAIL-EvIL", "by KUSH-COD3R", "one inbox, many lanes")
    border = "+" + "-" * inner + "+"
    lines = [border]
    lines.extend("|" + row[:inner].center(inner) + "|" for row in art)
    lines.append("|" + " " * inner + "|")
    lines.extend("|" + row[:inner].center(inner) + "|" for row in title)
    lines.append(border)
    return _banner_color("\n".join(lines) + "\n", "1;31")


def _render_startup_banner() -> str:
    """Return the startup splash with red accents on supported terminals."""
    return _render_terminal_banner()


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


def generate_batch_csv(source: TextIO, labels: Sequence[str] | None = None) -> str:
    """Generate a CSV containing each valid input email and its aliases.

    The source CSV must have a column named ``email`` (case-insensitive).
    Blank email rows are ignored. Invalid nonblank addresses stop the batch with
    a line-numbered error, so callers never receive a silently partial result.
    """
    reader = csv.DictReader(source)
    if reader.fieldnames is None:
        raise ValueError("Batch CSV must include an 'email' header.")

    email_field = next(
        (field for field in reader.fieldnames if field and field.strip().lower() == "email"),
        None,
    )
    if email_field is None:
        raise ValueError("Batch CSV must include an 'email' column.")

    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["email", "alias"])
    for row in reader:
        email = row.get(email_field)
        if email is None or not email.strip():
            continue
        email = email.strip()
        try:
            aliases = generate_aliases(email, labels)
        except ValueError as exc:
            raise ValueError(f"Invalid email on CSV line {reader.line_num}: {exc}") from exc
        writer.writerows((email, alias) for alias in aliases)

    return output.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address aliases to organize your inbox.",
        epilog="Example: EMAIL-EvIL.py alex@example.com --labels receipts travel --format json",
    )
    parser.add_argument("email", nargs="?", help="Email address to create aliases for; prompts if omitted.")
    parser.add_argument(
        "--batch-csv",
        metavar="PATH",
        help="Generate aliases for every email in a CSV with an 'email' column; outputs CSV rows.",
    )
    label_options = parser.add_mutually_exclusive_group()
    label_options.add_argument(
        "-l", "--labels", nargs="+", help="Custom labels, for example: --labels shopping receipts travel"
    )
    label_options.add_argument("--preset", choices=sorted(PRESET_LABELS), help="Use a built-in label set.")
    parser.add_argument(
        "-f", "--format", choices=("text", "terminal", "json", "csv"), default="terminal",
        help="Output format: terminal view, plain text, JSON, or CSV (default: terminal).",
    )
    parser.add_argument("-o", "--output", help="Write output to a file instead of the terminal.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Omit headings and artwork from output.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    """Resolve labels selected by CLI arguments."""
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    if args.labels is not None:
        return _normalize_labels(args.labels)
    return DEFAULT_LABELS.copy()


def render_aliases(aliases: Sequence[str], output_format: str = "text", quiet: bool = False) -> str:
    """Format aliases as readable text, a responsive terminal view, JSON, or CSV."""
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
        heading = f"YOUR ALIASES ({len(aliases)})"
        terminal_width = _terminal_width()
        box_width = max(8, min(terminal_width - 2, max(len(heading), 20)))
        content_width = max(1, box_width - 4)
        border = "+" + "-" * box_width + "+"
        rows = [border, "|" + heading[:box_width].center(box_width) + "|", border]
        for alias in aliases:
            wrapped = textwrap.wrap(alias, width=content_width, break_long_words=True, break_on_hyphens=False)
            rows.extend("|  " + part.ljust(content_width) + "  |" for part in wrapped or [""])
        rows.append(border)
        return _render_terminal_banner() + "\n".join(rows) + "\n"

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
        if args.batch_csv:
            if args.email is not None:
                raise ValueError("Do not provide an email argument when using --batch-csv.")
            with Path(args.batch_csv).open(encoding="utf-8", newline="") as batch_file:
                rendered = generate_batch_csv(batch_file, resolve_labels(args))
        else:
            if args.email is not None:
                email = args.email
            else:
                if not args.quiet:
                    stdout.write(_render_startup_banner())
                stdout.write("Enter your email: ")
                email = stdin.readline().strip()
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
