# Connecting to the Toolkit

Open Scrapers Desk does not implement scraping itself. It talks to the separate Open Scrapers Toolkit repository through the toolkit CLI. This page explains what the app expects, how validation works, and how to configure the connection cleanly.

## What the app expects

The configured toolkit path should point to the root of an `open-scrapers-toolkit` checkout. At minimum, the folder should contain:

- `package.json`
- `src/cli.ts`

It may also contain:

- `dist/cli.js`

The app treats that combination as a valid toolkit path.

## Configure the connection in the Overview tab

Set these fields:

- `Toolkit path`
- `Node executable`
- `Output directory`

Then click **Validate Backend**.

## What validation checks

When you validate the backend, the app checks:

1. whether the toolkit path looks like a valid toolkit repository
2. whether the Node runtime can execute `node --version`
3. whether the toolkit has a runnable CLI

The status snapshot then reports:

- toolkit availability
- Node version
- CLI mode
- a status message

## CLI execution modes

The app prefers source mode when possible:

```text
npx tsx src/cli.ts ...
```

If source mode is not available but a compiled build exists, it can fall back to:

```text
node dist/cli.js ...
```

### Why source mode is preferred

Source mode is helpful during development because:

- it reflects the latest toolkit edits immediately
- it avoids confusion from stale `dist/` output
- it matches contributor workflows closely

### Why dist mode still matters

Dist mode is still useful because:

- packaged and controlled environments often prefer compiled output
- it gives a clearer deployment artifact
- it helps isolate `tsx` tooling issues

## Recommended toolkit preparation

In the toolkit repo, run:

```powershell
npm install
npm run build
```

Even if the app chooses `tsx` mode, having a fresh build makes troubleshooting easier.

## Output directory guidance

The `Output directory` field tells the app where to look for saved JSON files and where `run-all` batches should write by default.

Recommended option:

- use the toolkit repository's `output/` folder

That keeps command-line runs and desktop runs in the same place.

## Common connection mistakes

### Toolkit path points to the wrong folder

Problem:

- user selects `src/` or another nested directory instead of the repo root

Fix:

- point the app at the toolkit repository root where `package.json` lives

### Node executable is missing

Problem:

- `node` is not on `PATH`
- packaged environments sometimes cannot resolve it automatically

Fix:

- set the full path to `node.exe` on the Overview tab

### Catalog will not load

Try these checks:

```powershell
npx tsx src/cli.ts list --format json
npm run build
```

If the catalog does not work in the terminal, the desktop app is only surfacing that backend problem.

If validation succeeds, move to the Run Scrapers tab and refresh the catalog.
