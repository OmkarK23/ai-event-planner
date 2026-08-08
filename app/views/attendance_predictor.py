import pandas as pd
import streamlit as st


def render(model, encoders):
    st.header("Event Attendance Predictor")

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
        event_type = st.selectbox("Event Type", list(le_event.classes_))
        expected = st.number_input("Expected Audience", min_value=10, value=100)
        budget = st.number_input("Budget", min_value=100, value=1000)

    with col2:
        day = st.selectbox("Day", list(le_day.classes_))
        time = st.selectbox("Start Time", list(le_time.classes_))
        location = st.selectbox("Location", list(le_location.classes_))
        promotion = st.selectbox("Promotion Channel", list(le_promo.classes_))

    if st.button("Predict Attendance", key="predict_attendance_btn"):

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

        prediction = model.predict(input_data)[0]

        st.success(f"Predicted Attendance: {int(prediction)} attendees")

        st.markdown(
            f"""
            ### Prediction Summary

            Based on a **{event_type}** event on **{day}** at **{time}** in **{location}**, promoted through **{promotion}**, the predicted attendance is:

            ## {int(prediction)} attendees
            """
        )
