# Packaging Windows Builds

This page explains how the desktop app is packaged for Windows, why the project currently uses a folder-based PyInstaller build, and how to turn that output into a traditional installer.

## Packaging stack

The Windows packaging flow uses:

- PyInstaller for the desktop executable bundle
- Inno Setup for the optional installer

## Prerequisites

Before building a Windows package, verify:

- Python dependencies are installed
- the source compiles cleanly
- the smoke test passes

Recommended prep:

```powershell
pip install -r requirements.txt
python -m compileall src
python scripts\smoke_test.py
```

## Build the executable bundle

Run:

```powershell
python scripts\build_exe.py
```

The build script calls PyInstaller with the project source path and writes output to:

- `dist/OpenScrapersDesk/`

It also uses dedicated build and spec locations under the repository so packaging artifacts stay predictable.

## Why the project currently uses a folder build

The repository currently favors a folder-based build over a single-file executable because it is usually more reliable for PyQt desktop apps, especially when troubleshooting local environments.

Advantages:

- fewer surprises with Qt runtime assets
- easier debugging
- clearer release contents

## Packaged entrypoint

The packaged app launches:

- `OpenScrapersDesk.exe`

The application entrypoint is designed to support both direct script execution and packaged execution, which helps avoid relative-import failures in the final build.

## Build the installer

After the PyInstaller output exists, compile the Inno Setup script:

- `installer/OpenScrapersDesk.iss`

That script produces an installer package in:

- `release/`

## Suggested release bundle contents

For a Windows release, include:

- the PyInstaller app bundle or installer
- a README or release notes summary
- a link to the toolkit repository
- a note that Node and the toolkit backend are still required

## Manual verification after packaging

Before uploading artifacts, verify:

1. the executable launches
2. the Overview tab renders correctly
3. toolkit validation works
4. the scraper catalog loads
5. a scraper can run successfully
6. the Results Library can open a saved JSON file

## Related pages

- [Installation](Installation.md)
- [Publishing Releases](Publishing-Releases.md)
- [Troubleshooting](Troubleshooting.md)
