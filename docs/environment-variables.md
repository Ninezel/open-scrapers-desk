# Environment Variables

This page lists the main environment variables used by Open Scrapers Desk and its example scripts.

## `.env` behavior

Open Scrapers Desk does not auto-load `.env` files by default.

Use `.env.example` as a reference if you want to:

- set variables in your shell profile
- configure an IDE launch profile
- feed variables into CI or scheduled jobs
- use your own dotenv loader

## Desktop app overrides

- `OPEN_SCRAPERS_TOOLKIT_PATH`
  Default toolkit checkout path used by the app settings loader.
- `OPEN_SCRAPERS_KOFI_URL`
  Overrides the default Ko-fi link shown by the desktop app.
- `OPEN_SCRAPERS_SKIP_ONBOARDING`
  When set to `1`, skips the first-run onboarding dialog.

## Python bridge and automation examples

- `OPEN_SCRAPERS_TOOLKIT_PATH`
  Toolkit checkout used by the bridge examples.
- `OPEN_SCRAPERS_NODE`
  Node executable used to run the toolkit CLI.
- `OPEN_SCRAPERS_SCRAPER_ID`
  Scraper ID used by the scheduled webhook example.
- `OPEN_SCRAPERS_DISCORD_WEBHOOK_URL`
  Discord webhook target for the scheduled webhook example.
- `DISCORD_PREFIX`
  Prefix used by the sample `discord.py` message-command example.
- `DISCORD_TOKEN`
  Bot token used by the sample `discord.py` example.

## Testing and headless runs

- `QT_QPA_PLATFORM`
  Use `offscreen` for headless smoke tests or screenshot-free CI runs.

For normal desktop use, you usually only need the saved app settings rather than environment variables.
