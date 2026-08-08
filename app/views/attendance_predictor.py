import pandas as pd
import streamlit as st


def render(model, encoders):
    st.header("Event attendance predictor")

    st.caption(
        "Trained on a synthetic dataset with hand-picked effect sizes "
        "(see README for methodology), not on real event outcomes. "
        "Treat predictions as a demo of the pipeline, not a validated forecast."
    )

    le_event = encoders["event"]
    le_day = encoders["day"]
    le_time = encoders["time"]
    le_location = encoders["location"]
    le_promo = encoders["promo"]

    col1, col2 = st.columns(2)

    with col1:
        event_type = st.selectbox("Event type", list(le_event.classes_))
        expected = st.number_input("Expected audience", min_value=10, value=100)
        budget = st.number_input("Budget", min_value=100, value=1000)

    with col2:
        day = st.selectbox("Day", list(le_day.classes_))
        time = st.selectbox("Start time", list(le_time.classes_))
        location = st.selectbox("Location", list(le_location.classes_))
        promotion = st.selectbox("Promotion channel", list(le_promo.classes_))

    if st.button("Predict attendance", key="predict_attendance_btn"):

        input_data = pd.DataFrame(
            [[
                le_event.transform([event_type])[0],
                le_day.transform([day])[0],
                le_time.transform([time])[0],
                le_location.transform([location])[0],
                le_promo.transform([promotion])[0],
                expected,
                budget,
            ]],
            columns=[
                "event_type_enc", "day_enc", "time_enc",
                "location_enc", "promo_enc", "expected_audience", "budget",
            ],
        )

        prediction = int(model.predict(input_data)[0])

        st.markdown(
            f"""
            <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden;
                        display: flex; margin-top: 24px; background: var(--surface);">
                <div style="flex: 1; padding: 24px; border-right: 1px dashed var(--border-tear);">
                    <div class="nav-label">PREDICTED ATTENDANCE</div>
                    <div style="font-family: var(--font-mono); font-size: 46px; font-weight: 700;
                                color: var(--accent); line-height: 1;">{prediction}</div>
                    <div style="font-size: 13px; color: var(--text-muted); margin-top: 6px;">attendees expected</div>
                </div>
                <div style="flex: 1.3; padding: 24px; display: flex; flex-direction: column;
                            justify-content: center; gap: 10px; font-family: var(--font-mono); font-size: 12px;">
                    <div><span style="color: var(--text-muted);">EVENT&nbsp;&nbsp;&nbsp;</span><span style="color: var(--text-primary);">{event_type}</span></div>
                    <div><span style="color: var(--text-muted);">WHEN&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: var(--text-primary);">{day} &middot; {time}</span></div>
                    <div><span style="color: var(--text-muted);">WHERE&nbsp;&nbsp;&nbsp;</span><span style="color: var(--text-primary);">{location}</span></div>
                    <div><span style="color: var(--text-muted);">PROMO&nbsp;&nbsp;&nbsp;</span><span style="color: var(--text-primary);">{promotion}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
