# EMAIL-EvIL

![EMAIL-EvIL banner](assets/email-evil-banner.svg)

```text
      .------------------------------------------------.
      |  You've got mail... and it's a little evil!   |
      '-------------------------.----------------------'
                                \\
          .-----.               \\
         / .---. \\       .-----------------.
        | | o o | |      /  EMAIL-EvIL!    \\
        | |  ^  | |     |  Your inbox's     |
         \\ '---' /      |  mischievous pal! |
          '-----'        \\_________________/
             \\                 ||
              \\________________||____
                               \\____/
```

A lightweight Python utility for generating plus-address aliases and putting one inbox under tighter control.

## What it does

Generate category-ready addresses from one email account:

```text
alex+shopping@example.com
alex+newsletters@example.com
alex+travel@example.com
alex+projects@example.com
alex+banking@example.com
```

One inbox. Multiple lanes. No clutter. Use the aliases in sign-ups and filters—where your provider supports plus-addressing.

## Run it

Run directly with Python 3.10 or later:

```bash
python3 EMAIL-EvIL.py "alex@example.com"
```

Or install the command locally:

```bash
python3 -m pip install .
email-evil "alex@example.com"
```

Omit the email argument to be prompted for it. Get the full option list with `email-evil --help`.

## Customize labels

```bash
email-evil "alex@example.com" --labels shopping receipts travel
email-evil "alex@example.com" --preset minimal
email-evil "alex@example.com" --preset personal
```

## Batch from a CSV

Create a CSV with an `email` column, then pass it to `--batch-csv`. The batch output is CSV with one row per generated alias, including the source email. Blank email rows are skipped; invalid addresses stop the batch with a line-numbered error.

Input (`emails.csv`):

```csv
email
alex@example.com
sam@example.net
```

Generate aliases and write the result to a file:

```bash
email-evil --batch-csv emails.csv --preset minimal --output aliases.csv
```

The output has `email` and `alias` columns. Batch mode only formats alias addresses; it does not send email or contact providers.

## Choose an output format

Use the ASCII terminal view for a more polished interactive display, or print machine-readable JSON and CSV:

```bash
email-evil "alex@example.com" --format terminal
email-evil "alex@example.com" --format json
email-evil "alex@example.com" --format csv
```

The terminal view includes a small ASCII banner and a boxed alias list. Use `--quiet` to suppress the artwork and box for clean output, or choose `--format text` for the plain-text view.

Write results to a file:

```bash
email-evil "alex@example.com" --format csv --output aliases.csv
email-evil "alex@example.com" --quiet
```

## Tests

Run the standard-library test suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Important notes

- **Generation only:** EMAIL-EvIL formats alias addresses as text; it does not send email or sign you up for anything.
- **No external services:** The program does not connect to email providers, APIs, or other network services.
- **Provider support varies:** Plus-addressing is not supported by every provider, and alias handling may differ. Check your provider's documentation before relying on an alias.
- **Use responsibly:** These aliases are intended for organizing your own inbox and filters, not for spam, unsolicited bulk messaging, or evading service rules.
