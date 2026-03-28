# Open Scrapers Desk

Open Scrapers Desk is a PyQt desktop application for people who want to use the Open Scrapers ecosystem without living in a terminal. It connects to the separate scraper backend repository, lets users queue scraper jobs from a GUI, and presents saved outputs in a readable workspace.

Repository split:

- Backend repo: `https://github.com/Ninezel/open-scrapers-toolkit`
- Desktop repo: `https://github.com/Ninezel/open-scrapers-desk`

## What the desktop app does

- connects to an Open Scrapers Toolkit checkout
- validates the Node and toolkit environment
- loads the scraper catalog from the backend
- queues a selected scraper, a whole category, or the full catalog
- shows source-health status from the toolkit `health` command
- scans result folders automatically
- displays summary views for the whole library and individual result payloads
- stores saved workspaces for different toolkit/output combinations
- includes a configurable Ko-fi support button

Default support link:

- `https://ko-fi.com/ninezel`

## Desktop features

- **Overview tab**: toolkit path, node path, output folder, default save format, saved workspaces, source-health snapshot, latest files
- **Run Scrapers tab**: scraper list, parameter inputs, output path selection, save format, pending job queue, live run log
- **Results Library tab**: library summary, output file browser, record table, detail pane, search
- **Logs & Help tab**: quick start guidance and activity log

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts/smoke_test.py
python -m open_scrapers_desk.app
```

If the module launch form does not work in your shell, this also works:

```bash
set PYTHONPATH=src
python src/open_scrapers_desk/app.py
```

## Toolkit setup

The toolkit repo should already be installed and built:

```bash
cd g:\Scrapers
npm install
npm run build
```

Then in the desktop app set:

- `Toolkit path`
- `Node executable`
- `Output directory`
- `Default save format`

## Packaging the Windows executable

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

This creates a Windows app bundle in `dist/OpenScrapersDesk/`.

The GitHub Actions workflow also creates a zipped artifact:

- `.github/workflows/build-windows.yml`

## Documentation

- [Desktop setup](docs/setup.md)
- [Architecture](docs/architecture.md)
- [Toolkit connection guide](docs/toolkit-connection.md)
- [Packaging and release guide](docs/packaging.md)
- [Publishing checklist](docs/publishing.md)
- [Release workflow](docs/release-workflow.md)
- [Wiki source pages](docs/wiki/Home.md)

## License

MIT
