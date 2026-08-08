"""
Tests for sentiment_analyzer.py (VADER-based, v2).

Mocks _get_analyzer() directly rather than nltk internals, so these tests
don't require the actual VADER lexicon to be downloaded -- they test our
threshold/breakdown logic, not VADER's own scoring, which isn't ours to test.
"""

from unittest.mock import MagicMock, patch

import sentiment_analyzer
from sentiment_analyzer import analyze_sentiment


def _mock_scores(pos, neu, neg, compound):
    mock_analyzer = MagicMock()
    mock_analyzer.polarity_scores.return_value = {
        "pos": pos, "neu": neu, "neg": neg, "compound": compound,
    }
    return mock_analyzer


def test_positive_case():
    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0.6, 0.4, 0.0, 0.7)):
        sentiment, score, breakdown = analyze_sentiment("great event")
    assert sentiment == "Positive"
    assert score == 0.7
    assert breakdown == {"positive": 0.6, "neutral": 0.4, "negative": 0.0}


def test_negative_case():
    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0.0, 0.3, 0.7, -0.6)):
        sentiment, score, breakdown = analyze_sentiment("terrible event")
    assert sentiment == "Negative"


def test_neutral_case():
    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0.1, 0.8, 0.1, 0.02)):
        sentiment, score, breakdown = analyze_sentiment("it happened")
    assert sentiment == "Neutral"


def test_threshold_boundaries():
    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0, 0, 0, 0.05)):
        sentiment, _, _ = analyze_sentiment("x")
    assert sentiment == "Positive"

    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0, 0, 0, -0.05)):
        sentiment, _, _ = analyze_sentiment("x")
    assert sentiment == "Negative"

    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0, 0, 0, 0.049)):
        sentiment, _, _ = analyze_sentiment("x")
    assert sentiment == "Neutral"


def test_breakdown_proportions_sum_to_approximately_one():
    with patch.object(sentiment_analyzer, "_get_analyzer", return_value=_mock_scores(0.3, 0.5, 0.2, 0.1)):
        _, _, breakdown = analyze_sentiment("mixed feedback")
    total = breakdown["positive"] + breakdown["neutral"] + breakdown["negative"]
    assert abs(total - 1.0) < 0.01
