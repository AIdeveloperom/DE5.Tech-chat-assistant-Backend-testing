import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            inquiry_type TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_lead(name, email, inquiry_type):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('INSERT INTO leads (name, email, inquiry_type, timestamp) VALUES (?, ?, ?, ?)',
                   (name, email, inquiry_type, timestamp))
    conn.commit()
    conn.close()

# Initialize the database when the module is imported
init_db()
