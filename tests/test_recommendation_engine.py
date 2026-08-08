"""
Tests for recommendation_engine.py -- built around a small synthetic CSV with
a known, deliberately-designed-in best answer, so the test can assert the
engine actually recovers it rather than just "doesn't crash."
"""

import pandas as pd
import pytest

from recommendation_engine import generate_recommendations


@pytest.fixture
def known_best_csv(tmp_path):
    """
    Construct a tiny dataset where 'Career Fair' events have an
    unambiguously higher turnout rate than every other event type, and
    similarly for one day/time/location/promo -- so the recommendation
    engine's output is checkable, not just plausible-looking.
    """
    rows = []
    # Career Fair: turnout rate ~1.5 (high)
    for _ in range(20):
        rows.append({
            "event_type": "Career Fair", "day_of_week": "Thursday", "start_time": "6PM",
            "location": "Online", "promotion_channel": "Multiple",
            "expected_audience": 100, "actual_attendance": 150, "budget": 5000,
            "feedback_score": 4.0, "feedback_text": "great",
        })
    # Everything else: turnout rate ~0.5 (low)
    for event_type in ["Workshop", "Seminar", "Research Talk"]:
        for _ in range(20):
            rows.append({
                "event_type": event_type, "day_of_week": "Monday", "start_time": "10AM",
                "location": "Library", "promotion_channel": "Flyers",
                "expected_audience": 100, "actual_attendance": 50, "budget": 500,
                "feedback_score": 2.0, "feedback_text": "meh",
            })

    df = pd.DataFrame(rows)
    path = tmp_path / "known_best.csv"
    df.to_csv(path, index=False)
    return str(path)


def test_recommends_the_known_best_event_type(known_best_csv):
    result = generate_recommendations(data_path=known_best_csv)
    assert "Career Fair" in result


def test_recommends_by_turnout_rate_not_raw_attendance(tmp_path):
    """
    Regression test for the original bug: a category with a larger
    expected_audience but the SAME turnout rate must not be picked over
    a category with a smaller expected_audience and a better turnout rate.
    """
    rows = []
    # Big events, but mediocre turnout rate (0.8)
    for _ in range(20):
        rows.append({
            "event_type": "Big Low Rate", "day_of_week": "Monday", "start_time": "10AM",
            "location": "Library", "promotion_channel": "Flyers",
            "expected_audience": 500, "actual_attendance": 400, "budget": 500,
            "feedback_score": 3.0, "feedback_text": "ok",
        })
    # Small events, but excellent turnout rate (1.5)
    for _ in range(20):
        rows.append({
            "event_type": "Small High Rate", "day_of_week": "Monday", "start_time": "10AM",
            "location": "Library", "promotion_channel": "Flyers",
            "expected_audience": 50, "actual_attendance": 75, "budget": 500,
            "feedback_score": 4.0, "feedback_text": "great",
        })
    df = pd.DataFrame(rows)
    path = tmp_path / "rate_vs_raw.csv"
    df.to_csv(path, index=False)

    result = generate_recommendations(data_path=str(path))
    assert "Small High Rate" in result
    assert "Big Low Rate" not in result.split("Best Event Type:")[1].split("\n")[0]


def test_output_contains_expected_sections(known_best_csv):
    result = generate_recommendations(data_path=known_best_csv)
    for heading in ["Best Event Type", "Best Promotion Channel", "Best Day", "Recommended Strategy"]:
        assert heading in result
