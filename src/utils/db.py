import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER", "GLORYDOGGZ"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT", "AHPROXW-DI24909"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database": os.getenv("SNOWFLAKE_DATABASE", "NBA_MVP_DB"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
}

def get_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS NBA_MVP_DB.PUBLIC.MVP_RANKINGS (
        RUN_ID VARCHAR(50),
        PLAYER_NAME VARCHAR(100),
        MVP_SCORE NUMBER(10, 4),
        PTS NUMBER(5, 1),
        REB NUMBER(5, 1),
        AST NUMBER(5, 1),
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


if __name__ == "__main__":
    print("Verifying Snowflake table structure...")
    create_table()
    print("Table verified successfully!")

    print("Inserting batch test records...")
    test_batch = [
        ("run_test_001", "Nikola Jokić", 98.5000, "2026-08-29 12:00:00"),
        ("run_test_001", "Shai Gilgeous-Alexander", 99.1000, "2026-08-29 12:00:00")
    ]
    insert_players_batch(test_batch)
    print("Batch test records inserted successfully into Snowflake!")