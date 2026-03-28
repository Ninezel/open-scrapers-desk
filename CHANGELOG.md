# Changelog

All notable changes to Open Scrapers Desk are documented in this file.

## Unreleased

- No unreleased changes recorded yet.

## 2026-03-28

### Full Expansion Workflow

- Completed a desktop app expansion pass so the GUI now matches the richer toolkit feature set and ships with updated docs and wiki content.

### Added

- Added saved workspace support for keeping multiple toolkit/output setups.
- Added queue-based job execution so users can line up multiple runs.
- Added source-health snapshot loading from the toolkit `health` command.
- Added richer library and payload summary views in the results browser.
- Added default save format handling so the desktop app can drive JSON, CSV, NDJSON, or all exports.
- Added zipped Windows build artifact publishing in GitHub Actions.

### Changed

- Updated the main window to surface health, workspaces, queued jobs, and better run controls.
- Updated desktop docs and wiki pages to match the new workflow.

### Maintenance

- Refreshed the packaging and publishing documentation to keep the release process aligned with the toolkit repo.
