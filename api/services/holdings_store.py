import sqlite3
import uuid
from pathlib import Path

_DB_DIR = Path(__file__).parents[2] / "data"
_DB_PATH = _DB_DIR / "holdings.db"

_SEED_USER = ("prov24@gmail.com", "Justan")

_SEED_HOLDINGS = [
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
        # Users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id      TEXT PRIMARY KEY,
                email   TEXT UNIQUE NOT NULL,
                name    TEXT NOT NULL,
                picture TEXT
            )
        """)

        # Seed user on first run
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            user_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
                (user_id, _SEED_USER[0], _SEED_USER[1]),
            )
        else:
            user_id = conn.execute("SELECT id FROM users LIMIT 1").fetchone()[0]

        # Holdings table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                ticker     TEXT PRIMARY KEY,
                shares     REAL NOT NULL,
                cost_basis REAL NOT NULL,
                user_id    TEXT REFERENCES users(id)
            )
        """)

        # Migrate: add user_id column if it doesn't exist yet
        cols = [r[1] for r in conn.execute("PRAGMA table_info(holdings)").fetchall()]
        if "user_id" not in cols:
            conn.execute("ALTER TABLE holdings ADD COLUMN user_id TEXT REFERENCES users(id)")

        # Assign any unowned holdings to the seed user
        conn.execute("UPDATE holdings SET user_id = ? WHERE user_id IS NULL", (user_id,))

        # Seed holdings on first run (no holdings at all)
        if conn.execute("SELECT COUNT(*) FROM holdings").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO holdings (ticker, shares, cost_basis, user_id) VALUES (?, ?, ?, ?)",
                [(t, s, c, user_id) for t, s, c in _SEED_HOLDINGS],
            )


def get_all(user_id: str) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT ticker, shares, cost_basis FROM holdings WHERE user_id = ? ORDER BY ticker",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get(ticker: str, user_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT ticker, shares, cost_basis FROM holdings WHERE ticker = ? AND user_id = ?",
            (ticker.upper(), user_id),
        ).fetchone()
    return dict(row) if row else None


def add(ticker: str, shares: float, cost_basis: float, user_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO holdings (ticker, shares, cost_basis, user_id) VALUES (?, ?, ?, ?)",
            (ticker.upper(), shares, cost_basis, user_id),
        )


def update(ticker: str, shares: float, cost_basis: float, user_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE holdings SET shares = ?, cost_basis = ? WHERE ticker = ? AND user_id = ?",
            (shares, cost_basis, ticker.upper(), user_id),
        )


def remove(ticker: str, user_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "DELETE FROM holdings WHERE ticker = ? AND user_id = ?",
            (ticker.upper(), user_id),
        )
