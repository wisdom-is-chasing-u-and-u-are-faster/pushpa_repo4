"""
Database Initializer: Executes db/schema.sql and db/seed.sql on startup.
"""

from app.db.connection import get_db
import sys
from pathlib import Path

# Add project root to sys.path for direct execution
repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


def init_database():
    """Initializes tables and seeds initial data if not present."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    schema_path = base_dir / "db" / "schema.sql"
    seed_path = base_dir / "db" / "seed.sql"

    with get_db() as conn:
        if schema_path.exists():
            schema_sql = schema_path.read_text(encoding="utf-8")
            conn.executescript(schema_sql)
        if seed_path.exists():
            seed_sql = seed_path.read_text(encoding="utf-8")
            conn.executescript(seed_sql)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
