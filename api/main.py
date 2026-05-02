from fastapi import FastAPI
from services import holdings_store
from routers import holdings, market, portfolio

holdings_store.init_db()

app = FastAPI(title="WealthShield API")
app.include_router(holdings.router)
app.include_router(market.router)
app.include_router(portfolio.router)
