#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

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


def _paint(text: str, code: str, *, enabled: bool) -> str:
    """Apply ANSI color when supported and not disabled by the user."""
    return f"\033[{code}m{text}\033[0m" if enabled else text


def _color_enabled(stream: TextIO, requested: bool = True) -> bool:
    return requested and getattr(stream, "isatty", lambda: False)() and "NO_COLOR" not in os.environ


def _render_terminal_banner(color: bool = True) -> str:
    """Render a compact, sharply defined dragon banner for Termux terminals."""
    use_color = color and _color_enabled(sys.stdout)
    width = min(42, max(24, _terminal_width()))
    inside = width - 2
    dragon = (
        "           /\\             /\\",
        "      ____/  \\___________/  \\____",
        "     /  _   /  /^^^^^\\  \\   _  \",
        "    /__/ \\_/  (  o o  )  \\_/ \\__\\",
        "             \\   ^   /",
        "              \\_____ /",
        "          ____/| |\\____",
        "         /____/   \\____\\",
    )
    title = ("INFERNAL INBOX", "EMAIL-EvIL", "by KUSH-COD3R", "one inbox, many lanes")
    border = "+" + "-" * inside + "+"
    lines = [_paint(border, "1;31", enabled=use_color)]
    for index, row in enumerate(dragon):
        eye_color = "1;33" if index == 3 else "31"
        lines.append("|" + _paint(row.center(inside), eye_color, enabled=use_color) + "|")
    lines.append("|" + " " * inside + "|")
    for index, label in enumerate(title):
        color_code = "1;31" if index < 2 else "1;33"
        lines.append("|" + _paint(label.center(inside), color_code, enabled=use_color) + "|")
    lines.append(_paint(border, "1;31", enabled=use_color))
    return "\n".join(lines) + "\n"


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
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    return _normalize_labels(args.labels)


def render_aliases(aliases: Sequence[str], output_format: str = "text", quiet: bool = False,
                   *, color: bool = True, stream: TextIO | None = None) -> str:
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
        width = max(20, min(_terminal_width() - 2, 60))
        inside = width - 2
        heading = f"YOUR ALIASES ({len(aliases)})"
        border = "+" + "-" * inside + "+"
        use_color = color and _color_enabled(stream or sys.stdout)
        rows = [
            _paint(border, "1;31", enabled=use_color),
            "|" + _paint(heading[:inside].center(inside), "1;33", enabled=use_color) + "|",
            _paint(border, "1;31", enabled=use_color),
        ]
        for alias in aliases:
            parts = textwrap.wrap(alias, width=max(1, inside - 4), break_long_words=True)
            rows.extend("|  " + part.ljust(inside - 4) + "  |" for part in parts)
        rows.append(_paint(border, "1;31", enabled=use_color))
        return _render_terminal_banner(color) + "\n".join(rows) + "\n"
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
                use_color = not args.no_color and _color_enabled(stdout)
                if not args.quiet:
                    stdout.write(_render_terminal_banner(color=not args.no_color))
                stdout.write(_paint("Enter your email: ", "1;33", enabled=use_color))
                email = stdin.readline().strip()
            else:
                email = args.email
            rendered = render_aliases(generate_aliases(email, labels), args.format, args.quiet,
                                      color=not args.no_color, stream=stdout)
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
