import json

import pytest

from email_aliases import generate_aliases


def test_generate_aliases_default_labels():
    aliases = generate_aliases("alex@example.com")
    assert aliases == [
        "alex+shopping@example.com",
        "alex+newsletters@example.com",
        "alex+travel@example.com",
        "alex+projects@example.com",
        "alex+banking@example.com",
    ]


def test_generate_aliases_custom_labels():
    aliases = generate_aliases("alex@example.com", ["work", "finance"])
    assert aliases == [
        "alex+work@example.com",
        "alex+finance@example.com",
    ]


def test_invalid_email_raises_value_error():
    with pytest.raises(ValueError):
        generate_aliases("not-an-email")


def test_command_like_output_format_json(monkeypatch, capsys):
    import email_aliases

    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: "alex@example.com",
    )
    rc = email_aliases.main(["--format", "json"])
    captured = capsys.readouterr()
    assert rc == 0
    assert json.loads(captured.out.replace("Generated aliases:\n", "")) == [
        "alex+shopping@example.com",
        "alex+newsletters@example.com",
        "alex+travel@example.com",
        "alex+projects@example.com",
        "alex+banking@example.com",
    ]
