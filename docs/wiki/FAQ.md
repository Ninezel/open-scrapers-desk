# FAQ

## Why is this separate from the scraper repo?

Because the scraper engine should stay reusable for developers, scripts, and automation without forcing a GUI dependency on every user.

## Does the desktop app replace the CLI?

No. The app sits on top of the CLI. It is a convenience layer for browsing, running, and reading scraper output, not a replacement for the backend.

## Can people still use the scrapers programmatically?

Yes. That is exactly why the backend remains a separate repository.

## Does the app build an `.exe`?

Yes. The repository includes a PyInstaller build script and an Inno Setup installer script for Windows packaging.

## Do I still need Node.js if I use the GUI?

Yes. The desktop app calls the toolkit CLI, so Node.js and the toolkit repository still need to be present.

## Where are settings stored?

The app stores settings in the current user's application-data area under `OpenScrapersDesk`. See [Settings and Data Locations](Settings-and-Data-Locations.md) for details.

## What happens if the toolkit output is already in a folder?

The Results Library can scan the output directory and also open JSON files directly.

## Can I change the Ko-fi link?

Yes. The app ships with `https://ko-fi.com/ninezel` as the default, but forks can override it in the Overview tab or through environment variables.

## Is the app Windows-only?

The packaging path is Windows-first, but local development with Python and Qt can be adapted for other platforms if the environment supports it. The installer instructions in this repo are focused on Windows.
