import sqlite3
import json

DB_FILE = "Saves/Forms/data.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    creator_id INTEGER,
    created_at TEXT,
    status TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER,
    created_at TEXT,
    responses TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ticket_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    author_id INTEGER,
    author_avatar TEXT,
    content TEXT,
    created_at TEXT,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS interactive_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    type TEXT,
    data TEXT
)
''')

conn.commit()

def save_interactive_message(message_id, channel_id, msg_type, data):
    cursor.execute(
        "INSERT INTO interactive_messages (message_id, channel_id, type, data) VALUES (?, ?, ?, ?)",
        (message_id, channel_id, msg_type, json.dumps(data))
    )
    conn.commit()

def delete_interactive_message(message_id):
    cursor.execute("DELETE FROM interactive_messages WHERE message_id = ?", (message_id,))
    conn.commit()

def get_all_interactive_messages():
    cursor.execute("SELECT message_id, channel_id, type, data FROM interactive_messages")
    return cursor.fetchall()
