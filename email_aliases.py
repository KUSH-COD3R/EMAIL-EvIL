#!/usr/bin/env python3
"""Compatibility wrapper for the EMAIL-EvIL package."""

from __future__ import annotations

from email_evil.aliases import generate_aliases
from email_evil.cli import main

__all__ = ["generate_aliases", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
