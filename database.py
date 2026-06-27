import sqlite3
from datetime import datetime

DB_NAME = "upgrade.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    # Eski tables'ni o'chirish
    try:
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS transactions")
        cur.execute("DROP TABLE IF EXISTS missions")
        cur.execute("DROP TABLE IF EXISTS user_missions")
        cur.execute("DROP TABLE IF EXISTS achievements")
        cur.execute("DROP TABLE IF EXISTS user_achievements")
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
        streak INTEGER DEFAULT 0,
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

    CREATE TABLE IF NOT EXISTS missions (
        mission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        difficulty TEXT,
        xp_reward INTEGER,
        coin_reward INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mission_id INTEGER,
        status TEXT DEFAULT 'active',
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY(mission_id) REFERENCES missions(mission_id)
    );

    CREATE TABLE IF NOT EXISTS achievements (
        achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        icon TEXT,
        requirement TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement_id INTEGER,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(achievement_id) REFERENCES achievements(achievement_id)
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
    # 1-lvl: 100 XP, 2-lvl: 200 XP, 3-lvl: 300 XP... 1000-lvl gacha
    return 100 * level


def get_top_users(limit=10, sort_by='level'):
    conn = connect()
    cur = conn.cursor()
    
    if sort_by == 'level':
        cur.execute("""
        SELECT user_id, username, balance, level, xp FROM users 
        ORDER BY level DESC, xp DESC
        LIMIT ?
        """, (limit,))
    elif sort_by == 'coin':
        cur.execute("""
        SELECT user_id, username, balance, level, xp FROM users 
        ORDER BY balance DESC
        LIMIT ?
        """, (limit,))
    else:
        cur.execute("""
        SELECT user_id, username, balance, level, xp FROM users 
        ORDER BY xp DESC
        LIMIT ?
        """, (limit,))
    
    users = cur.fetchall()
    conn.close()
    return users


# MISSIONS
def add_mission(title, description, difficulty, xp_reward, coin_reward):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO missions (title, description, difficulty, xp_reward, coin_reward)
    VALUES (?, ?, ?, ?, ?)
    """, (title, description, difficulty, xp_reward, coin_reward))
    
    conn.commit()
    mission_id = cur.lastrowid
    conn.close()
    return mission_id


def get_missions_by_difficulty(difficulty):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT mission_id, title, description, difficulty, xp_reward, coin_reward 
    FROM missions 
    WHERE difficulty = ?
    """, (difficulty,))
    
    missions = cur.fetchall()
    conn.close()
    return missions


def accept_mission(user_id, mission_id):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO user_missions (user_id, mission_id, status)
    VALUES (?, ?, 'active')
    """, (user_id, mission_id))
    
    conn.commit()
    conn.close()


def get_active_missions(user_id):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT um.id, m.mission_id, m.title, m.description, m.difficulty, m.xp_reward, m.coin_reward
    FROM user_missions um
    JOIN missions m ON um.mission_id = m.mission_id
    WHERE um.user_id = ? AND um.status = 'active'
    """, (user_id,))
    
    missions = cur.fetchall()
    conn.close()
    return missions


def complete_mission(user_id, mission_id):
    conn = connect()
    cur = conn.cursor()
    
    # Mission ma'lumotlarini olish
    cur.execute("SELECT xp_reward, coin_reward FROM missions WHERE mission_id = ?", (mission_id,))
    mission = cur.fetchone()
    
    if mission:
        xp_reward, coin_reward = mission
        
        # User_missions'ni tugallash
        cur.execute("""
        UPDATE user_missions
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE user_id = ? AND mission_id = ?
        """, (user_id, mission_id))
        
        # XP va coin qo'shish
        add_xp(user_id, xp_reward)
        cur.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE user_id = ?
        """, (coin_reward, user_id))
        
        conn.commit()
    
    conn.close()


# ACHIEVEMENTS
def add_achievement(title, description, icon, requirement):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO achievements (title, description, icon, requirement)
    VALUES (?, ?, ?, ?)
    """, (title, description, icon, requirement))
    
    conn.commit()
    achievement_id = cur.lastrowid
    conn.close()
    return achievement_id


def unlock_achievement(user_id, achievement_id):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT OR IGNORE INTO user_achievements (user_id, achievement_id)
    VALUES (?, ?)
    """, (user_id, achievement_id))
    
    conn.commit()
    conn.close()


def get_user_achievements(user_id):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT a.achievement_id, a.title, a.description, a.icon, ua.unlocked_at
    FROM user_achievements ua
    JOIN achievements a ON ua.achievement_id = a.achievement_id
    WHERE ua.user_id = ?
    """, (user_id,))
    
    achievements = cur.fetchall()
    conn.close()
    return achievements


def get_all_achievements():
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT achievement_id, title, description, icon FROM achievements")
    achievements = cur.fetchall()
    conn.close()
    return achievements
