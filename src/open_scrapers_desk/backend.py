from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from .models import BackendStatus, ScraperParameter, ScraperSummary, SourceHealthRecord
from .settings import is_toolkit_path


def _npx_program() -> str | None:
  candidates = ["npx.cmd", "npx.exe", "npx"] if os.name == "nt" else ["npx"]
  for candidate in candidates:
    path = shutil.which(candidate)
    if path:
      return path
  return None


def _cli_invocation(
  toolkit_path: Path,
  node_executable: str,
  *,
  prefer_source: bool = True,
) -> tuple[str, list[str], Path, str]:
  dist_cli = toolkit_path / "dist" / "cli.js"
  src_cli = toolkit_path / "src" / "cli.ts"
  npx_program = _npx_program()

  if prefer_source and src_cli.exists() and npx_program:
    return npx_program, ["tsx", "src/cli.ts"], toolkit_path, "tsx"

  if dist_cli.exists():
    return node_executable, [str(dist_cli)], toolkit_path, "dist"

  if src_cli.exists() and npx_program:
    return npx_program, ["tsx", "src/cli.ts"], toolkit_path, "tsx"

  raise FileNotFoundError(
    "Could not find a runnable scraper CLI. Build the toolkit with 'npm install' and 'npm run build', "
    "or make sure 'npx' is available."
  )


def validate_backend(toolkit_path: str, node_executable: str) -> BackendStatus:
  path = Path(toolkit_path) if toolkit_path else Path()
  if not toolkit_path or not is_toolkit_path(path):
    return BackendStatus(
      node_ok=False,
      toolkit_ok=False,
      cli_mode="missing",
      message="Toolkit path is missing or does not point to an Open Scrapers Toolkit checkout.",
    )

  try:
    node_result = subprocess.run(
      [node_executable, "--version"],
      check=True,
      capture_output=True,
      text=True,
      timeout=15,
    )
    node_version = node_result.stdout.strip()
  except Exception as error:  # noqa: BLE001
    return BackendStatus(
      node_ok=False,
      toolkit_ok=True,
      cli_mode="missing",
      message=f"Node runtime check failed: {error}",
    )

  try:
    _, _, _, cli_mode = _cli_invocation(path, node_executable)
  except Exception as error:  # noqa: BLE001
    return BackendStatus(
      node_ok=True,
      toolkit_ok=True,
      cli_mode="missing",
      node_version=node_version,
      message=str(error),
    )

  return BackendStatus(
    node_ok=True,
    toolkit_ok=True,
    cli_mode=cli_mode,
    node_version=node_version,
    message="Backend is ready.",
  )


def list_scrapers(toolkit_path: str, node_executable: str) -> list[ScraperSummary]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  command = [program, *base_args, "list", "--format", "json"]
  result = subprocess.run(
    command,
    cwd=working_dir,
    check=True,
    capture_output=True,
    text=True,
    timeout=60,
  )
  payload = json.loads(result.stdout)
  return [
    ScraperSummary(
      id=item["id"],
      category=item["category"],
      name=item["name"],
      description=item["description"],
      homepage=item["homepage"],
      source_name=item.get("sourceName", ""),
      params=[
        ScraperParameter(
          key=parameter.get("key", ""),
          description=parameter.get("description", ""),
          example=parameter.get("example", ""),
          required=bool(parameter.get("required", False)),
        )
        for parameter in item.get("params", [])
      ],
    )
    for item in payload
  ]


def build_run_command(
  toolkit_path: str,
  node_executable: str,
  scraper_id: str,
  limit: int,
  output_path: str,
  params: dict[str, str],
  save_format: str = "json",
) -> tuple[str, list[str], str]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  args = [*base_args, "run", scraper_id, "--limit", str(limit), "--output", output_path]
  if save_format and save_format != "json":
    args.extend(["--save-format", save_format])
  for key, value in params.items():
    if value.strip():
      args.extend(["--param", f"{key}={value}"])
  return program, args, str(working_dir)


def build_prompt_command(
  toolkit_path: str,
  node_executable: str,
  prompt: str,
  limit: int,
  output_path: str = "",
  params: dict[str, str] | None = None,
  save_format: str = "json",
  *,
  resolve_only: bool = False,
) -> tuple[str, list[str], str]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  args = [*base_args, "ask", prompt]
  if resolve_only:
    args.append("--resolve-only")
  else:
    args.extend(["--limit", str(limit), "--output", output_path])
    if save_format and save_format != "json":
      args.extend(["--save-format", save_format])
  for key, value in (params or {}).items():
    if value.strip():
      args.extend(["--param", f"{key}={value}"])
  return program, args, str(working_dir)


def build_run_all_command(
  toolkit_path: str,
  node_executable: str,
  limit: int,
  output_dir: str,
  category: str = "",
  save_format: str = "json",
) -> tuple[str, list[str], str]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  args = [*base_args, "run-all", "--limit", str(limit), "--out-dir", output_dir]
  if category and category != "all":
    args.extend(["--category", category])
  if save_format and save_format != "json":
    args.extend(["--save-format", save_format])
  return program, args, str(working_dir)


def fetch_health_summary(toolkit_path: str, node_executable: str) -> list[SourceHealthRecord]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  command = [program, *base_args, "health", "--format", "json"]
  result = subprocess.run(
    command,
    cwd=working_dir,
    check=True,
    capture_output=True,
    text=True,
    timeout=180,
  )
  payload = json.loads(result.stdout)
  return [
    SourceHealthRecord(
      scraper_id=item.get("metadata", {}).get("scraperId", ""),
      title=item.get("title", ""),
      category=item.get("metadata", {}).get("category", ""),
      source=item.get("source", ""),
      status=item.get("metadata", {}).get("status", ""),
      duration_ms=str(item.get("metadata", {}).get("durationMs", "")),
      records=str(item.get("metadata", {}).get("records", "")),
      summary=item.get("summary", ""),
    )
    for item in payload.get("records", [])
  ]


def build_health_command(
  toolkit_path: str,
  node_executable: str,
  *,
  category: str = "",
  limit: int = 1,
  alert_webhook_url: str = "",
  alert_discord_webhook_url: str = "",
) -> tuple[str, list[str], str]:
  program, base_args, working_dir, _ = _cli_invocation(
    Path(toolkit_path),
    node_executable,
    prefer_source=True,
  )
  args = [*base_args, "health", "--limit", str(limit), "--format", "table"]
  if category and category != "all":
    args.extend(["--category", category])
  if alert_webhook_url.strip():
    args.extend(["--alert-webhook", alert_webhook_url.strip()])
  if alert_discord_webhook_url.strip():
    args.extend(["--alert-discord-webhook", alert_discord_webhook_url.strip()])
  return program, args, str(working_dir)


def describe_command(program: str, args: Sequence[str]) -> str:
  return " ".join([program, *args])
