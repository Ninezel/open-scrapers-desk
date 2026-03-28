# Architecture

Key modules:

- `app.py`
- `ui/main_window.py`
- `backend.py`
- `discord_bridge.py`
- `results.py`
- `settings.py`
- `models.py`

The desktop app is a thin but useful GUI over the toolkit CLI. It does not duplicate scraper logic; it schedules and visualizes it. The same backend command layer now also powers the Python Discord bridge so bot workflows and GUI workflows stay aligned.
