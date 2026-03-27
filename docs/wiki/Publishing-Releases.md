# Publishing Releases

This page documents the recommended release process for Open Scrapers Desk. Because the desktop app depends on a separate toolkit repository, desktop releases should verify both the UI itself and the backend assumptions the UI makes.

## Release goals

A good release should:

- launch cleanly
- validate the toolkit successfully
- load the scraper catalog
- run a real scraper job
- ship docs that match the actual workflow

## Pre-release checks

Run these in the desktop repo:

```powershell
python -m compileall src
python scripts\smoke_test.py
python scripts\build_exe.py
```

Run these in the toolkit repo as well:

```powershell
npm run check
npm run build
npx tsx src/cli.ts list --format json
```

If the desktop app cannot talk to the current toolkit state, fix that before publishing.

## Recommended release flow

1. Confirm the toolkit and desktop repos are in sync.
2. Run local validation for both repos.
3. Build the PyInstaller desktop bundle.
4. Optionally compile the Inno Setup installer.
5. Test the packaged app manually.
6. Update release notes.
7. Create the GitHub release.
8. Upload the release artifact.
9. Sync the wiki pages.

## Manual packaged-app test

Before publishing, test the packaged build by:

1. launching `OpenScrapersDesk.exe`
2. validating the backend
3. refreshing the catalog
4. running at least one real scraper
5. opening the saved result in the Results Library
6. confirming the Ko-fi button opens the expected URL

## Release artifact choices

Common choices are:

- `OpenScrapersDesk-windows.zip`
- `OpenScrapersDesk-Setup.exe`

If you publish only one asset, include a clear note explaining whether it is:

- a portable bundle
- a standard Windows installer

## Release notes suggestions

Useful release notes usually include:

- version number
- user-visible changes
- packaging fixes
- toolkit compatibility notes
- known limitations

## Wiki synchronization

Do not leave the wiki stale after a release. Sync the wiki whenever setup steps, packaging steps, or user workflows change materially.

## Related pages

- [Packaging Windows Builds](Packaging-Windows-Builds.md)
- [Architecture](Architecture.md)
- [FAQ](FAQ.md)
