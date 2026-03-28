from __future__ import annotations

import json
import os
from urllib import request

from open_scrapers_desk.discord_bridge import run_scraper_to_preset_messages

TOOLKIT_PATH = os.environ.get("OPEN_SCRAPERS_TOOLKIT_PATH", r"g:\Scrapers")
NODE_EXECUTABLE = os.environ.get("OPEN_SCRAPERS_NODE", "node")
SCRAPER_ID = os.environ.get("OPEN_SCRAPERS_SCRAPER_ID", "bbc-world-news")
DISCORD_WEBHOOK_URL = os.environ.get("OPEN_SCRAPERS_DISCORD_WEBHOOK_URL", "")


def post_message(webhook_url: str, payload: dict) -> None:
  data = json.dumps(payload).encode("utf-8")
  webhook_request = request.Request(
    webhook_url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
  )
  with request.urlopen(webhook_request, timeout=30) as response:  # noqa: S310
    print(response.status)


def main() -> None:
  if not DISCORD_WEBHOOK_URL:
    raise RuntimeError("Set OPEN_SCRAPERS_DISCORD_WEBHOOK_URL before running this example.")

  messages = run_scraper_to_preset_messages(
    TOOLKIT_PATH,
    NODE_EXECUTABLE,
    SCRAPER_ID,
    preset="rich",
    limit=3,
  )

  for message in messages:
    post_message(DISCORD_WEBHOOK_URL, message)


if __name__ == "__main__":
  main()
