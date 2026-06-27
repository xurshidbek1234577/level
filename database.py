import sqlite3

DB_NAME = "upgrade.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        is_premium INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        type TEXT,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (user_id, username)
    VALUES (?, ?)
    """, (user_id, username))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()

    conn.close()
    return user


def update_balance(user_id, amount):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE user_id = ?
    """, (amount, user_id))

    cur.execute("""
    INSERT INTO transactions (user_id, amount, type, reason)
    VALUES (?, ?, ?, ?)
    """, (user_id, amount, "plus" if amount > 0 else "minus", "manual"))

    conn.commit()
    conn.close()
