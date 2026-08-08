"""
Feedback sentiment analysis.

v2 change log: replaced TextBlob with VADER (nltk.sentiment.vader).

Both are lexicon-based, not trained classifiers -- this is not a jump to
"real NLP" in the deep-learning sense, so don't oversell it as one. The
concrete improvement is that VADER is specifically tuned for short,
informal text (the kind event feedback actually is) and, unlike TextBlob,
accounts for:
  - negation ("not good" scores differently than "good")
  - intensifiers ("very good" vs "good")
  - punctuation and capitalization as emphasis ("great!!!" vs "great")

Uses VADER's own standard thresholds (compound >= 0.05 / <= -0.05) rather
than carrying over TextBlob's ad hoc 0.5/-0.3 cutoffs, since those were
tuned (if at all) for a different scoring distribution.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

_analyzer = None


def _get_analyzer():
    global _analyzer
    if _analyzer is None:
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            # One-time download on first run (~130KB). Requires network
            # access at that moment -- fine on Streamlit Cloud, but note
            # this if running somewhere fully offline.
            nltk.download("vader_lexicon", quiet=True)
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def analyze_sentiment(feedback):
    """
    Returns (sentiment, compound_score, breakdown).
    compound_score is in [-1, 1], same range TextBlob's polarity used, so
    existing callers that only unpack two values still work.
    breakdown is VADER's pos/neu/neg proportions (each 0-1, sum to 1) for
    callers that want to show more than a single number.
    """
    scores = _get_analyzer().polarity_scores(feedback)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    breakdown = {"positive": scores["pos"], "neutral": scores["neu"], "negative": scores["neg"]}
    return sentiment, compound, breakdown


if __name__ == "__main__":
    samples = [
        "The event was okay. Some parts were useful, but some parts could be improved.",
        "This was not a good use of my time.",
        "Absolutely loved it!! Best event all semester.",
    ]
    for s in samples:
        sentiment, score, breakdown = analyze_sentiment(s)
        print(f"{sentiment} ({score:+.3f}) -- {breakdown} -- {s!r}")
