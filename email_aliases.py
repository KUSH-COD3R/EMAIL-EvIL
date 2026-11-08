#!/usr/bin/env python3
"""Generate plus-address email aliases for organizing inboxes."""

from __future__ import annotations


def generate_aliases(email: str, labels: list[str] | None = None) -> list[str]:
    """Return a list of plus-address aliases for a given email."""
    if labels is None:
        labels = ["shopping", "newsletters", "travel", "projects", "banking"]

    if "@" not in email:
        raise ValueError("Please provide a valid email address containing '@'.")

    local_part, domain = email.split("@", 1)
    return [f"{local_part}+{label}@{domain}" for label in labels]


if __name__ == "__main__":
    user_email = input("Enter your email: ").strip()
    aliases = generate_aliases(user_email)

    print("Generated aliases:")
    for alias in aliases:
        print(alias)
