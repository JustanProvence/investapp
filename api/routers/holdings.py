from fastapi import APIRouter, HTTPException
from services import holdings_store as store
from models import HoldingCreate, HoldingUpdate, HoldingResponse, DeleteResponse

router = APIRouter(prefix="/holdings", tags=["holdings"])


@router.get("", response_model=list[HoldingResponse])
def list_holdings():
    return store.get_all()


@router.post("", response_model=HoldingResponse, status_code=201)
def add_holding(body: HoldingCreate):
    if store.get(body.ticker):
        raise HTTPException(status_code=409, detail=f"{body.ticker} already exists")
    store.add(body.ticker, body.shares, body.cost_basis)
    return store.get(body.ticker)


@router.put("/{ticker}", response_model=HoldingResponse)
def update_holding(ticker: str, body: HoldingUpdate):
    ticker = ticker.upper()
    if not store.get(ticker):
        raise HTTPException(status_code=404, detail=f"{ticker} not found")
    store.update(ticker, body.shares, body.cost_basis)
    return store.get(ticker)


@router.delete("/{ticker}", response_model=DeleteResponse)
def delete_holding(ticker: str):
    ticker = ticker.upper()
    if not store.get(ticker):
        raise HTTPException(status_code=404, detail=f"{ticker} not found")
    store.remove(ticker)
    return {"ok": True}
