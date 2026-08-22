import psycopg2

# Configure database credentials matching your Docker container
DB_PARAMS = {
    "dbname": "nba_mvp_db",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": "5433" 
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    # Fixed syntax: 'SERIAL' auto-increments, explicit DATA TYPES added, '%s' placeholders
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mvp_rankings (
        id SERIAL PRIMARY KEY,
        run_id VARCHAR(50),
        player_name VARCHAR(100),
        mvp_score NUMERIC(10, 4),
        run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_player(run_id, name, score, date):
    conn = get_connection()
    cur = conn.cursor()

    # Replaced '?' with Postgres '%s' syntax
    cur.execute("""
    INSERT INTO mvp_rankings (run_id, player_name, mvp_score, run_date)
    VALUES (%s, %s, %s, %s)
    """, (run_id, name, score, date))

    conn.commit()
    cur.close()
    conn.close()




if __name__ == "__main__":
    print("Creating table...")
    create_table()
    print("Table created successfully!")

    print("Inserting test record...")
    insert_player("run_001", "Nikola Jokic", 98.5, "2026-08-21")
    print("Record inserted successfully!")