#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

from __future__ import annotations

import argparse
from typing import Sequence

DEFAULT_LABELS = ["shopping", "newsletters", "travel", "projects", "banking"]
PRESET_LABELS = {
    "default": DEFAULT_LABELS,
    "minimal": ["shopping", "travel", "banking"],
    "personal": ["work", "family", "shopping", "travel"],
}


def _normalize_labels(labels: Sequence[str] | None) -> list[str]:
    """Return a clean, deduplicated list of alias labels."""
    if labels is None:
        return DEFAULT_LABELS.copy()

    normalized: list[str] = []
    seen: set[str] = set()

    for label in labels:
        cleaned = label.strip().lower().lstrip("+")
        if not cleaned or cleaned in seen:
            continue

        seen.add(cleaned)
        normalized.append(cleaned)

    if not normalized:
        return DEFAULT_LABELS.copy()

    return normalized


def validate_email(email: str) -> tuple[str, str]:
    """Validate and split an email address into local and domain parts."""
    address = email.strip()
    if not address or "@" not in address:
        raise ValueError("Please provide a valid email address containing '@'.")

    local_part, domain = address.rsplit("@", 1)
    if not local_part or not domain or "." not in domain:
        raise ValueError("Please provide a valid email address with a domain.")

    return local_part, domain


def generate_aliases(email: str, labels: Sequence[str] | None = None) -> list[str]:
    """Return a list of plus-address aliases for a given email."""
    local_part, domain = validate_email(email)
    normalized_labels = _normalize_labels(labels)
    return [f"{local_part}+{label}@{domain}" for label in normalized_labels]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plus-address email aliases for inbox organization.",
    )
    parser.add_argument("email", nargs="?", help="Email address to turn into plus-address aliases.")
    parser.add_argument(
        "-l",
        "--labels",
        nargs="*",
        default=None,
        help="Custom labels to add after the plus sign, such as shopping newsletters travel",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESET_LABELS),
        help="Use a built-in label set.",
    )
    return parser


def resolve_labels(args: argparse.Namespace) -> list[str]:
    if args.preset:
        return PRESET_LABELS[args.preset].copy()
    if args.labels is not None:
        return _normalize_labels(args.labels)
    return DEFAULT_LABELS.copy()


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    email = args.email or input("Enter your email: ").strip()

    try:
        aliases = generate_aliases(email, resolve_labels(args))
    except ValueError as exc:
        parser.exit(1, f"Error: {exc}\n")

    print("Generated aliases:")
    for alias in aliases:
        print(alias)
