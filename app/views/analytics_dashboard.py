import plotly.express as px
import streamlit as st

from chart_theme import themed, CATEGORY_COLORS, CONTINUOUS_SCALE, TEXT


def render(df):
    st.header("Event analytics dashboard")

    st.subheader("Dashboard filters")

    colf1, colf2 = st.columns(2)

    with colf1:
        selected_event = st.selectbox(
            "Filter by event type", ["All"] + sorted(df["event_type"].unique().tolist())
        )

    with colf2:
        selected_promo = st.selectbox(
            "Filter by promotion", ["All"] + sorted(df["promotion_channel"].unique().tolist())
        )

    filtered_df = df.copy()

    if selected_event != "All":
        filtered_df = filtered_df[filtered_df["event_type"] == selected_event]

    if selected_promo != "All":
        filtered_df = filtered_df[filtered_df["promotion_channel"] == selected_promo]

    st.markdown("---")

    total_events = len(filtered_df)
    avg_attendance = int(filtered_df["actual_attendance"].mean())
    avg_budget = int(filtered_df["budget"].mean())
    avg_feedback = round(filtered_df["feedback_score"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total events", total_events)
    col2.metric("Avg attendance", avg_attendance)
    col3.metric("Avg budget", f"${avg_budget}")
    col4.metric("Avg feedback", avg_feedback)

    st.markdown("---")

    st.subheader("Event insights")

    best_event = filtered_df.groupby("event_type")["actual_attendance"].mean().idxmax()
    best_promo = filtered_df.groupby("promotion_channel")["actual_attendance"].mean().idxmax()

    st.success(f"Highest average attendance comes from: **{best_event}** events.")
    st.info(f"Most effective promotion method: **{best_promo}**.")

    st.markdown("---")

    col5, col6 = st.columns(2)

    with col5:
        attendance_by_type = filtered_df.groupby("event_type")["actual_attendance"].mean().reset_index()
        fig1 = px.bar(
            attendance_by_type, x="event_type", y="actual_attendance",
            color="actual_attendance", color_continuous_scale=CONTINUOUS_SCALE,
            title="Average attendance by event type",
        )
        st.plotly_chart(themed(fig1), use_container_width=True)

    with col6:
        promo = filtered_df.groupby("promotion_channel")["actual_attendance"].mean().reset_index()
        fig2 = px.pie(
            promo, names="promotion_channel", values="actual_attendance",
            hole=0.55, title="Promotion effectiveness",
            color_discrete_sequence=CATEGORY_COLORS,
        )
        fig2.update_traces(textfont=dict(color=TEXT))
        st.plotly_chart(themed(fig2), use_container_width=True)

    col7, col8 = st.columns(2)

    with col7:
        fig3 = px.scatter(
            filtered_df, x="budget", y="actual_attendance", color="event_type",
            size="feedback_score", hover_data=["location", "promotion_channel"],
            title="Budget vs attendance", color_discrete_sequence=CATEGORY_COLORS,
        )
        st.plotly_chart(themed(fig3), use_container_width=True)

    with col8:
        fig4 = px.histogram(
            filtered_df, x="actual_attendance", color="event_type",
            nbins=25, title="Attendance distribution",
            color_discrete_sequence=CATEGORY_COLORS,
        )
        st.plotly_chart(themed(fig4), use_container_width=True)
