import streamlit as st

from database import get_history, storage_backend_label


def render():
    st.header("Saved event history")

    st.caption(f"Storage backend: {storage_backend_label()}")

    history = get_history()

    if len(history) == 0:
        st.info("No saved event history yet.")
        return

    for row in history:
        event_id, event_name, event_type, tool_used, input_summary, output_result, created_at = row

        with st.expander(f"{event_name} | {tool_used} | {created_at}"):
            st.write(f"**Event Type:** {event_type}")
            st.write(f"**Input Summary:** {input_summary}")
            st.text_area(
                "Saved Output", output_result, height=250, key=f"history_{event_id}"
            )
