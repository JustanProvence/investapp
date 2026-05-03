from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import users_store, holdings_store, watchlist_store
from routers import auth, holdings, watchlist, market, portfolio, oauth

users_store.init_db()
holdings_store.init_db()
watchlist_store.init_db()

app = FastAPI(title="Market Research API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8550"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth.router)
app.include_router(auth.router)
app.include_router(holdings.router)
app.include_router(watchlist.router)
app.include_router(market.router)
app.include_router(portfolio.router)
