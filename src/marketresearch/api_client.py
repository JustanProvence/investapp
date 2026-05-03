"""
Async HTTP client — all backend calls go through here.
Screens import from this module only; nothing touches the API directly.
"""
import httpx

_BASE = "http://127.0.0.1:8000"
_TIMEOUT = 20.0


# ── Internal helpers ──────────────────────────────────────────────────────────

def _auth(user_id: str) -> dict:
    return {"X-User-Id": user_id}


async def _get(path: str, headers: dict | None = None):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{_BASE}{path}", timeout=_TIMEOUT, headers=headers or {})
        r.raise_for_status()
        return r.json()


async def _post(path: str, body: dict, headers: dict | None = None):
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{_BASE}{path}", json=body, timeout=_TIMEOUT, headers=headers or {})
        r.raise_for_status()
        return r.json()


async def _put(path: str, body: dict, headers: dict | None = None):
    async with httpx.AsyncClient() as c:
        r = await c.put(f"{_BASE}{path}", json=body, timeout=_TIMEOUT, headers=headers or {})
        r.raise_for_status()
        return r.json()


async def _patch(path: str, body: dict, headers: dict | None = None):
    async with httpx.AsyncClient() as c:
        r = await c.patch(f"{_BASE}{path}", json=body, timeout=_TIMEOUT, headers=headers or {})
        r.raise_for_status()
        return r.json()


async def _delete(path: str, headers: dict | None = None):
    async with httpx.AsyncClient() as c:
        r = await c.delete(f"{_BASE}{path}", timeout=_TIMEOUT, headers=headers or {})
        r.raise_for_status()
        return r.json()


# ── Auth ──────────────────────────────────────────────────────────────────────

async def login(email: str) -> dict | None:
    """Returns user dict on success, None if email not recognised."""
    try:
        return await _post("/auth/login", {"email": email})
    except Exception:
        return None


async def set_theme_preference(mode: str, user_id: str) -> None:
    try:
        await _patch("/auth/preferences", {"theme_mode": mode}, headers=_auth(user_id))
    except Exception:
        pass


# ── Holdings ──────────────────────────────────────────────────────────────────

async def get_holdings(user_id: str) -> list[dict]:
    """Returns list of {ticker, shares, cost_basis}."""
    try:
        return await _get("/holdings", headers=_auth(user_id))
    except Exception:
        return []


async def add_holding(ticker: str, shares: float, cost_basis: float, user_id: str) -> dict | None:
    """Returns saved holding or None on error (e.g. duplicate)."""
    try:
        return await _post("/holdings", {
            "ticker": ticker, "shares": shares, "cost_basis": cost_basis,
        }, headers=_auth(user_id))
    except Exception:
        return None


async def update_holding(ticker: str, shares: float, cost_basis: float, user_id: str) -> dict | None:
    """Returns updated holding or None if not found."""
    try:
        return await _put(f"/holdings/{ticker}", {
            "shares": shares, "cost_basis": cost_basis,
        }, headers=_auth(user_id))
    except Exception:
        return None


async def delete_holding(ticker: str, user_id: str) -> bool:
    try:
        result = await _delete(f"/holdings/{ticker}", headers=_auth(user_id))
        return result.get("ok", False)
    except Exception:
        return False


# ── Market ────────────────────────────────────────────────────────────────────

async def search_tickers(query: str) -> list[dict]:
    """Returns list of {symbol, name, type} matching query."""
    try:
        data = await _get(f"/market/search?q={query}")
        return data.get("results", [])
    except Exception:
        return []


async def get_quote(ticker: str) -> dict | None:
    """Returns {ticker, price, change, change_pct, name, exchange, ...} or None."""
    try:
        return await _get(f"/market/{ticker}/quote")
    except Exception:
        return None


async def get_metrics(ticker: str) -> dict:
    """Returns {ticker, issuer_ticker, metrics: list[dict]} or empty shell on error."""
    try:
        return await _get(f"/market/{ticker}/metrics")
    except Exception:
        return {"metrics": [], "issuer_ticker": None}


# ── Watchlist ─────────────────────────────────────────────────────────────────

async def get_watchlist(user_id: str) -> list[dict]:
    try:
        return await _get("/watchlist", headers=_auth(user_id))
    except Exception:
        return []


async def add_watchlist_item(ticker: str, user_id: str) -> dict | None:
    try:
        return await _post("/watchlist", {"ticker": ticker}, headers=_auth(user_id))
    except Exception:
        return None


async def delete_watchlist_item(ticker: str, user_id: str) -> bool:
    try:
        result = await _delete(f"/watchlist/{ticker}", headers=_auth(user_id))
        return result.get("ok", False)
    except Exception:
        return False


# ── Portfolio ─────────────────────────────────────────────────────────────────

async def get_portfolio_summary(user_id: str) -> dict | None:
    """
    Returns {total_value, portfolio_yield, holdings: [...]} or None.
    Each holding has: ticker, name, shares, cost_basis, price, change_pct,
                      market_value, allocation_pct, dividend_yield, annual_income.
    """
    try:
        return await _get("/portfolio/summary", headers=_auth(user_id))
    except Exception:
        return None
