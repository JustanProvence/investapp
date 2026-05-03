from services.db import get_cursor


def init_db() -> None:
    with get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                ticker  TEXT NOT NULL,
                user_id TEXT NOT NULL REFERENCES users(id),
                PRIMARY KEY (ticker, user_id)
            )
        """)


def get_all(user_id: str) -> list[dict]:
    with get_cursor() as cur:
        cur.execute(
            "SELECT ticker FROM watchlist WHERE user_id = %s ORDER BY ticker",
            (user_id,),
        )
        return [dict(r) for r in cur.fetchall()]


def get(ticker: str, user_id: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            "SELECT ticker FROM watchlist WHERE ticker = %s AND user_id = %s",
            (ticker.upper(), user_id),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def add(ticker: str, user_id: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO watchlist (ticker, user_id) VALUES (%s, %s)",
            (ticker.upper(), user_id),
        )


def remove(ticker: str, user_id: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "DELETE FROM watchlist WHERE ticker = %s AND user_id = %s",
            (ticker.upper(), user_id),
        )
