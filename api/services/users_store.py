from services.db import get_cursor


def init_db() -> None:
    with get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         TEXT PRIMARY KEY,
                email      TEXT UNIQUE NOT NULL,
                name       TEXT NOT NULL,
                picture    TEXT,
                theme_mode TEXT DEFAULT 'light'
            )
        """)


def get_by_id(user_id: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, email, name, picture, theme_mode FROM users WHERE id = %s",
            (user_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def get_by_email(email: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, email, name, picture, theme_mode FROM users WHERE email = %s",
            (email,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def set_theme_mode(user_id: str, mode: str) -> None:
    with get_cursor() as cur:
        cur.execute(
            "UPDATE users SET theme_mode = %s WHERE id = %s",
            (mode if mode in ("light", "dark") else "light", user_id),
        )


def upsert(user_id: str, email: str, name: str, picture: str | None = None) -> dict:
    existing = get_by_email(email)
    if existing:
        with get_cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, picture = %s WHERE email = %s",
                (name, picture, email),
            )
        return get_by_id(existing["id"])

    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (id, email, name, picture) VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email,
                                           name  = EXCLUDED.name,
                                           picture = EXCLUDED.picture
            """,
            (user_id, email, name, picture),
        )
    return get_by_id(user_id)


def get_first() -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, email, name, picture, theme_mode FROM users LIMIT 1"
        )
        row = cur.fetchone()
    return dict(row) if row else None
