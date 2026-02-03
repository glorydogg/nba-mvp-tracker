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
        player_name TEXT,
        mvp_score REAL,
        run_date
        
    )
    """)

    conn.commit()
    conn.close()

def insert_player(name, score, date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO mvp_rankings (player_name, mvp_score, run_date)
    VALUES (?, ?, ?)
    """, (name, score, date))

    conn.commit()
    conn.close()


