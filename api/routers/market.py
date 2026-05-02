from fastapi import APIRouter, HTTPException
from services import market, metrics as metrics_svc
from models import QuoteResponse, MetricsResponse, MetricResult

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/search")
def search(q: str = ""):
    if len(q) < 1:
        return {"results": []}
    return {"results": market.search_symbols(q.upper())}


@router.get("/{ticker}/quote", response_model=QuoteResponse)
def get_quote(ticker: str):
    ticker = ticker.upper()
    data = market.get_quote(ticker)
    if data is None or not (data.get("price") or 0) > 0:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    return QuoteResponse(ticker=ticker, **data)


@router.get("/{ticker}/metrics", response_model=MetricsResponse)
def get_metrics(ticker: str):
    ticker = ticker.upper()
    fundamentals = market.get_fundamentals(ticker)
    statements   = market.get_statements(ticker)

    # ETFs have no stock-specific fundamentals; beta alone doesn't make it a stock
    _STOCK_KEYS = ("payout_ratio", "debt_equity", "revenue_growth_5y",
                   "eps_annual", "interest_coverage")
    is_etf = fundamentals is None or all(
        fundamentals.get(k) is None for k in _STOCK_KEYS
    )
    is_preferred = fundamentals and fundamentals.get("is_preferred", False)
    issuer_ticker = fundamentals.get("issuer_ticker") if fundamentals else None

    if is_preferred:
        fundamentals["_ticker"] = ticker
        results = metrics_svc.preferred_compute(fundamentals)
    elif is_etf:
        etf_info = market.get_etf_info(ticker)
        if not etf_info:
            raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
        results = metrics_svc.etf_compute(etf_info)
    else:
        results = metrics_svc.compute(fundamentals, statements)

    return MetricsResponse(
        ticker=ticker,
        issuer_ticker=issuer_ticker,
        metrics=[MetricResult(**m) for m in results],
    )
