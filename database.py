import sqlite3
import os
from datetime import datetime

DB_NAME = "upgrade.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    # Eski tables'ni o'chirish (fresh start uchun)
    try:
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS transactions")
    except:
        pass

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        xp_needed INTEGER DEFAULT 100,
        hp INTEGER DEFAULT 100,
        mp INTEGER DEFAULT 50,
        strength INTEGER DEFAULT 5,
        agility INTEGER DEFAULT 5,
        intelligence INTEGER DEFAULT 5,
        stat_points INTEGER DEFAULT 0,
        is_premium INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def update_user(user_id, **kwargs):
    conn = connect()
    cur = conn.cursor()
    
    allowed_fields = ['balance', 'level', 'xp', 'xp_needed', 'hp', 'mp', 'strength', 'agility', 'intelligence', 'stat_points', 'is_premium']
    
    updates = []
    values = []
    
    for key, value in kwargs.items():
        if key in allowed_fields:
            updates.append(f"{key} = ?")
            values.append(value)
    
    if updates:
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        values.append(user_id)
        cur.execute(query, tuple(values))
        conn.commit()
    
    conn.close()


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


def add_xp(user_id, xp_amount):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT xp, xp_needed, level FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    
    if user:
        current_xp, xp_needed, current_level = user
        new_xp = current_xp + xp_amount
        new_level = current_level
        
        while new_xp >= xp_needed:
            new_xp -= xp_needed
            new_level += 1
            xp_needed = xp_needed_for(new_level)
        
        cur.execute("""
        UPDATE users
        SET xp = ?, level = ?, xp_needed = ?, stat_points = stat_points + 1
        WHERE user_id = ?
        """, (new_xp, new_level, xp_needed, user_id))
        
        conn.commit()
    
    conn.close()


def allocate_stat(user_id, stat_type, amount):
    conn = connect()
    cur = conn.cursor()
    
    if stat_type not in ['strength', 'agility', 'intelligence']:
        conn.close()
        return False
    
    cur.execute("SELECT stat_points FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    
    if result and result[0] >= amount:
        query = f"UPDATE users SET {stat_type} = {stat_type} + ?, stat_points = stat_points - ? WHERE user_id = ?"
        cur.execute(query, (amount, amount, user_id))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False


def xp_needed_for(level):
    return 100 + (level - 1) * 50


def get_top_users(limit=10):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT user_id, username, balance, level FROM users 
    ORDER BY balance DESC 
    LIMIT ?
    """, (limit,))
    
    users = cur.fetchall()
    conn.close()
    return users
