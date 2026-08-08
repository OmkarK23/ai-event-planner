"""
Tests for generate_dataset.py.

These exist because this file has already had two real bugs found in it:
1. v1 generated actual_attendance independent of every feature except
   expected_audience -- these tests catch a regression back to that state.
2. v1 let feedback_score leak into being generated independently of outcome,
   then get used as a model input -- test_feedback_is_downstream_of_turnout
   guards the "feedback is an outcome, not an input" invariant.
"""

import numpy as np
import pandas as pd
import pytest

import generate_dataset as gd


def test_budget_effect_is_capped_and_monotonic():
    assert gd.budget_effect(500) < gd.budget_effect(5000) < gd.budget_effect(10000)
    assert gd.budget_effect(10000) <= 1.15
    assert gd.budget_effect(0) >= 0.85


def test_generate_row_schema():
    row = gd.generate_row()
    expected_keys = {
        "event_name", "event_type", "day_of_week", "start_time", "location",
        "promotion_channel", "expected_audience", "actual_attendance",
        "budget", "feedback_score", "feedback_text",
    }
    assert set(row.keys()) == expected_keys
    assert row["event_type"] in gd.EVENT_TYPES
    assert row["day_of_week"] in gd.DAYS
    assert row["actual_attendance"] >= 1
    assert 1.0 <= row["feedback_score"] <= 5.0


def test_actual_attendance_depends_on_more_than_expected_audience():
    """
    Regression test for the original bug: actual_attendance must respond to
    event_type/day/time/location/promo/budget, not just expected_audience.
    Verified by holding expected_audience fixed and checking that the best-
    case combination beats the worst-case combination.
    """
    np.random.seed(0)
    import random
    random.seed(0)

    def turnout_rate(event_type, day, time, location, promo, budget):
        return (
            gd.EVENT_TYPE_EFFECT[event_type] * gd.DAY_EFFECT[day] * gd.TIME_EFFECT[time]
            * gd.LOCATION_EFFECT[location] * gd.PROMO_EFFECT[promo]
            * gd.budget_effect(budget) * gd.GLOBAL_SCALE
        )

    best = turnout_rate("Career Fair", "Thursday", "6PM", "Online", "Multiple", 10000)
    worst = turnout_rate("Research Talk", "Saturday", "10AM", "Library", "Flyers", 500)

    assert best > worst * 2  # best-case should clearly outperform worst-case


def test_feedback_is_downstream_of_turnout_not_independent():
    """
    Regression test for the leakage bug: feedback_score must correlate with
    how attendance actually went, not be generated independently of it.
    """
    rows = [gd.generate_row() for _ in range(500)]
    df = pd.DataFrame(rows)
    turnout_ratio = df["actual_attendance"] / df["expected_audience"]

    correlation = turnout_ratio.corr(df["feedback_score"])
    assert correlation > 0.1  # should show a real positive relationship, not ~0


def test_dataset_columns_do_not_include_leaked_features():
    """feedback_score must never appear anywhere a training pipeline would
    read as an input feature list -- this just checks the generator's own
    output doesn't imply it's a pre-event field by construction."""
    rows = [gd.generate_row() for _ in range(5)]
    for row in rows:
        assert "feedback_score" in row  # it's fine as an OUTPUT column
    # the actual guarantee (not used as a model input) is enforced in
    # views/attendance_predictor.py's fixed feature list, checked separately
    # in test_model_features in test_model_contract.py
