# Architecture

Important modules:

- `src/open_scrapers_desk/app.py`: app entry point
- `src/open_scrapers_desk/ui/main_window.py`: main window and user workflows
- `src/open_scrapers_desk/backend.py`: CLI integration with the toolkit repo
- `src/open_scrapers_desk/results.py`: result scanning, loading, filtering, and summaries
- `src/open_scrapers_desk/settings.py`: persistent settings and workspace storage
- `src/open_scrapers_desk/models.py`: shared dataclasses

## Data flow

1. The app loads settings and saved workspaces.
2. It validates the toolkit path and Node runtime.
3. It reads the scraper catalog from `open-scrapers-toolkit`.
4. It builds CLI commands for run and batch actions.
5. It queues jobs and executes them sequentially through `QProcess`.
6. It scans saved outputs and renders both record-level and library-level summaries.
