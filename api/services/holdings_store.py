from services.db import get_cursor


def init_db() -> None:
    with get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                ticker     TEXT NOT NULL,
                shares     REAL NOT NULL,
                cost_basis REAL NOT NULL,
                user_id    TEXT REFERENCES users(id),
                PRIMARY KEY (ticker, user_id)
            )
        """)


def get_all(user_id: str) -> list[dict]:
    with get_cursor() as cur:
        cur.execute(
            "SELECT ticker, shares, cost_basis FROM holdings WHERE user_id = %s ORDER BY ticker",
            (user_id,),
        )
        return [dict(r) for r in cur.fetchall()]


def get(ticker: str, user_id: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            "SELECT ticker, shares, cost_basis FROM holdings WHERE ticker = %s AND user_id = %s",
            (ticker.upper(), user_id),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def add(ticker: str, shares: float, cost_basis: float, user_id: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO holdings (ticker, shares, cost_basis, user_id) VALUES (%s, %s, %s, %s)",
            (ticker.upper(), shares, cost_basis, user_id),
        )


def update(ticker: str, shares: float, cost_basis: float, user_id: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "UPDATE holdings SET shares = %s, cost_basis = %s WHERE ticker = %s AND user_id = %s",
            (shares, cost_basis, ticker.upper(), user_id),
        )


def remove(ticker: str, user_id: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "DELETE FROM holdings WHERE ticker = %s AND user_id = %s",
            (ticker.upper(), user_id),
        )
