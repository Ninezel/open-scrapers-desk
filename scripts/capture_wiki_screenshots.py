from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from open_scrapers_desk.models import AppSettings
from open_scrapers_desk.ui.main_window import MainWindow


def find_toolkit_root() -> Path:
  env_path = os.environ.get("OPEN_SCRAPERS_TOOLKIT_PATH")
  if env_path:
    return Path(env_path).resolve()

  candidates = [
    ROOT.parent / "Scrapers",
    ROOT.parent / "open-scrapers-toolkit",
  ]

  for candidate in candidates:
    if (candidate / "package.json").exists() and (candidate / "src" / "cli.ts").exists():
      return candidate.resolve()

  raise FileNotFoundError(
    "Could not find the toolkit repository. Set OPEN_SCRAPERS_TOOLKIT_PATH to continue."
  )


class MemorySettingsStore:
  def __init__(self, settings: AppSettings) -> None:
    self._settings = settings

  def load(self) -> AppSettings:
    return self._settings

  def save(self, settings: AppSettings) -> None:
    self._settings = settings


def select_scraper(window: MainWindow, scraper_id: str) -> None:
  for row in range(window.scraper_list.count()):
    item = window.scraper_list.item(row)
    if item.data(Qt.ItemDataRole.UserRole) == scraper_id:
      window.scraper_list.setCurrentRow(row)
      return


def select_result_file(window: MainWindow, filename: str) -> None:
  for row, summary in enumerate(window.result_files):
    if summary.path.name == filename:
      window.result_files_table.selectRow(row)
      return


def capture_window(window: MainWindow, path: Path) -> None:
  window.repaint()
  QApplication.processEvents()
  path.parent.mkdir(parents=True, exist_ok=True)
  window.grab().save(str(path))


def main() -> int:
  toolkit_root = find_toolkit_root()
  output_dir = toolkit_root / "output"

  settings = AppSettings(
    toolkit_path=str(toolkit_root),
    node_executable="node",
    output_dir=str(output_dir),
    kofi_url="https://ko-fi.com/ninezel",
    last_scraper_id="open-meteo-city-forecast",
    last_category="all",
  )

  app = QApplication(sys.argv)
  window = MainWindow(MemorySettingsStore(settings))
  window.resize(1520, 940)
  window.show()
  QApplication.processEvents()

  images_dir = ROOT / "docs" / "wiki" / "images"

  window.tabs.setCurrentIndex(0)
  QApplication.processEvents()
  capture_window(window, images_dir / "desk-overview.png")

  window.tabs.setCurrentIndex(1)
  QApplication.processEvents()
  select_scraper(window, "open-meteo-city-forecast")
  QApplication.processEvents()
  if "latitude" in window.param_inputs:
    window.param_inputs["latitude"].setText("51.5072")
  if "longitude" in window.param_inputs:
    window.param_inputs["longitude"].setText("-0.1276")
  if "label" in window.param_inputs:
    window.param_inputs["label"].setText("London")
  if "timezone" in window.param_inputs:
    window.param_inputs["timezone"].setText("Europe/London")
  capture_window(window, images_dir / "desk-run-tab.png")

  window.tabs.setCurrentIndex(2)
  QApplication.processEvents()
  select_result_file(window, "nasa-image-of-the-day.json")
  QApplication.processEvents()
  if window.record_table.rowCount() > 0:
    window.record_table.selectRow(0)
  QApplication.processEvents()
  capture_window(window, images_dir / "desk-results-library.png")

  window.tabs.setCurrentIndex(3)
  QApplication.processEvents()
  capture_window(window, images_dir / "desk-logs-help.png")

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
