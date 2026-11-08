# EMAIL-EvIL ✉️

<div align="center">

### Make your inbox easier to organize.

A small, dependency-free Python 3 CLI for generating plus-address aliases on desktop or Android with Termux.

[Quick start](#quick-start) · [Termux](#termux-android) · [Examples](#examples) · [Python API](#python-api)

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![No runtime dependencies](https://img.shields.io/badge/runtime%20dependencies-none-2ea44f)
![Local only](https://img.shields.io/badge/email%20sending-none-6f42c1)

</div>

> **Safety note:** EMAIL-EvIL only formats aliases locally. It does not send email, spoof sender identities, contact mail servers, or verify that an address exists. Plus-addressing support depends on your email provider.

## Features

- Generate aliases such as `alex+shopping@example.com`
- Use sensible defaults or provide custom labels
- Validate common email-address formats and normalize labels
- ASCII terminal banner, with a `--no-banner` option
- Readable output or JSON for scripts
- Python 3.10+; no runtime dependencies; works in Termux without root

## Quick start

```bash
python3 email_aliases.py alex@example.com
```

## Termux (Android)

```bash
pkg update
pkg install python git
git clone https://github.com/KUSH-COD3R/EMAIL-EvIL.git
cd EMAIL-EvIL
python3 email_aliases.py alex@example.com --labels shopping,receipts,travel
```

No package installation, root access, Termux:API, or extra Python dependencies are required. Run `python3 email_aliases.py` without an address for an interactive prompt. Use `--no-banner` for compact terminal output.

## Examples

Custom labels:

```bash
python3 email_aliases.py alex@example.com --labels work,travel --labels "side projects"
```

Machine-readable JSON (banner is automatically omitted):

```bash
python3 email_aliases.py alex@example.com --labels work,travel --json
```

```json
[
  "alex+work@example.com",
  "alex+travel@example.com"
]
```

## Python API

```python
from email_aliases import generate_aliases

aliases = generate_aliases("alex@example.com", ["work", "side projects"])
print(aliases)
# ['alex+work@example.com', 'alex+side-projects@example.com']
```

## Development

```bash
python3 -m pip install -e '.[test]'
python3 -m pytest
```

Tests run automatically on pushes and pull requests with GitHub Actions.

## Limitations

Validation is practical rather than a complete implementation of every email-address standard. Generating an alias does not verify that a mailbox exists or that its provider accepts plus-addressing. No message is sent by this project.

## Contributing

Bug reports and improvements are welcome. Keep contributions focused on safe, local alias generation and include tests for behavior changes.
