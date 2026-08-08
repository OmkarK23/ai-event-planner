"""Sidebar navigation. Renders the nav and returns the currently selected page.

Numbered like gate/stop numbers on a boarding pass rather than icon glyphs --
concrete to the subject and legible at a glance, instead of ambiguous symbols
like an arrow or a square standing in for "predict" or "plan"."""

import streamlit as st

NAV_ITEMS = [
    ("01", "Home"),
    ("02", "Analytics Dashboard"),
    ("03", "Attendance Predictor"),
    ("04", "AI Event Planner"),
    ("05", "Marketing Generator"),
    ("06", "Feedback Analyzer"),
    ("07", "AI Recommendations"),
    ("08", "Event History"),
]


def render_sidebar():
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-icon">AE</div>
            <div>
                <div class="brand-title">AI Event Hub</div>
                <div class="brand-subtitle">Smart tools. Smarter events.</div>
            </div>
        </div>
        <div class="nav-label">NAVIGATION</div>
        """,
        unsafe_allow_html=True,
    )

    for stop_number, nav_page in NAV_ITEMS:
        is_active = st.session_state.page == nav_page
        marker = "→" if is_active else " "
        label = f"{marker} {stop_number}   {nav_page}"
        if st.sidebar.button(label, key=f"nav_{nav_page}"):
            st.session_state.page = nav_page

    return st.session_state.page
