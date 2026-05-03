from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator


# ── Holdings ──────────────────────────────────────────────────────────────────

class HoldingCreate(BaseModel):
    ticker: str
    shares: float
    cost_basis: float

    @field_validator("ticker")
    @classmethod
    def upper(cls, v: str) -> str:
        return v.strip().upper()


class HoldingUpdate(BaseModel):
    shares: float
    cost_basis: float


class HoldingResponse(BaseModel):
    ticker: str
    shares: float
    cost_basis: float


class DeleteResponse(BaseModel):
    ok: bool = True


# ── Watchlist ─────────────────────────────────────────────────────────────────

class WatchlistCreate(BaseModel):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def upper(cls, v: str) -> str:
        return v.strip().upper()


class WatchlistResponse(BaseModel):
    ticker: str


# ── Market ────────────────────────────────────────────────────────────────────

class QuoteResponse(BaseModel):
    ticker: str
    price: float | None
    change: float | None
    change_pct: float | None
    prev_close: float | None
    name: str
    exchange: str
    currency: str


class MetricResult(BaseModel):
    name: str
    value: str
    status: Literal["good", "warn", "bad"]
    description: str


class MetricsResponse(BaseModel):
    ticker: str
    issuer_ticker: str | None = None
    metrics: list[MetricResult]


# ── Portfolio summary ─────────────────────────────────────────────────────────

class PortfolioHolding(BaseModel):
    ticker: str
    name: str
    shares: float
    cost_basis: float
    price: float | None
    change_pct: float | None
    market_value: float | None
    allocation_pct: float | None  # % of total portfolio value
    dividend_yield: float | None  # % (e.g. 0.38 = 0.38%)
    annual_income: float | None   # estimated annual dividend income $
    sector: str | None = None


class SummaryResponse(BaseModel):
    total_value: float | None = None
    portfolio_yield: float | None = None       # weighted-average yield %
    total_invested: float | None = None        # sum of shares × cost_basis
    unrealized_gain: float | None = None       # current value − total invested
    unrealized_pct: float | None = None        # unrealized gain as % of invested
    estimated_annual_income: float | None = None  # projected annual dividends
    holdings: list[PortfolioHolding] = []
    sector_allocation: list[dict] | None = None  # [{sector, allocation_pct}] sorted desc
