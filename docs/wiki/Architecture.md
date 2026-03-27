# Architecture

Open Scrapers Desk is a thin desktop layer over the Open Scrapers Toolkit backend. The application does not embed the scraper engine. Instead, it coordinates with the separate toolkit repository, runs CLI commands in a child process, and renders the resulting JSON in a desktop UI.

## High-level flow

1. The app loads saved settings.
2. The user configures the toolkit path, Node runtime, output directory, and Ko-fi link.
3. The app validates the backend.
4. The app loads the scraper catalog using `list --format json`.
5. The user launches scraper runs from the UI.
6. The app reads saved JSON files from disk and presents them in a searchable library.

## Main modules

### `src/open_scrapers_desk/app.py`

The application entrypoint. It creates the Qt application, applies styling, and opens the main window. It also supports both package-style and direct-script execution so packaged builds work reliably.

### `src/open_scrapers_desk/ui/main_window.py`

This is the primary UI controller. It builds the four-tab layout and owns:

- settings form wiring
- backend refresh actions
- scraper catalog display
- run-process orchestration
- result table and detail rendering
- activity logging
- Ko-fi button actions

### `src/open_scrapers_desk/backend.py`

This module bridges the GUI to the Node toolkit. It:

- validates the toolkit path
- checks the Node runtime
- determines whether `tsx` or `dist` mode should be used
- loads the catalog
- builds command lines for single and batch runs

### `src/open_scrapers_desk/results.py`

This module scans output directories, loads JSON payloads, normalizes them into desktop-side data classes, and provides record filtering helpers.

### `src/open_scrapers_desk/settings.py`

This module handles:

- settings-file location
- default toolkit discovery
- default output-directory logic
- Ko-fi URL normalization and defaults

### `src/open_scrapers_desk/models.py`

Contains the small data classes used across the application for:

- settings
- backend status
- scraper summaries
- result summaries
- result payloads and records

## Backend integration strategy

The app prefers:

```text
npx tsx src/cli.ts ...
```

When source mode is available because that reflects the latest toolkit source immediately.

It can fall back to:

```text
node dist/cli.js ...
```

when a compiled CLI is available and source mode is not preferred or possible.

## Process model

The app launches scraper jobs through `QProcess`, which gives the UI:

- non-blocking execution
- live stdout capture
- live stderr capture
- exit-code visibility

This is why run logs appear in real time instead of only after a command finishes.

## Result-reading model

The desktop app does not parse each upstream source directly. It reads the normalized JSON already produced by the toolkit. That keeps responsibilities clean:

- toolkit handles source fetching and normalization
- desktop app handles browsing and presentation

## Why the repository is separate

The separate-repo design keeps the ecosystem healthier:

- developers can reuse the toolkit without GUI dependencies
- the desktop app can package independently
- backend and GUI concerns stay easier to reason about
- public releases can target different audiences without mixing stacks

## Related pages

- [Connecting to the Toolkit](Connecting-to-the-Toolkit.md)
- [Using the Desktop App](Using-the-Desktop-App.md)
- [Packaging Windows Builds](Packaging-Windows-Builds.md)
