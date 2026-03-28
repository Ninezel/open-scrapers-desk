# Changelog

All notable changes to Open Scrapers Desk are documented in this file.

## Unreleased

- No unreleased changes recorded yet.

## 2026-03-28 11:25:15 +00:00

### Environment And Documentation Workflow

- Audited the desktop repo environment surface, added a reference `.env.example`, and refreshed the repo docs and wiki so GUI overrides, bridge example variables, and `.env` expectations are clearly documented.

### Added

- Added `.env.example` to document the desktop repo's common environment overrides and example variables.
- Added a dedicated environment-variable reference in `docs/environment-variables.md`.
- Added a matching wiki page in `docs/wiki/Environment-Variables.md`.

### Changed

- Clarified that the desktop app and Python examples read normal process environment variables and do not auto-load `.env` files by themselves.
- Refreshed installation, toolkit-connection, Discord bridge, and troubleshooting docs in both the repo docs and wiki source.

## 2026-03-28 11:16:34 +00:00

### Roadmap Expansion Workflow

- Completed the next desktop roadmap pass by improving result presentation, bridge presets, automation previews, packaging outputs, onboarding guidance, and the desktop repo docs and wiki source.

### Added

- Added dashboard-style result metrics and stronger summary cards in the Results Library.
- Added side-by-side payload comparison HTML for two selected saved results.
- Added alert webhook and Discord webhook settings on the Overview tab.
- Added Discord formatting preset selection in the desktop UI and Python bridge surface.
- Added run-command and health-command preview actions for automation workflows.
- Added `release/OpenScrapersDesk-windows.zip` and `release/OpenScrapersDesk-windows.zip.sha256` output from the local build script.
- Added new Python bridge examples for preset formatting and Discord webhook automation.
- Added a dedicated desktop troubleshooting document in `docs/troubleshooting.md`.

### Changed

- Updated the main window onboarding flow so the smoke test does not block in headless environments.
- Updated README, docs, and wiki pages to reflect the larger desktop feature set and timestamped release workflow.
- Updated the Windows build workflow so the build script is the single source of truth for zip and checksum generation.

### Maintenance

- Bumped the Python package metadata to the `0.3.0` release line.

## 2026-03-28 10:39:41 +00:00

### Documentation And Roadmap Workflow

- Expanded the docs and wiki so GUI usage, Python bridge usage, and the next roadmap priorities are easier to understand and keep aligned with the toolkit repo.

### Added

- Added a dedicated roadmap page for the desktop repo.

### Changed

- Expanded the setup and bridge docs so both GUI users and bot builders have clearer guidance.
- Updated the main repo docs and wiki pages to match the new workflow.

## 2026-03-28 10:31:24 +00:00

### Discord Bot Bridge Workflow

- Extended the desktop repository so Python Discord bots can reuse the toolkit through a lightweight bridge layer instead of implementing their own subprocess wrapper.

### Added

- Added `src/open_scrapers_desk/discord_bridge.py` for Python bot integrations.
- Added packaging metadata in `pyproject.toml` so the bridge can be installed from GitHub.
- Added Discord bot bridge documentation and a starter `discord.py` example.

### Changed

- Updated the smoke test to cover the new bridge module.

## 2026-03-28 10:04:47 +00:00

### Full Expansion Workflow

- Completed a desktop app expansion pass so the GUI now matches the richer toolkit feature set and ships with updated docs and wiki content.

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
