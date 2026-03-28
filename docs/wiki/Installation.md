# Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts/smoke_test.py
python -m open_scrapers_desk.app
```

Bridge-only install for Python bot projects:

```bash
pip install git+https://github.com/Ninezel/open-scrapers-desk.git
```
