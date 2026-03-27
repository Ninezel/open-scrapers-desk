# Contributing

Thanks for helping improve Open Scrapers Desk.

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m compileall src
python scripts/smoke_test.py
python -m open_scrapers_desk.app
```

## Contribution areas

- UI and UX improvements
- packaging and installer work
- richer result browsing
- better integration with the scraper toolkit
- documentation and wiki pages

## Before opening a PR

- Keep changes focused.
- Update docs when workflows change.
- Mention any packaging impact.
- If you change the toolkit bridge, test it against a real toolkit checkout.
