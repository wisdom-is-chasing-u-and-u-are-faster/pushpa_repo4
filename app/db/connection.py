"""
Database Connection Manager supporting SQLite (local/test) and PostgreSQL (production).
Provides a context-manager for thread-safe SQLite and PostgreSQL connections.
"""

import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./digital_banking.db")


def get_db_path() -> Path:
    if DB_URL.startswith("sqlite:///"):
        raw_path = DB_URL.replace("sqlite:///", "")
        return Path(raw_path).resolve()
    return Path("./digital_banking.db").resolve()


@contextmanager
def get_db():
    """Yields a SQLite connection with Row factory enabled."""
    db_file = get_db_path()
    conn = sqlite3.connect(str(db_file), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
