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

A tiny Python tool for generating plus-address email aliases so you can organize inboxes, filter newsletters, and manage personal or business email streams more cleanly.

This project is intentionally simple and safe: it does not send email, exploit providers, or interact with mail servers. It only transforms an address into valid plus-address variants that your mail provider may support.

## Features

- Generate plus-address aliases from a base email
- Custom labels for shopping, newsletters, travel, projects, and more
- CLI support for quick use in scripts and shell workflows
- JSON or plain-text output for automation
- Minimal dependencies and easy setup

## Installation

```bash
git clone https://github.com/KUSH-COD3R/EMAIL-EvIL.git
cd EMAIL-EvIL
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Usage

Generate default aliases:

```bash
email-evil yourname@example.com
```

Custom labels:

```bash
email-evil yourname@example.com --label shopping --label travel --label invoices
```

Use a comma-separated list:

```bash
email-evil yourname@example.com --labels shopping,newsletters,travel
```

Output as JSON:

```bash
email-evil yourname@example.com --format json
```

Run the script directly:

```bash
python email_aliases.py
```

Example output:

```text
Generated aliases:
yourname+shopping@example.com
yourname+newsletters@example.com
yourname+travel@example.com
yourname+projects@example.com
yourname+banking@example.com
```

## Example programmatic use

```python
from email_aliases import generate_aliases

aliases = generate_aliases("alex@example.com", ["work", "news", "finance"])
print(aliases)
# ['alex+work@example.com', 'alex+news@example.com', 'alex+finance@example.com']
```

## Notes

Plus-addressing is supported by some providers and may not work everywhere. This project simply generates valid alias formats for organizations that do support them.

## License

MIT. See [LICENSE](LICENSE).
