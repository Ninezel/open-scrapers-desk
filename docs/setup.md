# Desktop Setup

## Requirements

- Python 3.11+
- Node.js 20+ for the backend toolkit
- a local clone of `open-scrapers-toolkit`

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
