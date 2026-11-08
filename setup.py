from setuptools import setup

setup(
    name="email-evil",
    version="1.0.0",
    description="Generate plus-address email aliases for inbox organization",
    py_modules=["email_aliases"],
    python_requires=">=3.10",
    entry_points={"console_scripts": ["email-evil=email_aliases:main"]},
)
