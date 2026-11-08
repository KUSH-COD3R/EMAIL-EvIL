#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

import argparse
import csv
import json
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
    return max(20, shutil.get_terminal_size((80, 24)).columns)


def _render_terminal_banner() -> str:
    """Plain ASCII art, with no trailing backslashes or terminal color codes."""
    width = min(42, _terminal_width())
    inside = width - 2
    lines = (
        "  ^     ^ ",
        " ( o   o )",
        "  |  ^  |  EMAIL-EvIL",
        "  |  v  |  by KUSH-COD3R",
        "   one inbox, many lanes",
    )
    border = "+" + "-" * inside + "+"
    body = ["|" + line[:inside].center(inside) + "|" for line in lines]
    return "\n".join((border, *body, border, ""))


def _render_startup_banner() -> str:
    return _render_terminal_banner()


def _normalize_labels(labels: Sequence[str] | None) -> list[str]:
    if labels is None:
        return DEFAULT_LABELS.copy()
    result: list[str] = []
    seen: set[str] = set()
    for label in labels:
        cleaned = label.strip().lower().lstrip("+")
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)
    return result or DEFAULT_LABELS.copy()


def validate_email(email: str) -> tuple[str, str]:
    address = email.strip()
    if not address or "@" not in address:
        raise ValueError("Please provide an email address containing '@'.")
    local, domain = address.rsplit("@", 1)
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise ValueError("Please provide an email address with a valid-looking domain.")
    if any(char.isspace() for char in address):
        raise ValueError("Email addresses must not contain spaces.")
    return local, domain


def generate_aliases(email: str, labels: Sequence[str] | None = None) -> list[str]:
    local, domain = validate_email(email)
    return [f"{local}+{label}@{domain}" for label in _normalize_labels(labels)]


def generate_batch_csv(source: TextIO, labels: Sequence[str] | None = None) -> str:
    reader = csv.DictReader(source)
    if not reader.fieldnames:
        raise ValueError("Batch CSV must include an 'email' header.")
    field = next((name for name in reader.fieldnames if name and name.strip().lower() == "email"), None)
    if field is None:
        raise ValueError("Batch CSV must include an 'email' column.")
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["email", "alias"])
    for row in reader:
        email = (row.get(field) or "").strip()
        if not email:
            continue
        try:
            aliases = generate_aliases(email, labels)
        except ValueError as exc:
            raise ValueError(f"Invalid email on CSV line {reader.line_num}: {exc}") from exc
        writer.writerows((email, alias) for alias in aliases)
    return output.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate plus-address aliases for your inbox.")
    parser.add_argument("email", nargs="?", help="Email address; prompts if omitted.")
    parser.add_argument("--batch-csv", metavar="PATH", help="Read emails from a CSV with an email column.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--labels", nargs="+", help="Custom alias labels.")
    group.add_argument("--preset", choices=sorted(PRESET_LABELS), help="Use a built-in label set.")
    parser.add_argument("-f", "--format", choices=("terminal", "text", "json", "csv"), default="terminal")
    parser.add_argument("-o", "--output", help="Write output to a file.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Hide banner and headings.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    return _normalize_labels(args.labels)


def render_aliases(aliases: Sequence[str], output_format: str = "text", quiet: bool = False) -> str:
    if output_format == "json":
        return json.dumps(list(aliases), indent=2) + "\n"
    if output_format == "csv":
        output = StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(["alias"])
        writer.writerows((alias,) for alias in aliases)
        return output.getvalue()
    if output_format == "terminal":
        if quiet:
            return "\n".join(aliases) + "\n"
        heading = f"YOUR ALIASES ({len(aliases)})"
        width = max(20, min(_terminal_width() - 2, 60))
        inside = width - 2
        border = "+" + "-" * inside + "+"
        rows = [border, "|" + heading[:inside].center(inside) + "|", border]
        for alias in aliases:
            parts = textwrap.wrap(alias, width=max(1, inside - 4), break_long_words=True)
            rows.extend("|  " + part.ljust(inside - 4) + "  |" for part in parts)
        rows.append(border)
        return _render_terminal_banner() + "\n".join(rows) + "\n"
    text = list(aliases)
    if not quiet:
        text.insert(0, "Generated aliases:")
    return "\n".join(text) + "\n"


def main(argv: Sequence[str] | None = None, *, stdin: TextIO | None = None,
         stdout: TextIO | None = None, stderr: TextIO | None = None) -> int:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = build_parser().parse_args(argv)
    try:
        labels = resolve_labels(args)
        if args.batch_csv:
            if args.email is not None:
                raise ValueError("Do not provide an email argument with --batch-csv.")
            with Path(args.batch_csv).open(encoding="utf-8", newline="") as source:
                rendered = generate_batch_csv(source, labels)
        else:
            if args.email is None:
                if not args.quiet:
                    stdout.write(_render_startup_banner())
                stdout.write("Enter your email: ")
                email = stdin.readline().strip()
            else:
                email = args.email
            rendered = render_aliases(generate_aliases(email, labels), args.format, args.quiet)
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
