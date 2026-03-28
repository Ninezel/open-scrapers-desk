# Discord Bot Bridge

Open Scrapers Desk now includes a lightweight Python bridge for Discord bots that want to reuse the toolkit scrapers without building their own CLI wrapper.

## Install

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

This installs the Python package layer. Your bot still needs a local checkout of `open-scrapers-toolkit` because the bridge runs the toolkit CLI underneath.

## Basic flow

1. Keep a local copy of `open-scrapers-toolkit`
2. Make sure `node` and the toolkit are available
3. Call `run_scraper_payload()` or `run_scraper_to_discord_messages()`
4. Send the returned payloads with `discord.py`, `py-cord`, `nextcord`, or a compatible library

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

Each returned item looks like a Discord-style payload:

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

## Available helpers

- `run_scraper_payload()`
- `record_to_discord_embed()`
- `payload_to_discord_messages()`
- `run_scraper_to_discord_messages()`

## Starter example

- `examples/discord-bots/discord-py-message-command.py`

## Notes

- Keep result limits low for chat commands.
- The bridge depends on a working toolkit checkout, not just the desktop app itself.
- The bridge intentionally returns plain dictionaries so it stays flexible across Discord libraries.
