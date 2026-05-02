import json
import time
import os
from pathlib import Path

import finnhub
import yfinance as yf
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[2] / ".env")

_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY", ""))

_CACHE_PATH = Path(__file__).parents[2] / "data" / "cache.json"
_TTL_QUOTE = 15 * 60        # 15 minutes
_TTL_FUND  = 24 * 60 * 60  # 24 hours


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _load_cache() -> dict:
    try:
        if _CACHE_PATH.exists():
            return json.loads(_CACHE_PATH.read_text())
    except Exception:
        pass
    return {}


def _save_cache(cache: dict) -> None:
    _CACHE_PATH.parent.mkdir(exist_ok=True)
    try:
        _CACHE_PATH.write_text(json.dumps(cache))
    except Exception:
        pass


def _cached(key: str, ttl: int, fetch_fn):
    cache = _load_cache()
    entry = cache.get(key)
    if entry and time.time() < entry["expires"]:
        return entry["data"]
    data = fetch_fn()
    if data is not None:
        cache[key] = {"expires": time.time() + ttl, "data": data}
        _save_cache(cache)
    return data


# ── Public API ────────────────────────────────────────────────────────────────

def get_quote(ticker: str) -> dict | None:
    """Live price, daily change, company name and exchange (15-min cache).

    Tries Finnhub first; falls back to yfinance for ETFs and funds that
    Finnhub's company_profile2 doesn't cover.
    """
    def fetch():
        try:
            q  = _client.quote(ticker)
            p  = _client.company_profile2(symbol=ticker)
            price    = q.get("c") or 0
            exchange = p.get("exchange", "")
            name     = p.get("name", "")

            if exchange and price > 0:
                return {
                    "price":      price,
                    "change":     q.get("d"),
                    "change_pct": q.get("dp"),
                    "prev_close": q.get("pc"),
                    "name":       name or ticker,
                    "exchange":   exchange,
                    "currency":   p.get("currency", "USD"),
                }
        except Exception:
            pass

        # Finnhub returned no exchange (ETF / fund / unknown) — try yfinance
        try:
            info = yf.Ticker(ticker).info
            yf_price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
            if not yf_price:
                return None
            prev      = info.get("regularMarketPreviousClose") or yf_price
            change    = yf_price - prev
            chg_pct   = (change / prev * 100) if prev else 0
            return {
                "price":      yf_price,
                "change":     change,
                "change_pct": chg_pct,
                "prev_close": prev,
                "name":       info.get("longName") or info.get("shortName") or ticker,
                "exchange":   info.get("fullExchangeName") or info.get("exchange") or "N/A",
                "currency":   info.get("currency", "USD"),
            }
        except Exception:
            return None

    return _cached(f"{ticker}_quote", _TTL_QUOTE, fetch)


def get_fundamentals(ticker: str) -> dict | None:
    """Key financial ratios from Finnhub basic-financials (24-hr cache).

    Also detects preferred stocks: Finnhub maps them to the issuer's common-stock
    data, making metrics like FCF and payout ratio misleading. We flag these so
    the router can route to a preferred-specific metric set.
    """
    def fetch():
        try:
            m = _client.company_basic_financials(ticker, "all").get("metric", {})
        except Exception:
            return None

        # Detect when Finnhub maps a preferred/derivative ticker to a different
        # underlying common-stock issuer (e.g. STRC → MSTR).
        issuer_ticker = None
        finnhub_industry = None
        try:
            profile = _client.company_profile2(symbol=ticker)
            profile_ticker = (profile.get("ticker") or "").upper()
            if profile_ticker and profile_ticker != ticker.upper():
                issuer_ticker = profile_ticker
            finnhub_industry = profile.get("finnhubIndustry") or None
        except Exception:
            pass

        div_yield = m.get("dividendYieldIndicatedAnnual")
        eps       = m.get("epsAnnual")
        dps       = m.get("dividendPerShareAnnual") or 0

        # Fetch yfinance info once — used for dividend fallback and sector detection.
        yf_info = {}
        try:
            yf_info = yf.Ticker(ticker).info or {}
        except Exception:
            pass

        if div_yield is None:
            div_rate = yf_info.get("dividendRate") or 0
            price    = yf_info.get("regularMarketPrice") or 0
            if div_rate > 0 and price > 0:
                div_yield = div_rate / price * 100
                dps       = div_rate

        sector     = finnhub_industry or yf_info.get("sector") or None
        is_utility = "util" in (sector or "").lower()

        ebitda     = yf_info.get("ebitda")
        total_debt = yf_info.get("totalDebt")
        debt_ebitda = (total_debt / ebitda) if (total_debt and ebitda and ebitda > 0) else None

        # Preferred-stock heuristic:
        # High yield (>7%) + issuer has negative EPS + payout ratio unavailable
        # → Finnhub is returning the common issuer's financials for a preferred share.
        payout = m.get("payoutRatioAnnual")
        is_preferred = (
            div_yield is not None and div_yield > 7
            and eps is not None and eps < 0
            and payout is None
        )

        return {
            "payout_ratio":       payout,
            "debt_equity":        m.get("totalDebt/totalEquityAnnual"),
            "dividend_yield":     div_yield,
            "dividend_growth_5y": m.get("dividendGrowthRate5Y"),
            "revenue_growth_5y":  m.get("revenueGrowth5Y"),
            "dps_annual":         dps or m.get("dividendPerShareAnnual"),
            "eps_annual":         eps,
            "ocf_per_share_ttm":  m.get("cashFlowPerShareTTM"),
            "interest_coverage":  m.get("netInterestCoverageAnnual"),
            "debt_ebitda":        debt_ebitda,
            "current_ratio":      m.get("currentRatioAnnual"),
            "beta":               m.get("beta"),
            "sector":             sector,
            "is_preferred":       is_preferred,
            "is_utility":         is_utility,
            "issuer_ticker":      issuer_ticker,
        }

    return _cached(f"{ticker}_fundamentals", _TTL_FUND, fetch)


