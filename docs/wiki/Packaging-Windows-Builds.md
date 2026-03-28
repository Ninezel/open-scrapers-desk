# Packaging Windows Builds

Local build:

```bash
python scripts/build_exe.py
```

CI build:

- smoke tests the app
- builds the PyInstaller bundle
- creates a zip file
- uploads both artifacts
