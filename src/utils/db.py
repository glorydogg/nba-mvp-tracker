import os
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


def get_connection():
    """
    Create a Snowflake connection.

    Required env vars:
      - SNOWFLAKE_USER
      - SNOWFLAKE_PASSWORD
      - SNOWFLAKE_ACCOUNT

    Optional:
      - SNOWFLAKE_WAREHOUSE (default: COMPUTE_WH)
      - SNOWFLAKE_DATABASE  (default: NBA_MVP_DB)
      - SNOWFLAKE_SCHEMA    (default: PUBLIC)
      - SNOWFLAKE_PASSCODE  (6-digit MFA code — preferred for CI / non-interactive)
      - SNOWFLAKE_AUTHENTICATOR (e.g. externalbrowser for local SSO)
    """
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")

    if not all([user, password, account]):
        raise ValueError(
            "Missing required Snowflake credentials. "
            "Set SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, and SNOWFLAKE_ACCOUNT "
            f"in your environment or in {env_path}"
        )

    connect_kwargs = {
        "user": user,
        "password": password,
        "account": account,
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "NBA_MVP_DB"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
    }

    # Prefer non-interactive MFA via env var (CI-friendly)
    passcode = os.getenv("SNOWFLAKE_PASSCODE")
    authenticator = os.getenv("SNOWFLAKE_AUTHENTICATOR")

    if authenticator:
        connect_kwargs["authenticator"] = authenticator
    elif passcode:
        connect_kwargs["passcode"] = passcode
    else:
        # Fallback: interactive prompt only when running in a real terminal
        import sys
        if sys.stdin.isatty():
            mfa_code = input("Enter Google Authenticator 6-digit code (or set SNOWFLAKE_PASSCODE): ").strip()
            if mfa_code:
                connect_kwargs["passcode"] = mfa_code

    return snowflake.connector.connect(**connect_kwargs)


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS MVP_RANKINGS (
                RUN_ID      VARCHAR(50),
                PLAYER_NAME VARCHAR(100),
                MVP_SCORE   NUMBER(10, 4),
                RUN_DATE    TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        conn.commit()
    finally:
        cur.close()
        conn.close()


def insert_players_batch(players_data):
    """
    Insert a list of player tuples in a single round-trip.
    players_data format: [(run_id, name, score, date), ...]
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        insert_query = """
            INSERT INTO MVP_RANKINGS (RUN_ID, PLAYER_NAME, MVP_SCORE, RUN_DATE)
            VALUES (%s, %s, %s, %s)
        """
        cur.executemany(insert_query, players_data)
        conn.commit()
    finally:
        cur.close()
        conn.close()