def get_statements(ticker: str) -> dict:
    """Multi-year cash flow and income data via yfinance (24-hr cache).

    Returns lists ordered most-recent first.
    """
    def fetch():
        def _series(df, *candidates):
            if df is None or df.empty:
                return []
            for name in candidates:
                match = next((k for k in df.index if name.lower() in k.lower()), None)
                if match:
                    return [v for v in df.loc[match].dropna().tolist()
                            if isinstance(v, (int, float))]
            return []

        try:
            t  = yf.Ticker(ticker)
            cf = t.cashflow
            inc = t.financials
            return {
                "ocf":            _series(cf,  "Operating Cash Flow", "Total Cash From Operating"),
                "net_income":     _series(inc, "Net Income"),
                "revenue":        _series(inc, "Total Revenue"),
                "fcf":            _series(cf,  "Free Cash Flow"),
                "dividends_paid": _series(cf,  "Common Stock Dividends", "Dividends Paid"),
            }
        except Exception:
            return {"ocf": [], "net_income": [], "revenue": [], "fcf": [], "dividends_paid": []}

    return _cached(f"{ticker}_statements", _TTL_FUND, fetch)


def search_symbols(query: str) -> list[dict]:
    """Ticker symbol search via Finnhub (5-min cache)."""
    def fetch():
        try:
            raw = _client.symbol_lookup(query)
            allowed = {"Common Stock", "ETP", "ETF", "ADR"}
            return [
                {"symbol": r["symbol"], "name": r["description"], "type": r.get("type", "")}
                for r in raw.get("result", [])
                if r.get("type", "") in allowed and "." not in r["symbol"]
            ][:8]
        except Exception:
            return []
    return _cached(f"search_{query.lower()}", 5 * 60, fetch)


def get_etf_info(ticker: str) -> dict | None:
    """ETF/fund metadata from yfinance for tickers Finnhub doesn't cover (24-hr cache)."""
    def fetch():
        try:
            info = yf.Ticker(ticker).info
            if not info.get("totalAssets"):
                return None
            return {
                "distribution_yield":    info.get("yield"),
                "beta_3y":               info.get("beta3Year"),
                "total_assets":          info.get("totalAssets"),
                "ytd_return":            info.get("ytdReturn"),
                "three_year_avg_return": info.get("threeYearAverageReturn"),
                "category":              info.get("category"),
                "fund_family":           info.get("fundFamily"),
                "nav":                   info.get("navPrice"),
            }
        except Exception:
            return None
    return _cached(f"{ticker}_etf_info", _TTL_FUND, fetch)


def clear_cache(ticker: str | None = None) -> None:
    """Remove cached entries — all entries if ticker is None."""
    cache = _load_cache()
    if ticker:
        cache = {k: v for k, v in cache.items() if not k.startswith(ticker)}
    else:
        cache = {}
    _save_cache(cache)
