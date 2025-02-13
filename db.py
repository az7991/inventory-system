import sqlite3

def connect_db():
    return sqlite3.connect("inventory.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        item TEXT PRIMARY KEY,
        quantity INTEGER
    )
    """)
    conn.commit()
    conn.close()
