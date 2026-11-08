#!/usr/bin/env python3
"""Generate plus-address aliases for organizing your inbox.

This utility formats addresses locally only; it never sends email.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable

DEFAULT_LABELS = ("shopping", "newsletters", "travel", "projects", "banking")
_LOCAL_PART_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")
_DOMAIN_LABEL_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
_LABEL_RE = re.compile(r"[^a-z0-9]+")
BANNER = r"""
  _____ __  __    _    ___ _      _____       _ _
 | ____|  \/  |  / \  |_ _| |    | ____|_   _(_) |
 |  _| | |\/| | / _ \  | || |    |  _| \ \ / / | |
 | |___| |  | |/ ___ \ | || |___ | |___ \ V /| | |
 |_____|_|  |_/_/   \_\___|_____|_____| \_/ |_|_|

       _________
      /        /|
     / EMAIL  / |
    /  EVIL  /  |
   /________/   |
   |  inbox |   |
   | aliases|  /
   |________| /
                 Python 3 inbox alias generator
"""
RAINBOW = ("\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m")
RESET = "\033[0m"


def colorize_banner(banner: str = BANNER, *, use_color: bool = True) -> str:
    """Apply cycling ANSI rainbow colors, or return plain text when disabled."""
    if not use_color:
        return banner
    colored_lines = []
    for index, line in enumerate(banner.splitlines()):
        colored_lines.append(f"{RAINBOW[index % len(RAINBOW)]}{line}{RESET}" if line else "")
    return "\n".join(colored_lines)


def normalize_labels(labels: Iterable[str] | None = None) -> list[str]:
    """Normalize custom labels for plus-address aliases."""
    if labels is None:
        return list(DEFAULT_LABELS)

    normalized: list[str] = []
    seen: set[str] = set()
    for value in labels:
        label = _LABEL_RE.sub("-", str(value).strip().lower()).strip("-")
        if not label:
            raise ValueError("Labels must contain at least one letter or number.")
        if label not in seen:
            normalized.append(label)
            seen.add(label)
    if not normalized:
        raise ValueError("Provide at least one non-empty label.")
    return normalized


def _validate_email(email: str) -> tuple[str, str]:
    """Validate a practical, unquoted email address and return its parts."""
    if not isinstance(email, str):
        raise TypeError("Email address must be a string.")

    candidate = email.strip()
    if len(candidate) > 254 or candidate.count("@") != 1:
        raise ValueError("Enter an email address in the form name@example.com.")

    local_part, domain = candidate.rsplit("@", 1)
    if (
        not local_part
        or len(local_part) > 64
        or not _LOCAL_PART_RE.fullmatch(local_part)
        or local_part.startswith(".")
        or local_part.endswith(".")
        or ".." in local_part
    ):
        raise ValueError("Enter a valid email address with a practical local part.")

    if not domain or len(domain) > 253:
        raise ValueError("Enter a valid email domain, such as example.com.")
    domain_labels = domain.split(".")
    if len(domain_labels) < 2 or any(
        not _DOMAIN_LABEL_RE.fullmatch(part) for part in domain_labels
    ):
        raise ValueError("Enter a valid email domain, such as example.com.")
    return local_part, domain


def generate_aliases(email: str, labels: Iterable[str] | None = None) -> list[str]:
    """Return plus-address aliases; provider support is not checked."""
    local_part, domain = _validate_email(email)
    return [f"{local_part}+{label}@{domain}" for label in normalize_labels(labels)]


def _parse_labels(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    return [part.strip() for value in values for part in value.split(",") if part.strip()]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address aliases for inbox organization. No email is sent."
    )
    parser.add_argument("email", nargs="?", help="Email address to create aliases for")
    parser.add_argument(
        "--labels", "-l", action="append", metavar="LABEL[,LABEL...]",
        help="Custom labels; repeat the option or provide comma-separated labels",
    )
    parser.add_argument("--json", action="store_true", help="Print results as a JSON array")
    parser.add_argument(
        "--no-banner", action="store_true", help="Hide the startup banner in terminal output"
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable ANSI rainbow colors in the banner"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    email = args.email if args.email is not None else input("Email address: ")

    try:
        aliases = generate_aliases(email, _parse_labels(args.labels))
    except (TypeError, ValueError) as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(aliases, indent=2))
    else:
        if not args.no_banner:
            print(colorize_banner(use_color=not args.no_color))
        print("Generated inbox aliases:\n")
        for alias in aliases:
            print(f"  + {alias}")
        print("\nLocal generation only — no email was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
