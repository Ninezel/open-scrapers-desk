# Packaging Windows Builds

## Build the executable

```bash
python scripts/build_exe.py
```

## Build the installer

Use Inno Setup with:

- `installer/OpenScrapersDesk.iss`

Make sure the PyInstaller output already exists in `dist/OpenScrapersDesk/`.
