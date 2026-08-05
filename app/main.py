import streamlit as st
import sys
import os
import joblib
import plotly.express as px
import pandas as pd

# Access src folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(SRC_DIR)

from ai_strategy_generator import generate_event_strategy
from marketing_generator import generate_marketing_content
from sentiment_analyzer import analyze_sentiment
from database import create_table, save_event, get_history, storage_backend_label
from recommendation_engine import generate_recommendations
# Load trained model
MODEL_PATH = os.path.join(CURRENT_DIR, "..", "models", "attendance_model.pkl")
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "event_data.csv")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)
create_table()
# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI Event Planning System",
    layout="wide",
)

# -------------------------
# CUSTOM STYLING
# -------------------------
st.markdown("""
<style>

/* =========================
APP BACKGROUND
========================= */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 45%,
        #1e1b4b 100%
    );
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================
TYPOGRAPHY
========================= */

h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: white;
    margin-bottom: 0.5rem;
}

h2, h3 {
    color: #e0e7ff;
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617 0%,
        #111827 100%
    );
    border-right: 1px solid #334155;
    min-width: 270px !important;
    max-width: 270px !important;
}
/* =========================
PREMIUM SIDEBAR NAV
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617 0%,
        #071126 100%
    );
    border-right: 1px solid #1e293b;
    min-width: 280px !important;
    max-width: 280px !important;
    padding-top: 10px;
}

/* Button container */

section[data-testid="stSidebar"] .stButton {
    width: 100%;
}

/* NAV BUTTON */

section[data-testid="stSidebar"] .stButton > button {

    width: 100%;
    height: 78px !important;
    min-height: 78px !important;

    display: flex;
    align-items: center;
    justify-content: flex-start;

    padding: 0 22px !important;
    margin-bottom: 16px;

    background: rgba(15,23,42,0.85);

    color: #e2e8f0;

    border: 1px solid rgba(
        100,
        116,
        139,
        0.35
    );

    border-radius: 22px;

    font-size: 15px;
    font-weight: 650;
    line-height: 1.25;

    box-shadow:
        0 6px 18px rgba(
            0,
            0,
            0,
            0.22
        );

    transition:
        all .35s ease;

    text-align: left;

    overflow: hidden;
}

/* HOVER */

section[data-testid="stSidebar"] .stButton > button:hover {

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #ec4899
    );

    color: white;

    transform:
        translateX(8px)
        scale(1.03);

    border: 1px solid #818cf8;

    box-shadow:
        0 18px 36px rgba(
            124,
            58,
            237,
            0.42
        );
}

/* CLICK */

section[data-testid="stSidebar"] .stButton > button:active {

    transform: scale(.98);
}
}
section[data-testid="stSidebar"] .stButton>button:hover {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #ec4899);
    color: white;
    transform: translateX(6px) scale(1.02);
    border: 1px solid #818cf8;
    box-shadow: 0 12px 30px rgba(124, 58, 237, 0.35);
}
/* Sidebar brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 35px;
    margin-top: 15px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;
    box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
}

.brand-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

.brand-subtitle {
    font-size: 13px;
    color: #94a3b8;
}

/* Navigation label */
.nav-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}

/* Nav Cards */
.nav-card {
    display: flex;
    align-items: center;
    gap: 14px;

    width: 100%;
    min-height: 62px;

    padding: 14px 16px;
    margin-bottom: 12px;

    border-radius: 16px;
    border: 1px solid #334155;

    background: rgba(30, 41, 59, 0.75);
    color: #cbd5e1;

    transition: all 0.3s ease;
    cursor: pointer;
}

.nav-card:hover {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #ec4899);
    color: white;
    transform: translateX(6px) scale(1.02);
    box-shadow: 0 12px 30px rgba(124, 58, 237, 0.35);
    border: 1px solid #818cf8;
}

/* Active selected nav item */
.active-nav {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #ec4899);
    color: white;
    border: 1px solid #818cf8;
    box-shadow: 0 14px 35px rgba(124, 58, 237, 0.45);
}

.nav-icon {
    font-size: 25px;
    width: 32px;
    text-align: center;
    color: #38bdf8;
}

.active-nav .nav-icon {
    color: white;
}

.nav-text {
    flex: 1;
    font-size: 14px;
    line-height: 1.3;
}

.nav-arrow {
    font-size: 24px;
    color: #cbd5e1;
}

/* Sidebar block navigation */

section[data-testid="stSidebar"] .stButton>button {

    background: rgba(30,41,59,0.85);
    color: #e0e7ff;

    border: 1px solid #475569;
    border-radius: 16px;

    padding: 14px 16px;
    margin-bottom: 10px;

    text-align: left;
    width: 100%;

    font-weight: 600;
    font-size: 14px;

    transition: all 0.3s ease;
    box-shadow: none;
}

section[data-testid="stSidebar"] .stButton>button:hover {

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );

    color: white;
    transform: translateX(4px);

    border: 1px solid #818cf8;
}

/* =========================
MAIN BUTTONS
========================= */

.stButton>button {

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6,
        #ec4899
    );

    color: white;
    border: none;
    border-radius: 12px;

    padding: 0.75rem 1rem;

    font-weight: 700;
    font-size: 16px;

    box-shadow: 0 8px 20px rgba(
        99,
        102,
        241,
        0.35
    );

    transition: all 0.3s ease;
}

.stButton>button:hover {

    transform: translateY(-2px);

    box-shadow: 0 12px 28px rgba(
        236,
        72,
        153,
        0.35
    );
}

/* =========================
INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {

    background-color: #1e293b !important;
    color: white !important;

    border-radius: 10px !important;
    border: 1px solid #475569 !important;
}

/* =========================
METRICS
========================= */

div[data-testid="stMetric"] {

    background: rgba(
        30,
        41,
        59,
        0.85
    );

    padding: 20px;
    border-radius: 18px;

    border: 1px solid #475569;

    box-shadow: 0 8px 20px rgba(
        0,
        0,
        0,
        0.25
    );
}

/* =========================
FEATURE CARDS
========================= */

.feature-card {

    background: rgba(
        30,
        41,
        59,
        0.6
    );

    border: 1px solid rgba(
        255,
        255,
        255,
        0.08
    );

    border-radius: 20px;
    padding: 25px;

    backdrop-filter: blur(12px);

    transition: all 0.35s ease;
}

.feature-card:hover {

    transform: translateY(-6px);

    box-shadow: 0 20px 40px rgba(
        99,
        102,
        241,
        0.35
    );

    border: 1px solid rgba(
        99,
        102,
        241,
        0.45
    );
}

/* =========================
ALERTS + EXPANDERS
========================= */

.streamlit-expanderHeader {
    background-color: #1e293b;
    border-radius: 10px;
}

.stAlert {
    border-radius: 14px;
}

/* =========================
FOOTER
========================= */

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 3rem;
    font-size: 14px;
}
/* =========================
PAGE FADE ANIMATION
========================= */

.block-container {
    animation: fadeIn 0.55s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* =========================
GLASS KPI CARDS
========================= */

.kpi-card {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-6px);
    border: 1px solid rgba(129, 140, 248, 0.7);
    box-shadow: 0 18px 38px rgba(124,58,237,0.35);
}

.kpi-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
}

/* =========================
FOOTER BRANDING
========================= */

.custom-footer {
    margin-top: 60px;
    padding: 20px;
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    border-top: 1px solid rgba(148,163,184,0.2);
}
</style>
""", unsafe_allow_html=True)
# -------------------------
# BLOCK STYLE NAVIGATION
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-icon">✦</div>
        <div>
            <div class="brand-title">AI Event Hub</div>
            <div class="brand-subtitle">Smart Tools. Smarter Events.</div>
        </div>
    </div>
    <div class="nav-label">NAVIGATION</div>
    """,
    unsafe_allow_html=True
)

nav_items = {
    "Home": "⌂  Overview | Home",
    "Analytics Dashboard": "▥  Insights | Analytics Dashboard",
    "Attendance Predictor": "↗  Predict | Attendance Predictor",
    "AI Event Planner": "▣  Plan | AI Event Planner",
    "Marketing Generator": "◉  Create | Marketing Generator",
    "Feedback Analyzer": "▢  Analyze | Feedback Analyzer",
    "AI Recommendations": "✧  Optimize | AI Recommendations",
    "Event History": "↺  History | Event History"
}
for nav_page, label in nav_items.items():

    is_active = st.session_state.page == nav_page
    active_prefix = "● " if is_active else "○ "

    if st.sidebar.button(
        active_prefix + label,
        key=f"nav_{nav_page}"
    ):
        st.session_state.page = nav_page

page = st.session_state.page
# ==================================================
# HOME PAGE
# ==================================================
if page == "Home":

    st.markdown("""
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
    """, unsafe_allow_html=True)
    st.markdown("### Project Snapshot")

    st.markdown(
    	"""
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
            		<div class="kpi-value">SQLite</div>
        	</div>
    	</div>
    	""",
    	unsafe_allow_html=True
	)
    st.markdown("## Core Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("""
        ### Attendance Prediction
        Predict expected turnout using ML.
        """)

        st.info("""
        ### AI Strategy
        Generate planning recommendations.
        """)

    with c2:
        st.success("""
        ### Marketing Generator
        Create promotional content.
        """)

        st.success("""
        ### Sentiment Analysis
        Analyze attendee feedback.
        """)

    with c3:
        st.warning("""
        ### Analytics Dashboard
        Visualize event performance.
        """)

        st.warning("""
        ### AI Recommendations
        Optimize planning decisions.
        """)

    st.markdown("---")

    st.markdown("""
    ### Why This Project Matters

    This platform demonstrates:

    - Machine Learning
    - NLP
    - Recommendation Systems
    - Analytics Engineering
    - Dashboard Development
    - Product Thinking
    """)
# ==================================================
# ATTENDANCE PREDICTOR
# ==================================================

if page == "Attendance Predictor":

    st.header("Event Attendance Predictor")

    st.caption(
        "Trained on a synthetic dataset with hand-picked effect sizes "
        "(see README for methodology), not on real event outcomes. "
        "Treat predictions as a demo of the pipeline, not a validated forecast."
    )

    event_mapping = {
        "Career Fair": 0,
        "Hackathon": 1,
        "Networking": 2,
        "Research Talk": 3,
        "Seminar": 4,
        "Social Event": 5,
        "Workshop": 6
    }

    day_mapping = {
        "Friday": 0,
        "Monday": 1,
        "Saturday": 2,
        "Thursday": 3,
        "Tuesday": 4,
        "Wednesday": 5
    }

    time_mapping = {
        "10AM": 0,
        "12PM": 1,
        "2PM": 2,
        "4PM": 3,
        "6PM": 4
    }

    location_mapping = {
        "Engineering Hall": 0,
        "Library": 1,
        "Online": 2,
        "Student Center": 3,
        "University Center": 4
    }

    promo_mapping = {
        "Email": 0,
        "Flyers": 1,
        "Instagram": 2,
        "LinkedIn": 3,
        "Multiple": 4
    }

    col1, col2 = st.columns(2)

    with col1:

        event_type = st.selectbox(
            "Event Type",
            list(event_mapping.keys())
        )

        expected = st.number_input(
            "Expected Audience",
            min_value=10,
            value=100
        )

        budget = st.number_input(
            "Budget",
            min_value=100,
            value=1000
        )

    with col2:

        day = st.selectbox(
            "Day",
            list(day_mapping.keys())
        )

        time = st.selectbox(
            "Start Time",
            list(time_mapping.keys())
        )

        location = st.selectbox(
            "Location",
            list(location_mapping.keys())
        )

        promotion = st.selectbox(
            "Promotion Channel",
            list(promo_mapping.keys())
        )

    if st.button(
        "Predict Attendance",
        key="predict_attendance_btn"
    ):

        input_data = pd.DataFrame(
            [[
                event_mapping[event_type],
                day_mapping[day],
                time_mapping[time],
                location_mapping[location],
                promo_mapping[promotion],
                expected,
                budget
            ]],
            columns=[
                'event_type_enc',
                'day_enc',
                'time_enc',
                'location_enc',
                'promo_enc',
                'expected_audience',
                'budget'
            ]
        )

        prediction = model.predict(
            input_data
        )[0]

        st.success(
            f"Predicted Attendance: {int(prediction)} attendees"
        )

        st.markdown(
            f"""
            ### Prediction Summary

            Based on a **{event_type}** event on **{day}** at **{time}** in **{location}**, promoted through **{promotion}**, the predicted attendance is:

            ## {int(prediction)} attendees
            """
        )
# ==================================================
# AI EVENT PLANNER
# ==================================================

if page == "AI Event Planner":

    st.header("AI Event Strategy Generator")

    st.caption(
        "Generates a structured planning checklist using rule-based logic "
        "(no external model call) -- deterministic and free to run."
    )

    col1, col2 = st.columns(2)

    with col1:

        event_type = st.selectbox(
            "Event Type",
            [
                "Workshop",
                "Networking",
                "Hackathon",
                "Career Fair",
                "Seminar",
                "Research Talk",
                "Social Event"
            ],
            key="planner_event_type"
        )

        target = st.text_input(
            "Target Audience",
            placeholder="Example: Graduate students interested in data analytics",
            key="planner_target"
        )

        expected = st.number_input(
            "Expected Audience",
            min_value=10,
            value=100,
            key="planner_expected"
        )

        budget = st.number_input(
            "Budget ($)",
            min_value=100,
            value=1000,
            key="planner_budget"
        )

    with col2:

        location = st.selectbox(
            "Location",
            [
                "University Center",
                "Engineering Hall",
                "Library",
                "Online",
                "Student Center"
            ],
            key="planner_location"
        )

        day = st.selectbox(
            "Day",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ],
            key="planner_day"
        )

        time = st.selectbox(
            "Time",
            [
                "10AM",
                "12PM",
                "2PM",
                "4PM",
                "6PM"
            ],
            key="planner_time"
        )

        promo = st.selectbox(
            "Promotion Channel",
            [
                "Email",
                "Instagram",
                "LinkedIn",
                "Flyers",
                "Multiple"
            ],
            key="planner_promo"
        )

    if st.button("Generate Strategy", key="planner_generate_strategy_btn"):

        strategy = generate_event_strategy(
            event_type,
            target,
            expected,
            budget,
            location,
            day,
            time,
            promo
        )

        st.success("Strategy Generated")

        st.text_area(
            "AI Event Plan",
            strategy,
            height=400,
            key="planner_strategy_output"
        )

        save_event(
            event_name=f"{event_type} Event",
            event_type=event_type,
            tool_used="AI Event Planner",
            input_summary=f"{target}, {expected} attendees, ${budget}, {location}, {day} at {time}, promotion: {promo}",
            output_result=strategy
        )

        st.info("Saved to Event History.")

# ==================================================
# MARKETING GENERATOR
# ==================================================

if page == "Marketing Generator":

    st.header("Marketing Content Generator")

    col1, col2 = st.columns(2)

    with col1:

        event_name = st.text_input(
            "Event Name",
            placeholder="Example: Data Analytics Networking Night",
            key="marketing_event_name"
        )

        event_type = st.selectbox(
            "Event Type",
            [
                "Workshop",
                "Networking",
                "Hackathon",
                "Career Fair",
                "Seminar",
                "Research Talk",
                "Social Event"
            ],
            key="marketing_event_type"
        )

        location = st.selectbox(
            "Location",
            [
                "University Center",
                "Engineering Hall",
                "Library",
                "Online",
                "Student Center"
            ],
            key="marketing_location"
        )

    with col2:

        date = st.text_input(
            "Event Date",
            placeholder="Example: June 20, 2026",
            key="marketing_date"
        )

        time = st.selectbox(
            "Time",
            [
                "10AM",
                "12PM",
                "2PM",
                "4PM",
                "6PM"
            ],
            key="marketing_time"
        )

        audience = st.text_input(
            "Target Audience",
            placeholder="Example: Graduate students and professionals",
            key="marketing_audience"
        )

    if st.button(
        "Generate Marketing Content",
        key="marketing_generate_btn"
    ):

        content, used_ai, note = generate_marketing_content(
            event_name,
            event_type,
            location,
            date,
            time,
            audience
        )

        if used_ai:
            st.success("Content generated with AI (OpenAI)")
        else:
            st.warning(f"Using rule-based template. {note}")

        st.text_area(
            "Generated Content",
            content,
            height=500,
            key="marketing_output"
        )

        save_event(
            event_name=event_name,
            event_type=event_type,
            tool_used="Marketing Generator (AI)" if used_ai else "Marketing Generator (Template)",
            input_summary=f"{date}, {time}, {location}, audience: {audience}",
            output_result=content
        )

        st.info("Saved to Event History.")
# ==================================================
# FEEDBACK ANALYZER
# ==================================================

if page == "Feedback Analyzer":

    st.header("Feedback Sentiment Analyzer")

    feedback = st.text_area(
        "Paste attendee feedback here",
        height=200
    )

    if st.button("Analyze Feedback"):

        if feedback.strip() == "":
            st.warning("Please enter feedback text first.")

        else:
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
# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

if page == "Analytics Dashboard":

    st.header("Event Analytics Dashboard")

    # -------------------------
    # FILTERS
    # -------------------------

    st.subheader("Dashboard Filters")

    colf1, colf2 = st.columns(2)

    with colf1:
        selected_event = st.selectbox(
            "Filter by Event Type",
            ["All"] + sorted(
                df["event_type"].unique().tolist()
            )
        )

    with colf2:
        selected_promo = st.selectbox(
            "Filter by Promotion",
            ["All"] + sorted(
                df["promotion_channel"].unique().tolist()
            )
        )

    filtered_df = df.copy()

    if selected_event != "All":
        filtered_df = filtered_df[
            filtered_df["event_type"] == selected_event
        ]

    if selected_promo != "All":
        filtered_df = filtered_df[
            filtered_df["promotion_channel"] == selected_promo
        ]

    st.markdown("---")

    # -------------------------
    # KPI CARDS
    # -------------------------

    total_events = len(filtered_df)
    avg_attendance = int(
        filtered_df["actual_attendance"].mean()
    )
    avg_budget = int(
        filtered_df["budget"].mean()
    )
    avg_feedback = round(
        filtered_df["feedback_score"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Events",
        total_events
    )

    col2.metric(
        "Avg Attendance",
        avg_attendance
    )

    col3.metric(
        "Avg Budget",
        f"${avg_budget}"
    )

    col4.metric(
        "Avg Feedback",
        avg_feedback
    )

    st.markdown("---")

    # -------------------------
    # INSIGHTS
    # -------------------------

    st.subheader("AI Event Insights")

    best_event = filtered_df.groupby(
        "event_type"
    )["actual_attendance"].mean().idxmax()

    best_promo = filtered_df.groupby(
        "promotion_channel"
    )["actual_attendance"].mean().idxmax()

    st.success(
        f"Highest average attendance comes from: **{best_event}** events."
    )

    st.info(
        f"Most effective promotion method: **{best_promo}**."
    )

    st.markdown("---")

    # -------------------------
    # CHARTS
    # -------------------------

    col5, col6 = st.columns(2)

    with col5:

        attendance_by_type = filtered_df.groupby(
            "event_type"
        )["actual_attendance"].mean().reset_index()

        fig1 = px.bar(
            attendance_by_type,
            x="event_type",
            y="actual_attendance",
            color="actual_attendance",
            title="Average Attendance by Event Type",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col6:

        promo = filtered_df.groupby(
            "promotion_channel"
        )["actual_attendance"].mean().reset_index()

        fig2 = px.pie(
            promo,
            names="promotion_channel",
            values="actual_attendance",
            hole=0.45,
            title="Promotion Effectiveness",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    col7, col8 = st.columns(2)

    with col7:

        fig3 = px.scatter(
            filtered_df,
            x="budget",
            y="actual_attendance",
            color="event_type",
            size="feedback_score",
            hover_data=[
                "location",
                "promotion_channel"
            ],
            title="Budget vs Attendance",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col8:

        fig4 = px.histogram(
            filtered_df,
            x="actual_attendance",
            color="event_type",
            nbins=25,
            title="Attendance Distribution",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )
# ==================================================
# AI RECOMMENDATIONS
# ==================================================

if page == "AI Recommendations":

    st.header("AI Event Recommendation Engine")

    st.markdown(
        """
        This module analyzes historical event performance data and recommends the best planning strategy to improve turnout and engagement.
        """
    )

    if st.button("Generate Recommendations", key="recommendation_btn"):

        recommendations = generate_recommendations(data_path=DATA_PATH)

        st.success("Recommendations Generated")

        st.markdown(recommendations)
# ==================================================
# EVENT HISTORY
# ==================================================

if page == "Event History":

    st.header("Saved Event History")

    st.caption(f"Storage backend: {storage_backend_label()}")

    history = get_history()

    if len(history) == 0:
        st.info("No saved event history yet.")

    else:
        for row in history:
            event_id, event_name, event_type, tool_used, input_summary, output_result, created_at = row

            with st.expander(f"{event_name} | {tool_used} | {created_at}"):

                st.write(f"**Event Type:** {event_type}")
                st.write(f"**Input Summary:** {input_summary}")
                st.text_area(
                    "Saved Output",
                    output_result,
                    height=250,
                    key=f"history_{event_id}"
                )
st.markdown(
    """
    <div class="custom-footer">
        Built by Omkar Kalekar • AI Engineering Project • 2026
    </div>
    """,
    unsafe_allow_html=True
)
