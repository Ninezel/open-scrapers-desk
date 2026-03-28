# Packaging

## Local `.exe` build

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

Output:

- `dist/OpenScrapersDesk/`
- `release/OpenScrapersDesk-windows.zip`
- `release/OpenScrapersDesk-windows.zip.sha256`

## Installer

The repository still includes:

- `installer/OpenScrapersDesk.iss`

Use Inno Setup after building the PyInstaller output if you want a traditional installer.

## GitHub Actions

The Windows workflow now:

- installs dependencies
- runs the smoke test
- builds the executable
- creates a zipped release bundle and checksum
- uploads the folder artifact, zip artifact, and SHA256 manifest

## Signing note

Code signing is still a future improvement. Until that is added, the zip bundle plus SHA256 manifest is the main integrity workflow for shared builds.
