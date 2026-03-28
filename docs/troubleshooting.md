# Troubleshooting

## The desktop app says the toolkit is missing

Check:

- the `Toolkit path` points to a real `open-scrapers-toolkit` checkout
- the toolkit repo has already run `npm install`
- the toolkit repo has already run `npm run build`

## The app opens but no scrapers appear

Check:

- the `Node executable` path is valid
- the backend status shows a working CLI mode
- the toolkit repo can run `npx tsx src/cli.ts list`

## Health rows do not load

That usually means one of these:

- the toolkit path is wrong
- Node cannot run
- the toolkit has not been built yet
- a source check timed out because the network or upstream source is unavailable

## Queued jobs seem stuck

The desktop app runs one `QProcess` job at a time. Wait for the current job to finish, then the next queued item will start automatically.

## The packaged `.exe` was built but Windows still warns me

Code signing is not set up yet. Use the generated checksum file:

- `release/OpenScrapersDesk-windows.zip.sha256`

## Python bridge commands fail

Check:

- the toolkit path points to a built toolkit checkout
- `node` works in a regular terminal
- the scraper ID exists in the toolkit catalog
- any required scraper parameters were supplied

## `.env` values do not seem to load

That is expected unless you load them yourself. The desktop app and example scripts read normal process environment variables, but they do not auto-load `.env` files on their own.
