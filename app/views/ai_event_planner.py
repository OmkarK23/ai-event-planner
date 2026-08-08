import streamlit as st

from ai_strategy_generator import generate_event_strategy
from database import save_event


def render(event_types, days, times, locations, promo_channels):
    st.header("AI Event Strategy Generator")

    st.caption(
        "Generates a structured planning checklist using rule-based logic "
        "(no external model call) -- deterministic and free to run."
    )

    col1, col2 = st.columns(2)

    with col1:
        event_type = st.selectbox("Event Type", event_types, key="planner_event_type")
        target = st.text_input(
            "Target Audience",
            placeholder="Example: Graduate students interested in data analytics",
            key="planner_target",
        )
        expected = st.number_input("Expected Audience", min_value=10, value=100, key="planner_expected")
        budget = st.number_input("Budget ($)", min_value=100, value=1000, key="planner_budget")

    with col2:
        location = st.selectbox("Location", locations, key="planner_location")
        day = st.selectbox("Day", days, key="planner_day")
        time = st.selectbox("Time", times, key="planner_time")
        promo = st.selectbox("Promotion Channel", promo_channels, key="planner_promo")

    if st.button("Generate Strategy", key="planner_generate_strategy_btn"):

        strategy = generate_event_strategy(
            event_type, target, expected, budget, location, day, time, promo
        )

        st.success("Strategy Generated")

        st.text_area("Event Plan", strategy, height=400, key="planner_strategy_output")

        save_event(
            event_name=f"{event_type} Event",
            event_type=event_type,
            tool_used="AI Event Planner",
            input_summary=f"{target}, {expected} attendees, ${budget}, {location}, {day} at {time}, promotion: {promo}",
            output_result=strategy,
        )

        st.info("Saved to Event History.")
