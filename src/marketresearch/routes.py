LOGIN = "/"
SUMMARY = "/summary"
ANALYSIS = "/analysis"
ANALYSIS_ADD = "/analysis/add"
ANALYSIS_TICKER = "/analysis/ticker"
HOLDINGS = "/holdings"
HOLDINGS_ADD = "/holdings/add"
HOLDINGS_UPDATE = "/holdings/update"
HOLDINGS_TICKER = "/holdings/ticker"
SETTINGS = "/settings"
DASHBOARD = "/dashboard"

def asset(asset_id: str) -> str:
    return f"/asset/{asset_id}"

def ticker(ticker_id: str) -> str:
    return f"/holdings/ticker/{ticker_id}"

def holding_update(ticker_id: str) -> str:
    return f"/holdings/update/{ticker_id}"

def analysis_ticker(ticker_id: str) -> str:
    return f"/analysis/ticker/{ticker_id}"
