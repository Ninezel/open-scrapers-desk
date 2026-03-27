from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

# Support both package execution and direct script execution.
if __package__ in {None, ""}:
  sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from open_scrapers_desk.settings import SettingsStore
from open_scrapers_desk.style import APP_STYLE
from open_scrapers_desk.ui.main_window import MainWindow


def main() -> int:
  app = QApplication(sys.argv)
  app.setApplicationName("Open Scrapers Desk")
  app.setOrganizationName("Open Scrapers")
  app.setStyleSheet(APP_STYLE)

  window = MainWindow(SettingsStore())
  window.show()
  return app.exec()


if __name__ == "__main__":
  raise SystemExit(main())
