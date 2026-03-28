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


def _metric_bar(label: str, value: int, max_value: int) -> str:
  width = 12 if max_value <= 0 else max(12, round((value / max_value) * 100))
  safe_label = label or "unknown"
  return (
    f"<div style='margin:6px 0;'>"
    f"<div><b>{safe_label}</b> ({value})</div>"
    f"<div style='background:#d7ddd8;border-radius:999px;height:10px;overflow:hidden;'>"
    f"<div style='background:#0f5e4f;height:10px;width:{width}%;'></div>"
    f"</div>"
    f"</div>"
  )


def build_library_summary_html(result_files: list[ResultFileSummary]) -> str:
  if not result_files:
    return "<i>No saved result files yet.</i>"

  category_counts = Counter(summary.category for summary in result_files)
  source_counts = Counter(summary.source for summary in result_files if summary.source)
  total_records = sum(summary.record_count for summary in result_files)
  max_category = max(category_counts.values(), default=1)
  max_source = max(source_counts.values(), default=1)
  recent_files = "".join(
    f"<li>{summary.scraper_name} ({summary.record_count} records, {summary.fetched_at})</li>"
    for summary in result_files[:5]
  )
  category_html = "".join(
    _metric_bar(category, count, max_category)
    for category, count in category_counts.most_common()
  )
  source_html = "".join(
    _metric_bar(source, count, max_source)
    for source, count in source_counts.most_common(5)
  )

  return f"""
    <h3>Library Snapshot</h3>
    <div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;'>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:140px;'>
        <div style='font-size:12px;color:#5b6b65;'>Files</div>
        <div style='font-size:24px;font-weight:700;'>{len(result_files)}</div>
      </div>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:140px;'>
        <div style='font-size:12px;color:#5b6b65;'>Total records</div>
        <div style='font-size:24px;font-weight:700;'>{total_records}</div>
      </div>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:180px;'>
        <div style='font-size:12px;color:#5b6b65;'>Latest source</div>
        <div style='font-size:18px;font-weight:700;'>{result_files[0].source}</div>
      </div>
    </div>
    <h4>By category</h4>
    {category_html}
    <h4>Top sources</h4>
    {source_html}
    <h4>Latest files</h4>
    <ul>{recent_files}</ul>
  """


def build_payload_summary_html(payload: ResultPayload) -> str:
  if not payload.records:
    return "<i>No records available in this payload.</i>"

  tag_counts = Counter(tag for record in payload.records for tag in record.tags)
  author_counts = Counter(author for record in payload.records for author in record.authors)
  location_counts = Counter(record.location for record in payload.records if record.location)
  max_tags = max(tag_counts.values(), default=1)
  max_authors = max(author_counts.values(), default=1)
  max_locations = max(location_counts.values(), default=1)
  recent_titles = "".join(
    f"<li>{record.title}</li>" for record in payload.records[:5]
  )
  tag_html = "".join(_metric_bar(tag, count, max_tags) for tag, count in tag_counts.most_common(8))
  author_html = "".join(
    _metric_bar(author, count, max_authors) for author, count in author_counts.most_common(5)
  )
  location_html = "".join(
    _metric_bar(location, count, max_locations)
    for location, count in location_counts.most_common(5)
  )

  return f"""
    <h3>{payload.scraper_name}</h3>
    <div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;'>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:140px;'>
        <div style='font-size:12px;color:#5b6b65;'>Category</div>
        <div style='font-size:18px;font-weight:700;'>{payload.category}</div>
      </div>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:160px;'>
        <div style='font-size:12px;color:#5b6b65;'>Records</div>
        <div style='font-size:24px;font-weight:700;'>{len(payload.records)}</div>
      </div>
      <div style='background:#f4f6f5;padding:12px 14px;border-radius:12px;min-width:220px;'>
        <div style='font-size:12px;color:#5b6b65;'>Source</div>
        <div style='font-size:18px;font-weight:700;'>{payload.source}</div>
      </div>
    </div>
    <p><b>Fetched:</b> {payload.fetched_at}</p>
    <h4>Top tags</h4>
    {tag_html or '<p><i>None</i></p>'}
    <h4>Top authors</h4>
    {author_html or '<p><i>None</i></p>'}
    <h4>Top locations</h4>
    {location_html or '<p><i>None</i></p>'}
    <h4>First records</h4>
    <ul>{recent_titles}</ul>
  """


def build_payload_comparison_html(left: ResultPayload, right: ResultPayload) -> str:
  left_tags = set(tag for record in left.records for tag in record.tags)
  right_tags = set(tag for record in right.records for tag in record.tags)
  left_authors = set(author for record in left.records for author in record.authors)
  right_authors = set(author for record in right.records for author in record.authors)

  shared_tags = sorted(left_tags & right_tags)[:8]
  shared_authors = sorted(left_authors & right_authors)[:8]

  return f"""
    <h3>Compare Payloads</h3>
    <table cellspacing='8'>
      <tr><td><b>Left</b></td><td>{left.scraper_name}</td></tr>
      <tr><td><b>Right</b></td><td>{right.scraper_name}</td></tr>
      <tr><td><b>Record count</b></td><td>{len(left.records)} vs {len(right.records)}</td></tr>
      <tr><td><b>Category</b></td><td>{left.category} vs {right.category}</td></tr>
      <tr><td><b>Source</b></td><td>{left.source} vs {right.source}</td></tr>
      <tr><td><b>Fetched</b></td><td>{left.fetched_at} vs {right.fetched_at}</td></tr>
    </table>
    <h4>Shared tags</h4>
    <p>{', '.join(shared_tags) if shared_tags else 'None'}</p>
    <h4>Shared authors</h4>
    <p>{', '.join(shared_authors) if shared_authors else 'None'}</p>
    <h4>Quick reading note</h4>
    <p>
      {left.scraper_name} leans toward {left.category} records from {left.source},
      while {right.scraper_name} currently contains {len(right.records)} records from {right.source}.
    </p>
  """
