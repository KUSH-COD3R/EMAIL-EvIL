<p align="center">
  <svg width="1000" height="260" viewBox="0 0 1000 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="EMAIL-EvIL Banner">
    <defs>
      <linearGradient id="bg" x1="0%" x2="100%" y1="0%" y2="100%">
        <stop offset="0%" stop-color="#04070d"/>
        <stop offset="45%" stop-color="#0c1323"/>
        <stop offset="100%" stop-color="#101827"/>
      </linearGradient>
      <linearGradient id="accent" x1="0%" x2="100%" y1="0%" y2="0%">
        <stop offset="0%" stop-color="#00f5d4"/>
        <stop offset="35%" stop-color="#2dd4bf"/>
        <stop offset="70%" stop-color="#a78bfa"/>
        <stop offset="100%" stop-color="#f472b6"/>
      </linearGradient>
      <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2.8" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    <rect width="1000" height="260" fill="url(#bg)"/>
    <rect x="22" y="22" width="956" height="216" rx="14" fill="none" stroke="url(#accent)" stroke-width="1.4" opacity="0.9"/>
    <g opacity="0.14" stroke="url(#accent)" fill="none">
      <path d="M70 200 H930"/>
      <path d="M110 60 H890"/>
      <path d="M125 40 L165 220"/>
      <path d="M875 40 L835 220"/>
      <path d="M220 40 L180 220"/>
      <path d="M780 40 L820 220"/>
    </g>

    <g>
      <text x="500" y="96" text-anchor="middle" font-family="Consolas, Monaco, monospace" font-size="52" font-weight="700" fill="#f8fafc" letter-spacing="2" filter="url(#softGlow)">
        EMAIL-EvIL
      </text>

      <text x="500" y="136" text-anchor="middle" font-family="Consolas, Monaco, monospace" font-size="15" fill="#7dd3fc" letter-spacing="5">
        [ PLUS ADDRESSES • INBOX ORGANIZATION • SECURITY TOOLS ]
      </text>

      <rect x="235" y="152" width="530" height="2.5" fill="url(#accent)" opacity="0.95"/>

      <text x="500" y="188" text-anchor="middle" font-family="Consolas, Monaco, monospace" font-size="14" fill="#cbd5e1" letter-spacing="2">
        GENERATE • TEST • MANAGE • ORGANIZE
      </text>
    </g>
  </svg>
</p>

<h1 align="center">EMAIL-EvIL</h1>

<p align="center">
  <b>Generate plus-address aliases for smarter inbox organization</b>
</p>

<p align="center">
  <a href="https://github.com/KUSH-COD3R/EMAIL-EvIL/issues">Report Bug</a>
  ·
  <a href="https://github.com/KUSH-COD3R/EMAIL-EvIL/pulls">Request Feature</a>
</p>

---

# EMAIL-EvIL

EMAIL-EvIL is a small but polished Python package for generating plus-address aliases for inbox organization, filtering, and personal mail hygiene.

It turns a normal address like `alex@example.com` into aliases such as:

```text
alex+shopping@example.com
alex+travel@example.com
alex+banking@example.com
```

This project is designed for harmless inbox management and is best used with providers that support plus-addressing.

## Features

- Generate aliases from a base email
- Support custom labels and predefined defaults
- Command-line interface for quick use
- JSON output for automation and scripts
- Package install via `pip install -e .`
- Clean, testable Python module structure
- Built-in preset categories for common alias uses
- Optional file output and structured JSON export
- Extra validation and predictable alias generation

## Installation

```bash
git clone https://github.com/KUSH-COD3R/EMAIL-EvIL.git
cd EMAIL-EvIL
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Quick Start

```bash
email-evil alex@example.com
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

### Built-in categories

```bash
email-evil alex@example.com --preset personal
email-evil alex@example.com --preset business
email-evil alex@example.com --preset security
```

### Custom labels

```bash
email-evil alex@example.com --label work --label invoices --label family
```

### Comma-separated labels

```bash
email-evil alex@example.com --labels work,finance,travel
```

### JSON output

```bash
email-evil alex@example.com --format json
```

### Write to a file

```bash
email-evil alex@example.com --output aliases.txt
```

## Python API

```python
from email_evil.aliases import generate_aliases

aliases = generate_aliases("alex@example.com", ["work", "newsletters", "travel"])
print(aliases)
# ['alex+work@example.com', 'alex+newsletters@example.com', 'alex+travel@example.com']
```

## Project layout

```text
EMAIL-EvIL/
├── LICENSE
├── README.md
├── pyproject.toml
├── email_aliases.py
├── email_evil/
│   ├── __init__.py
│   ├── __main__.py
│   ├── aliases.py
│   ├── cli.py
│   └── presets.py
├── tests/
│   └── test_email_aliases.py
└── .gitignore
```

## Notes

Plus-addressing support varies by mail provider. This tool simply generates valid alias patterns that many providers accept.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
