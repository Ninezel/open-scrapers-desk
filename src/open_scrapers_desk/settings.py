from __future__ import annotations

import json
import os
from pathlib import Path

from .models import AppSettings


COMMON_TOOLKIT_NAMES = [
  "Scrapers",
  "open-scrapers-toolkit",
  "OpenScrapersToolkit",
  "OpenScrapers",
]


def default_kofi_url() -> str:
  return os.environ.get("OPEN_SCRAPERS_KOFI_URL", "").strip()


def normalize_url(value: str) -> str:
  url = value.strip()
  if not url:
    return ""
  if url.startswith(("http://", "https://")):
    return url
  return f"https://{url}"


def app_data_dir() -> Path:
  base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
  path = base / "OpenScrapersDesk"
  path.mkdir(parents=True, exist_ok=True)
  return path


def config_path() -> Path:
  return app_data_dir() / "settings.json"


def is_toolkit_path(path: Path) -> bool:
  return (path / "package.json").exists() and (
    (path / "dist" / "cli.js").exists() or (path / "src" / "cli.ts").exists()
  )


def find_default_toolkit_path() -> str:
  env_path = os.environ.get("OPEN_SCRAPERS_TOOLKIT_PATH")
  if env_path and is_toolkit_path(Path(env_path)):
    return str(Path(env_path).resolve())

  module_path = Path(__file__).resolve()
  repo_root = module_path.parents[2]
  search_root = repo_root.parent if len(module_path.parents) > 3 else repo_root
  candidates: list[Path] = [Path.cwd(), Path.cwd().parent, repo_root, search_root]
  seen: set[Path] = set()

  for base in candidates:
    for candidate in [base, *[base / name for name in COMMON_TOOLKIT_NAMES]]:
      resolved = candidate.resolve()
      if resolved in seen:
        continue
      seen.add(resolved)
      if is_toolkit_path(resolved):
        return str(resolved)

  return ""


def default_output_dir(toolkit_path: str) -> str:
  if toolkit_path:
    return str((Path(toolkit_path) / "output").resolve())
  return str((app_data_dir() / "output").resolve())


class SettingsStore:
  def __init__(self) -> None:
    self._path = config_path()

  def load(self) -> AppSettings:
    if not self._path.exists():
      toolkit_path = find_default_toolkit_path()
      settings = AppSettings(
        toolkit_path=toolkit_path,
        output_dir=default_output_dir(toolkit_path),
        kofi_url=default_kofi_url(),
      )
      self.save(settings)
      return settings

    raw = json.loads(self._path.read_text(encoding="utf-8"))
    toolkit_path = raw.get("toolkit_path") or find_default_toolkit_path()
    output_dir = raw.get("output_dir") or default_output_dir(toolkit_path)

    return AppSettings(
      toolkit_path=toolkit_path,
      node_executable=raw.get("node_executable", "node"),
      output_dir=output_dir,
      kofi_url=normalize_url(raw.get("kofi_url", "") or default_kofi_url()),
      last_scraper_id=raw.get("last_scraper_id", ""),
      last_category=raw.get("last_category", "all"),
    )

  def save(self, settings: AppSettings) -> None:
    payload = {
      "toolkit_path": settings.toolkit_path,
      "node_executable": settings.node_executable,
      "output_dir": settings.output_dir,
      "kofi_url": normalize_url(settings.kofi_url),
      "last_scraper_id": settings.last_scraper_id,
      "last_category": settings.last_category,
    }
    self._path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
