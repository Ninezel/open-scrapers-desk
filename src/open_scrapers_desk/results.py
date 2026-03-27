from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ResultFileSummary, ResultPayload, ResultRecord


def _read_payload(path: Path) -> dict[str, Any]:
  return json.loads(path.read_text(encoding="utf-8"))


def scan_result_files(output_dir: str) -> list[ResultFileSummary]:
  root = Path(output_dir)
  if not root.exists():
    return []

  summaries: list[ResultFileSummary] = []
  for path in sorted(root.rglob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
    try:
      payload = _read_payload(path)
    except Exception:  # noqa: BLE001
      continue

    summaries.append(
      ResultFileSummary(
        path=path,
        scraper_id=payload.get("scraperId", "unknown"),
        scraper_name=payload.get("scraperName", path.stem),
        category=payload.get("category", "unknown"),
        source=payload.get("source", "unknown"),
        fetched_at=payload.get("fetchedAt", ""),
        record_count=len(payload.get("records", [])),
      )
    )

  return summaries


def load_result_payload(path: str) -> ResultPayload:
  payload = _read_payload(Path(path))
  records = [
    ResultRecord(
      id=item.get("id", ""),
      title=item.get("title", "Untitled record"),
      source=item.get("source", payload.get("source", "")),
      url=item.get("url", ""),
      summary=item.get("summary", ""),
      published_at=item.get("publishedAt", ""),
      authors=item.get("authors", []),
      tags=item.get("tags", []),
      location=item.get("location", ""),
      metadata=item.get("metadata", {}),
    )
    for item in payload.get("records", [])
  ]

  return ResultPayload(
    scraper_id=payload.get("scraperId", "unknown"),
    scraper_name=payload.get("scraperName", "Unknown"),
    category=payload.get("category", "unknown"),
    source=payload.get("source", ""),
    fetched_at=payload.get("fetchedAt", ""),
    records=records,
    meta=payload.get("meta", {}),
  )


def filter_records(records: list[ResultRecord], query: str) -> list[ResultRecord]:
  needle = query.strip().lower()
  if not needle:
    return records

  filtered: list[ResultRecord] = []
  for record in records:
    haystacks = [
      record.title,
      record.summary,
      record.source,
      record.location,
      " ".join(record.tags),
      " ".join(record.authors),
    ]
    if any(needle in (value or "").lower() for value in haystacks):
      filtered.append(record)

  return filtered


def format_meta_html(meta: dict[str, Any]) -> str:
  if not meta:
    return "<i>No metadata available.</i>"

  rows = []
  for key, value in meta.items():
    rows.append(f"<tr><td><b>{key}</b></td><td>{value}</td></tr>")
  return "<table cellspacing='6'>" + "".join(rows) + "</table>"
