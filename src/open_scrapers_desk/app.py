from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .settings import SettingsStore
from .style import APP_STYLE
from .ui.main_window import MainWindow


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
