import streamlit as st

from database import storage_backend_label

FEATURES = [
    ("Attendance prediction", "Trained Random Forest model, evaluated against baselines.", "real-ai"),
    ("Marketing generator", "Calls OpenAI for real copy, with a template fallback.", "real-ai"),
    ("Event strategy", "Rule-based planning checklist -- no model call.", "rule-based"),
    ("Sentiment analysis", "Lexicon-based scoring (TextBlob), not a trained classifier.", "rule-based"),
    ("Analytics dashboard", "Visualize event performance across the dataset.", "rule-based"),
    ("Recommendations", "Turnout-rate statistics over historical events.", "rule-based"),
]


def render():
    st.markdown(
        """
        <div style="border: 1px solid var(--border); border-radius: 8px; padding: 32px; margin-bottom: 28px;">
            <h1 style="margin-bottom: 8px;">AI event planning &amp; engagement system</h1>
            <p style="font-size: 16px; color: var(--text-muted); margin: 0;">
            Attendance prediction, AI-assisted content, and feedback analysis for event organizers.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-label">PROJECT SNAPSHOT</div>', unsafe_allow_html=True)

    db_backend = "Postgres" if "Postgres" in storage_backend_label() else "SQLite"

    snapshot = [
        ("Modules", "8"),
        ("Trained ML models", "1"),
        ("NLP engine", "TextBlob"),
        ("Database", db_backend),
    ]

    cols = st.columns(4)
    for col, (title, value) in zip(cols, snapshot):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="nav-label" style="margin-top: 32px;">CORE FEATURES</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size: 12px; color: var(--text-muted); margin: -6px 0 16px;">'
        '<span style="color: var(--accent);">&#9679;</span> real trained ML / LLM &nbsp;&nbsp;'
        '<span style="color: #6fd1c9;">&#9679;</span> rule-based / deterministic</p>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    for i, (title, desc, kind) in enumerate(FEATURES):
        target_col = col1 if i % 2 == 0 else col2
        card_class = "is-real-ai" if kind == "real-ai" else "is-rule-based"
        tag_text = "TRAINED" if kind == "real-ai" else "RULE-BASED"
        with target_col:
            st.markdown(
                f"""
                <div class="feature-card {card_class}">
                    <div class="feature-card-title">{title}<span class="feature-card-tag">{tag_text}</span></div>
                    <p class="feature-card-desc">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="margin-top: 28px; border-top: 1px dashed var(--border-tear); padding-top: 20px;">
        <p style="font-size: 13px; color: var(--text-muted); line-height: 1.7;">
        This project pairs a trained ML model and real LLM calls (with graceful fallback)
        with deterministic tooling for the parts that don't need a model --
        see the README for the full breakdown of what's trained, what's an API call,
        and what's rule-based logic.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
