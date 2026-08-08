import streamlit as st

from sentiment_analyzer import analyze_sentiment


def render():
    st.header("Feedback sentiment analyzer")

    st.caption("Lexicon-based sentiment scoring (TextBlob) -- a quick read, not a trained classifier.")

    feedback = st.text_area("Paste attendee feedback here", height=200)

    if st.button("Analyze Feedback"):

        if feedback.strip() == "":
            st.warning("Please enter feedback text first.")
            return

        sentiment, score = analyze_sentiment(feedback)

        st.success(f"Sentiment: {sentiment}")
        st.info(f"Polarity Score: {round(score, 3)}")

        if sentiment == "Positive":
            st.markdown(
                "### Insight: Attendees responded well. You can reuse similar content, timing, and engagement activities for future events."
            )
        elif sentiment == "Negative":
            st.markdown(
                "### Insight: Feedback suggests improvement is needed. Review event timing, communication, organization, and audience engagement."
            )
        else:
            st.markdown(
                "### Insight: Feedback is mixed or neutral. Consider collecting more detailed comments to understand attendee expectations."
            )
