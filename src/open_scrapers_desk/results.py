from __future__ import annotations

from collections import Counter
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


def build_library_summary_html(result_files: list[ResultFileSummary]) -> str:
  if not result_files:
    return "<i>No saved result files yet.</i>"

  category_counts = Counter(summary.category for summary in result_files)
  source_counts = Counter(summary.source for summary in result_files if summary.source)
  total_records = sum(summary.record_count for summary in result_files)
  recent_files = "".join(
    f"<li>{summary.scraper_name} ({summary.record_count} records, {summary.fetched_at})</li>"
    for summary in result_files[:5]
  )
  category_html = "".join(
    f"<li>{category}: {count}</li>" for category, count in category_counts.most_common()
  )
  source_html = "".join(
    f"<li>{source}: {count}</li>" for source, count in source_counts.most_common(5)
  )

  return f"""
    <h3>Library Snapshot</h3>
    <p><b>Files:</b> {len(result_files)}<br>
    <b>Total records:</b> {total_records}</p>
    <h4>By category</h4>
    <ul>{category_html}</ul>
    <h4>Top sources</h4>
    <ul>{source_html}</ul>
    <h4>Latest files</h4>
    <ul>{recent_files}</ul>
  """


def build_payload_summary_html(payload: ResultPayload) -> str:
  if not payload.records:
    return "<i>No records available in this payload.</i>"

  tag_counts = Counter(tag for record in payload.records for tag in record.tags)
  author_counts = Counter(author for record in payload.records for author in record.authors)
  recent_titles = "".join(
    f"<li>{record.title}</li>" for record in payload.records[:5]
  )
  tag_html = "".join(f"<li>{tag}: {count}</li>" for tag, count in tag_counts.most_common(8))
  author_html = "".join(
    f"<li>{author}: {count}</li>" for author, count in author_counts.most_common(5)
  )

  return f"""
    <h3>{payload.scraper_name}</h3>
    <p><b>Category:</b> {payload.category}<br>
    <b>Source:</b> {payload.source}<br>
    <b>Records:</b> {len(payload.records)}<br>
    <b>Fetched:</b> {payload.fetched_at}</p>
    <h4>Top tags</h4>
    <ul>{tag_html or '<li>None</li>'}</ul>
    <h4>Top authors</h4>
    <ul>{author_html or '<li>None</li>'}</ul>
    <h4>First records</h4>
    <ul>{recent_titles}</ul>
  """
