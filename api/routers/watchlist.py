from fastapi import APIRouter, Depends, HTTPException
from services import watchlist_store as store
from models import WatchlistCreate, WatchlistResponse, DeleteResponse
from dependencies import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=list[WatchlistResponse])
def list_watchlist(user: dict = Depends(get_current_user)):
    return store.get_all(user["id"])


@router.post("", response_model=WatchlistResponse, status_code=201)
def add_to_watchlist(body: WatchlistCreate, user: dict = Depends(get_current_user)):
    if store.get(body.ticker, user["id"]):
        raise HTTPException(status_code=409, detail=f"{body.ticker} already in watchlist")
    store.add(body.ticker, user["id"])
    return store.get(body.ticker, user["id"])


@router.delete("/{ticker}", response_model=DeleteResponse)
def remove_from_watchlist(ticker: str, user: dict = Depends(get_current_user)):
    ticker = ticker.upper()
    if not store.get(ticker, user["id"]):
        raise HTTPException(status_code=404, detail=f"{ticker} not found")
    store.remove(ticker, user["id"])
    return {"ok": True}
