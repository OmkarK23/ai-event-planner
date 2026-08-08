"""Sidebar navigation. Renders the nav and returns the currently selected page."""

import streamlit as st

NAV_ITEMS = {
    "Home": "⌂  Overview | Home",
    "Analytics Dashboard": "▥  Insights | Analytics Dashboard",
    "Attendance Predictor": "↗  Predict | Attendance Predictor",
    "AI Event Planner": "▣  Plan | AI Event Planner",
    "Marketing Generator": "◉  Create | Marketing Generator",
    "Feedback Analyzer": "▢  Analyze | Feedback Analyzer",
    "AI Recommendations": "✧  Optimize | AI Recommendations",
    "Event History": "↺  History | Event History",
}


def render_sidebar():
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
        unsafe_allow_html=True,
    )

    for nav_page, label in NAV_ITEMS.items():
        is_active = st.session_state.page == nav_page
        active_prefix = "● " if is_active else "○ "

        if st.sidebar.button(active_prefix + label, key=f"nav_{nav_page}"):
            st.session_state.page = nav_page

    return st.session_state.page
