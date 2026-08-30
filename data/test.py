import pytest
import os
from src.utils.db import get_connection, create_table


def test_snowflake_connection():
    """Verify that Snowflake is reachable with current credentials."""
    conn = get_connection()
    assert conn is not None
    conn.close()


def test_create_table():
    """Verify that table creation executes without throwing errors."""
    try:
        create_table()
        assert True
    except Exception as e:
        pytest.fail(f"Table creation failed: {e}")


def test_required_env_vars():
    """Make sure the critical env vars are present."""
    required = ["SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD", "SNOWFLAKE_ACCOUNT"]
    missing = [var for var in required if not os.getenv(var)]
    assert not missing, f"Missing required env vars: {missing}"