from textblob import TextBlob


def analyze_sentiment(feedback):

    analysis = TextBlob(feedback)
    polarity = analysis.sentiment.polarity

    # Improved thresholds

    if polarity >= 0.5:
        sentiment = "Positive"

    elif polarity <= -0.3:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, polarity


if __name__ == "__main__":

    sample = """
    The event was okay. Some parts were useful,
    but some parts could be improved.
    """

    sentiment, score = analyze_sentiment(sample)

    print("Sentiment:", sentiment)
    print("Polarity Score:", score)
