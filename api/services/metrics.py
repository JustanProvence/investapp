"""
Compute the 9 WealthShield health metrics from raw market data.

All inputs come from market.get_fundamentals() and market.get_statements().
Returns a list of dicts ready to pass straight to the frontend.
"""


def _safe_div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def _cagr(values: list[float]) -> float | None:
    """Annualised growth rate from a list of values, most-recent first."""
    if len(values) < 2:
        return None
    newest, oldest = values[0], values[-1]
    # Both must be positive — a sign change means the series crossed zero,
    # making CAGR meaningless and producing complex numbers via fractional power.
    if oldest <= 0 or newest <= 0:
        return None
    n = len(values) - 1
    return ((newest / oldest) ** (1 / n) - 1) * 100


def _pct(v: float | None, decimals: int = 1) -> str:
    if v is None:
        return "N/A"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.{decimals}f}%"


def _x(v: float | None, decimals: int = 2) -> str:
    if v is None:
        return "N/A"
    return f"{v:.{decimals}f}x"


def compute(fundamentals: dict, statements: dict) -> list[dict]:
    """
    Returns list of:
      { name, value, status ("good"|"warn"|"bad"), description }
    Skips any metric where the required data is missing.
    """
    f = fundamentals or {}
    s = statements or {}
    results = []

    # 1. Distribution yield ────────────────────────────────────────────────────
    dy = f.get("dividend_yield")   # Finnhub returns as % (e.g. 0.38 = 0.38%)
    if dy is not None and dy > 0:
        if dy >= 3:
            status = "good"
            desc = "Strong yield — meaningful income relative to share price."
        elif dy >= 1:
            status = "warn"
            desc = "Moderate yield — some income but below high-yield thresholds."
        else:
            status = "bad"
            desc = "Very low yield — minimal income generation."
        results.append({"name": "Distribution Yield", "value": f"{dy:.2f}%",
                         "status": status, "description": desc})

    # 2. FCF coverage of dividends ────────────────────────────────────────────
    fcf  = s.get("fcf", [])
    divs = s.get("dividends_paid", [])
    if fcf and divs:
        fcf_val = fcf[0]
        div_val = abs(divs[0]) if divs[0] != 0 else None
        ratio   = _safe_div(fcf_val, div_val)
        if ratio is not None:
            if ratio >= 1.5:
                status = "good"
                desc = "Free cash flow comfortably covers dividend obligations with substantial margin."
            elif ratio >= 1.0:
                status = "warn"
                desc = "FCF covers dividends but the margin is thinner than ideal."
            else:
                status = "bad"
                desc = "FCF does not fully cover dividends — payout sustainability is at risk."
            results.append({"name": "FCF > Dividends", "value": _x(ratio),
                             "status": status, "description": desc})

    # 3a. Payout ratio — earnings method (total dividends paid / net income) ───
    net_inc = s.get("net_income", [])
    if divs and net_inc and net_inc[0] and net_inc[0] > 0:
        payout_e = _safe_div(abs(divs[0]), net_inc[0])
        if payout_e is not None:
            pct = payout_e * 100
            if pct < 50:
                status = "good"
                desc = "Low payout ratio — significant earnings retained for growth and future dividend increases."
            elif pct < 75:
                status = "warn"
                desc = "Moderate payout — some buffer remains but dividend growth may be limited."
            else:
                status = "bad"
                desc = "High payout ratio limits room for growth and raises dividend cut risk."
            results.append({"name": "Payout Ratio (Earnings)", "value": f"{pct:.1f}%",
                             "status": status, "description": desc})

    # 3b. Payout ratio — per-share method (DPS / EPS) ─────────────────────────
    dps    = f.get("dps_annual")
    eps    = f.get("eps_annual")
    pct_ps = None
    if dps and eps and eps > 0:
        ratio = _safe_div(dps, eps)
        if ratio is not None:
            pct_ps = ratio * 100
    elif f.get("payout_ratio") is not None:
        pct_ps = f.get("payout_ratio")  # Finnhub pre-calculated, already in %
    if pct_ps is not None:
        if pct_ps < 50:
            status = "good"
            desc = "Low per-share payout — EPS comfortably supports the dividend with room to grow."
        elif pct_ps < 75:
            status = "warn"
            desc = "Moderate per-share payout — dividend is covered but growth headroom is limited."
        else:
            status = "bad"
            desc = "High per-share payout — dividend consumes most EPS, raising sustainability concerns."
        results.append({"name": "Payout Ratio (DPS/EPS)", "value": f"{pct_ps:.1f}%",
                         "status": status, "description": desc})

    # 3. Debt to equity ────────────────────────────────────────────────────────
    de = f.get("debt_equity")
    if de is not None:
        if de < 0.5:
            status = "good"
            desc = "Conservative leverage with a clean balance sheet."
        elif de < 1.5:
            status = "warn"
            desc = "Moderate leverage — manageable but worth monitoring."
        else:
            status = "bad"
            desc = "High leverage increases financial risk, especially in rising rate environments."
        results.append({"name": "Debt to Equity", "value": f"{de:.2f}",
                         "status": status, "description": desc})

    # 4. Interest coverage (inverse proxy for rate sensitivity) ────────────────
    ic = f.get("interest_coverage")
    if ic is not None:
        if ic > 5:
            status = "good"
            desc = "Strong interest coverage — low sensitivity to rate increases."
        elif ic > 2:
            status = "warn"
            desc = "Moderate coverage — some exposure to rising interest rates."
        else:
            status = "bad"
            desc = "Weak coverage — highly sensitive to interest rate changes."
        results.append({"name": "Interest Coverage", "value": _x(ic),
                         "status": status, "description": desc})


    # 5. Revenue growth (5yr) ──────────────────────────────────────────────────
    rev_growth = f.get("revenue_growth_5y")
    if rev_growth is not None:
        if rev_growth > 5:
            status = "good"
            desc = "Strong top-line growth sustained over 5 years."
        elif rev_growth >= 0:
            status = "warn"
            desc = "Modest revenue growth — stable but not expanding rapidly."
        else:
            status = "bad"
            desc = "Revenue has declined over the past 5 years."
        results.append({"name": "Revenue Trend (5yr)", "value": _pct(rev_growth),
                         "status": status, "description": desc})

    # 6. Dividend growth (5yr) ─────────────────────────────────────────────────
    div_growth = f.get("dividend_growth_5y")
    if div_growth is not None:
        if div_growth > 5:
            status = "good"
            desc = "Dividend growth well above inflation — strong shareholder returns."
        elif div_growth >= 2:
            status = "warn"
            desc = "Modest dividend growth — keeps pace with inflation but not much more."
        else:
            status = "bad"
            desc = "Dividend growth is stagnant or declining."
        results.append({"name": "Dividend Growth (5yr)", "value": _pct(div_growth),
                         "status": status, "description": desc})

    # 7. OCF vs net income (earnings quality) ──────────────────────────────────
    ocf = s.get("ocf", [])
    if ocf and net_inc and net_inc[0] != 0:
        ratio = ocf[0] / net_inc[0]
        if ratio >= 1.0:
            status, val = "good", "High Quality"
            desc = "Operating cash flow exceeds net income — strong earnings quality signal."
        elif ratio >= 0.8:
            status, val = "warn", "Moderate"
            desc = "OCF slightly below net income — worth monitoring accrual patterns."
        else:
            status, val = "bad", "Low Quality"
            desc = "Net income significantly exceeds OCF — potential earnings quality concern."
        results.append({"name": "OCF > Net Income", "value": val,
                         "status": status, "description": desc})

    # 8. OCF growth CAGR ───────────────────────────────────────────────────────
    if len(ocf) >= 2:
        ocf_cagr = _cagr(ocf)
        if ocf_cagr is not None:
            if ocf_cagr > 5:
                status = "good"
                desc = "Operating cash flow has grown solidly over the measurement period."
            elif ocf_cagr >= 0:
                status = "warn"
                desc = "OCF growth is positive but modest."
            else:
                status = "bad"
                desc = "Operating cash flow has contracted — may signal earnings pressure."
            results.append({"name": f"OCF Growth ({len(ocf) - 1}yr)",
                             "value": _pct(ocf_cagr), "status": status, "description": desc})

    # 9. Beta ──────────────────────────────────────────────────────────────────
    beta = f.get("beta")
    if beta is not None:
        if beta < 0.8:
            status = "good"
            desc = "Low beta — this stock is less volatile than the broader market (defensive)."
        elif beta <= 1.2:
            status = "warn"
            desc = "Beta close to 1 — moves broadly in line with the market."
        else:
            status = "bad"
            desc = "High beta — amplified swings increase downside risk in market sell-offs."
        results.append({"name": "Beta", "value": f"{beta:.2f}",
                         "status": status, "description": desc})

    # 10. Chowder Rule (yield + 5yr dividend growth) ───────────────────────────
    dy = f.get("dividend_yield")
    dg = f.get("dividend_growth_5y")
    if dy is not None and dg is not None:
        score = dy + dg
        if f.get("is_utility"):
            threshold = 8
            tier = "utility"
        elif dy >= 3:
            threshold = 12
            tier = "high-yield (≥3% yield)"
        else:
            threshold = 15
            tier = "growth (<3% yield)"
        status = "good" if score >= threshold else "bad"
        desc = (
            f"Yield {dy:.2f}% + 5yr div growth {dg:.1f}% = {score:.1f}. "
            f"{'Meets' if status == 'good' else 'Falls short of'} the "
            f"{threshold}% target for {tier} stocks."
        )
        results.append({"name": "Chowder Rule", "value": f"{score:.1f}",
                         "status": status, "description": desc})

    return results


