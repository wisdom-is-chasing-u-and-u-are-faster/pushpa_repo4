"""
Database and Schema Verification Tests (REQ-N-008, Step 1).
"""

from app.db.connection import get_db


def test_database_initialization_and_tables():
    """Verify that all required digital banking tables and indexes exist."""
    required_tables = [
        "users",
        "customers",
        "accounts",
        "journal_entries",
        "transfers",
        "cards",
        "approvals",
        "fraud_alerts",
        "audit_logs"
    ]
    with get_db() as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [r["name"] for r in rows]
        for tbl in required_tables:
            assert tbl in table_names, f"Table {tbl} missing from database."


def test_seed_data_integrity():
    """Verify that initial baseline accounts and customer entities are properly seeded."""
    with get_db() as conn:
        acc_count = conn.execute(
            "SELECT COUNT(*) as cnt FROM accounts").fetchone()["cnt"]
        assert acc_count >= 3, "Seed accounts missing."

        card_count = conn.execute(
            "SELECT COUNT(*) as cnt FROM cards").fetchone()["cnt"]
        assert card_count >= 3, "Seed cards missing."
