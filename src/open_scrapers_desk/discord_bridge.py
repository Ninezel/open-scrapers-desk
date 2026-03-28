from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from .backend import build_run_command
from .models import ResultPayload, ResultRecord
from .results import load_result_payload


def _truncate(value: str, limit: int) -> str:
  if len(value) <= limit:
    return value
  if limit <= 3:
    return value[:limit]
  return value[: limit - 3] + "..."


def run_scraper_payload(
  toolkit_path: str,
  node_executable: str,
  scraper_id: str,
  *,
  limit: int = 3,
  params: dict[str, str] | None = None,
  timeout: int = 180,
) -> ResultPayload:
  with TemporaryDirectory(prefix="open-scrapers-discord-") as temp_dir:
    output_path = Path(temp_dir) / f"{scraper_id}.json"
    program, args, working_dir = build_run_command(
      toolkit_path,
      node_executable,
      scraper_id,
      limit,
      str(output_path),
      params or {},
      "json",
    )

    subprocess.run(
      [program, *args],
      cwd=working_dir,
      check=True,
      capture_output=True,
      text=True,
      timeout=timeout,
    )

    return load_result_payload(str(output_path))


def record_to_discord_embed(
  payload: ResultPayload,
  record: ResultRecord,
  *,
  include_metadata: bool = False,
  title_prefix: str = "",
) -> dict[str, Any]:
  fields: list[dict[str, Any]] = []

  if record.published_at:
    fields.append({"name": "Published", "value": record.published_at, "inline": True})

  if record.location:
    fields.append({"name": "Location", "value": record.location, "inline": True})

  if record.authors:
    fields.append({
      "name": "Authors",
      "value": _truncate(", ".join(record.authors), 1024),
    })

  if record.tags:
    fields.append({
      "name": "Tags",
      "value": _truncate(", ".join(record.tags), 1024),
    })

  if include_metadata and record.metadata:
    fields.append({
      "name": "Metadata",
      "value": _truncate(str(record.metadata), 1024),
    })

  title = f"{title_prefix} {record.title}".strip() if title_prefix else record.title

  embed: dict[str, Any] = {
    "title": _truncate(title, 250),
    "description": _truncate(record.summary or "No summary provided.", 4000),
    "fields": fields[:25],
    "footer": {"text": f"{payload.scraper_name} • {record.source}"},
    "timestamp": record.published_at or payload.fetched_at,
  }
  if record.url:
    embed["url"] = record.url
  return embed


def payload_to_discord_messages(
  payload: ResultPayload,
  *,
  include_metadata: bool = False,
  max_embeds_per_message: int = 10,
  max_records: int = 5,
  title_prefix: str = "",
) -> list[dict[str, Any]]:
  embeds = [
    record_to_discord_embed(
      payload,
      record,
      include_metadata=include_metadata,
      title_prefix=title_prefix,
    )
    for record in payload.records[:max_records]
  ]

  if not embeds:
    return [
      {
        "content": f"**{payload.scraper_name}** returned no records at {payload.fetched_at}.",
        "embeds": [],
      }
    ]

  messages: list[dict[str, Any]] = []
  for index in range(0, len(embeds), max_embeds_per_message):
    message: dict[str, Any] = {
      "embeds": embeds[index : index + max_embeds_per_message],
    }
    if index == 0:
      message["content"] = (
        f"**{payload.scraper_name}** pulled {len(payload.records)} record(s) "
        f"from {payload.source} at {payload.fetched_at}."
      )
    messages.append(message)

  return messages


def run_scraper_to_discord_messages(
  toolkit_path: str,
  node_executable: str,
  scraper_id: str,
  *,
  limit: int = 3,
  params: dict[str, str] | None = None,
  timeout: int = 180,
  include_metadata: bool = False,
  max_embeds_per_message: int = 10,
  max_records: int = 5,
  title_prefix: str = "",
) -> list[dict[str, Any]]:
  payload = run_scraper_payload(
    toolkit_path,
    node_executable,
    scraper_id,
    limit=limit,
    params=params,
    timeout=timeout,
  )
  return payload_to_discord_messages(
    payload,
    include_metadata=include_metadata,
    max_embeds_per_message=max_embeds_per_message,
    max_records=max_records,
    title_prefix=title_prefix,
  )
