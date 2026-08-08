"""
Tests for database.py -- specifically the Postgres/SQLite fallback logic,
since that's the part with real behavioral branches worth protecting against
regression (e.g. accidentally always using SQLite even when a URL is set).
"""

import importlib
import os

import pytest


@pytest.fixture
def db_module(monkeypatch, tmp_path):
    """Fresh import of database.py per test, with LOCAL_DB_PATH redirected to
    a temp file so tests never touch the real data/event_history.db."""
    monkeypatch.delenv("SUPABASE_DB_URL", raising=False)
    import database
    importlib.reload(database)
    monkeypatch.setattr(database, "LOCAL_DB_PATH", str(tmp_path / "test_history.db"))
    return database


def test_uses_sqlite_when_no_url_configured(db_module):
    assert db_module.using_postgres() is False
    assert "SQLite" in db_module.storage_backend_label()


def test_uses_postgres_when_url_configured(db_module, monkeypatch):
    monkeypatch.setenv("SUPABASE_DB_URL", "postgresql://user:pass@host:5432/db")
    assert db_module.using_postgres() is True
    assert "Postgres" in db_module.storage_backend_label()


def test_sqlite_create_save_and_read_roundtrip(db_module):
    db_module.create_table()
    db_module.save_event(
        event_name="Test Event",
        event_type="Workshop",
        tool_used="Marketing Generator (Template)",
        input_summary="test input",
        output_result="test output",
    )
    history = db_module.get_history()

    assert len(history) == 1
    row = history[0]
    _, event_name, event_type, tool_used, input_summary, output_result, created_at = row
    assert event_name == "Test Event"
    assert event_type == "Workshop"
    assert output_result == "test output"


def test_sqlite_history_persists_across_reconnect(db_module):
    db_module.create_table()
    db_module.save_event("A", "Workshop", "tool", "in", "out")
    db_module.save_event("B", "Hackathon", "tool", "in", "out")

    # simulate a fresh connection (e.g. app restart) by calling create_table
    # again and re-reading -- should not wipe existing rows
    db_module.create_table()
    history = db_module.get_history()
    assert len(history) == 2


def test_history_ordered_most_recent_first(db_module):
    db_module.create_table()
    db_module.save_event("First", "Workshop", "tool", "in", "out")
    db_module.save_event("Second", "Workshop", "tool", "in", "out")

    history = db_module.get_history()
    assert history[0][1] == "Second"
    assert history[1][1] == "First"
