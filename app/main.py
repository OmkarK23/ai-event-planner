import streamlit as st
import sys
import os
import joblib
import plotly.express as px
import pandas as pd

# Access src folder
sys.path.append('../src')

from ai_strategy_generator import generate_event_strategy
from marketing_generator import generate_marketing_content
from sentiment_analyzer import analyze_sentiment
from database import create_table, save_event, get_history
from recommendation_engine import generate_recommendations
# Load trained model
model = joblib.load('../models/attendance_model.pkl')
df = pd.read_csv('../data/event_data.csv')
create_table()
# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI Event Planning System",
    layout="wide"
)

# -------------------------
# CUSTOM STYLING
# -------------------------

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #4CC9F0;
    text-align: center;
}

.stButton>button {
    background-color: #4361EE;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    font-size: 16px;
}

.stTextArea textarea {
    background-color: #1E1E1E;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------

st.title("AI Event Planning & Engagement System")

st.markdown(
    "### Smart Event Planning Powered by AI and Machine Learning"
)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Feature",
    [
	"Home",
	"Analytics Dashboard",
        "Attendance Predictor",
        "AI Event Planner",
        "Marketing Generator",
        "Feedback Analyzer",
	"AI Recommendations",
	"Event History"
    ]
)
# ==================================================
# HOME PAGE
# ==================================================

if page == "Home":

    st.header("Welcome to the AI Event Planning System")

    st.markdown(
        """
        This platform helps event organizers make smarter planning decisions using AI, machine learning, and analytics.

        ### Key Capabilities

        - Predict expected event attendance
        - Generate AI-powered event strategies
        - Create marketing content for multiple channels
        - Analyze attendee feedback sentiment
        - Visualize engagement and performance trends

        ### Project Value

        This project demonstrates applied AI engineering skills across:

        - Machine Learning
        - Natural Language Processing
        - Data Analytics
        - Dashboard Development
        - Product Thinking
        """
    )
# ==================================================
# ATTENDANCE PREDICTOR
# ==================================================

if page == "Attendance Predictor":

    st.header("Event Attendance Predictor")

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

        feedback = st.slider(
            "Expected Feedback Score",
            1.0,
            5.0,
            4.0
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

    if st.button("Predict Attendance"):

        input_data = pd.DataFrame(
            [[
                event_mapping[event_type],
                day_mapping[day],
                time_mapping[time],
                location_mapping[location],
                promo_mapping[promotion],
                expected,
                budget,
                feedback
            ]],
            columns=[
                'event_type_enc',
                'day_enc',
                'time_enc',
                'location_enc',
                'promo_enc',
                'expected_audience',
                'budget',
                'feedback_score'
            ]
        )

        prediction = model.predict(input_data)[0]

        st.success(
            f"Predicted Attendance: {int(prediction)} attendees"
        )

        st.markdown(
            f"""
            ### Prediction Summary
            Based on a **{event_type}** on **{day}** at **{time}** in **{location}**, promoted through **{promotion}**, the expected attendance is approximately:

            ## {int(prediction)} attendees
            """
        )
# ==================================================
# AI EVENT PLANNER
# ==================================================

if page == "AI Event Planner":

    st.header("AI Event Strategy Generator")

    event_type = st.selectbox(
        "Event Type",
        [
            "Workshop",
            "Networking",
            "Career Fair",
            "Research Talk",
            "Seminar"
        ]
    )

    target = st.text_input(
        "Target Audience"
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

    location = st.text_input(
        "Location"
    )

    day = st.selectbox(
        "Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    time = st.selectbox(
        "Time",
        [
            "10AM",
            "12PM",
            "2PM",
            "4PM",
            "6PM"
        ]
    )

    promo = st.selectbox(
        "Promotion",
        [
            "Email",
            "Instagram",
            "LinkedIn",
            "Multiple"
        ]
    )

if st.button("Generate Strategy", key="generate_strategy_btn" ):

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
        height=400
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

    event_name = st.text_input(
        "Event Name"
    )

    event_type = st.text_input(
        "Event Type"
    )

    location = st.text_input(
        "Location"
    )

    date = st.text_input(
        "Date"
    )

    time = st.text_input(
        "Time"
    )

    audience = st.text_input(
        "Target Audience"
    )
if st.button("Generate Marketing Content", key="generate_marketing_btn"):
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
        height=400
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

        recommendations = generate_recommendations()

        st.success("Recommendations Generated")

        st.markdown(recommendations)
# ==================================================
# EVENT HISTORY
# ==================================================

if page == "Event History":

    st.header("Saved Event History")

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
