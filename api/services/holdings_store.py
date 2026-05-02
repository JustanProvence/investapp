import sqlite3
import os
from pathlib import Path

_DB_DIR = Path(__file__).parents[2] / "data"
_DB_PATH = _DB_DIR / "holdings.db"

_SEED = [
    ("AAPL", 142.5, 145.00),
    ("MSFT", 85.0,  310.00),
    ("JNJ",  60.0,  162.00),
    ("O",    200.0, 55.00),
]


def _connect() -> sqlite3.Connection:
    _DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                ticker     TEXT PRIMARY KEY,
                shares     REAL NOT NULL,
                cost_basis REAL NOT NULL
            )
        """)
        # Seed with demo data on first run only
        if conn.execute("SELECT COUNT(*) FROM holdings").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO holdings (ticker, shares, cost_basis) VALUES (?, ?, ?)",
                _SEED,
            )


def get_all() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT ticker, shares, cost_basis FROM holdings ORDER BY ticker"
        ).fetchall()
    return [dict(r) for r in rows]


def get(ticker: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT ticker, shares, cost_basis FROM holdings WHERE ticker = ?",
            (ticker.upper(),),
        ).fetchone()
    return dict(row) if row else None


def add(ticker: str, shares: float, cost_basis: float) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO holdings (ticker, shares, cost_basis) VALUES (?, ?, ?)",
            (ticker.upper(), shares, cost_basis),
        )


def update(ticker: str, shares: float, cost_basis: float) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE holdings SET shares = ?, cost_basis = ? WHERE ticker = ?",
            (shares, cost_basis, ticker.upper()),
        )


def remove(ticker: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM holdings WHERE ticker = ?", (ticker.upper(),))
