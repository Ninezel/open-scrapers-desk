# Packaging

## Local `.exe` build

```bash
pip install -r requirements.txt
python scripts/build_exe.py
```

Output:

- `dist/OpenScrapersDesk/`

## Installer

The repository still includes:

- `installer/OpenScrapersDesk.iss`

Use Inno Setup after building the PyInstaller output if you want a traditional installer.

## GitHub Actions

The Windows workflow now:

- installs dependencies
- runs the smoke test
- builds the executable
- creates a zipped release bundle
- uploads both the folder artifact and zip artifact
