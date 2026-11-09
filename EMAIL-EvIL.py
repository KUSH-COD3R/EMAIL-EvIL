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
    return max(20, shutil.get_terminal_size((80, 24)).columns)


def _paint(text: str, code: str, *, enabled: bool, stream: TextIO | None = None) -> str:
    """Use ANSI colors only for an interactive terminal, respecting NO_COLOR."""
    target = stream or sys.stdout
    if enabled and "NO_COLOR" not in os.environ and getattr(target, "isatty", lambda: False)():
        return f"\033[{code}m{text}\033[0m"
    return text


def _render_banner(color: bool = True, stream: TextIO | None = None) -> str:
    """Render a compact dragon banner sized for mobile terminals."""
    width = min(42, max(24, _terminal_width()))
    inside = width - 2
    dragon = (
        "          /\\  /\\",
        "         //\\\\//\\\\",
        "        (  o  o  )",
        "     ___/   ^^   \\___",
        "    /  /|  /\\  |\\  \\ ",
        "   /__/ |_/  \\_| \\__\\",
        "       /_/    \\_\\",
    )
    title = ("INFERNAL INBOX", "EMAIL-EvIL", "by KUSH-COD3R", "one inbox, many lanes")
    border = "+" + "-" * inside + "+"
    lines = [_paint(border, "1;31", enabled=color, stream=stream)]
    for index, row in enumerate(dragon):
        shade = "1;33" if index < 3 else "31"
        lines.append("|" + _paint(row.center(inside), shade, enabled=color, stream=stream) + "|")
    lines.append("|" + " " * inside + "|")
    for index, label in enumerate(title):
        shade = "1;31" if index < 2 else "1;33"
        lines.append("|" + _paint(label.center(inside), shade, enabled=color, stream=stream) + "|")
    lines.append(_paint(border, "1;31", enabled=color, stream=stream))
    return "\n".join(lines) + "\n"


def _render_command_help(*, color: bool = True, stream: TextIO | None = None) -> str:
    """Show a compact guide to every supported command-line option."""
    heading = _paint("COMMANDS", "1;33", enabled=color, stream=stream)
    commands = (
        "EMAIL                         Generate aliases for one address",
        "-l, --labels LABEL...         Set custom labels",
        "--preset default|minimal|personal",
        "-f, --format terminal|text|json|csv",
        "-o, --output FILE            Save results to a file",
        "--batch-csv FILE             Generate from a CSV email column",
        "-q, --quiet                  Hide banner and headings",
        "--no-color                  Disable terminal colors",
        "--version                   Show version",
        "-h, --help                  Show full help and exit",
    )
    return heading + "\n" + "\n".join(commands) + "\n\n"


def _normalize_labels(labels: Sequence[str] | None) -> list[str]:
    if labels is None:
        return DEFAULT_LABELS.copy()
    result: list[str] = []
    seen: set[str] = set()
    for label in labels:
        cleaned = label.strip().lower().lstrip("+")
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result or DEFAULT_LABELS.copy()


def validate_email(email: str) -> tuple[str, str]:
    address = email.strip()
    if not address or "@" not in address:
        raise ValueError("Please provide an email address containing '@'.")
    local, domain = address.rsplit("@", 1)
    if not local or "." not in domain:
        raise ValueError("Please provide an email address with a valid-looking domain.")
    if any(char.isspace() for char in address):
        raise ValueError("Email addresses must not contain spaces.")
    return local, domain


def generate_aliases(email: str, labels: Sequence[str] | None = None) -> list[str]:
    local, domain = validate_email(email)
    return [f"{local}+{label}@{domain}" for label in _normalize_labels(labels)]


def generate_batch_csv(source: TextIO, labels: Sequence[str] | None = None) -> str:
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
        email = (row.get(email_field) or "").strip()
        if not email:
            continue
        try:
            aliases = generate_aliases(email, labels)
        except ValueError as exc:
            raise ValueError(f"Invalid email on CSV line {reader.line_num}: {exc}") from exc
        writer.writerows((email, alias) for alias in aliases)
    return output.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address aliases for your inbox.",
        epilog="Example: EMAIL-EvIL.py alex@example.com --labels shopping travel --format json",
    )
    parser.add_argument("email", nargs="?", help="Email address; prompts if omitted.")
    parser.add_argument("--batch-csv", metavar="PATH", help="Read a CSV with an 'email' column.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--labels", nargs="+", help="Custom alias labels.")
    group.add_argument("--preset", choices=sorted(PRESET_LABELS), help="Use a preset label pack.")
    parser.add_argument("-f", "--format", choices=("terminal", "text", "json", "csv"), default="terminal")
    parser.add_argument("-o", "--output", help="Write the output to a file.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Hide the banner and headings.")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    return _normalize_labels(args.labels)


def render_aliases(
    aliases: Sequence[str],
    output_format: str = "text",
    quiet: bool = False,
    *,
    color: bool = True,
    stream: TextIO | None = None,
) -> str:
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
        banner = _render_banner(color=color, stream=stream)
        width = max(20, min(_terminal_width() - 2, 60))
        inside = width - 2
        border = "+" + "-" * inside + "+"
        heading = _paint(f"YOUR ALIASES ({len(aliases)})", "1;33", enabled=color, stream=stream)
        rows = [
            _paint(border, "1;31", enabled=color, stream=stream),
            "|" + heading.center(inside) + "|",
            _paint(border, "1;31", enabled=color, stream=stream),
        ]
        for alias in aliases:
            parts = textwrap.wrap(alias, width=max(1, inside - 4), break_long_words=True)
            rows.extend("|  " + part.ljust(inside - 4) + "  |" for part in parts)
        rows.append(_paint(border, "1;31", enabled=color, stream=stream))
        return banner + "\n".join(rows) + "\n"
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
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = build_parser().parse_args(argv)

    try:
        labels = resolve_labels(args)
        if args.batch_csv:
            if args.email is not None:
                raise ValueError("Do not provide an email argument when using --batch-csv.")
            with Path(args.batch_csv).open(encoding="utf-8", newline="") as source:
                rendered = generate_batch_csv(source, labels)
        else:
            if args.email is None:
                use_color = not args.no_color
                if not args.quiet:
                    stdout.write(_render_banner(color=use_color, stream=stdout))
                    stdout.write(_render_command_help(color=use_color, stream=stdout))
                prompt = "ENTER YOUR ADDRESS, MORTAL: "
                stdout.write(_paint(prompt, "1;31", enabled=use_color, stream=stdout))
                email = stdin.readline().strip()
            else:
                email = args.email
            rendered = render_aliases(
                generate_aliases(email, labels),
                args.format,
                args.quiet,
                color=not args.no_color,
                stream=stdout,
            )

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
