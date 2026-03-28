# Connecting To The Toolkit

The desktop app expects a local clone of `open-scrapers-toolkit`.

Prepare it with:

```bash
npm install
npm run build
```

Then point the desktop app at that folder and refresh the backend status.

Useful environment overrides:

- `OPEN_SCRAPERS_TOOLKIT_PATH`
- `OPEN_SCRAPERS_NODE`

The Python Discord bridge in this repo uses the same toolkit checkout and Node runtime, so the same preparation steps apply when you are building a bot instead of launching the GUI.
