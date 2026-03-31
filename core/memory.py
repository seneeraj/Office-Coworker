import sqlite3
from config import DB_PATH

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()

    import sqlite3
from config import DB_PATH

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            response TEXT
        )
        """)

    def save(self, user_input, response):
        self.conn.execute(
            "INSERT INTO history (user_input, response) VALUES (?, ?)",
            (user_input, response)
        )
        self.conn.commit()

    def fetch_recent(self, limit=5):
        return self.conn.execute(
            "SELECT user_input, response FROM history ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()


context = "\n".join([f"User: {h[0]} AI: {h[1]}" for h in history])

prompt = context + "\nUser: " + user_input    
