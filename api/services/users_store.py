import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).parents[2] / "data" / "holdings.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _migrate() -> None:
    with _connect() as conn:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
        if "theme_mode" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN theme_mode TEXT DEFAULT 'light'")


_migrate()


def get_by_id(user_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, email, name, picture, theme_mode FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def get_by_email(email: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, email, name, picture, theme_mode FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    return dict(row) if row else None


def set_theme_mode(user_id: str, mode: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET theme_mode = ? WHERE id = ?",
            (mode if mode in ("light", "dark") else "light", user_id),
        )


def upsert(user_id: str, email: str, name: str, picture: str | None = None) -> dict:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (id, email, name, picture) VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET email=excluded.email,
                                          name=excluded.name,
                                          picture=excluded.picture
            """,
            (user_id, email, name, picture),
        )
    return get_by_id(user_id)


def get_first() -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, email, name, picture, theme_mode FROM users LIMIT 1"
        ).fetchone()
    return dict(row) if row else None
