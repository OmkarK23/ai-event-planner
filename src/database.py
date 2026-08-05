"""
Event history storage.

v2 change log:
- v1 wrote SQLite to /tmp/event_history.db. On Streamlit Cloud, /tmp gets wiped
  on every redeploy and on the free tier's auto-sleep-on-inactivity restart, so
  "persistent storage" was not actually true for the deployed app -- only within
  a single running session.
- v2 uses a hosted Postgres database (e.g. Supabase's free tier) when configured,
  so history genuinely persists across restarts. Falls back to local SQLite
  (now in data/, not /tmp) when no Postgres URL is configured, so local
  development without any cloud setup still works.

Configure Postgres via ONE of:
  - environment variable SUPABASE_DB_URL, or
  - Streamlit secrets: .streamlit/secrets.toml with
        SUPABASE_DB_URL = "postgresql://postgres:[password]@[host]:5432/postgres"
    (on Streamlit Cloud: App settings -> Secrets)

Get that connection string from Supabase: Project Settings -> Database ->
Connection string (URI). Never commit it -- .streamlit/secrets.toml should be
in .gitignore.
"""

import os
import sqlite3
from datetime import datetime

LOCAL_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "event_history.db"
)


def _get_db_url():
    url = os.environ.get("SUPABASE_DB_URL")
    if url:
        return url
    try:
        import streamlit as st
        return st.secrets.get("SUPABASE_DB_URL")
    except Exception:
        return None


def using_postgres():
    return _get_db_url() is not None


def storage_backend_label():
    """For UI display, so the app is honest about which backend is active."""
    if using_postgres():
        return "Postgres (persistent across restarts)"
    return "Local SQLite (persists locally; resets on Streamlit Cloud redeploys)"


def _pg_connection():
    import psycopg2
    return psycopg2.connect(_get_db_url())


def _sqlite_connection():
    os.makedirs(os.path.dirname(LOCAL_DB_PATH), exist_ok=True)
    return sqlite3.connect(LOCAL_DB_PATH)


def create_table():
    if using_postgres():
        conn = _pg_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS event_history (
                id SERIAL PRIMARY KEY,
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
    else:
        conn = _sqlite_connection()
        cur = conn.cursor()
        cur.execute("""
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


def save_event(event_name, event_type, tool_used, input_summary, output_result):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if using_postgres():
        conn = _pg_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO event_history
                (event_name, event_type, tool_used, input_summary, output_result, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (event_name, event_type, tool_used, input_summary, output_result, created_at))
        conn.commit()
        conn.close()
    else:
        conn = _sqlite_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO event_history
                (event_name, event_type, tool_used, input_summary, output_result, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event_name, event_type, tool_used, input_summary, output_result, created_at))
        conn.commit()
        conn.close()


def get_history():
    query = """
        SELECT id, event_name, event_type, tool_used, input_summary, output_result, created_at
        FROM event_history
        ORDER BY id DESC
    """
    if using_postgres():
        conn = _pg_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
    else:
        conn = _sqlite_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
    return rows


if __name__ == "__main__":
    create_table()
    print(f"Database ready. Backend: {storage_backend_label()}")
