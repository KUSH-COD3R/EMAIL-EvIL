"""Command-line interface for EMAIL-EvIL."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .aliases import generate_aliases
from .colors import colorize, Colors
from .presets import PRESETS


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
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("email", nargs="?", help="Base email address used to generate aliases.")
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        help="Use a predefined alias preset.",
    )
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
    parser.add_argument(
        "--show-preset",
        action="store_true",
        help="Display the available preset groups and exit.",
    )
    args = parser.parse_args(argv)

    if args.show_preset:
        print(colorize("Available presets:", Colors.BOLD + Colors.CYAN))
        for name, labels in PRESETS.items():
            print(f"  {name}: {', '.join(labels)}")
        return 0

    email_value = args.email or input(colorize("Enter your email: ", Colors.YELLOW)).strip()
    labels = _parse_labels(args.label, args.labels)
    if args.preset:
        labels = PRESETS[args.preset] + labels

    try:
        aliases = generate_aliases(email_value, labels)
    except ValueError as exc:
        print(colorize(f"Error: {exc}", Colors.RED), file=sys.stderr)
        return 2

    if args.format == "json":
        rendered = json.dumps(aliases, indent=2)
    else:
        rendered = colorize("Generated aliases:\n", Colors.BOLD + Colors.CYAN) + "\n".join(
            colorize(alias, Colors.GREEN) for alias in aliases
        )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered.replace("\033[0m", "") + "\n", encoding="utf-8")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
