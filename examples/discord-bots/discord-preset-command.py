from __future__ import annotations

from open_scrapers_desk.discord_bridge import run_scraper_to_preset_messages

TOOLKIT_PATH = r"g:\Scrapers"
NODE_EXECUTABLE = "node"


def build_messages(scraper_id: str) -> list[dict]:
  return run_scraper_to_preset_messages(
    TOOLKIT_PATH,
    NODE_EXECUTABLE,
    scraper_id,
    preset="compact",
    limit=2,
  )


if __name__ == "__main__":
  payloads = build_messages("bbc-world-news")
  for payload in payloads:
    print(payload)
