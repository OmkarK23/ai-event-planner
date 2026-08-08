"""
Tests for marketing_generator.py -- focused on the fallback path, since
that's the behavior guaranteeing the app never hard-crashes for a visitor
without an OpenAI key. The real API call path isn't tested here (would
require network + a funded key); it's covered by manual testing per the
README.
"""

import pytest

from marketing_generator import generate_marketing_content, _get_api_key


def test_falls_back_to_template_when_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    content, used_ai, note = generate_marketing_content(
        event_name="Test Night",
        event_type="Networking",
        location="University Center",
        date="June 15",
        time="6 PM",
        target_audience="graduate students",
    )

    assert used_ai is False
    assert "No OPENAI_API_KEY" in note
    assert "Test Night" in content
    assert "EMAIL INVITATION" in content


def test_template_includes_all_five_sections(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    content, _, _ = generate_marketing_content(
        "Event", "Workshop", "Library", "July 1", "2PM", "students",
    )

    for section in ["EMAIL INVITATION", "INSTAGRAM CAPTION", "LINKEDIN POST", "REMINDER MESSAGE", "THANK YOU MESSAGE"]:
        assert section in content


def test_get_api_key_reads_env_var(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    assert _get_api_key() == "sk-test-123"


def test_get_api_key_none_when_unset(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert _get_api_key() is None
