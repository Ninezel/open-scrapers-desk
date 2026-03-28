# Toolkit Connection Guide

Open Scrapers Desk expects the separate toolkit repo to exist locally.

Recommended workflow:

1. Clone `open-scrapers-toolkit`
2. Run `npm install`
3. Run `npm run build`
4. Open the desktop app
5. Set `Toolkit path`, `Node executable`, and `Output directory`
6. Refresh backend status and source health

Useful environment overrides when launching the app or examples:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_NODE`

The app uses the toolkit CLI for:

- catalog loading
- scraper runs
- batch runs
- source-health reporting
- automation command previews for run and health workflows

The Python Discord bridge in this repo also uses the toolkit CLI under the hood so bot integrations stay aligned with the same scraper behavior as the desktop app.
