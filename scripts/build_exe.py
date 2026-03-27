from __future__ import annotations

from pathlib import Path

import PyInstaller.__main__


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
ENTRYPOINT = SOURCE_ROOT / "open_scrapers_desk" / "app.py"


def main() -> None:
  PyInstaller.__main__.run(
    [
      "--noconfirm",
      "--clean",
      "--windowed",
      "--name=OpenScrapersDesk",
      f"--paths={SOURCE_ROOT}",
      f"--distpath={PROJECT_ROOT / 'dist'}",
      f"--workpath={PROJECT_ROOT / 'build' / 'pyinstaller'}",
      f"--specpath={PROJECT_ROOT}",
      str(ENTRYPOINT),
    ]
  )


if __name__ == "__main__":
  main()
