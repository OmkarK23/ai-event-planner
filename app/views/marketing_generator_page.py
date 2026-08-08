import streamlit as st

from marketing_generator import generate_marketing_content
from database import save_event


def render(event_types, times, locations):
    st.header("Marketing Content Generator")

    col1, col2 = st.columns(2)

    with col1:
        event_name = st.text_input(
            "Event Name",
            placeholder="Example: Data Analytics Networking Night",
            key="marketing_event_name",
        )
        event_type = st.selectbox("Event Type", event_types, key="marketing_event_type")
        location = st.selectbox("Location", locations, key="marketing_location")

    with col2:
        date = st.text_input("Event Date", placeholder="Example: June 20, 2026", key="marketing_date")
        time = st.selectbox("Time", times, key="marketing_time")
        audience = st.text_input(
            "Target Audience",
            placeholder="Example: Graduate students and professionals",
            key="marketing_audience",
        )

    if st.button("Generate Marketing Content", key="marketing_generate_btn"):

        content, used_ai, note = generate_marketing_content(
            event_name, event_type, location, date, time, audience
        )

        if used_ai:
            st.success("Content generated with AI (OpenAI)")
        else:
            st.warning(f"Using rule-based template. {note}")

        st.text_area("Generated Content", content, height=500, key="marketing_output")

        save_event(
            event_name=event_name,
            event_type=event_type,
            tool_used="Marketing Generator (AI)" if used_ai else "Marketing Generator (Template)",
            input_summary=f"{date}, {time}, {location}, audience: {audience}",
            output_result=content,
        )

        st.info("Saved to Event History.")
