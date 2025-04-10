import sqlite3
from config import CHANNEL_ID

DB_FILE = "database.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            file_id TEXT,
            title TEXT,
            artist TEXT,
            user_id INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_id TEXT,
            title TEXT,
            artist TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


def get_cached_track(query: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT file_id, title, artist FROM tracks WHERE query = ?", (query.lower(),))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"file_id": row[0], "title": row[1], "artist": row[2]}
    return None


def save_track(query, file_id, title, artist, user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO tracks (query, file_id, title, artist, user_id) VALUES (?, ?, ?, ?, ?)",
                (query.lower(), file_id, title, artist, user_id))
    conn.commit()
    conn.close()


def log_query(query):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, count FROM queries WHERE query = ?", (query.lower(),))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE queries SET count = ? WHERE id = ?", (row[1] + 1, row[0]))
    else:
        cur.execute("INSERT INTO queries (query) VALUES (?)", (query.lower(),))
    conn.commit()
    conn.close()


def get_top_queries(limit=10):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT query, count FROM queries ORDER BY count DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def save_favorite(user_id, file_id, title, artist):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO favorites (user_id, file_id, title, artist) VALUES (?, ?, ?, ?)",
                (user_id, file_id, title, artist))
    conn.commit()
    conn.close()


def get_favorites(user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT file_id, title, artist FROM favorites WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_queries():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT query FROM queries")
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows
