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


def test_json_cli_output(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "alex@example.com")
    from email_aliases import main as alias_main

    rc = alias_main(["--format", "json"])
    captured = capsys.readouterr()
    assert rc == 0
    parsed = json.loads(captured.out.replace("Generated aliases:\n", ""))
    assert parsed == [
        "alex+shopping@example.com",
        "alex+newsletters@example.com",
        "alex+travel@example.com",
        "alex+projects@example.com",
        "alex+banking@example.com",
    ]
