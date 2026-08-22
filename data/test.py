import pytest
import psycopg2
from src.utils.db import DB_PARAMS, create_table, fetch_all_rankings

def test_postgres_connection():
    """Verify that PostgreSQL container is reachable."""
    conn = psycopg2.connect(**DB_PARAMS)
    assert conn is not None
    conn.close()

def test_create_table():
    """Verify that table creation executes without throwing errors."""
    try:
        create_table()
        assert True
    except Exception as e:
        pytest.fail(f"Table creation failed: {e}")