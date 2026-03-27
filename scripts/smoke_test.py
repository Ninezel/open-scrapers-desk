from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, "src")

from PyQt6.QtWidgets import QApplication

from open_scrapers_desk.settings import SettingsStore
from open_scrapers_desk.ui.main_window import MainWindow


def main() -> None:
  app = QApplication([])
  window = MainWindow(SettingsStore())
  print(window.windowTitle())
  window.close()


if __name__ == "__main__":
  main()
