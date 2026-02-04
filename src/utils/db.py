import sqlite3

DB_PATH = "nba.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS mvp_rankings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id,
        player_name TEXT,
        mvp_score REAL,
        run_date
        
    )
    """)

    conn.commit()
    conn.close()

def insert_player(run_id, name, score, date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO mvp_rankings (run_id, player_name, mvp_score, run_date)
    VALUES (?, ?, ?, ?)
    """, (run_id, name, score, date))

    conn.commit()
    conn.close()


