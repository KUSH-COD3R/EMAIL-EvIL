# EMAIL-EvIL

A lightweight Python utility for generating plus-address email aliases and turning one inbox into a high-control, category-based routing system.

## What it does

This tool creates aliases like:

```text
alex+shopping@example.com
alex+newsletters@example.com
alex+travel@example.com
alex+projects@example.com
alex+banking@example.com
```

One inbox. Multiple lanes. Cleaner filtering.

If your email provider supports plus-addressing, you can route messages by category without creating a pile of extra inboxes.

## Usage

```bash
python3 email_aliases.py "alex@example.com"
```

Example output:

```text
Generated aliases:
alex+shopping@example.com
alex+newsletters@example.com
alex+travel@example.com
alex+projects@example.com
alex+banking@example.com
```

## Custom labels

Use your own alias labels:

```bash
python3 email_aliases.py "alex@example.com" --labels shopping receipts travel
```

Built-in presets are also available:

```bash
python3 email_aliases.py "alex@example.com" --preset minimal
python3 email_aliases.py "alex@example.com" --preset personal
```

## Tests

Run the built-in unittest suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Notes

Plus-addressing support varies by provider, but when it works, it gives you a clean way to segment mail and keep your inbox under tighter control.
