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
        mvp_score REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_player(name, score):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO mvp_rankings (player_name, mvp_score)
    VALUES (?, ?)
    """, (name, score))

    conn.commit()
    conn.close()
