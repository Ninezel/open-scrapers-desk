# Packaging And Release Guide

This repository is set up for Windows-first desktop distribution.

## Build the executable

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

Output:

- `dist/OpenScrapersDesk/`

## Smoke test before release

```bash
python -m compileall src
python scripts/smoke_test.py
```

## Installer support

The repo includes an Inno Setup script:

- `installer/OpenScrapersDesk.iss`

After building the PyInstaller output, compile the Inno Setup script to create a Windows installer.

## Suggested release contents

- `OpenScrapersDesk.exe` bundle from PyInstaller
- `README.md`
- release notes
- clear link to the backend toolkit repo

## GitHub Actions workflow

The Windows build workflow can create artifacts for tag-based releases. Extend it later if you want:

- installer compilation
- code signing
- release asset uploads
