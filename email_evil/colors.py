"""Utilities for better terminal output."""

from __future__ import annotations

class Colors:
    """Basic ANSI color helpers."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{Colors.RESET}"
