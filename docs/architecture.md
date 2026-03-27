# Architecture

Open Scrapers Desk is a thin desktop layer over the Open Scrapers Toolkit backend.

## High-level flow

1. User configures toolkit path and node executable.
2. The app validates the backend.
3. The app loads the scraper catalog by calling the toolkit CLI.
4. The user launches scraper jobs from the desktop UI.
5. The app reads JSON output files and presents them in a structured view.

## Key modules

- `src/open_scrapers_desk/app.py`
  - app entry point
- `src/open_scrapers_desk/ui/main_window.py`
  - main UI and process handling
- `src/open_scrapers_desk/backend.py`
  - bridge to the Node CLI
- `src/open_scrapers_desk/results.py`
  - result scanning and parsing
- `src/open_scrapers_desk/settings.py`
  - persistent desktop settings
- `src/open_scrapers_desk/style.py`
  - app stylesheet

## Backend integration strategy

The desktop app prefers the toolkit source mode when available:

- `npx tsx src/cli.ts`

It falls back to the compiled CLI when needed:

- `node dist/cli.js`

That gives developers a smoother experience while still supporting packaged releases.

## Why a separate repository

- the scraper engine stays reusable on its own
- desktop packaging does not complicate the toolkit repo
- developers can depend on the toolkit without taking on a GUI stack
- non-programmers get a dedicated product surface
