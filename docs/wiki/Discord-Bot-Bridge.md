# Discord Bot Bridge

Open Scrapers Desk includes a lightweight Python bridge that lets Discord bots run toolkit scrapers and format the results into Discord-style payload objects.

## Install

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```

## Toolkit requirement

The bridge still needs:

- a local `open-scrapers-toolkit` checkout
- a working `node` runtime
- the toolkit installed and built

## Main helpers

- `run_scraper_payload()`
- `payload_to_discord_messages()`
- `run_scraper_to_discord_messages()`

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

Related pages:

- [Connecting To The Toolkit](Connecting-to-the-Toolkit)
- [Roadmap](Roadmap)
