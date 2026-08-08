import streamlit as st

import context
from styles import CUSTOM_CSS
from nav import render_sidebar

from views import (
    home,
    attendance_predictor,
    ai_event_planner,
    marketing_generator_page,
    feedback_analyzer,
    analytics_dashboard,
    ai_recommendations,
    event_history,
)

st.set_page_config(
    page_title="AI Event Planning System",
    layout="wide",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

page = render_sidebar()

if page == "Home":
    home.render()

elif page == "Analytics Dashboard":
    analytics_dashboard.render(context.df)

elif page == "Attendance Predictor":
    attendance_predictor.render(context.model, context.encoders)

elif page == "AI Event Planner":
    ai_event_planner.render(
        context.EVENT_TYPES, context.DAYS, context.TIMES,
        context.LOCATIONS, context.PROMO_CHANNELS,
    )

elif page == "Marketing Generator":
    marketing_generator_page.render(
        context.EVENT_TYPES, context.TIMES, context.LOCATIONS
    )

elif page == "Feedback Analyzer":
    feedback_analyzer.render()

elif page == "AI Recommendations":
    ai_recommendations.render(context.DATA_PATH)

elif page == "Event History":
    event_history.render()

st.markdown(
    """
    <div class="custom-footer">
        Built by Omkar Kalekar • AI Engineering Project • 2026
    </div>
    """,
    unsafe_allow_html=True,
)
