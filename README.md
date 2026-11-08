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
python3 email_aliases.py "alex@example.com"
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

## Choose an output format

Print JSON or CSV to the terminal:

```bash
email-evil "alex@example.com" --format json
email-evil "alex@example.com" --format csv
```

Write results to a file and omit the text heading when piping output:

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
