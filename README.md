# Market Research

A dividend-focused portfolio analysis tool built with [Flet](https://flet.dev) (UI) and [FastAPI](https://fastapi.tiangolo.com) (API). Tracks holdings, fetches live market data, and scores each position across health metrics such as yield, payout ratio, FCF coverage, leverage, and dividend growth.

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- A free [Finnhub](https://finnhub.io) API key

## Environment setup

Create a `.env` file in the project root:

```
FINNHUB_API_KEY=your_api_key_here
```

Get a free key at https://finnhub.io/register. The app will start without one but all market data calls will fail.

## Install dependencies

```bash
poetry install
```

This creates a `.venv-linux/` virtualenv (Linux/WSL) used by `start.sh`.

## Running

The easiest way is the provided script, which starts both services together:

```bash
bash start.sh
```

| Service | URL |
|---|---|
| UI (Flet) | http://127.0.0.1:8550 |
| API (FastAPI) | http://127.0.0.1:8000 |

Press `Ctrl+C` to stop both.

### Running services individually

**API:**
```bash
PYTHONPATH=api .venv-linux/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**UI:**
```bash
PYTHONPATH=src .venv-linux/bin/python -m my_flet_app.main
```

## Data storage

All runtime data lives inside the project under `data/` (created automatically on first run, excluded from git):

| File | Contents |
|---|---|
| `data/holdings.db` | SQLite database — your portfolio holdings (ticker, shares, cost basis) |
| `data/cache.json` | Market data cache — quotes (15 min TTL), fundamentals and statements (24 hr TTL) |

On first run, `holdings.db` is seeded with a small set of demo holdings so the UI has something to display. Replace these with your own positions via the Holdings screen.

To force-refresh market data for a ticker, clear its cache entry:

```python
# from the project root
PYTHONPATH=api .venv-linux/bin/python -c "from services.market import clear_cache; clear_cache('TICKER')"
```

Pass no argument to `clear_cache()` to wipe the entire cache.
