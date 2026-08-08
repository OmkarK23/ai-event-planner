import streamlit as st

from database import storage_backend_label


def render():
    st.markdown(
        """
        <div style="
            background: rgba(15,23,42,0.7);
            padding:40px;
            border-radius:25px;
            border:1px solid #334155;
            box-shadow:0 12px 30px rgba(0,0,0,0.35);
        ">
            <h1 style='text-align:center;'>AI Event Planning & Engagement System</h1>
            <p style='text-align:center; font-size:20px; color:#cbd5e1;'>
            Intelligent event planning powered by Machine Learning, NLP, and Analytics
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Project Snapshot")

    db_backend = "Postgres" if "Postgres" in storage_backend_label() else "SQLite"

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:18px; margin-top:18px; margin-bottom:35px;">
            <div class="kpi-card">
                <div class="kpi-title">AI Modules</div>
                <div class="kpi-value">6+</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">ML Model</div>
                <div class="kpi-value">1</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">NLP Engine</div>
                <div class="kpi-value">TextBlob</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Database</div>
                <div class="kpi-value">{db_backend}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Core Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("### Attendance Prediction\nPredict expected turnout using ML.")
        st.info("### Event Strategy\nGenerate a rule-based planning checklist.")

    with c2:
        st.success("### Marketing Generator\nAI-generated promotional content (with template fallback).")
        st.success("### Sentiment Analysis\nAnalyze attendee feedback.")

    with c3:
        st.warning("### Analytics Dashboard\nVisualize event performance.")
        st.warning("### Recommendations\nData-driven planning suggestions.")

    st.markdown("---")

    st.markdown(
        """
        ### Why This Project Matters

        This platform demonstrates:

        - Machine learning (trained model, evaluated against baselines)
        - LLM integration with graceful degradation
        - NLP (lexicon-based sentiment)
        - Recommendation systems
        - Analytics engineering
        - Dashboard development
        - Product thinking
        """
    )
