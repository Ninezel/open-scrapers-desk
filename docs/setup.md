# Setup

This guide covers local development and first-time use.

## Requirements

- Python 3.11+
- Node.js 20+
- npm
- a separate checkout of `open-scrapers-toolkit`

## 1. Prepare the scraper backend

In the toolkit repository:

```bash
npm install
npm run build
```

The desktop app can talk to either:

- `dist/cli.js`
- `src/cli.ts` through `npx tsx`

## 2. Prepare the desktop app

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts/smoke_test.py
```

## 3. Launch the app

```bash
set PYTHONPATH=src
python src/open_scrapers_desk/app.py
```

## 4. Configure paths in the app

On the Overview tab:

- set the toolkit path
- confirm the node executable
- set the output directory
- add your Ko-fi link if you want the built-in support button enabled
- click **Validate Backend**

## 5. Run a scraper

On the Run Scrapers tab:

- choose a scraper
- enter any optional parameters
- set a limit
- choose an output file
- click **Run Selected**

## 6. Read results

On the Results Library tab:

- refresh the library
- choose a result file
- browse the records table
- use the detail pane for summaries and metadata
