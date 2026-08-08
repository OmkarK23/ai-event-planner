import streamlit as st

from recommendation_engine import generate_recommendations


def render(data_path):
    st.header("Event recommendation engine")

    st.markdown(
        "This module analyzes historical event performance data and recommends "
        "the best planning strategy to improve turnout and engagement."
    )

    if st.button("Generate Recommendations", key="recommendation_btn"):
        recommendations = generate_recommendations(data_path=data_path)
        st.success("Recommendations Generated")
        st.markdown(recommendations)
