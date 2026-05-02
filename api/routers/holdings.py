from fastapi import APIRouter, Depends, HTTPException
from services import holdings_store as store
from models import HoldingCreate, HoldingUpdate, HoldingResponse, DeleteResponse
from dependencies import get_current_user

router = APIRouter(prefix="/holdings", tags=["holdings"])


@router.get("", response_model=list[HoldingResponse])
def list_holdings(user: dict = Depends(get_current_user)):
    return store.get_all(user["id"])


@router.post("", response_model=HoldingResponse, status_code=201)
def add_holding(body: HoldingCreate, user: dict = Depends(get_current_user)):
    if store.get(body.ticker, user["id"]):
        raise HTTPException(status_code=409, detail=f"{body.ticker} already exists")
    store.add(body.ticker, body.shares, body.cost_basis, user["id"])
    return store.get(body.ticker, user["id"])


@router.put("/{ticker}", response_model=HoldingResponse)
def update_holding(ticker: str, body: HoldingUpdate, user: dict = Depends(get_current_user)):
    ticker = ticker.upper()
    if not store.get(ticker, user["id"]):
        raise HTTPException(status_code=404, detail=f"{ticker} not found")
    store.update(ticker, body.shares, body.cost_basis, user["id"])
    return store.get(ticker, user["id"])


@router.delete("/{ticker}", response_model=DeleteResponse)
def delete_holding(ticker: str, user: dict = Depends(get_current_user)):
    ticker = ticker.upper()
    if not store.get(ticker, user["id"]):
        raise HTTPException(status_code=404, detail=f"{ticker} not found")
    store.remove(ticker, user["id"])
    return {"ok": True}
