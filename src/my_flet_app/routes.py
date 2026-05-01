LOGIN = "/"
SUMMARY = "/summary"
ANALYSIS = "/analysis"
HOLDINGS = "/holdings"
HOLDINGS_ADD = "/holdings/add"
HOLDINGS_UPDATE = "/holdings/update"
SETTINGS = "/settings"
DASHBOARD = "/dashboard"

def asset(asset_id: str) -> str:
    return f"/asset/{asset_id}"
