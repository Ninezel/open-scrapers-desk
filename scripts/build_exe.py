from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import PyInstaller.__main__


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
ENTRYPOINT = SOURCE_ROOT / "open_scrapers_desk" / "app.py"
DIST_DIR = PROJECT_ROOT / "dist"
APP_DIR = DIST_DIR / "OpenScrapersDesk"
RELEASE_DIR = PROJECT_ROOT / "release"


def _zip_directory(source_dir: Path, target_zip: Path) -> None:
  target_zip.parent.mkdir(parents=True, exist_ok=True)
  with ZipFile(target_zip, "w", compression=ZIP_DEFLATED) as archive:
    for path in source_dir.rglob("*"):
      if path.is_file():
        archive.write(path, path.relative_to(source_dir.parent))


def _write_sha256(path: Path) -> Path:
  digest = sha256(path.read_bytes()).hexdigest()
  manifest = path.with_suffix(path.suffix + ".sha256")
  manifest.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
  return manifest


def main() -> None:
  PyInstaller.__main__.run(
    [
      "--noconfirm",
      "--clean",
      "--windowed",
      "--name=OpenScrapersDesk",
      f"--paths={SOURCE_ROOT}",
      f"--distpath={DIST_DIR}",
      f"--workpath={PROJECT_ROOT / 'build' / 'pyinstaller'}",
      f"--specpath={PROJECT_ROOT}",
      str(ENTRYPOINT),
    ]
  )

  release_zip = RELEASE_DIR / "OpenScrapersDesk-windows.zip"
  _zip_directory(APP_DIR, release_zip)
  _write_sha256(release_zip)


if __name__ == "__main__":
  main()
