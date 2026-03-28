from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ScraperParameter:
  key: str
  description: str
  example: str = ""
  required: bool = False


@dataclass(slots=True)
class ScraperSummary:
  id: str
  category: str
  name: str
  description: str
  homepage: str
  source_name: str = ""
  params: list[ScraperParameter] = field(default_factory=list)


@dataclass(slots=True)
class BackendStatus:
  node_ok: bool
  toolkit_ok: bool
  cli_mode: str
  node_version: str = ""
  message: str = ""


@dataclass(slots=True)
class AppSettings:
  toolkit_path: str = ""
  node_executable: str = "node"
  output_dir: str = ""
  kofi_url: str = ""
  alert_webhook_url: str = ""
  alert_discord_webhook_url: str = ""
  discord_format_preset: str = "rich"
  first_run_completed: bool = False
  save_format: str = "json"
  last_scraper_id: str = ""
  last_category: str = "all"
  active_workspace: str = ""
  workspaces: list["WorkspaceProfile"] = field(default_factory=list)


@dataclass(slots=True)
class WorkspaceProfile:
  name: str
  toolkit_path: str
  node_executable: str
  output_dir: str
  save_format: str = "json"


@dataclass(slots=True)
class SourceHealthRecord:
  scraper_id: str
  title: str
  category: str
  source: str
  status: str
  duration_ms: str = ""
  records: str = ""
  summary: str = ""


@dataclass(slots=True)
class ResultRecord:
  id: str
  title: str
  source: str
  url: str = ""
  summary: str = ""
  published_at: str = ""
  authors: list[str] = field(default_factory=list)
  tags: list[str] = field(default_factory=list)
  location: str = ""
  metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ResultPayload:
  scraper_id: str
  scraper_name: str
  category: str
  source: str
  fetched_at: str
  records: list[ResultRecord]
  meta: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ResultFileSummary:
  path: Path
  scraper_id: str
  scraper_name: str
  category: str
  source: str
  fetched_at: str
  record_count: int
