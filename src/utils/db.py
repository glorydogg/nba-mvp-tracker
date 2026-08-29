import snowflake.connector


SNOWFLAKE_CONFIG = {
    "user": "GLORYDOGGZ",
    "password": "WbP8d6qFeJnC6XU",
    "account": "AHPROXW-DI24909",  # e.g., xy12345.us-east-1
    "warehouse": "COMPUTE_WH",
    "database": "NBA_MVP_DB",
    "schema": "PUBLIC"
}

def get_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    # Snowflake syntax: Data types are upper-cased, table created in active schema
    cur.execute("""
    CREATE TABLE IF NOT EXISTS MVP_RANKINGS (
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

    print("Inserting test record...")
    insert_player("run_001", "Nikola Jokic", 98.5000, 26.4, 12.4, 9.0, "2026-08-29 12:00:00")
    print("Record inserted successfully into Snowflake!")