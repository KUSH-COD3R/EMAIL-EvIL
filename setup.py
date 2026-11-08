from pathlib import Path

from setuptools import setup

setup(
    name="email-evil",
    version="1.0.0",
    description="Generate plus-address email aliases for inbox organization",
    python_requires=">=3.10",
    scripts=[str(Path(__file__).parent / "EMAIL-EvIL.py")],
)
