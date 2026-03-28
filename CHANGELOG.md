# Changelog

All notable changes to Open Scrapers Desk are documented in this file.

## Unreleased

- No unreleased changes recorded yet.

## 2026-03-28

### Full Expansion Workflow

- Completed a desktop app expansion pass so the GUI now matches the richer toolkit feature set and ships with updated docs and wiki content.

### Discord Bot Bridge Workflow

- Extended the desktop repository so Python Discord bots can reuse the toolkit through a lightweight bridge layer instead of implementing their own subprocess wrapper.

### Documentation And Roadmap Workflow

- Expanded the docs and wiki so GUI usage, Python bridge usage, and the next roadmap priorities are easier to understand and keep aligned with the toolkit repo.

### Added

- Added saved workspace support for keeping multiple toolkit/output setups.
- Added queue-based job execution so users can line up multiple runs.
- Added source-health snapshot loading from the toolkit `health` command.
- Added richer library and payload summary views in the results browser.
- Added default save format handling so the desktop app can drive JSON, CSV, NDJSON, or all exports.
- Added zipped Windows build artifact publishing in GitHub Actions.
- Added `src/open_scrapers_desk/discord_bridge.py` for Python bot integrations.
- Added packaging metadata in `pyproject.toml` so the bridge can be installed from GitHub.
- Added Discord bot bridge documentation and a starter `discord.py` example.
- Added a dedicated roadmap page for the desktop repo.

### Changed

- Updated the main window to surface health, workspaces, queued jobs, and better run controls.
- Updated desktop docs and wiki pages to match the new workflow.
- Updated the smoke test to cover the new bridge module.
- Expanded the setup and bridge docs so both GUI users and bot builders have clearer guidance.

### Maintenance

- Refreshed the packaging and publishing documentation to keep the release process aligned with the toolkit repo.
- Aligned the Python package metadata with the current `0.2.0` release line.
