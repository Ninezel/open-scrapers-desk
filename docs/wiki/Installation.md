# Installation

## Requirements

- Windows
- Python 3.11+
- Node.js 20+
- npm
- a clone of `open-scrapers-toolkit`

## Desktop app setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Backend setup

In the toolkit repo:

```bash
npm install
npm run build
```

## Launch

```bash
set PYTHONPATH=src
python src/open_scrapers_desk/app.py
```
