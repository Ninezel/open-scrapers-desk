# Discord Bot Bridge

Open Scrapers Desk includes a lightweight Python bridge that lets Discord bots run toolkit scrapers and format the results into Discord-style payload objects.

## Install

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

The bridge examples read normal process environment variables. They do not auto-load `.env` files on their own.

## Toolkit requirement

The bridge still needs:

- a local `open-scrapers-toolkit` checkout
- a working `node` runtime
- the toolkit installed and built

## Main helpers

- `run_scraper_payload()`
- `payload_to_discord_messages()`
- `run_scraper_to_discord_messages()`
- `run_scraper_to_preset_messages()`

Built-in presets:

- `compact`
- `rich`
- `alerts`

## Example

```python
from open_scrapers_desk.discord_bridge import run_scraper_to_discord_messages

messages = run_scraper_to_discord_messages(
  r"g:\Scrapers",
  "node",
  "bbc-world-news",
  limit=3,
)
```

Returned payloads are plain dictionaries so they can be adapted to `discord.py` and compatible libraries without extra glue code.

Starter file:

- `examples/discord-bots/discord-py-message-command.py`
- `examples/discord-bots/discord-preset-command.py`
- `examples/automation/scheduled-discord-webhook.py`

Useful example variables:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_NODE`
- `OPEN_SCRAPERS_SCRAPER_ID`
- `OPEN_SCRAPERS_DISCORD_WEBHOOK_URL`
- `DISCORD_PREFIX`
- `DISCORD_TOKEN`

Related pages:

- [Connecting To The Toolkit](Connecting-to-the-Toolkit)
- [Roadmap](Roadmap)
