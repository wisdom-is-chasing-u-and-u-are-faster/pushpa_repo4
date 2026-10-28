"""
Pytest configuration and test client fixtures.
"""

from app.main import app
from app.db.init_db import init_database
import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure test DB is isolated
os.environ["DATABASE_URL"] = "sqlite:///./test_digital_banking.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_database()
    yield
    test_db = Path("./test_digital_banking.db")
    if test_db.exists():
        try:
            test_db.unlink()
        except Exception:
            pass


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
