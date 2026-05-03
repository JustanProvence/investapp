# Project: Market Research App

A personal portfolio & market research tool built with **Flet** (Python UI) and **FastAPI** (backend API).

---

## Architecture

```
/home/dev/app/
├── api/                        FastAPI backend (port 8000)
│   ├── main.py                 App entry, routers registered, CORS middleware
│   ├── dependencies.py         Auth dependency — supports JWT Bearer + X-User-Id header
│   ├── auth_utils.py           Stdlib-only HS256 JWT sign/verify (no extra deps)
│   ├── models.py               Pydantic request/response models
│   ├── routers/
│   │   ├── auth.py             POST /auth/login (email), PATCH /auth/preferences
│   │   ├── oauth.py            GET /auth/google/authorize + /auth/google/callback
│   │   ├── holdings.py         CRUD /holdings
│   │   ├── watchlist.py        CRUD /watchlist
│   │   ├── market.py           GET /market/search, /market/{ticker}/quote+metrics
│   │   └── portfolio.py        GET /portfolio/summary
│   └── services/
│       ├── users_store.py      SQLite users table (id, email, name, picture, theme_mode)
│       ├── holdings_store.py   SQLite holdings table
│       ├── watchlist_store.py  SQLite watchlist table
│       └── market.py           Finnhub API wrapper
├── src/marketresearch/         Flet UI (port 8550)
│   ├── main.py                 Router + page setup. Handles /auth/callback/{jwt} route
│   ├── routes.py               Route constants + helpers
│   ├── theme.py                Light/dark theme tokens
│   ├── api_client.py           All backend calls via httpx (_BASE = http://127.0.0.1:8000)
│   ├── logo_b64.py             Base64-encoded logo/google logos (light + dark variants)
│   ├── assets/
│   │   ├── index.html          Custom Flet loading screen (uses logo.png + spinner)
│   │   └── logo.png            Correct logo (copied from design/logo.png, 34 KB)
│   ├── components/
│   │   ├── app_bar.py          build_app_bar(page) — dark-mode-aware logo
│   │   └── bottom_nav.py       4-tab nav: Summary | Holdings | Watch | Settings
│   └── screens/
│       ├── login.py            Email login + Google OAuth button
│       ├── summary.py          Portfolio overview, donut charts, income, total return
│       ├── holdings.py         Holdings list, add, update, ticker detail
│       └── watchlist.py        Watchlist list, add, ticker health detail
├── data/holdings.db            SQLite database (holdings + watchlist + users tables)
├── design/                     Source assets (logo.png, logo-dark.png, google-logo*.png)
└── .env                        Secrets (never commit)
```

---

## How to Start (Development)

**Servers must be started manually in WSL2:**

```bash
# API — must bind to 0.0.0.0 so Windows browser can reach OAuth endpoints
source .venv-linux/bin/activate && cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# UI (separate terminal)
source .venv-linux/bin/activate && cd src
python -m marketresearch.main
```

**Docker port mapping required:** `-p 8550:8550 -p 8000:8000`
- Port 8550: Flet web UI (browser)
- Port 8000: FastAPI (needed by browser for Google OAuth redirects)

Internal Flet→API calls use `http://127.0.0.1:8000` (container-local, not browser-facing).

---

## Environment Variables (`/home/dev/app/.env`)

```
FINNHUB_API_KEY=...
GOOGLE_CLIENT_ID=...          # From Google Cloud Console OAuth 2.0 credentials
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
JWT_SECRET=...                # Random hex string (openssl rand -hex 32)
```

---

## Authentication

Two login paths coexist:

**Email login** (dev/testing):
- `POST /auth/login` with `{"email": "..."}` — returns user dict
- No password check; seed user is `prov24@gmail.com` / name `Justan`
- Frontend stores `user` dict in `page.session.store`
- API calls pass `X-User-Id: <user.id>` header

**Google OAuth**:
1. Browser → `GET /auth/google/authorize` → redirects to Google consent
2. Google → `GET /auth/google/callback?code=...` → exchanges code for profile
3. API upserts user (using Google `sub` as user ID), issues JWT
4. API redirects browser to `http://localhost:8550/auth/callback/<jwt>`
5. Flet `route_change` decodes JWT payload, sets `page.session.store`, navigates to Summary

JWT payload: `{sub, email, name, picture, theme_mode, iat, exp}`
`dependencies.py` accepts **both** JWT Bearer token and legacy `X-User-Id` header.

---

## Key UI Decisions

- **Dark mode**: detected via `page.session.store.get("theme_mode")` falling back to `page.platform_brightness`. Logo and Google logo swap to `-dark.png` variants.
- **Bottom nav** index: 0=Summary, 1=Holdings, 2=Watch, 3=Settings
- **Canvas charts**: pre-created `canvas.Canvas` objects (stable refs) in `summary_view` — shapes updated in-place so Flet diffs correctly. Creating new canvases on data load causes stale renders.
- **Watchlist → Holdings**: "Add to Holdings" button stores `holdings_prefill_ticker` + `holdings_from_watchlist` in session, navigates to add page. On save, removes ticker from watchlist and returns to Watch tab.
- **Custom loading screen**: `assets/index.html` overrides Flet's default. The `assets_dir` in `main.py` uses `os.path.dirname(__file__)` (absolute path) — relative paths resolve to the wrong location via `get_current_script_dir()`.

---

## Gotchas

- `ft.ImageFit` does not exist in this Flet version — omit `fit=` on `ft.Image`
- `page.client_storage` does not exist — use `page.session.store`
- `page.launch_url()` is async — must be wrapped in `asyncio.create_task()`
- Use `ft.UrlLauncher().launch_url(url, web_only_window_name="_self")` to redirect the current browser tab
- `page.go()` is deprecated — use `asyncio.create_task(page.push_route(...))` or `page.go()` only in sync `route_change`
- The `start.sh` script binds API to `127.0.0.1` — change to `0.0.0.0` for OAuth to work from browser
- Google OAuth `web_popup_window_name` on `page.launch_url` is only used in popup mode — it does NOT control same-tab navigation
