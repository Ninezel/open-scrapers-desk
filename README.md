# Open Scrapers Desk

Open Scrapers Desk is a PyQt desktop application for people who want to use the Open Scrapers ecosystem without living in a terminal. It connects to the separate scraper backend repository, lets users run scraper jobs from a GUI, and presents saved JSON results in a readable workspace.

This repository is intentionally separate from the scraper engine:

- Backend repo: `open-scrapers-toolkit`
- Desktop repo: `open-scrapers-desk`

That split keeps the scrapers reusable for developers while giving non-programmers a clean app to work with.

## What the desktop app does

- connects to an Open Scrapers Toolkit checkout
- validates the Node and toolkit environment
- loads the scraper catalog from the backend
- runs a selected scraper, a whole category, or the full catalog
- scans JSON output folders automatically
- shows records in a searchable desktop UI
- displays summaries, metadata, links, tags, and source details

## Desktop features

- **Overview tab**: toolkit path, node path, output folder, health checks, latest files
- **Run Scrapers tab**: scraper list, parameter inputs, output path selection, live run log
- **Results Library tab**: output file browser, record table, detail pane, search
- **Logs & Help tab**: quick start guidance and activity log

## Repository relationship

This app expects the backend toolkit repository to exist separately. The recommended workflow is:

1. Clone `open-scrapers-toolkit`
2. Run `npm install`
3. Run `npm run build`
4. Clone this repository
5. Start Open Scrapers Desk and point it to the toolkit path

The app will also use `npx tsx src/cli.ts` when available, which makes local development friendlier if the toolkit `dist/` output is stale.

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

## Packaging the Windows executable

Build the desktop executable with PyInstaller:

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

This creates a Windows app bundle in `dist/OpenScrapersDesk/`.

If you want a traditional installer, use the included Inno Setup script:

```text
installer/OpenScrapersDesk.iss
```

Compile it with Inno Setup after building the PyInstaller output.

## GitHub automation

This repo includes a Windows build workflow:

- [.github/workflows/build-windows.yml](.github/workflows/build-windows.yml)

It can build the app on tag pushes and upload the desktop bundle as a GitHub Actions artifact.

## Documentation

- [Desktop setup](docs/setup.md)
- [Architecture](docs/architecture.md)
- [Toolkit connection guide](docs/toolkit-connection.md)
- [Packaging and release guide](docs/packaging.md)
- [Publishing checklist](docs/publishing.md)
- [Wiki source pages](docs/wiki/Home.md)

## Why PyQt

PyQt gives the project:

- a native-feeling Windows desktop interface
- a mature packaging path for `.exe` builds
- strong layout and table widgets for reading data-heavy outputs
- a low-friction path for future charts, export tools, and dashboards

## Roadmap

- richer visual summaries and charts
- background job queueing
- saved workspaces
- source health indicators
- release signing and installer automation

## License

MIT
