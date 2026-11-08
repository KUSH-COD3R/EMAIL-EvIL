"""Core alias generation helpers for EMAIL-EvIL."""

from __future__ import annotations

import re

DEFAULT_LABELS = ["shopping", "newsletters", "travel", "projects", "banking"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_labels(labels: list[str] | None) -> list[str]:
    if labels is None:
        return DEFAULT_LABELS.copy()

    cleaned: list[str] = []
    for label in labels:
        if label is None:
            continue
        value = str(label).strip().lower()
        if value and re.fullmatch(r"[a-z0-9._-]+", value):
            cleaned.append(value)

    return cleaned or DEFAULT_LABELS.copy()


def generate_aliases(email: str, labels: list[str] | None = None) -> list[str]:
    """Return a list of valid plus-address aliases for a given email."""
    if not isinstance(email, str):
        raise ValueError("Email address must be a string.")

    normalized = email.strip()
    if not normalized or not EMAIL_RE.fullmatch(normalized):
        raise ValueError("Please provide a valid email address containing '@' and a domain.")

    local_part, domain = normalized.split("@", 1)
    normalized_labels = _normalize_labels(labels)
    return [f"{local_part}+{label}@{domain}" for label in normalized_labels]
