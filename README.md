# Open Scrapers Desk

Open Scrapers Desk is a PyQt desktop application for people who want to use the Open Scrapers ecosystem without living in a terminal. It connects to the separate scraper backend repository, lets users queue scraper jobs from a GUI, and presents saved outputs in a readable workspace.

Repository split:

- Backend repo: `https://github.com/Ninezel/open-scrapers-toolkit`
- Desktop repo: `https://github.com/Ninezel/open-scrapers-desk`
- The desktop repo now also exposes a lightweight Python bridge for Discord bots that want to run toolkit scrapers and turn the results into Discord-ready payloads.
- The Python bridge now also supports prompt-driven Discord flows, so Python bots can ask the toolkit for weather, research, reports, and news without hard-coding scraper IDs.

## What the desktop app does

- connects to an Open Scrapers Toolkit checkout
- validates the Node and toolkit environment
- loads the scraper catalog from the backend
- queues a selected scraper, a whole category, or the full catalog
- shows source-health status from the toolkit `health` command
- scans result folders automatically
- displays dashboard-style summary views for the whole library and individual result payloads
- compares two saved result payloads side by side
- stores saved workspaces for different toolkit/output combinations
- exposes Python helper functions for Discord bots and automation scripts
- previews run and health-alert automation commands
- provides Discord formatting presets for Python-side integrations
- produces both a zip bundle and SHA256 checksum during local Windows packaging
- includes a configurable Ko-fi support button

Default support link:

- `https://ko-fi.com/ninezel`

## Desktop features

- **Overview tab**: toolkit path, node path, output folder, default save format, saved workspaces, source-health snapshot, alert webhook settings, latest files
- **Run Scrapers tab**: scraper list, parameter inputs, output path selection, save format, pending job queue, live run log, automation command previews
- **Results Library tab**: dashboard summaries, output file browser, compare view, record table, detail pane, search
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

## Use it as a Python bridge for Discord bots

Install from GitHub:

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

Then use the bridge with a local `open-scrapers-toolkit` checkout:

```python
from open_scrapers_desk.discord_bridge import run_scraper_to_discord_messages

messages = run_scraper_to_discord_messages(
  r"g:\Scrapers",
  "node",
  "bbc-world-news",
  limit=3,
)
```

Preset-based bridge helper:

```python
from open_scrapers_desk.discord_bridge import run_scraper_to_preset_messages
```

Prompt-driven bridge helpers:

```python
from open_scrapers_desk.discord_bridge import (
  resolve_prompt,
  run_prompt_to_discord_messages,
  run_prompt_to_preset_messages,
)
```

Starter example:

- `examples/discord-bots/discord-py-message-command.py`
- `examples/discord-bots/discord-prompt-command.py`
- `examples/discord-bots/discord-preset-command.py`
- `examples/automation/scheduled-discord-webhook.py`

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

## Environment variables and examples

This repo does not auto-load `.env` files by default. `.env.example` is included as a reference for shells, CI jobs, IDE launchers, or your own dotenv setup.

Common variables:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_NODE`
- `OPEN_SCRAPERS_KOFI_URL`
- `OPEN_SCRAPERS_SCRAPER_ID`
- `OPEN_SCRAPERS_DISCORD_WEBHOOK_URL`
- `OPEN_SCRAPERS_SKIP_ONBOARDING`
- `DISCORD_PREFIX`
- `DISCORD_TOKEN`

## Packaging the Windows executable

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

This creates a Windows app bundle in `dist/OpenScrapersDesk/`.

It also creates:

- `release/OpenScrapersDesk-windows.zip`
- `release/OpenScrapersDesk-windows.zip.sha256`

The GitHub Actions workflow also creates a zipped artifact:

- `.github/workflows/build-windows.yml`

## Documentation

- [Desktop setup](docs/setup.md)
- [Environment variables](docs/environment-variables.md)
- [Architecture](docs/architecture.md)
- [Toolkit connection guide](docs/toolkit-connection.md)
- [Discord bot bridge](docs/discord-bots.md)
- [Roadmap](docs/roadmap.md)
- [Packaging and release guide](docs/packaging.md)
- [Publishing checklist](docs/publishing.md)
- [Release workflow](docs/release-workflow.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Wiki source pages](docs/wiki/Home.md)

## Next roadmap focus

Current next-step priorities for the desktop repo are:

- recurring job execution instead of command previews alone
- richer publish flows around Discord and generic webhooks
- keep the Python bridge aligned with the toolkit prompt-routing and slash-command workflow
- more polished installer and signing workflows
- more onboarding, troubleshooting, and accessibility improvements

The fuller planning notes live in [docs/roadmap.md](docs/roadmap.md).

## License

MIT
