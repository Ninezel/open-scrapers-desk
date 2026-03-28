# Environment Variables

Open Scrapers Desk does not auto-load `.env` files by default.

Use `.env.example` as a reference if you want to supply variables through your shell, IDE, CI job, or your own dotenv loader.

Main variables:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_NODE`
- `OPEN_SCRAPERS_KOFI_URL`
- `OPEN_SCRAPERS_SCRAPER_ID`
- `OPEN_SCRAPERS_DISCORD_WEBHOOK_URL`
- `OPEN_SCRAPERS_SKIP_ONBOARDING`
- `QT_QPA_PLATFORM`
- `DISCORD_PREFIX`
- `DISCORD_TOKEN`

Headless/testing:

- `QT_QPA_PLATFORM=offscreen`

For everyday GUI use, most settings are stored by the app itself rather than read from environment variables on each launch.
