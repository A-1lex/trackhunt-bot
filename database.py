
import sqlite3
from config import DB_PATH
from datetime import datetime

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        file_id TEXT,
        title TEXT,
        artist TEXT,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_id TEXT,
        title TEXT,
        artist TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def save_track(query, file_id, title, artist, user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tracks (query, file_id, title, artist, user_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (query, file_id, title, artist, user_id, datetime.now()))
    conn.commit()
    conn.close()

def get_cached_track(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT file_id, title, artist FROM tracks WHERE query = ? ORDER BY timestamp DESC LIMIT 1", (query,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"file_id": row[0], "title": row[1], "artist": row[2]}
    return None

def get_top_queries(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT query, COUNT(*) as count
        FROM tracks
        GROUP BY query
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))
    results = cur.fetchall()
    conn.close()
    return results

def save_favorite(user_id, file_id, title, artist):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO favorites (user_id, file_id, title, artist, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, file_id, title, artist, datetime.now()))
    conn.commit()
    conn.close()

def get_favorites(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT file_id, title, artist FROM favorites
        WHERE user_id = ? ORDER BY timestamp DESC
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_all_queries():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT query FROM tracks")
    results = [row[0] for row in cur.fetchall()]
    conn.close()
import sqlite3
from config import DB_PATH
from datetime import datetime

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        file_id TEXT,
        title TEXT,
        artist TEXT,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_id TEXT,
        title TEXT,
        artist TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def save_track(query, file_id, title, artist, user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tracks (query, file_id, title, artist, user_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (query, file_id, title, artist, user_id, datetime.now()))
    conn.commit()
    conn.close()

def get_cached_track(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT file_id, title, artist FROM tracks WHERE query = ? ORDER BY timestamp DESC LIMIT 1", (query,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"file_id": row[0], "title": row[1], "artist": row[2]}
    return None

def get_top_queries(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT query, COUNT(*) as count
        FROM tracks
        GROUP BY query
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))
    results = cur.fetchall()
    conn.close()
    return results

def save_favorite(user_id, file_id, title, artist):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO favorites (user_id, file_id, title, artist, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, file_id, title, artist, datetime.now()))
    conn.commit()
    conn.close()

def get_favorites(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT file_id, title, artist FROM favorites
        WHERE user_id = ? ORDER BY timestamp DESC
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_all_queries():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT query FROM tracks")
    results = [row[0] for row in cur.fetchall()]
    conn.close()
    return results