def preferred_compute(fundamentals: dict) -> list[dict]:
    """
    Metrics for preferred stocks and similar fixed-income equity instruments.
    Uses the same {name, value, status, description} format.
    Each metric name is tagged with the ticker it is sourced from.
    """
    f      = fundamentals or {}
    issuer = f.get("issuer_ticker")          # e.g. "MSTR" for STRC
    ticker = f.get("_ticker", "this ticker") # populated by router

    def _src(source: str) -> str:
        """Append '(TICKER)' source label to metric name."""
        return f" ({source})"

    results = []

    # 1. Distribution yield — specific to the preferred security itself
    dy = f.get("dividend_yield")
    if dy is not None and dy > 0:
        if dy >= 6:
            status = "good"
            desc = "High preferred dividend yield relative to par — strong income generation."
        elif dy >= 4:
            status = "warn"
            desc = "Moderate preferred yield — decent income, typical for investment-grade preferreds."
        else:
            status = "bad"
            desc = "Low preferred yield — limited income relative to price paid."
        results.append({"name": f"Distribution Yield{_src(ticker)}",
                         "value": f"{dy:.2f}%",
                         "status": status, "description": desc})

    # 2. Beta — price behaviour of the preferred itself
    beta = f.get("beta")
    if beta is not None:
        if beta < 0.5:
            status = "good"
            desc = "Low price volatility relative to the market — behaves closer to a bond."
        elif beta <= 1.0:
            status = "warn"
            desc = "Moderate volatility — more equity-like sensitivity than a typical preferred."
        else:
            status = "bad"
            desc = "High beta for a preferred — price swings significantly with the broader market."
        results.append({"name": f"Beta{_src(ticker)}",
                         "value": f"{beta:.2f}",
                         "status": status, "description": desc})

    # 3–4. Issuer credit metrics — sourced from the common issuer
    issuer_label = issuer or "issuer"

    de = f.get("debt_equity")
    if de is not None:
        if de < 1.0:
            status = "good"
            desc = (f"Relatively conservative leverage at {issuer_label} — "
                    "preferred dividend has a reasonable safety buffer.")
        elif de < 3.0:
            status = "warn"
            desc = (f"Moderate leverage at {issuer_label} — "
                    "monitor for deterioration in credit quality.")
        else:
            status = "bad"
            desc = (f"High leverage at {issuer_label} — "
                    "elevated risk of preferred dividend suspension in a downturn.")
        results.append({"name": f"Debt / Equity{_src(issuer_label)}",
                         "value": f"{de:.2f}",
                         "status": status, "description": desc})

    ic = f.get("interest_coverage")
    if ic is not None and ic > -500:
        if ic > 3:
            status = "good"
            desc = (f"{issuer_label} comfortably covers its fixed obligations, "
                    "supporting preferred dividend safety.")
        elif ic > 1:
            status = "warn"
            desc = (f"{issuer_label} coverage is thin — "
                    "preferred dividend may be at risk in a downturn.")
        else:
            status = "bad"
            desc = (f"{issuer_label} cannot fully cover fixed charges — "
                    "elevated preferred dividend risk.")
        results.append({"name": f"Interest Coverage{_src(issuer_label)}",
                         "value": f"{ic:.2f}x",
                         "status": status, "description": desc})

    return results


def etf_compute(info: dict) -> list[dict]:
    """
    ETF/fund-specific metrics from yfinance info dict.
    Uses the same {name, value, status, description} format as compute().
    """
    results = []
    i = info or {}

    # 1. Distribution yield ────────────────────────────────────────────────────
    dy = i.get("distribution_yield")
    if dy is not None:
        pct_val = dy * 100
        if pct_val >= 4:
            status = "good"
            desc = "Strong distribution yield relative to the broader market."
        elif pct_val >= 2:
            status = "warn"
            desc = "Moderate yield — decent income but below high-yield thresholds."
        else:
            status = "bad"
            desc = "Low distribution yield — limited income generation."
        results.append({"name": "Distribution Yield", "value": f"{pct_val:.2f}%",
                         "status": status, "description": desc})

    # 2. Beta (3-year) ─────────────────────────────────────────────────────────
    beta = i.get("beta_3y")
    if beta is not None:
        if beta < 0.8:
            status = "good"
            desc = "Low beta — this fund moves less than the broader market (defensive)."
        elif beta <= 1.1:
            status = "warn"
            desc = "Beta close to 1 — tracks the market fairly closely."
        else:
            status = "bad"
            desc = "High beta — amplified market swings increase downside risk."
        results.append({"name": "Beta (3-Year)", "value": f"{beta:.2f}",
                         "status": status, "description": desc})

    # 3. Total assets (fund size / liquidity) ──────────────────────────────────
    aum = i.get("total_assets")
    if aum is not None:
        if aum >= 1_000_000_000:
            status = "good"
            val  = f"${aum / 1_000_000_000:.1f}B"
            desc = "Large fund with strong liquidity and low closure risk."
        elif aum >= 100_000_000:
            status = "warn"
            val  = f"${aum / 1_000_000:.0f}M"
            desc = "Mid-size fund — adequate liquidity, but watch for low-volume days."
        else:
            status = "bad"
            val  = f"${aum / 1_000_000:.0f}M"
            desc = "Small fund — higher bid/ask spreads and potential closure risk."
        results.append({"name": "Assets Under Mgmt", "value": val,
                         "status": status, "description": desc})

    # 4. YTD return ────────────────────────────────────────────────────────────
    ytd = i.get("ytd_return")
    if ytd is not None:
        pct_val = ytd * 100 if abs(ytd) < 2 else ytd  # normalise if decimal
        if pct_val > 5:
            status = "good"
            desc = "Strong year-to-date performance relative to typical benchmarks."
        elif pct_val >= 0:
            status = "warn"
            desc = "Modest positive return year-to-date."
        else:
            status = "bad"
            desc = "Negative year-to-date return — underperforming so far this year."
        results.append({"name": "YTD Return", "value": f"{pct_val:.2f}%",
                         "status": status, "description": desc})

    # 5. 3-year average annual return ──────────────────────────────────────────
    r3 = i.get("three_year_avg_return")
    if r3 is not None:
        pct_val = r3 * 100 if abs(r3) < 2 else r3
        if pct_val > 8:
            status = "good"
            desc = "Strong 3-year annualised return — consistent long-term performance."
        elif pct_val >= 3:
            status = "warn"
            desc = "Moderate 3-year return — steady but not standout performance."
        else:
            status = "bad"
            desc = "Below-average 3-year return — consider comparing against similar funds."
        results.append({"name": "3-Year Avg Return", "value": f"{pct_val:.2f}%",
                         "status": status, "description": desc})

    # 6. Category (informational) ──────────────────────────────────────────────
    cat = i.get("category")
    fam = i.get("fund_family")
    if cat:
        label = f"{fam} — {cat}" if fam else cat
        results.append({"name": "Fund Category", "value": label,
                         "status": "warn",
                         "description": "Morningstar category classification for this fund."})

    return results
