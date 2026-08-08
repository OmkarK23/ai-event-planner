import streamlit as st

from sentiment_analyzer import analyze_sentiment


def render():
    st.header("Feedback sentiment analyzer")

    st.caption(
        "Lexicon-based sentiment scoring (VADER) -- tuned for short, informal text and "
        "handles negation/intensifiers, but still not a trained classifier."
    )

    feedback = st.text_area("Paste attendee feedback here", height=200)

    if st.button("Analyze Feedback"):

        if feedback.strip() == "":
            st.warning("Please enter feedback text first.")
            return

        sentiment, score, breakdown = analyze_sentiment(feedback)

        st.success(f"Sentiment: {sentiment}")
        st.info(f"Compound score: {round(score, 3)} (range -1 to 1)")

        st.markdown('<div class="nav-label" style="margin-top: 20px;">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
        bcol1, bcol2, bcol3 = st.columns(3)
        bcol1.metric("Positive", f"{breakdown['positive']:.0%}")
        bcol2.metric("Neutral", f"{breakdown['neutral']:.0%}")
        bcol3.metric("Negative", f"{breakdown['negative']:.0%}")

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
