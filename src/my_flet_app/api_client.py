"""
Async HTTP client — all backend calls go through here.
Screens import from this module only; nothing touches the API directly.
"""
import httpx

_BASE = "http://127.0.0.1:8000"
_TIMEOUT = 20.0


# ── Internal helpers ──────────────────────────────────────────────────────────

async def _get(path: str):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{_BASE}{path}", timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()


async def _post(path: str, body: dict):
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{_BASE}{path}", json=body, timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()


async def _put(path: str, body: dict):
    async with httpx.AsyncClient() as c:
        r = await c.put(f"{_BASE}{path}", json=body, timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()


async def _delete(path: str):
    async with httpx.AsyncClient() as c:
        r = await c.delete(f"{_BASE}{path}", timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()


# ── Holdings ──────────────────────────────────────────────────────────────────

async def get_holdings() -> list[dict]:
    """Returns list of {ticker, shares, cost_basis}."""
    try:
        return await _get("/holdings")
    except Exception:
        return []


async def add_holding(ticker: str, shares: float, cost_basis: float) -> dict | None:
    """Returns saved holding or None on error (e.g. duplicate)."""
    try:
        return await _post("/holdings", {
            "ticker": ticker, "shares": shares, "cost_basis": cost_basis,
        })
    except Exception:
        return None


async def update_holding(ticker: str, shares: float, cost_basis: float) -> dict | None:
    """Returns updated holding or None if not found."""
    try:
        return await _put(f"/holdings/{ticker}", {
            "shares": shares, "cost_basis": cost_basis,
        })
    except Exception:
        return None


async def delete_holding(ticker: str) -> bool:
    try:
        result = await _delete(f"/holdings/{ticker}")
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


# ── Portfolio ─────────────────────────────────────────────────────────────────

async def get_portfolio_summary() -> dict | None:
    """
    Returns {total_value, portfolio_yield, holdings: [...]} or None.
    Each holding has: ticker, name, shares, cost_basis, price, change_pct,
                      market_value, allocation_pct, dividend_yield, annual_income.
    """
    try:
        return await _get("/portfolio/summary")
    except Exception:
        return None
