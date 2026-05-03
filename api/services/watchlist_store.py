import sqlite3
from pathlib import Path

_DB_DIR  = Path(__file__).parents[2] / "data"
_DB_PATH = _DB_DIR / "holdings.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                ticker  TEXT NOT NULL,
                user_id TEXT NOT NULL,
                PRIMARY KEY (ticker, user_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)


def get_all(user_id: str) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT ticker FROM watchlist WHERE user_id = ? ORDER BY ticker",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get(ticker: str, user_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT ticker FROM watchlist WHERE ticker = ? AND user_id = ?",
            (ticker.upper(), user_id),
        ).fetchone()
    return dict(row) if row else None


def add(ticker: str, user_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO watchlist (ticker, user_id) VALUES (?, ?)",
            (ticker.upper(), user_id),
        )


def remove(ticker: str, user_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "DELETE FROM watchlist WHERE ticker = ? AND user_id = ?",
            (ticker.upper(), user_id),
        )
