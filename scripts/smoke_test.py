from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, "src")

from PyQt6.QtWidgets import QApplication

from open_scrapers_desk.discord_bridge import (
  payload_to_discord_messages,
  run_prompt_to_preset_messages,
)
from open_scrapers_desk.models import ResultPayload, ResultRecord
from open_scrapers_desk.settings import SettingsStore
from open_scrapers_desk.ui.main_window import MainWindow


def main() -> None:
  messages = payload_to_discord_messages(
    ResultPayload(
      scraper_id="smoke-test",
      scraper_name="Smoke Test",
      category="reports",
      source="Open Scrapers",
      fetched_at="2026-03-28T14:00:00.000Z",
      records=[
        ResultRecord(
          id="record-1",
          title="Smoke test record",
          source="Open Scrapers",
          summary="Smoke test summary",
        )
      ],
    )
  )
  print(len(messages))
  print(callable(run_prompt_to_preset_messages))

  app = QApplication([])
  window = MainWindow(SettingsStore())
  print(window.windowTitle())
  window.close()


if __name__ == "__main__":
  main()
