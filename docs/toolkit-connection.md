# Toolkit Connection Guide

The desktop app is not the scraper engine. It talks to the separate Node-based toolkit repository.

## Expected backend layout

The configured toolkit path should contain:

- `package.json`
- `src/cli.ts`
- optionally `dist/cli.js`

## Supported execution modes

### Source mode

Used when the app can find `npx` and toolkit source files.

Command shape:

```text
npx tsx src/cli.ts ...
```

Pros:

- uses the latest source immediately
- avoids confusion from stale `dist/` output

### Dist mode

Used when the compiled CLI is available and source-mode execution is not preferred or possible.

Command shape:

```text
node dist/cli.js ...
```

Pros:

- better for packaged or controlled environments

## Recommended backend prep

```bash
npm install
npm run build
```

## Common issues

### Toolkit path invalid

Fix:

- point the app to the toolkit repository root, not the `src/` folder

### Node executable missing

Fix:

- set the full path to `node.exe` on the Overview tab

### Catalog not loading

Fix:

- run `npm install` in the toolkit repo
- run `npm run build`
- make sure `npx` or `node` works in your environment
