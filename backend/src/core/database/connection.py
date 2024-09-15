from contextlib import contextmanager

import psycopg2

from src.config import Settings

settings: Settings = Settings()


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
        host=settings.db_host,
        port=settings.db_port,
    )
    try:
        yield conn
    finally:
        conn.close()
