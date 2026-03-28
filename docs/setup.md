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

If you only want the Python bridge for bots and automation, you can install from GitHub instead:

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
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
5. Optionally set health alert webhook targets.
6. Pick a Discord formatting preset if you use the Python bridge.
7. Save settings or save a named workspace.
8. Refresh backend status, catalog, and source health.

## Discord bot bridge

This repository also includes a Python bridge for Discord bots that want to call the toolkit and format results as Discord payloads.

Install it from GitHub:

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

Then see `docs/discord-bots.md` for the bridge workflow.

## Recommended usage paths

Use the desktop GUI when you want:

- a visual workspace for running scrapers
- saved workspaces and output browsing
- source-health review without writing code

Use the Python bridge when you want:

- a Discord bot command
- a scheduled script
- a small internal automation service
- Python-side control over when and how scraper results are published

## New desktop helpers

- compare two saved payloads from the Results Library
- preview run commands before wiring them into Task Scheduler or cron
- preview health commands with alert webhook options
- keep reusable workspaces for different toolkit/output combinations
