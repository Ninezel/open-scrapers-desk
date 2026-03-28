# Discord Bot Bridge

Open Scrapers Desk includes a lightweight Python bridge for Discord bots that want to reuse the toolkit scrapers without writing their own subprocess wrapper.

## What this bridge is for

Use this repo when you want Python-side integrations such as:

- `discord.py`, `py-cord`, `nextcord`, or similar bots
- scheduled posting scripts
- moderation or announcement bots that pull public data on demand
- internal Python automation that wants the toolkit outputs without reimplementing the CLI orchestration

## What this bridge is not

The bridge does not replace the toolkit itself. It depends on a local `open-scrapers-toolkit` checkout and uses the toolkit CLI under the hood.

If you want direct Node usage instead, use the toolkit repo's own TypeScript library exports.

## Install

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

## Prepare the toolkit

```bash
cd g:\Scrapers
npm install
npm run build
```

You also need:

- a working `node` executable
- a local path to the toolkit checkout

## Typical bridge flow

1. Keep a local toolkit checkout ready.
2. Call `run_scraper_payload()` if you want the normalized result object in Python.
3. Call `payload_to_discord_messages()` if you want to format an existing payload.
4. Call `run_scraper_to_discord_messages()` if you want one function to both scrape and format.
5. Call `run_scraper_to_preset_messages()` if you want a quick compact, rich, or alert-style format.
6. Send the resulting payload dictionaries through your Discord library.

## Function guide

### `run_scraper_payload()`

Use this when you want the raw normalized payload:

```python
from open_scrapers_desk.discord_bridge import run_scraper_payload

payload = run_scraper_payload(
  r"g:\Scrapers",
  "node",
  "world-bank-gdp",
  limit=1,
  params={"country": "GBR"},
)
```

### `payload_to_discord_messages()`

Use this when you already have a payload and only want Discord formatting:

```python
from open_scrapers_desk.discord_bridge import payload_to_discord_messages
```

### `run_scraper_to_discord_messages()`

Use this for the common bot-command path:

```python
from open_scrapers_desk.discord_bridge import run_scraper_to_discord_messages

messages = run_scraper_to_discord_messages(
  r"g:\Scrapers",
  "node",
  "bbc-world-news",
  limit=3,
)
```

### `run_scraper_to_preset_messages()`

Use this when you want a built-in formatting preset:

```python
from open_scrapers_desk.discord_bridge import run_scraper_to_preset_messages

messages = run_scraper_to_preset_messages(
  r"g:\Scrapers",
  "node",
  "bbc-world-news",
  preset="compact",
)
```

## Returned payload shape

Each returned item is a plain dictionary shaped like:

```python
{
  "content": "...",
  "embeds": [
    {
      "title": "...",
      "description": "...",
      "fields": [...],
      "footer": {"text": "..."},
      "timestamp": "..."
    }
  ]
}
```

This keeps the bridge flexible across Discord libraries.

## Full command example

Starter example:

- `examples/discord-bots/discord-py-message-command.py`
- `examples/discord-bots/discord-preset-command.py`

## Presets

Built-in presets:

- `compact`
- `rich`
- `alerts`

Use them through `run_scraper_to_preset_messages()` when you want channel-ready defaults without repeating the same formatting arguments in every command handler.

The basic flow is:

1. receive a command such as `!scrape bbc-world-news`
2. call `run_scraper_to_discord_messages()`
3. turn each embed dictionary into a Discord embed object
4. reply with the returned content and embeds

## Good usage practices

- Keep result limits low for chat commands.
- Avoid exposing every scraper to every channel by default.
- Validate user-supplied scraper IDs or maintain an allowlist.
- Keep the toolkit built and ready so bot commands stay fast.
- Remember that source-health and result availability depend on the upstream public endpoints.

## Automation example

See:

- `examples/automation/scheduled-discord-webhook.py`

This example shows a Python-side scheduled workflow that runs a scraper through the bridge, formats the result with a preset, and posts the messages to a Discord webhook using only the standard library.

## Related docs

- `docs/setup.md`
- `docs/toolkit-connection.md`
- `docs/roadmap.md`
