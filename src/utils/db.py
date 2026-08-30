import os
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

def get_connection():
    password = os.getenv("SNOWFLAKE_PASSWORD")
    if not password:
        raise ValueError(f"SNOWFLAKE_PASSWORD missing or empty in .env at {env_path}")

    # Prompt terminal for the 6-digit code from Google Authenticator
    mfa_code = input("Enter Google Authenticator 6-digit code: ")

    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER", "GLORYDOGGZ"),
        password=password,
        account=os.getenv("SNOWFLAKE_ACCOUNT", "AHPROXW-DI24909"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "NBA_MVP_DB"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
        passcode=mfa_code
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS NBA_MVP_DB.PUBLIC.MVP_RANKINGS (
        RUN_ID VARCHAR(50),
        PLAYER_NAME VARCHAR(100),
        MVP_SCORE NUMBER(10, 4),
        RUN_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
    )
    """)

    cur.close()
    conn.close()


def insert_players_batch(players_data):
    """
    Inserts a list of player tuples in a single database round-trip.
    players_data format: [(run_id, name, score, date), ...]
    """
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO NBA_MVP_DB.PUBLIC.MVP_RANKINGS (RUN_ID, PLAYER_NAME, MVP_SCORE, RUN_DATE)
    VALUES (%s, %s, %s, %s)
    """
    
    cur.executemany(insert_query, players_data)
    conn.commit()
    cur.close()
    conn.close()