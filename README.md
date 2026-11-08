# EMAIL-EvIL

A small Python utility for generating plus-address email aliases to help organize inboxes without creating extra mailboxes.

## What it does

This tool writes aliases like:

```text
alex+shopping@example.com
alex+newsletters@example.com
alex+travel@example.com
alex+projects@example.com
alex+banking@example.com
```

Give your inbox a little edge: spin one address into sleek, category-ready aliases—if your email provider supports plus-addressing.

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

You can supply your own alias labels:

```bash
python3 email_aliases.py "alex@example.com" --labels shopping receipts travel
```

You can also use built-in presets:

```bash
python3 email_aliases.py "alex@example.com" --preset minimal
python3 email_aliases.py "alex@example.com" --preset personal
```

## Tests

Run the built-in `unittest` suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Notes

Plus-addressing support varies by email provider.
