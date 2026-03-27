# Troubleshooting

This page covers the most common desktop-app problems, from toolkit connection errors to packaged executable issues.

## The `.exe` fails to launch

If you are using an older packaged build and see an import error about a relative import with no known parent package, update to a newer build. The app entrypoint was adjusted to support packaged execution cleanly.

If the issue continues:

- delete the older extracted app folder
- extract the latest release again
- launch the new `OpenScrapersDesk.exe`

## Backend validation fails

Check these first:

1. the toolkit path points to the repository root
2. Node.js is installed
3. the configured Node executable is valid
4. the toolkit can run in the terminal

Manual toolkit test:

```powershell
npx tsx src/cli.ts list --format json
```

## Node version is unavailable in the app

That usually means the configured `node` command could not run. Fix it by:

- installing Node.js
- adding Node to `PATH`
- or selecting the full `node.exe` path in the Overview tab

## Catalog load fails

If backend validation passes but the scraper catalog still does not load:

1. run `npm install` in the toolkit repo
2. run `npm run build`
3. retry the catalog command manually
4. refresh the app again

## Run buttons do nothing useful

The app prevents overlapping jobs. If a process is already running, wait for it to finish before starting another one.

Also check:

- whether an output file path is set for single runs
- whether the selected category is `all` when trying `Run Category`

## Results Library is empty

Possible causes:

- no JSON output has been created yet
- the wrong output directory is configured
- files exist but are not valid result payloads

Try:

- opening the configured output folder from the Overview tab
- refreshing the library
- loading a known JSON file manually

## Ko-fi button is disabled or does not open

Check the `Ko-fi link` field on the Overview tab. If it is empty or invalid, save settings again. The app normally defaults this field to:

- `https://ko-fi.com/ninezel`

If a valid URL is present, the support buttons should be enabled.

## The app starts but cannot find the toolkit automatically

Automatic toolkit discovery is a convenience, not a guarantee. Set the toolkit path manually in the Overview tab if your folders are arranged differently.
