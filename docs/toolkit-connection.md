# Toolkit Connection Guide

Open Scrapers Desk expects the separate toolkit repo to exist locally.

Recommended workflow:

1. Clone `open-scrapers-toolkit`
2. Run `npm install`
3. Run `npm run build`
4. Open the desktop app
5. Set `Toolkit path`, `Node executable`, and `Output directory`
6. Refresh backend status and source health

The app uses the toolkit CLI for:

- catalog loading
- scraper runs
- batch runs
- source-health reporting
