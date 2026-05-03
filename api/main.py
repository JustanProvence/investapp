from fastapi import FastAPI
from services import holdings_store, watchlist_store
from routers import auth, holdings, watchlist, market, portfolio

holdings_store.init_db()
watchlist_store.init_db()

app = FastAPI(title="WealthShield API")
app.include_router(auth.router)
app.include_router(holdings.router)
app.include_router(watchlist.router)
app.include_router(market.router)
app.include_router(portfolio.router)
