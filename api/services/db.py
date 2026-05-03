import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[2] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "")


@contextmanager
def get_cursor():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                yield cur
    finally:
        conn.close()
