"""
Guards against the exact class of bug that shipped once already: a mismatch
between what features the saved model expects and what the app actually
feeds it (e.g. accidentally reintroducing feedback_score as an input, or the
UI's encoders getting out of sync with the model's training order).
"""

import os

import joblib
import pandas as pd
import pytest

from conftest import MODELS_DIR, DATA_DIR

EXPECTED_FEATURES = [
    "event_type_enc", "day_enc", "time_enc",
    "location_enc", "promo_enc", "expected_audience", "budget",
]


@pytest.fixture(scope="module")
def model():
    return joblib.load(os.path.join(MODELS_DIR, "attendance_model.pkl"))


@pytest.fixture(scope="module")
def encoders():
    return joblib.load(os.path.join(MODELS_DIR, "label_encoders.pkl"))


def test_feedback_score_is_not_a_model_feature(model):
    """The core regression test for the leakage bug: feedback_score must
    never be part of what the trained model expects as input."""
    n_features = model.n_features_in_
    assert n_features == len(EXPECTED_FEATURES)


def test_encoders_have_expected_keys(encoders):
    assert set(encoders.keys()) == {"event", "day", "time", "location", "promo"}


def test_encoder_classes_match_dataset_categories(encoders):
    df = pd.read_csv(os.path.join(DATA_DIR, "event_data.csv"))

    assert set(encoders["event"].classes_) == set(df["event_type"].unique())
    assert set(encoders["day"].classes_) == set(df["day_of_week"].unique())
    assert set(encoders["location"].classes_) == set(df["location"].unique())
    assert set(encoders["promo"].classes_) == set(df["promotion_channel"].unique())


def test_model_predicts_a_reasonable_range(model, encoders):
    """Sanity check: predictions should be positive and within a plausible
    order of magnitude for the dataset's expected_audience range (10-500)."""
    row = pd.DataFrame(
        [[
            encoders["event"].transform(["Career Fair"])[0],
            encoders["day"].transform(["Thursday"])[0],
            encoders["time"].transform(["6PM"])[0],
            encoders["location"].transform(["Online"])[0],
            encoders["promo"].transform(["Multiple"])[0],
            200, 8000,
        ]],
        columns=EXPECTED_FEATURES,
    )
    prediction = model.predict(row)[0]
    assert 0 < prediction < 2000


def test_best_combo_beats_worst_combo(model, encoders):
    """Regression test for the original bug where the model had learned
    almost nothing beyond expected_audience -- best and worst case
    combinations (same expected_audience) should differ meaningfully."""
    def make_row(event, day, time, location, promo, expected, budget):
        return pd.DataFrame(
            [[
                encoders["event"].transform([event])[0],
                encoders["day"].transform([day])[0],
                encoders["time"].transform([time])[0],
                encoders["location"].transform([location])[0],
                encoders["promo"].transform([promo])[0],
                expected, budget,
            ]],
            columns=EXPECTED_FEATURES,
        )

    best = model.predict(make_row("Career Fair", "Thursday", "6PM", "Online", "Multiple", 200, 8000))[0]
    worst = model.predict(make_row("Research Talk", "Saturday", "10AM", "Library", "Flyers", 200, 1000))[0]

    assert best > worst * 1.5
