# FAQ

## Why is this separate from the scraper repo?

Because the scraper engine should stay reusable for developers without forcing a GUI dependency.

## Does this replace the CLI?

No. It sits on top of the CLI.

## Can people still use the scrapers programmatically?

Yes. That is why the backend remains a separate repository.

## Does the app build an `.exe`?

Yes. The repository includes a PyInstaller build script for Windows.
