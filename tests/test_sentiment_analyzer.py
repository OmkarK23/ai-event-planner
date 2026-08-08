"""
Tests for sentiment_analyzer.py -- covers the threshold logic, which is the
only actual decision this module makes (TextBlob itself isn't ours to test).
"""

from unittest.mock import MagicMock, patch

from sentiment_analyzer import analyze_sentiment


def _mock_polarity(value):
    mock_blob = MagicMock()
    mock_blob.sentiment.polarity = value
    return mock_blob


def test_high_polarity_is_positive():
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(0.8)):
        sentiment, score = analyze_sentiment("great event")
    assert sentiment == "Positive"
    assert score == 0.8


def test_low_polarity_is_negative():
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(-0.5)):
        sentiment, score = analyze_sentiment("terrible event")
    assert sentiment == "Negative"


def test_mid_polarity_is_neutral():
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(0.1)):
        sentiment, score = analyze_sentiment("it was fine")
    assert sentiment == "Neutral"


def test_threshold_boundaries():
    # exactly at the positive threshold
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(0.5)):
        sentiment, _ = analyze_sentiment("x")
    assert sentiment == "Positive"

    # exactly at the negative threshold
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(-0.3)):
        sentiment, _ = analyze_sentiment("x")
    assert sentiment == "Negative"

    # just inside neutral band
    with patch("sentiment_analyzer.TextBlob", return_value=_mock_polarity(-0.29)):
        sentiment, _ = analyze_sentiment("x")
    assert sentiment == "Neutral"
