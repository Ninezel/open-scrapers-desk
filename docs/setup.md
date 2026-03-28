# Desktop Setup

## Requirements

- Python 3.11+
- Node.js 20+ for the backend toolkit
- a local clone of `open-scrapers-toolkit`
- Git is recommended if you want to install the Python bot bridge directly from GitHub

## Install the desktop app

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts/smoke_test.py
```

## Launch

```bash
python -m open_scrapers_desk.app
```

Alternative:

```bash
set PYTHONPATH=src
python src/open_scrapers_desk/app.py
```

## First-run checklist

1. Set the toolkit path.
2. Set the Node executable.
3. Choose the output directory.
4. Pick a default save format.
5. Save settings or save a named workspace.
6. Refresh backend status, catalog, and source health.

## Discord bot bridge

This repository also includes a Python bridge for Discord bots that want to call the toolkit and format results as Discord payloads.

Install it from GitHub:

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

Then see `docs/discord-bots.md` for the bridge workflow.
