# Installation

This page covers first-time setup for Open Scrapers Desk in both development and packaged-app scenarios.

## Requirements

- Windows for the packaged `.exe` workflow
- Python 3.11 or newer for local development
- Node.js 20 or newer
- npm
- a separate checkout of `open-scrapers-toolkit`

## Prepare the toolkit first

Open Scrapers Desk is not the scraper engine. It depends on the toolkit repository being available separately.

In the toolkit repo:

```powershell
npm install
npm run build
```

That gives the desktop app a healthy backend to validate against.

## Install the desktop app for development

In the desktop repo:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts\smoke_test.py
```

The compile step catches syntax issues. The smoke test checks the application basics before you start clicking around manually.

## Launch in development mode

Preferred module launch:

```powershell
python -m open_scrapers_desk.app
```

If your shell does not resolve the package path cleanly, use:

```powershell
$env:PYTHONPATH="src"
python src\open_scrapers_desk\app.py
```

The app entrypoint is written to support both module execution and direct script execution.

## Launch the packaged `.exe`

If you are using a built release instead of a source checkout, run:

```powershell
dist\OpenScrapersDesk\OpenScrapersDesk.exe
```

Or use the installed shortcut if you created an installer package with Inno Setup.

## Recommended first-run configuration

On the Overview tab, set:

- `Toolkit path`
- `Node executable`
- `Output directory`
- `Ko-fi link` if you want to override the default support URL

Then click **Validate Backend**.

## What happens on the first run

The app stores settings under the current Windows profile and tries to help with defaults:

- it looks for likely toolkit folder names near the current repo
- it defaults the output folder to `<toolkit>/output` when a toolkit is found
- it preloads the Ko-fi URL with `https://ko-fi.com/ninezel`

## Useful environment variables

Optional variables include:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_KOFI_URL`

These can pre-populate the application settings before the UI is even opened.

## Local validation checklist

Before reporting install problems, verify these basics:

```powershell
node --version
npm --version
python --version
python -m compileall src
python scripts\smoke_test.py
```

And in the toolkit repo:

```powershell
npx tsx src/cli.ts list --format json
```

If the toolkit catalog command fails in the terminal, the desktop app will not be able to load scrapers either.
