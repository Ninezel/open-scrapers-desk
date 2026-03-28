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

Recommended next pages:

- [Connecting To The Toolkit](Connecting-to-the-Toolkit)
- [Discord Bot Bridge](Discord-Bot-Bridge)
- [Using The Desktop App](Using-the-Desktop-App)
- [Troubleshooting](Troubleshooting)
- [Roadmap](Roadmap)
