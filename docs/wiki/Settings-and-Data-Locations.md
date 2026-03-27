# Settings and Data Locations

This page explains where Open Scrapers Desk stores its own settings, how it chooses defaults, and how it decides where result files live.

## Settings file location

The desktop app stores its settings in the current user's application-data directory under:

```text
%APPDATA%\OpenScrapersDesk\settings.json
```

That file stores values such as:

- toolkit path
- Node executable
- output directory
- Ko-fi URL
- last selected scraper
- last selected category

## Default toolkit detection

On first load, the app tries to discover a nearby toolkit checkout automatically. It looks for common folder names such as:

- `Scrapers`
- `open-scrapers-toolkit`
- `OpenScrapersToolkit`
- `OpenScrapers`

This makes first-run setup smoother when both repos live next to each other.

## Default output directory

If a valid toolkit path is known, the default output directory becomes:

```text
<toolkit-path>\output
```

If not, the app falls back to an output folder inside its own application-data area.

## Ko-fi URL behavior

The app ships with this default support link:

- `https://ko-fi.com/ninezel`

The app also normalizes plain `ko-fi.com/...` style input into full HTTPS URLs. Placeholder or empty values resolve back to the default Ninezel link.

## Result file discovery

The Results Library scans the configured output directory recursively for `*.json` files. It reads each candidate file and keeps the ones that parse as valid result payloads.

This means:

- nested output folders are supported
- older run outputs remain visible
- batch output directories can be browsed without manual import

## Recommended practice

For the cleanest experience, point both the CLI and the desktop app at the same output directory so every run ends up in one discoverable library.
