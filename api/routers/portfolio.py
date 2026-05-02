from fastapi import APIRouter
from services import holdings_store as store, market
from models import SummaryResponse, PortfolioHolding

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/summary", response_model=SummaryResponse)
def get_summary():
    holdings = store.get_all()
    if not holdings:
        return SummaryResponse(total_value=None, portfolio_yield=None, holdings=[])

    # Enrich each holding with live quote data
    enriched: list[PortfolioHolding] = []
    for h in holdings:
        ticker = h["ticker"]
        quote  = market.get_quote(ticker) or {}
        fund   = market.get_fundamentals(ticker) or {}

        price         = quote.get("price")
        market_value  = h["shares"] * price if price else None
        div_yield     = fund.get("dividend_yield")           # already in % (e.g. 0.38)

        # ETFs store distribution yield in etf_info (decimal) not in fundamentals
        if div_yield is None:
            etf = market.get_etf_info(ticker) or {}
            dist = etf.get("distribution_yield")
            if dist:
                div_yield = dist * 100   # convert 0.119 → 11.9

        annual_income = (market_value * div_yield / 100
                         if market_value and div_yield else None)

        enriched.append(PortfolioHolding(
            ticker        = ticker,
            name          = quote.get("name", ticker),
            shares        = h["shares"],
            cost_basis    = h["cost_basis"],
            price         = price,
            change_pct    = quote.get("change_pct"),
            market_value  = market_value,
            allocation_pct= None,           # filled in after total is known
            dividend_yield= div_yield,
            annual_income = annual_income,
        ))

    # Total portfolio value
    values     = [p.market_value for p in enriched if p.market_value is not None]
    total      = sum(values) if values else None

    # Total cost basis across all holdings
    total_invested = sum(
        p.shares * p.cost_basis for p in enriched if p.cost_basis is not None
    ) or None

    # Allocation %, weighted yield, and income
    total_income = 0.0
    for p in enriched:
        if total and p.market_value is not None:
            p.allocation_pct = round(p.market_value / total * 100, 2)
        if p.annual_income:
            total_income += p.annual_income

    portfolio_yield = round(total_income / total * 100, 4) if total else None

    unrealized_gain = (round(total - total_invested, 2)
                       if total and total_invested else None)
    unrealized_pct  = (round(unrealized_gain / total_invested * 100, 2)
                       if unrealized_gain is not None and total_invested else None)

    return SummaryResponse(
        total_value              = round(total, 2) if total else None,
        portfolio_yield          = portfolio_yield,
        total_invested           = round(total_invested, 2) if total_invested else None,
        unrealized_gain          = unrealized_gain,
        unrealized_pct           = unrealized_pct,
        estimated_annual_income  = round(total_income, 2) if total_income else None,
        holdings                 = enriched,
    )
