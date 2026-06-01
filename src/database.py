import sqlite3
import os
from datetime import datetime


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "..", "data")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "event_history.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_type TEXT,
            tool_used TEXT,
            input_summary TEXT,
            output_result TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_event(
    event_name,
    event_type,
    tool_used,
    input_summary,
    output_result
):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO event_history (
            event_name,
            event_type,
            tool_used,
            input_summary,
            output_result,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        event_name,
        event_type,
        tool_used,
        input_summary,
        output_result,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            event_name,
            event_type,
            tool_used,
            input_summary,
            output_result,
            created_at
        FROM event_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows
